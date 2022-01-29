#!/usr/bin/env python
# code/dask/MB_numba_dask2.py
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
from numba import jit, uint8, int64, float64, complex128
from numba.types import Tuple as nb_tuple
import dask
from dask.distributed import Client
import time
import matplotlib.pyplot as plt

@jit(uint8(complex128,int64), nopython=True, fastmath=True)
def nIter(c, imax):
  z = complex(0, 0)
  for i in range(imax):
    z = z*z + c
    if z.real*z.real + z.imag*z.imag > 4:
      break
  return i

@jit(nb_tuple((int64[:],uint8[:,:]))(int64,float64[:],int64,float64[:],
        int64,int64,int64), nopython=True)
def MB(nC, Re_limits, nR, Im_limits, imax, job_id, n_jobs):
  Re = np.linspace(Re_limits[0], Re_limits[1], nC)
  Im = np.linspace(Im_limits[0], Im_limits[1], nR)
  my_rows = np.arange(job_id, len(Im), n_jobs, dtype=np.int64)
  n_rows_here = len(my_rows)
  img = np.zeros((n_rows_here, nC), dtype=np.uint8)
  row_counter = 0
  for i in my_rows:
    I = Im[i]
    for j,R in enumerate(Re):
      c = complex(R, I)
      img[row_counter, j] = nIter(c, imax)
    row_counter += 1
  return my_rows, img

def main():
  imax = 255
  N = 35_000
  T_s = time.time()
  nR, nC = N, N
  Re_limits = np.array([-0.7440, -0.7433])
  Im_limits = np.array([ 0.1315,  0.1322])
  n_groups = 16
  n_jobs_per_group = 18
  n_jobs = n_jobs_per_group*n_groups
 #client = Client('127.0.0.1:8786')
  client = Client('143.198.155.245:8786')
  results = []
  for c in range(n_groups):
    tasks  = []
    Tcs = time.time()
    for i in range(n_jobs_per_group):
      job = dask.delayed(MB)(nC, Re_limits, nR, Im_limits, 255,
              c*n_jobs_per_group+i, n_jobs)
      tasks.append(job)
    results.extend( dask.compute(*tasks) )
    Tce = time.time() - Tcs
    print(f'group {c:2d} took {Tce:.3f} sec')
  client.close()

  # reassemble the image
  img = np.empty((N,N), dtype=np.uint8)
  for i in range(len(results)):
    my_rows, img_rows = results[i]
    img[my_rows,:] = img_rows

  print(f'{time.time() - T_s:.3f}  {N:5d}')
  return
  plt.imshow(img)
  plt.show()
if __name__ == '__main__': main()
