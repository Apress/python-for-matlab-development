#!/usr/bin/env python3
# code/dask/MB_numba_dask.py
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

@jit(uint8[:,:](float64[:],float64[:],int64,int64,int64),
                nopython=True)
def MB(Re, Im, imax, job_id, n_jobs):
  nR = len(Im)
  nC = len(Re)
  my_rows = range(job_id, len(Im), n_jobs)
  n_rows_here = len(my_rows)
  img = np.zeros((n_rows_here, nC), dtype=np.uint8)
  row_counter = 0
  for i in my_rows:
    I = Im[i]
    for j,R in enumerate(Re):
      c = complex(R, I)
      img[row_counter, j] = nIter(c, imax)
    row_counter += 1
  return img

def main():
  imax = 255
  N = 35_000
  T_s = time.time()
  nR, nC = N, N
  Re = np.linspace(-0.7440, -0.7433, nC)
  Im = np.linspace( 0.1315,  0.1322, nR)
  n_jobs = 18
 #client = Client('127.0.0.1:8786')
  client = Client('143.198.155.245:8786')
  tasks  = []
  for i in range(n_jobs):
    job = dask.delayed(MB)(Re, Im, 255, i, n_jobs)
    tasks.append(job)
  results = dask.compute(*tasks)
  client.close()

  # reassemble the image
  img = np.empty((N,N), dtype=np.uint8)
  for i in range(n_jobs):
    my_rows = range(i, len(Im), n_jobs)
    img[my_rows,:] = results[i][:]

  print(f'{time.time() - T_s:.3f}  {N:5d}')
  plt.imshow(img)
  plt.show()
if __name__ == '__main__': main()
