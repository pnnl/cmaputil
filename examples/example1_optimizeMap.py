# -*- coding: utf-8 -*-
"""
This example provides the ability to create figures like Figure 4 in our colormap paper.
A colormap is input and the iterations to optimize it are shown at each stage.

@author: Jamie R. Nunez
(C) 2017 - Pacific Northwest National Laboratory
"""
# Imports
from time import time

import cv2
import matplotlib.cm as cm # Used with eval()
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import cmaputil as cmu
import cmaputil.cvdutil as cvu

FLABEL = 20
FAX = 16

#%% Get iteration data
cmap = 'viridis' # The optimized version of this colormap is cividis!

# Get original RGB/Jab
t = time()
rgb1, jab1 = cmu.get_rgb_jab(cmap)

# Get CVD RGB/Jab
rgb2, jab2 = cmu.get_rgb_jab(cvu.get_cvd(rgb1, severity=100))

# Make perceptual deltas (for a' vs. b') straight
# Need to set a and b before straightening J
jab3 = cmu.make_linear(jab2)
rgb3 = cmu.convert(jab3, cmu.CSPACE2, cmu.CSPACE1)

# Linearize J'
jab4, jab5 = cmu.correct_J(jab3) # This will create a figure showing the J bounds
if jab4 is not None:
    rgb4 = cmu.convert(jab4, cmu.CSPACE2, cmu.CSPACE1)
    rgb4 = np.clip(rgb4, 0, 1)
if jab5 is not None:
    rgb5 = cmu.convert(jab5, cmu.CSPACE2, cmu.CSPACE1)
    rgb5 = np.clip(rgb5, 0, 1)

#%% Figure: Iterations for optimization

fig = plt.figure(figsize=(25, 12), dpi=500)

# Plot original colormap properties
ax = plt.subplot(5, 5, 1)
plt.title('Input', fontsize=FLABEL)
cmu.plot_colormap_info(fig, rgb1, sp=[5, 5, 1], show=False)
cmu.plot_colormap_info(fig, rgb1, sp=[5, 5, 1], show=False, leg=False)

# Plot converted (to CVD space) colormap properties
ax = plt.subplot(5, 5, 2)
plt.title('Step 1: CVD', fontsize=FLABEL)
cmu.plot_colormap_info(fig, rgb2, sp=[5, 5, 2], show=False)

# Plot for linearized a' and b'
ax = plt.subplot(5, 5, 3)
plt.title('Step 3:\na\' vs. b\' Linearized', fontsize=FLABEL)
cmu.plot_colormap_info(fig, rgb3, sp=[5, 5, 3], show=False)

# If able, plot colormap wth linear J', fitted to original J'
if jab4 is not None:
    ax = plt.subplot(5, 5, 4)
    plt.title('Step 4:\nJ\' fit to original', fontsize=FLABEL)
    cmu.plot_colormap_info(fig, rgb4, sp=[5, 5, 4], show=False)

# If able, plot colormap wth linear J', fitted to max J' range
if jab5 is not None:
    ax = plt.subplot(5, 5, 5)
    plt.title('Step 4:\nJ\' fit to maximize range', fontsize=FLABEL)
    cmu.plot_colormap_info(fig, rgb5, sp=[5, 5, 5], show=False)

plt.show()

#%% Plot changes in a' vs. b'

fig = plt.figure(figsize=(8, 6), dpi=500)

# Line plot colors: black, red, and blue.
c = [(0, 0, 0),
    (99 / 255., 198 / 255., 10 / 255.),
    (184 / 255., 156 / 255., 239 / 255.)]

# Plot original a' and b'
plt.plot(jab1[1, :], jab1[2, :], c='k', lw=12)
plt.plot(jab1[1, :], jab1[2, :], c=c[0], lw=10)

# Plot CVD a' and b'
plt.plot(jab2[1, :], jab2[2, :], c='k', lw=12)
plt.plot(jab2[1, :], jab2[2, :], c=c[1], lw=10)

# Plot optimized a' and b'
jab3 = cmu.convert(rgb3, cmu.CSPACE1, cmu.CSPACE2)
plt.plot(jab3[1, :], jab3[2, :], c='k', lw=8)
plt.plot(jab3[1, :], jab3[2, :], c=c[2], lw=6)

# Standard Formatting
plt.title('Iterative changes in a\' vs. b\'', fontsize=FLABEL)
plt.xlabel('a\'', fontsize=FLABEL)
plt.ylabel('b\'', fontsize=FLABEL)
plt.xticks([-40, 0, 40], fontsize=FAX)
plt.yticks([-40, 0, 40], fontsize=FAX)
plt.axis([-43, 43, -43, 43])

# Format legend
p1 = mpatches.Patch(color=c[0], label='Original')
p2 = mpatches.Patch(color=c[1], label='CVD')
p3 = mpatches.Patch(color=c[2], label='Perc. Unif. CVD')
patches = [p1, p2, p3]
plt.legend(handles=patches, loc='lower right', fontsize=FAX)

plt.show()
