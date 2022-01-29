% code/griddata/spiral_interp.m
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
K = 0.005;
% subsample f(x,y) at 114 points
t = linspace(0,800,1100);
X = [K*t.*cos(t)+1; K*t.*sin(t)-1];
in_range = (-0.6 < X(1,:)) & ...
            (X(1,:) < 1.0) & ...
           (-1.0 < X(2,:)) & ...
            (X(2,:) < 0.4);
x_known = X(1,in_range);
y_known = X(2,in_range);

F_known = f(x_known, y_known);
% make a 200 x 200 regular grid
nX = 200; nY = 200;
[X, Y] = meshgrid(...
    linspace(-.6,  1,nX),...
    linspace(-1 ,-.4,nY));
% interpolate  to the regular grid
F_near   = griddata(...
        x_known, y_known, ...
        F_known, X,Y, 'nearest');
F_linear = griddata(...
        x_known, y_known,...
        F_known, X,Y, 'linear');
F_cubic  = griddata(...
        x_known, y_known,...
        F_known, X,Y, 'cubic');
function [S] = f(x,y)
   S = x + 2*(cos(7*x) + ...
       sin(5*y)) + 3*y.*sin(6*x);
end
