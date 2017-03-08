# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 12:05:59 2017

@author: Jamie Nunez
"""
__author__ = 'Jamie Dunn (jamie.dunn@pnnl.gov)'
__copyright__ = 'Copyright (c) 2017 PNNL'
__license__ = 'Battelle Memorial Institute BSD-like license'

#%% Imports
import matplotlib.pyplot as plt
import numpy as np

import colormap_module as mod

#%% Globals
CUSTNAME = 'JDUNN_CustomMap' # Name of custom colormap saved as a .npy file
PATH = '' # Path to image files

#%% Custom Functions
def plot_sub(i, img, title, cmap=None):
    '''
    Plots image as subplot for larger image.
    '''
    plt.subplot(i)
    plt.imshow(img, cmap=cmap)
    plt.axis('off')
    plt.title(title)
    return

def plot_mixed_NanoSIMS(img1_rgb, img1_iso, img2, mixed_img, name=None):
    '''
    Example use.
    
    Plots returned NanoSIMS images from mix_images function.
    '''
    plt.figure(figsize=(8, 8), dpi=600)
    plot_sub(221, img1_rgb, '12C14N-')
    plot_sub(222, img1_iso, 'Isoluminant 12C14N-')
    plot_sub(223, img2, 'Secondary Electrons', cmap='gray')
    plot_sub(224, mixed_img, 'Mixed')
    plt.tight_layout()
    
    if name is not None:
        plt.savefig(name)
    plt.show()

#%% Main

cmap = CUSTNAME

# Open 12C14N- image and normalize
CN = np.loadtxt(PATH + '12C14N.txt')
high = 3; low = -1
CN = CN * (CN > 2500)
CN = mod.bound(mod.normalize(CN), high, low)

# Open Secondary Electron image and normalize
se = np.loadtxt(PATH + 'SE.txt')
se = mod.bound(mod.normalize(np.log(se)), 3, -3)

#name = None
name = 'Test1'
mod.plot_colormap_info(cmap, name=name)

name = 'Test2'
maprevolve = False # Can set to true for full 3D rotation. Takes 20-30 minutes
a, b, c = mod.mix_images(CN, se, CUSTNAME, high, low, name=name,
                         maprevolve=maprevolve)

name = 'Test3'
plot_mixed_NanoSIMS(a, b, se, c, name=name)