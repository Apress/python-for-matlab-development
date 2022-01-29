% code/matlab_py/write_yaml.m
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
py_str = py.yaml.dump(mat_x);
% Error using py.yaml.dump
% Conversion of MATLAB 'datetime' to Python is not supported.

mat_x.data.date = sprintf('%s', mat_x.data.date);
py_str = py.yaml.dump(mat_x);
py_str

% Python str with no properties.
%   data:
%     date: 11-Dec-2020 03:25:00
%     dict:
%       food: flakes
%       pet: fish
%     items: !!python/tuple
%     - titles: !!python/tuple
%       - A Tale of Two Cities
%       - Wuthering Heights
%     - green
%     - orange
%     values: !!python/tuple
%     - 2
%     - 3
%     - 4
%     - 5.0

mat_str = string(py_str);
fh = fopen('new_demo.yaml', 'w');
fwrite(fh, mat_str);
fclose(fh);
