#!/usr/bin/env python3
# code/dask/save_KCMb.py
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
import sys
import scipy.io
from run_fr import global_matrices, read_tri

def main():
    for i in range(1,8):
        model = f'satellite/satellite.{i}'
        node_xy = read_tri(f'{model}.ele', f'{model}.node')[1]
        K, C, M, b, u_to_c = global_matrices(model)
        keep_nodes = np.argwhere((np.abs(23.5 - node_xy[:,0]) < 1.5) *
                                 (np.abs(10.5 - node_xy[:,1]) < 1.5)).ravel()
        keep_dof_full = sorted(np.hstack([keep_nodes*2, keep_nodes*2+1]))
        keep_dof = sorted([u_to_c[_] for _ in keep_dof_full]) # constrained DOF

#       u_to_c2 = [[_,u_to_c[_]] for _ in u_to_c]
        d = {
                'K'      : K       ,
                'C'      : C       ,
                'M'      : M       ,
                'b'      : b       ,
                'keep_dof' : keep_dof , }
        outF = f'KCMb_{i}.mat'
        scipy.io.savemat(outF, d)
        print(f'wrote {outF}')

if __name__ == "__main__": main()
