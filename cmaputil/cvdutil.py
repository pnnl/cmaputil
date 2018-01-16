# -*- coding: utf-8 -*-
"""
ETo be renamed cvdutil
Utilities for working in color vision deficiency (CVD) space
@author: Jamie R. Nunez
(C) 2017 - Pacific Northwest National Laboratory
"""
#%% Imports
import numpy as np

import cmaputil as cmu

#%% Global Variables
SEV = 100
CSPACE1 = cmu.CSPACE1
CSPACE2 = cmu.CSPACE2
CVD_TYPE = 'deuteranomaly'

#%% Functions

def get_cvd(data, cvd_type=CVD_TYPE, severity=100):
    '''
    Converts RGB values to CVD space RGB values.

    Parameters
    ----------
    data: string or 3 x 256 array
        Colormap name OR array with complete color data. Invalid
        colormap names throw a ValueError. Refer to _check_cmap for
        more information.
    cvd_type: string
        Type of CVD to be simulated. Options: deuteranomaly or
        protanomaly. Default: deuteranomaly.
    severity: int
        Severity of CVD to be simulated. Can be any integer between 0
        and 100. Default: 100
    Returns
    ----------
    cvd: 3 x 256 array
        Colormap data in CVD space
    '''

    rgb,_ = cmu.get_rgb_jab(data, calc_jab=False)
    cvd_space = {'name': 'sRGB1+CVD', 'cvd_type': cvd_type,
                 'severity': severity}
    cvd = cmu.convert(rgb, cvd_space, CSPACE1)
    return cvd

def _iter_make_linear(jab):

    # Linearize a' and b' changes
    jab1 = cmu.make_linear(np.copy(jab))

    # Convert J'a'b' values to RGB values and clip
    rgb1 = np.clip(cmu.convert(jab1, CSPACE2, CSPACE1), 0, 1) 

    # Convert RGB to CVD RGB space
    rgb2 = get_cvd(rgb1)

    # Bring back to to J'a'b'
    jab2 = cmu.convert(rgb2, CSPACE1, CSPACE2)

    # Force to have same J' as original J'a'b' array
    jab2[0, :] = jab1[0, :]

    return jab2

def iter_make_linear(jab, l=100000):
    '''
    Takes J'a'b' array and performs the following two times: linearizes
    the change of a' and b' then converts to CVD space and back (to
    ensure colormap is still CVD compatible).

    Parameters
    ----------
    data: 3 x 256 array
        J'a'b' values for colormap
    Returns
    ----------
    rgb: 3 x 256 array
        RGB data
    jab: 3 x 256 array
        J'a'b' data
    '''

    jab = np.copy(jab)
    jab = _iter_make_linear(_iter_make_linear(jab))
    rgb = cmu.convert(jab, CSPACE2, CSPACE1)
    return rgb, jab