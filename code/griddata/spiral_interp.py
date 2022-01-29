# code/griddata/spiral_interp.py
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
from scipy.interpolate import griddata
def f(x,y):
   return x + 2*(np.cos(7*x)+
      np.sin(5*y)) + 3*y*np.sin(6*x)
K = 0.005
# subsample f(x,y) at 114 points
t = np.linspace(0,800,num=1100)
X = np.array([K*t*np.cos(t)+1,
              K*t*np.sin(t)-1])
in_range = (-0.6 < X[0,:]) * \
            (X[0,:] < 1.0) * \
           (-1.0 < X[1,:]) * \
            (X[1,:] < 0.4)
x_known = X[0,in_range]
y_known = X[1,in_range]

F_known = f(x_known, y_known)
# make a 200 x 200 regular grid
nX, nY = 200, 200
Y, X = np.mgrid[-1.0:-0.4:nY*1j,
                -0.6: 1.0:nX*1j]
# interpolate to the regular grid
F_near   = griddata(
    (x_known, y_known),
    F_known, (X,Y), method='nearest')
F_linear = griddata(
    (x_known, y_known),
    F_known, (X,Y),method='linear')
F_cubic  = griddata(
    (x_known, y_known),
    F_known, (X,Y),method='cubic')
