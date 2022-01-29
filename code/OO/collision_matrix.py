#!/usr/bin/env python3
# code/OO/collision_matrix.py
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
from numpy.random import rand
import time

def collision_matrix(x, y, R):
    """
    Use broadcasting to return a square matrix of Boolean
    values with True at position [i,j] and [j,i] if
    circles i and j intersect.
    """
    dx = x[:,np.newaxis] - x[np.newaxis,:]
    dy = y[:,np.newaxis] - y[np.newaxis,:]
    sep = np.sqrt( dx**2 + dy**2 )
    sum_r = R[:,np.newaxis] + R[np.newaxis,:]
    return sep < sum_r

def run_sim(N, n_iter):
  box_x, box_y = 10., 6.
  r_min, r_max = 0.1, 0.3
  print(f'n balls={N}')
  for i in range(n_iter):
    x = r_max + (box_x-2*r_max)*rand(N)
    y = r_max + (box_y-2*r_max)*rand(N)
    R = 0.1 + 0.8*rand(N)
    T_s = time.time()
    coll = collision_matrix(x, y, R)
    n_coll = (np.sum(coll) - N)//2
    print(f'n coll={n_coll} Hz = '
          f'{1/(time.time()-T_s):.2f}')
