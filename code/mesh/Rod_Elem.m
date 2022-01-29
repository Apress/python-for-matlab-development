% code/mesh/Rod_Elem.m
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
classdef Rod_Elem
    properties
        % inputs to the constructor
        id
        node_a   % Node object
        node_b   % Node object
        radius   {mustBeNumeric}
        E        {mustBeNumeric} % Young's modulus of elasticity
        rho      {mustBeNumeric} % density
        % derived values
        dX
        dY
        length
        cross_sect_area
        mass
    end
    methods
        function elem = Rod_Elem(eid, node_a, node_b, radius, E, rho)
            elem.id     = eid;
            elem.node_a = node_a;
            elem.node_b = node_b;
            elem.radius = radius;
            elem.E      = E;
            elem.rho    = rho;
            elem.dX     = node_b.x - node_a.x;
            elem.dY     = node_b.y - node_a.y;
            elem.length = sqrt(elem.dX^2 + elem.dY^2);
            elem.cross_sect_area = radius^2;  % square cross section
            elem.mass = elem.rho * elem.length * elem.cross_sect_area;
        end
        function K = stiffness_matrix(elem)
            Ks = elem.E * elem.cross_sect_area / elem.length;
            cos    = elem.dX/elem.length;
            sin    = elem.dY/elem.length;
            cos2   = cos^2;
            sin2   = sin^2;
            sincos = sin*cos;
            K = Ks*[ cos2  ,  sincos, -cos2  , -sincos;
                     sincos,  sin2  , -sincos, -sin2  ;
                    -cos2  , -sincos,  cos2  ,  sincos;
                    -sincos, -sin2  ,  sincos,  sin2  ];
        end
        function M = mass_matrix(elem)
            M = 0.5 * elem.mass * [1 1 1 1]';  % 4 x 1
        end
    end
end
