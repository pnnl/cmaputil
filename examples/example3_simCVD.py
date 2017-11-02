# -*- coding: utf-8 -*-
"""
Can be used to recreate Fig 2 from the paper.

@author: Jamie R. Nunez
(C) 2017 - Pacific Northwest National Laboratory
"""

#%% Imports

from time import time

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.spatial import ConvexHull, Delaunay
from viscm.gui import sRGB_gamut_Jp_slice

import cmaputil as cmu
import cvdutil as cvu

#%% Globals
FLABEL = 20
FAX = 16
UNIFORM_SPACE = 'CAM02-UCS'

#%% Functions

# From https://stackoverflow.com/questions/24733185/volume-of-convex-hull-with-qhull-from-scipy
def tetrahedron_volume(a, b, c, d):
    return np.abs(np.einsum('ij,ij->i', a-d, np.cross(b-d, c-d))) / 6

# From https://stackoverflow.com/questions/24733185/volume-of-convex-hull-with-qhull-from-scipy
def convex_hull_volume(pts):
    ch = ConvexHull(pts)
    dt = Delaunay(pts[ch.vertices])
    tets = dt.points[dt.simplices]
    return np.sum(tetrahedron_volume(tets[:, 0], tets[:, 1],
                                     tets[:, 2], tets[:, 3]))

# Quick help function to add J'a'b' (from a RGB value) to the given set
def add(rgb, severity, jab_set, cvd_type='deuteranomaly'):
    
    if severity is None: # Full trichromatic vision
        jab = cmu.convert(rgb, 'sRGB1', UNIFORM_SPACE)
    
    else: # Simulate CVD
        jab = cmu.convert(cvu.get_cvd(rgb, severity=severity, cvd_type=cvd_type), 'sRGB1', UNIFORM_SPACE)
    
    # Add to set
    jab_set.add(tuple(jab))

def gen_ab_spaces(Jps, sevs):
    
    # Initialize
    cvdd = []
    ab_values = set()
    cvdd_ab_values = [set(), set(), set(), set(), set(), set(), set(), set(), set(), set(), set()]
    
    t = time()
    for Jp in Jps:
        
        # Get a'b' for this J'
        ab_space = sRGB_gamut_Jp_slice(Jp, UNIFORM_SPACE)
        
        # Iterate through each a',b' pair
        for i in range(ab_space.shape[0]): # b'
            for j in range(ab_space.shape[1]): # a'
            
                # Check if this J'a'b' converts to a RGB value
                if np.sum(ab_space[i, j, :]) > 0:
                    
                    rgb = ab_space[i, j, :3]
                    add(rgb, None, ab_values)
                    
                    # Find the RGB for each severity
                    for sev in sevs:
                        add(rgb, sev, cvdd_ab_values[sev / 10])
    
        # Report time taken for this iteration
        print '%.2f' % (time() - t)
        t = time()
    
    # Calculate percent areas
    ab_values_temp = np.vstack({tuple(row) for row in np.asarray(list(ab_values))})
    normal_area = convex_hull_volume(ab_values_temp)
    
    for sev in sevs:  
        cvdd_ab_values_temp = np.vstack({tuple(row) for row in np.asarray(list(cvdd_ab_values[sev / 10]))})
        cvdd.append(convex_hull_volume(cvdd_ab_values_temp) / normal_area * 100)
        
    return cvdd, ab_values, cvdd_ab_values
    
def plot_ab_surfaces(full_color_vision_ab, cvd_ab, severity=100):
    
    ab_xy = np.asarray(list(full_color_vision_ab))
    cvd_xy = np.asarray(list(cvd_ab[severity / 10]))
    
    labels = ['J\'', 'a\'', 'b\'']
    pairs = [[1, 0], [2, 0], [2, 1]]
    
    for p in pairs:
        
        plt.figure(figsize=(6,6))
        
        plt.scatter(ab_xy[:, p[0]], ab_xy[:, p[1]], c='k', lw=0)
        plt.scatter(cvd_xy[:, p[0]], cvd_xy[:, p[1]], c='gray', lw=0)
        
        # Format
        if p[0] > 0: # a' or b' bounds
            xmin = -50; xmax = 50;
        else: # J' bounds
            xmin = 0; xmax = 100;
            
        if p[1] > 0:
            ymin = -50; ymax = 50;
            
        else:
            ymin = 0; ymax = 100;
        plt.xticks([])
        plt.yticks([])
        plt.axis([xmin, xmax, ymin, ymax])
        plt.xlabel(labels[p[0]], fontsize=16)
        plt.ylabel(labels[p[1]], fontsize=16)
        plt.show()

#%% Full trichromatic color vision vs.cvd color vision

# Get a'b' spaces covered by normal vision and CVD
# Iterates through all possible values. Takes a while!
Jps = np.linspace(0, 100, 11, dtype=int)
sevs = np.linspace(0, 100, 11, dtype=int)
cvdd, full_color_vision_ab, cvd_ab = gen_ab_spaces(Jps, sevs)

# Plot 2D surface comparisons
plot_ab_surfaces(full_color_vision_ab, cvd_ab)

# Plot CVD % of full color vision
fig = plt.figure(figsize=(4.5, 6))
d, = plt.plot(sevs, cvdd, c='k', lw=3)
plt.xlabel('Severity', fontsize=FLABEL)
plt.ylabel('Percent of Normal Color Vision', fontsize=FLABEL)
plt.xticks([0, 25, 50, 75, 100], fontsize=FAX)
plt.yticks([0, 25, 50, 75, 100], fontsize=FAX)
plt.axis([0, 100, 0, 100])
plt.show()