import sys
import os
import platform

import numpy as np
from scipy.interpolate import UnivariateSpline
import scipy.constants as consts

# atoms/mol =  6.0221413e23  atoms/mol
AVOGADRO = consts.Avogadro

QCHARGE = consts.e

# Planck's Constant:  h*c ~= 12398.42 eV*Ang
PLANCK_HC = 1.e10 * consts.Planck * consts.c / QCHARGE

# electron rest mass in eV
E_MASS = consts.electron_mass * consts.c**2 / QCHARGE

# classical electron radius in cm
R_ELECTRON_CM = 100.0 * consts.physical_constants['classical electron radius'][0]


SI_PREFIXES = {'f': 1.e-15, 'femto': 1.e-15,
               'p': 1.e-12, 'pico': 1.e-12,
               'n': 1.e-9, 'nano': 1.e-9,
               '\u03bc': 1.e-6, 'u': 1.e-6, 'micro': 1.e-6,
               'm': 1.e-3, 'milli': 1.e-3}

def index_nearest(array, value):
    """return index of array *nearest* to value
    """
    return np.abs(array-value).argmin()

def as_ndarray(obj):
    """make sure a float, int, list of floats or ints,
    or tuple of floats or ints, acts as a numpy array
    """
    if isinstance(obj, (float, int)):
        return np.array([obj])
    return np.asarray(obj)

def elam_spline(xin, yin, yspl_in, xout):
    """
    interpolate values from Elam photoabsorption and
    scattering tables, according to Elam, and following
    standard interpolation methods.  Calc borrowed from D. Dale.

    Parameters:
        xin (ndarray): x values for interpolation data
        yin (ndarray): y values for interpolation data
        yspl_in (ndarray): spline coefficients (second derivatives of y) for
                       interpolation data
        xout(float or ndarray): x values to be evaluated at

    Returns:
        ndarray: interpolated values
    """
    x = as_ndarray(xout)
    x[np.where(x < min(xin))] = min(xin)
    x[np.where(x > max(xin))] = max(xin)

    lo, hi = np.array([(np.flatnonzero(xin < e)[-1],
                        np.flatnonzero(xin > e)[0])
                       for e in x]).transpose()

    diff = xin[hi] - xin[lo]
    if any(diff <= 0):
        raise ValueError('x must be strictly increasing')
    a = (xin[hi] - x) / diff
    b = (x - xin[lo]) / diff
    return (a * yin[lo] + b * yin[hi] +
            (diff*diff/6) * ((a*a - 1) * a * yspl_in[lo] +
                             (b*b - 1) * b * yspl_in[hi]))
