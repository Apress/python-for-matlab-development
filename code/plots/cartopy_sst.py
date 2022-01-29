#!/usr/bin/env python3
# code/plots/cartopy_sst.py
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
import os
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import cartopy.crs as ccrs
from mpl_toolkits.axes_grid1 import make_axes_locatable

os.environ["CARTOPY_USER_BACKGROUNDS"] = "cartopy/background"
File = 'oisst-avhrr-v02r01.20190101.nc'
rg = Dataset(File, 'r')
lat = rg["lat"][:]
lon = rg["lon"][:]
sst_ds = rg["sst"][0][0]
sst = sst_ds.data
mask = sst_ds.mask
sst[mask] = np.NaN
fig = plt.figure()
Ortho = ccrs.Orthographic(-10, 15)
PC = ccrs.PlateCarree()
ax = fig.add_subplot(1, 1, 1, projection=Ortho)
#           - or -
# ax = fig.add_subplot(1, 1, 1, projection=PC)
ax.coastlines()
ax.set_global()
ax.gridlines()
h = ax.contourf(lon, lat, sst, levels=20,
    vmin=-2, vmax=35, transform=PC, cmap='jet')
divider = make_axes_locatable(ax)
ax_cb = divider.new_horizontal(size="5%", pad=0.1,
    axes_class=plt.Axes)
fig.add_axes(ax_cb)
plt.colorbar(h, cax=ax_cb)
ax.background_img(name='VI', resolution='low')
ax.set_title('SST 2020-01-02 [Celcius]')
plt.savefig('sst_globe.png', bbox_inches='tight',
    pad_inches=0, transparent=True)
plt.show()
