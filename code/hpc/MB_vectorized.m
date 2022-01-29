% code/hpc/MB_vectorized.m
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

main()

function [img]=nIter(c, imax)
  [nR,nC]= size(c);
  z = complex(zeros(nR,nC), ...
              zeros(nR,nC));
  img = zeros(nR,nC,'uint8');
  Idx = ones(nR,nC,'logical');

  for i = 0:imax-1
    z(Idx) = z(Idx).*z(Idx)+ ...
           + c(Idx);
    New = (real(z).^2+ ...
           imag(z).^2 <= 4);
    if ~any(New,'all')
        break
    end
    img(New) = i;
    Idx = Idx & New;
  end
end
function [] = main()
  imax = 255;
  for N = [500 1000 2000 5000]
    tic
    nR = N; nC = N;
    Re = linspace(-0.7440,...
                  -0.7433, nC);
    Im = linspace( 0.1315,...
                   0.1322, nR);
    [zR, zI] = meshgrid(Re,Im);
    z_init = complex(zR,zI);
    img = nIter(z_init, imax);
    fprintf('%5d %.3f\n',N,toc);
  end
end
