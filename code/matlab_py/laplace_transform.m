% code/matlab_py/laplace_transform.m
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
sympy = py.importlib.import_module('sympy');
s = sympy.symbols('s');
t = sympy.symbols('t');
a = sympy.symbols('a', pyargs('real','True', 'positive','True'));
omega = sympy.symbols('omega', pyargs('real','True'));
f = sympy.exp(-a*t)*sympy.cos(omega*t);
L = sympy.laplace_transform(f, t, s)
% L = 
%   Python tuple with no properties.
%     ((a + s)/(omega**2 + (a + s)**2), -a, Eq(2*Abs(arg(omega)), 0))
>> latex = py.importlib.import_module('sympy.printing.latex');
>> latex.print_latex(L{1})
%  \frac{a + s}{\omega^{2} + \left(a + s\right)^{2}}
