#!/usr/bin/env python3
# code/plots/cartopy_whale.py
# {{{
# This code accompanies the book _Python for MATLAB Development:
# Extend MATLAB with 300,000+ Modules from the Python Package Index_ 
# ISBN 978-1-4842-7222-0 | ISBN 978-1-4842-7223-7 (eBook)
# DOI 10.1007/978-1-4842-7223-7
# https://github.com/Apress/python-for-matlab-development
# 
# Copyright © 2022 Albert Danial
# 
# MIT License:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# }}}
import numpy as np
import shapely.geometry as sgeom
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

fig = plt.figure()
PC = ccrs.PlateCarree()
ax = fig.add_subplot(1, 1, 1, projection=PC)
ax.coastlines(resolution='50m')
ax.set_extent([-80, -50, 30, 55], crs=PC)

ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle='-')
ax.add_feature(cfeature.LAKES.with_scale('50m'),
                alpha=0.5)
ax.add_feature(cfeature.RIVERS.with_scale('50m'))

plt.title('Blue Whale 158390, Fall 2018')
path = np.loadtxt('whale_path.txt')
track = sgeom.LineString(path)
error = track.buffer(.5) # degrees
ax.gridlines(draw_labels=True)
ax.add_geometries([error], ccrs.PlateCarree(),
        facecolor='#1F18F4', alpha=.5)
ax.add_geometries([track], ccrs.PlateCarree(),
        facecolor='none', edgecolor='r')
plt.savefig('whale.png', bbox_inches='tight',
        pad_inches=0, transparent=True)
plt.show()
