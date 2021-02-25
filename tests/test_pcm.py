import numpy.testing as npt
import numpy as np
import hdstats
import joblib
import pytest


class TestPixelCompositeMosaic:

    data = joblib.load('data/landchar-small.pkl')

    def test_data(self):
        assert self.data.shape == (200, 200, 8, 18)
        assert self.data.dtype == np.float32

    def test_nangeomedian_shape(self):
        gm = hdstats.nangeomedian_pcm(self.data)
        assert gm.shape == (200, 200, 8)

    def test_nangeomedian_value(self):
        gm = hdstats.nangeomedian_pcm(self.data, nodata=np.nan)
        npt.assert_allclose(gm[0,0,:], hdstats.nangeomedian(self.data[0,0,:,:]), rtol=1e-4, atol=1e-4)
        npt.assert_approx_equal(np.nanmean(gm), 0.1432, significant=4)

    def test_nangeomedian_fixed(self):
        data = self.data
        fixeddata = (data * 10000).astype(np.int16)
#        fixeddata[1,1,0,:] = -999
        fgm = hdstats.nangeomedian_pcm(fixeddata)
        gm = (hdstats.nangeomedian_pcm(data)*10000).astype(np.int16)
        npt.assert_approx_equal(np.nanmean(fgm), np.nanmean(gm), significant=4)

    def test_nangeomedian_ro(self):
        data = self.data.copy()
        data.setflags(write=False)
        gm = hdstats.nangeomedian_pcm(data)
        assert gm.shape == (200, 200, 8)

    def test_nangeomedian_baddata(self):
        baddata = self.data[:3,:3,:,:].copy()
        baddata[1,1,0,:] = np.nan
        gm = hdstats.nangeomedian_pcm(baddata)
        print(gm[1,1,0])
        assert np.isnan(gm[1,1,0])

class TestMedianAbsoluteDeviation:

    data = joblib.load('data/landchar-small.pkl')
    gm = hdstats.nangeomedian_pcm(data)

    def test_emad(self):
        emad = hdstats.emad_pcm(self.data, self.gm)
        assert emad.shape == (200, 200)

    def test_emad_uint16(self):
        stat = hdstats.emad_pcm(self.data, self.gm)
        intdata = (self.data * 10000).astype(np.uint16)
        intdata[1,1,0,:] = 0
        intstat = hdstats.emad_pcm(intdata, self.gm, nodata=0)
        npt.assert_approx_equal(np.nanmean(stat),
                                np.nanmean(intstat),
                                significant=4)

    def test_emad_baddata(self):
        baddata = self.data[:3,:3,:,:].copy()
        baddata[1,1,0,:] = np.nan
        emad = hdstats.emad_pcm(baddata, self.gm)
        print(emad.shape)
        assert np.isnan(emad[1,1])

    def test_smad(self):
        smad = hdstats.smad_pcm(self.data, self.gm)
        assert smad.shape == (200, 200)

    def test_smad_uint16(self):
        stat = hdstats.smad_pcm(self.data, self.gm)
        intdata = (self.data * 10000).astype(np.uint16)
        intdata[1,1,0,:] = 0
        intstat = hdstats.smad_pcm(intdata, self.gm, nodata=0)
        npt.assert_approx_equal(np.nanmean(stat),
                                np.nanmean(intstat),
                                significant=4)

    def test_smad_baddata(self):
        baddata = self.data[:3,:3,:,:].copy()
        baddata[1,1,0,:] = np.nan
        smad = hdstats.smad_pcm(baddata, self.gm)
        assert np.isnan(smad[1,1])

    def test_bcmad(self):
        bcmad = hdstats.smad_pcm(self.data, self.gm)
        assert bcmad.shape == (200, 200)

    def test_bcmad_uint16(self):
        stat = hdstats.bcmad_pcm(self.data, self.gm)
        intdata = (self.data * 10000).astype(np.uint16)
        intdata[1,1,0,:] = 0
        intstat = hdstats.bcmad_pcm(intdata, self.gm, nodata=0)
        npt.assert_approx_equal(np.nanmean(stat),
                                np.nanmean(intstat),
                                significant=4)

    def test_bcmad_baddata(self):
        baddata = self.data[:3,:3,:,:].copy()
        baddata[1,1,0,:] = np.nan
        bcmad = hdstats.smad_pcm(baddata, self.gm)
        assert np.isnan(bcmad[1,1])
