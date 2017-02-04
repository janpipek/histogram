# -*- coding: utf-8 -*-
from __future__ import division

import numpy as np
import unittest

from numpy.testing import assert_array_almost_equal, assert_array_equal

from histogram import Histogram


class TestHistogram(unittest.TestCase):

    def test___add__(self):
        h1 = Histogram(3,[0,10],data=[1,2,3])

        h = h1 + 1
        assert_array_almost_equal(h1.data, [1,2,3])
        assert_array_almost_equal(h.data,  [2,3,4])

        h = h1 + [2,3,4]
        assert_array_almost_equal(h1.data, [1,2,3])
        assert_array_almost_equal(h.data,  [3,5,7])

        h = h1 + np.array([2,3,4])
        assert_array_almost_equal(h1.data, [1,2,3])
        assert_array_almost_equal(h.data,  [3,5,7])

        h2 = Histogram(3,[0,10],data=[4,5,6])

        h = h1 + h2
        assert_array_almost_equal(h1.data, [1,2,3])
        assert_array_almost_equal(h.data,  [5,7,9])

    def test___call__(self):
        h1 = Histogram(10,[0,10],data=[x+10 for x in range(10)])
        h2 = Histogram(10,[0,10],9,[-10,-1])
        h2.data[3,3] = 5
        self.assertAlmostEqual(h1(5),15)

    def test___truediv__(self):
        h1 = Histogram(3,[0,10],data=[1,2,3])
        h2 = Histogram(3,[0,10],data=[2,1,0])

        h3 = h1 / 2
        assert_array_equal(h1.data, np.array([1,2,3],dtype=np.int64))
        assert_array_almost_equal(h3.data,  [0.5,1,1.5])

        h3 = h2 / h1
        assert_array_equal(h1.data, np.array([1,2,3],dtype=np.int64))
        assert_array_equal(h2.data, np.array([2,1,0],dtype=np.int64))
        assert_array_almost_equal(h3.data,  [2.0,0.5,0.0])

        h3 = h1 / h2
        assert_array_equal(h1.data, np.array([1,2,3],dtype=np.int64))
        assert_array_equal(h2.data, np.array([2,1,0],dtype=np.int64))
        assert_array_almost_equal(h3.data, [0.5,2.0,0.0])

    def test_div_uncert(self):
        h1 = Histogram(3,[0,10],data=[1,2,3],uncert=[1,2,3])
        h2 = h1 / 2
        assert_array_almost_equal(h2.uncert,[0.5,1,1.5])
        h3 = h1 / h2
        uncrat = np.sqrt((h1.uncert/h1.data)**2 + (h2.uncert/h2.data)**2)
        assert_array_almost_equal(h3.uncert,uncrat * h3.data)

    def test_mul_uncert(self):
        h1 = Histogram(3,[0,10],data=[1,2,3],uncert=[1,2,3])
        h2 = h1 * 2
        assert_array_almost_equal(h2.uncert,[2,4,6])
        h3 = h1 * h2
        uncrat = np.sqrt((h1.uncert/h1.data)**2 + (h2.uncert/h2.data)**2)
        assert_array_almost_equal(h3.uncert,uncrat * h3.data)

    def test___iadd__(self):
        h1 = Histogram(3,[0,10],data=[1,2,3])

        h1 += 1
        assert_array_almost_equal(h1.data, [2,3,4])

        h1 += [2,3,4]
        assert_array_almost_equal(h1.data, [4,6,8])

        h2 = Histogram(3,[0,10],data=[4,5,6])

        h1 += h2
        assert_array_almost_equal(h1.data, [8,11,14])

    def test___itruediv__(self):
        h1 = Histogram(3,[0,10],data=[1,2,3])
        h2 = Histogram(3,[0,10],data=[2,1,0])

        h3 = h1.clone(np.float64)
        h3 /= 2
        assert_array_equal(h1.data, np.array([1,2,3],dtype=np.int64))
        assert_array_almost_equal(h3.data,  [0.5,1,1.5])

        h3 = h1.clone()
        try:
            h3 /= h1
        except TypeError:
            assert True
        else:
            assert False

        h3 = h1.clone(np.float64)
        h3 /= h2
        assert_array_equal(h1.data, np.array([1,2,3],dtype=np.int64))
        assert_array_almost_equal(h3.data,  [0.5,2.0,0.0])

    def test___imul__(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.__imul__(that))
        assert True # TODO: implement your test here

    def test___init__(self):
        self.assertRaises(TypeError,Histogram)

        h1a = Histogram(100,[0,10])
        h1b = Histogram(100,[0,10],'x')
        h1c = Histogram(100,[0,10],'x','label')
        h1d = Histogram(100,[0,10],'x','label','title')

        h2a = Histogram(np.linspace(0,10,101))
        h2b = Histogram(np.linspace(0,10,101),'x')
        h2c = Histogram(np.linspace(0,10,101),'x','label')
        h2d = Histogram(np.linspace(0,10,101),'x','label','title')

        h3a = Histogram((np.linspace(0,10,101),))
        h3b = Histogram((np.linspace(0,10,101),'x'))
        h3c = Histogram((np.linspace(0,10,101),'x'),'label')
        h3d = Histogram((np.linspace(0,10,101),'x'),'label','title')

        self.assertTrue(h1a.isidentical(h2a))
        self.assertTrue(h1b.isidentical(h2b))
        self.assertTrue(h1c.isidentical(h2c))
        self.assertTrue(h1d.isidentical(h2d))

        self.assertTrue(h1a.isidentical(h3a))
        self.assertTrue(h1b.isidentical(h3b))
        self.assertTrue(h1c.isidentical(h3c))
        self.assertTrue(h1d.isidentical(h3d))

    def test___isub__(self):
        h1 = Histogram(3,[0,10],data=[1,2,3])

        h1 -= 1
        assert_array_almost_equal(h1.data, [0,1,2])

        h1 -= [2,3,4]
        assert_array_almost_equal(h1.data, [-2,-2,-2])

        h1 = Histogram(3,[0,10],data=[10,10,10])
        h2 = Histogram(3,[0,10],data=[ 4, 5, 6])
        h1 -= h2
        assert_array_almost_equal(h1.data, [6,5,4])

    def test___mul__(self):
        h1 = Histogram(3,[0,10],data=[1,2,3])

        h2 = h1 * 2.
        self.assertEqual(h2.data.dtype,np.float)

    def test___radd__(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.__radd__(that))
        assert True # TODO: implement your test here

    def test___rtruediv__(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.__rtruediv__(that))
        assert True # TODO: implement your test here

    def test___rmul__(self):
        h1 = Histogram(3,[0,10],data=[1,2,3])

        h2 = 2. * h1
        self.assertEqual(h2.data.dtype,np.float)

    def test___rsub__(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.__rsub__(that))
        assert True # TODO: implement your test here

    def test___str__(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.__str__())
        assert True # TODO: implement your test here

    def test___sub__(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.__sub__(that))
        assert True # TODO: implement your test here

    def test_added_uncert(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.added_uncert(that, nans))
        assert True # TODO: implement your test here

    def test_added_uncert_ratio(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.added_uncert_ratio(that, nans))
        assert True # TODO: implement your test here

    def test_asline(self):
        h = Histogram(10,[0,10])
        h.data = np.array([1,2,3,4,5,0,1,2,9,0],dtype=np.int64)
        x,y,ext = h.asline()
        assert_array_almost_equal(x,[0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10])
        assert_array_almost_equal(y,[1,1,2,2,3,3,4,4,5,5,0,0,1,1,2,2,9,9,0, 0])
        assert_array_almost_equal(ext,[0,10,0,9])

        h = Histogram(10,[0,10])
        h.data = np.array([0,2,3,4,5,0,1,2,9,0],dtype=np.int64)
        x,y,ext = h.asline()
        assert_array_almost_equal(x,[0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10])
        assert_array_almost_equal(y,[0,0,2,2,3,3,4,4,5,5,0,0,1,1,2,2,9,9,0, 0])
        assert_array_almost_equal(ext,[0,10,0,9])

        h = Histogram(10,[0,10])
        h.data = np.array([0,2,-4,4,5,0,1,2,9,0],dtype=np.int64)
        x,y,ext = h.asline()
        assert_array_almost_equal(x,[0,1,1,2, 2, 3,3,4,4,5,5,6,6,7,7,8,8,9,9,10])
        assert_array_almost_equal(y,[0,0,2,2,-4,-4,4,4,5,5,0,0,1,1,2,2,9,9,0, 0])
        assert_array_almost_equal(ext,[0,10,-4,9])

        h = Histogram(10,[-1,9])
        h.data = np.array([-1,2,-4,4,5,0,1,2,9,-10],dtype=np.int64)
        x,y,ext = h.asline()
        assert_array_almost_equal(x,[-1, 0,0,1, 1, 2,2,3,3,4,4,5,5,6,6,7,7,8,  8,  9])
        assert_array_almost_equal(y,[-1,-1,2,2,-4,-4,4,4,5,5,0,0,1,1,2,2,9,9,-10,-10])
        assert_array_almost_equal(ext,[-1,9,-10,9])

        h = Histogram(10,[0,10])
        h.data = np.array([1,2,3,4,5,0,1,2,9,0],dtype=np.int64)

        x,y,ext = h.asline(2)
        assert_array_almost_equal(x,[2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10])
        assert_array_almost_equal(y,[3,3,4,4,5,5,0,0,1,1,2,2,9,9,0, 0])
        assert_array_almost_equal(ext,[2,10,0,9])

        x,y,ext = h.asline(1.9)
        assert_array_almost_equal(x,[2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10])
        assert_array_almost_equal(y,[3,3,4,4,5,5,0,0,1,1,2,2,9,9,0, 0])
        assert_array_almost_equal(ext,[2,10,0,9])

        x,y,ext = h.asline(2.9,7)
        assert_array_almost_equal(x,[3,4,4,5,5,6])
        assert_array_almost_equal(y,[4,4,5,5,0,0])
        assert_array_almost_equal(ext,[3,6,0,5])


    def test_aspolygon(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.aspolygon(ymin, range))
        assert True # TODO: implement your test here

    def test_binvolumes(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.binvolumes())
        assert True # TODO: implement your test here

    def test_binwidth(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.binwidth(b, axis))
        assert True # TODO: implement your test here

    def test_binwidths(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.binwidths())
        assert True # TODO: implement your test here

    def test_clear_nans(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.clear_nans(val))
        assert True # TODO: implement your test here

    def test_clone(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.clone(dtype, **kwargs))
        assert True # TODO: implement your test here

    def test_cut_1d(self):
        h1 = Histogram(100,[0,10])

        '''
        h1a = h1.cut(-3,3)
        h1c = h1.cut(1,3)
        h1b = h1.cut(0,3)
        h1d = h1.cut(3,10)
        h1e = h1.cut(3,20)

        h1 = Histogram(10,[0,10])
        h1.data = np.linspace(0,9,10)

        h1a = h1.cut(-3,3)
        assert_array_almost_equal(h1a.axes[0].edges,[0,1,2,3]))
        assert_array_almost_equal(h1a.data,[0,1,2]))

        h1c = h1.cut(1,3)
        assert_array_almost_equal(h1c.axes[0].edges,[1,2,3]))
        assert_array_almost_equal(h1c.data,[1,2]))

        h1b = h1.cut(0,3)
        assert_array_almost_equal(h1b.axes[0].edges,[0,1,2,3]))
        assert_array_almost_equal(h1b.data,[0,1,2]))

        h1d = h1.cut(3,10)
        assert_array_almost_equal(h1d.axes[0].edges,[3,4,5,6,7,8,9,10]))
        assert_array_almost_equal(h1d.data,[3,4,5,6,7,8,9]))

        h1e = h1.cut(3,20)
        assert_array_almost_equal(h1e.axes[0].edges,[3,4,5,6,7,8,9,10]))
        assert_array_almost_equal(h1e.data,[3,4,5,6,7,8,9]))
        '''


    def test_cut_2d(self):
        h2 = Histogram((100,[0,10]),(90,[-3,3]))
        #h2a = h2.cut((-1,1),axis=0)

        h3 = Histogram((100,[-30,330]), (100,[-50,50]))
        #h3a = h3.cut(-30,30,axis=0)
        h3b = h3.cut(270,330,axis=0)

    def test_cut_data(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.cut_data(*range, **kwargs))
        assert True # TODO: implement your test here

    def test_dim(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.dim())
        assert True # TODO: implement your test here

    def test_dtype(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.dtype(that, div))
        assert True # TODO: implement your test here

    def test_edge_grid(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.edge_grid())
        assert True # TODO: implement your test here

    def test_edges(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.edges())
        assert True # TODO: implement your test here

    def test_errorbars(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.errorbars(maxdim, asratio))
        assert True # TODO: implement your test here

    def test_extent(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.extent(maxdim, uncert, pad))
        assert True # TODO: implement your test here

    def test_fill(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.fill(*args))
        assert True # TODO: implement your test here

    def test_fill_from_sample(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.fill_from_sample(sample, weights))
        assert True # TODO: implement your test here

    def test_fill_one(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.fill_one(pt, wt))
        assert True # TODO: implement your test here

    def test_fit(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.fit(fcn, p0, **kwargs))
        assert True # TODO: implement your test here

    def test_fit_signal(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.fit_signal(fcn_sig, fcn_bkg, p0, npsig, **kwargs))
        assert True # TODO: implement your test here

    def test_fit_slices(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.fit_slices(axis, *args, **kwargs))
        assert True # TODO: implement your test here

    def test_fit_slices_signal(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.fit_slices_signal(axis, *args, **kwargs))
        assert True # TODO: implement your test here

    def test_grid(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.grid())
        assert True # TODO: implement your test here

    def test_integral(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.integral(uncert))
        assert True # TODO: implement your test here

    def test_interpolate_nans(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.interpolate_nans(**kwargs))
        assert True # TODO: implement your test here

    def test_isuniform(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.isuniform(tol))
        assert True # TODO: implement your test here

    def test_max(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.max(uncert))
        assert True # TODO: implement your test here

    def test_mean(self):
        h = Histogram(10,[0,10])
        h.fill([3,3,3])
        self.assertAlmostEqual(h.mean()[0],3.5)

        h.fill([1,5])
        self.assertAlmostEqual(h.mean()[0],3.5)

    def test_min(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.min(uncert))
        assert True # TODO: implement your test here

    def test_occupancy(self):
        h = Histogram(10,[0,10])
        h.fill([1,1,1,2,2,2,3])
        hocc = h.occupancy(4,[-0.5,3.5])
        assert_array_almost_equal(hocc.data, [7,1,0,2])

    def test_overflow(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.overflow())
        assert True # TODO: implement your test here

    def test_profile(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.profile(axis, fnsig, fnbkg, npsig, p0, cut, rebin, fnprof, p0prof, **kwargs))
        assert True # TODO: implement your test here

    def test_profile_gauss(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.profile_gauss(mean, width, axis, npar, **kwargs))
        assert True # TODO: implement your test here

    def test_projection(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.projection(axis))
        assert True # TODO: implement your test here

    def test_rebin(self):
        h = Histogram(10,[0,10])
        h.set(1)
        hexpect = Histogram(5,[0,10])
        hexpect.set(2)
        hrebin = h.rebin(2)
        assert_array_almost_equal(hrebin.data, hexpect.data)
        assert_array_almost_equal(hrebin.axes[0].edges, hexpect.axes[0].edges)

    def test_reset(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.reset())
        assert True # TODO: implement your test here

    def test_set(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.set(val, uncert))
        assert True # TODO: implement your test here

    def test_shape(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.shape())
        assert True # TODO: implement your test here

    def test_size(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.size())
        assert True # TODO: implement your test here

    def test_slices(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.slices(axis))
        assert True # TODO: implement your test here

    def test_slices_data(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.slices_data(axis))
        assert True # TODO: implement your test here

    def test_slices_uncert(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.slices_uncert(axis))
        assert True # TODO: implement your test here

    def test_smooth(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.smooth(weight))
        assert True # TODO: implement your test here

    def test_std(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.std())
        assert True # TODO: implement your test here

    def test_sum(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.sum(*axes, **kwargs))
        assert True # TODO: implement your test here

    def test_sum_over_axes(self):
        # histogram = Histogram(*axes, **kwargs)
        # self.assertEqual(expected, histogram.sum_over_axes(*axes))
        assert True # TODO: implement your test here


if __name__ == '__main__':
    from . import main
    main()