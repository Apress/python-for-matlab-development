% code/mesh/run_fem.m
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
model_file_base = 'code/dask/sat.5';
model_file_base = 'satellite/satellite.1';
x = load_model(model_file_base);

adapter_ring_nodes = find(abs( 2  - x.vertices(:,2) ) < 0.1) ;
adapter_ring_dof = sort([adapter_ring_nodes*2-1 ; adapter_ring_nodes*2 ])';
run_fem_fn(model_file_base, adapter_ring_dof)

function run_fem_fn(varargin)
  if size(varargin,2) == 0
      tri_model = 'beam.4';
  else
      tri_model = varargin{1};
  end
  constrained_dof_list = varargin{2};

  T_start = tic;

  m = FE_model(tri_model, 1e7, .1, .1);

  [K, M, u_to_c] = m.KM(constrained_dof_list);
  nDof = size(M,1);
  
  b = rand(nDof,1);
  tic;
  x = K\b;
  err = norm(K*x - b);
  fprintf('time to solve Kx=b = %.3f   error = %14.8e\n', toc, err)

% if nDof > 8e+5
%   return
%   fprintf('model too big, skipping eigensolution\n')
% end
  
  T_eig_start = tic;
  [v,w] = eigs(K, M, 6, 'smallestabs');
  w = diag(w);
  fprintf('eigensolution Kx = l Mx: %7.3f sec\n', toc(T_eig_start));
  fprintf('Total                  : %7.3f sec\n', toc(T_start));

  for i = 1:size(w,1)
    Hz = sqrt( abs(w(i)) )/(2*pi);
    fprintf('%2d %20.3f  %20.3f Hz\n',i, w(i), Hz)
  end
end
