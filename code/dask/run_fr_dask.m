% code/dask/run_fr_dask.m
% {{{
% This code accompanies the book _Python for MATLAB Development:
% Extend MATLAB with 300,000+ Modules from the Python Package Index_ 
% ISBN 978-1-4842-7222-0 | ISBN 978-1-4842-7223-7 (eBook)
% DOI 10.1007/978-1-4842-7223-7
% https://github.com/Apress/python-for-matlab-development
% 
% Copyright © 2022 Albert Danial
% 
% MIT License:
% Permission is hereby granted, free of charge, to any person obtaining a copy
% of this software and associated documentation files (the "Software"), to deal
% in the Software without restriction, including without limitation the rights
% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
% copies of the Software, and to permit persons to whom the Software is
% furnished to do so, subject to the following conditions:
% 
% The above copyright notice and this permission notice shall be included in
% all copies or substantial portions of the Software.
% 
% THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
% THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
% FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
% DEALINGS IN THE SOFTWARE.
% }}}
clear all
Im = @py.importlib.import_module;
np      = Im('numpy');
pysolve = Im('pysolve');

T_main_s = tic;

%%
load('KCMb_7.mat') % K, C, M, b, keep_dof
fprintf('Keeping response at %d DOF\n', length(keep_dof))
load_history = load('load_hist_smoothed.txt');
n_jobs = int64(100);
n_FFT = 4096;
solve_with = "coiled";
% solve_with = "localhost";
% solve_with = "digitalocean";

%%
n_freq = int64(floor(n_FFT/2));
dT    = 5.0e-4;   % time between each load_history point
Time  = 0:dT:dT*n_FFT;
Fs    = 1/dT;     % sampling frequency Hz
Hertz = linspace(0, Fs/2, n_freq); % only to Nyquist
dHz   = Hertz(2);
P = fft(load_history);
P_Nyq = P(1:n_freq);
n_dof = size(M,1);
fprintf('Time: %d times, 0.0 to %.6f sec steps of %.6f sec\n', n_FFT, Time(end), dT)
fprintf('Freq: %d freq, 0.0 to %.1f Hz steps of %.1f Hz\n', n_freq, Hertz(end), dHz)

% convert MATLAB-native arrays to Python-native
b = rand(n_dof,1);
K = mat2py(K);
C = K * 0.004; % proportional damping
M = mat2py(M);
b = np.array(b);
P_Nyq = mat2py(P_Nyq);
Hertz = np.array(Hertz);
keep_dof = np.array(keep_dof).astype(np.int64);
  
x = pysolve.remote_solve(solve_with, n_jobs, K, C, M, b, P_Nyq, Hertz, keep_dof);
x = py2mat(x);

fprintf('%d frequencies took %.3f s\n', n_freq, toc(T_main_s))
