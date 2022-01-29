% code/OO/run_oo_sim.m
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
function res = run_oo_sim(N, n_iter)
  fprintf('n balls=%d\n', N)
  box_x = 10.;
  box_y =  6.;
  r_min = 0.1;
  r_max = 0.3;
  for i = 1:n_iter
    tic
    balls = {};
    for j = 1:N
      x = r_max + (box_x-2*r_max)*rand();
      y = r_max + (box_y-2*r_max)*rand();
      R = 0.1 + 0.8*rand();
      balls{j} = Ball(x,y,R);
    end
    coll = eye(N);
    for j = 1:N
      for k = j+1:N
        coll(j,k) = balls{j}.collides_with(balls{k});
        coll(k,j) = coll(j,k);
      end
    end
    n_coll = (sum(sum(coll)) - N)/2;
    fprintf('n coll=%d Hz = %.2f\n', n_coll, 1/toc)
  end
end
