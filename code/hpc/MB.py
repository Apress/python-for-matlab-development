#!/usr/bin/env python3
# file: code/hpc/MB.py

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
import time
def nIter(c, imax):
  z = complex(0, 0)
  for i in range(imax):
    z = z*z + c
    if abs(z) > 2:
      break
  return np.uint8(i)

def MB(Re, Im, imax):
  nR = len(Im)
  nC = len(Re)
  img = np.zeros((nR, nC),
          dtype=np.uint8)
  for i in range(nR):
    for j in range(nC):
      c = complex(Re[j],Im[i])
      img[i,j] = nIter(c,imax)
  return img

def main():
  imax = 255
  for N in [500,1000,2000,5000]:
    T_s = time.time()
    nR, nC = N, N
    Re = np.linspace(-0.7440,
                     -0.7433, nC)
    Im = np.linspace( 0.1315,
                      0.1322, nR)
    img = MB(Re, Im, imax)
    print(N, time.time() - T_s)
if __name__ == '__main__': main()
