#!/usr/bin/env python3
# code/dask/run_fr_dask.py
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
import sys
import numpy as np
from   timeit import default_timer
from run_fr import read_tri, stiffness_terms, save_to_pkl, \
    constrain_dof, toc, global_matrices
import dask
from dask.distributed import Client, LocalCluster
import pysolve

tic = default_timer

def main():
    T_total_s = tic()
    model = 'one'
    model = 'tiny'
    model = 'sat.0'
    model = 'satellite/satellite.7'
    node_xy = read_tri(f'{model}.ele', f'{model}.node')[1]
    solve_with = 'localhost' # localhost digitalocean coiled
    solve_with = 'coiled' # localhost digitalocean coiled
    n_jobs = 3
    n_jobs = 2

    load_history = np.loadtxt('data/load_hist_smoothed.txt')
    n_FFT  = 8192
    n_FFT  = 4096
    n_FFT  = 2048
    n_freq = n_FFT // 2 # + 1 # only work up to Nyquist frequency
    dT = 5.0e-4  # time between each load_history point
    Time  = np.arange(0, dT*n_FFT, dT)
    Fs = 1/dT    # sampling frequency
    Hertz = np.linspace(0, Fs/2, num=n_freq) # only to Nyquist
    dHz = Hertz[1]
    print(f'Time: {n_FFT} times, 0.0 to {Time[-1]:.6f} sec steps of {dT:.6f} sec')
    print(f'Freq: {n_freq} freq, 0.0 to {Hertz[-1]:.1f} Hz steps of {dHz:.1f} Hz')
    print(f'      {n_jobs} workers')

    K, C, M, b, u_to_c = global_matrices(model)
    P = np.fft.rfft(load_history, n=n_FFT)
    P_Nyq = P[:n_freq] # only to Nyquist

    keep_nodes = np.argwhere((np.abs(23.5 - node_xy[:,0]) < 1.5) *
                             (np.abs(10.5 - node_xy[:,1]) < 1.5)).ravel()
    keep_dof_full = sorted(np.hstack([keep_nodes*2, keep_nodes*2+1]))
    keep_dof = sorted([u_to_c[_] for _ in keep_dof_full]) # constrained DOF

    if not len(keep_dof):
        print('keep_dof is empty; expand radius')
        return
    print(f'keeping {len(keep_dof)} out of {K.shape[0]} DOF')

    solnx = pysolve.remote_solve(solve_with, n_jobs, K, C, M, b,
                                 P_Nyq, Hertz, keep_dof)
    print(solnx)
    toc('Total time = ', T_total_s)

if __name__ == "__main__": main()
