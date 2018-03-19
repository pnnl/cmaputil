# -*- coding: utf-8 -*-
"""
Can be used to create plots like in Fig 1 and 5 of the paper

@author: Jamie R. Nunez
(C) 2017 - Pacific Northwest National Laboratory
"""

# Imports
import numpy as np

import cmaputil as cmu
import cmaputil.cvdutil as cvu

# Globals
FLABEL = 20
FAX = 16

# Input colormap name
cmap = 'viridis'

# Optimize
rgb1, jab1 = cmu.get_rgb_jab(cmap) # Original colormap
rgb2, jab2 = cmu.get_rgb_jab(cvu.get_cvd(rgb1)) # CVD colormap
jab3 = cmu.make_linear(jab2) # Uniformize hue (a' vs. b')
_, jab4 = cmu.correct_J(jab3) # Linearize J'

# Convert back to sRGB
rgb4 = cmu.convert(jab4, cmu.CSPACE2, cmu.CSPACE1)
rgb4 = np.clip(rgb4, 0, 1)

# Resimulate CVD in case corrections took the map outside CVD-safe space
rgb4 = cvu.get_cvd(rgb4)

#%% Creat CDPS plots (shown in Fig 1 and 5 of the paper)

# Import test data
img_name = 'example_nanosims_image.txt' # Image used for paper
img = np.loadtxt(img_name)[45:, :-45] # Make square
high = 3; low = -1 # Std. Dev bounds for normalizing
img = cmu.bound(cmu.normalize(img), high, low) # Normalize
slice_img = np.array(img[265, 50:-50], ndmin=2) # Slice used in paper
gslope = 27.4798474 # Slope for gray. Used to normalize CDPS slopes.

# CDPS plot for original map
cmu.cdps_plot(slice_img, cmap, rgb1, 1, gslope)

# CDPS plot for CVD-simulated map
cmu.cdps_plot(slice_img, cmap, rgb2, 2, gslope)

# CDPS plot for optimized map
cmu.cdps_plot(slice_img, cmap, rgb4, 4, gslope)
