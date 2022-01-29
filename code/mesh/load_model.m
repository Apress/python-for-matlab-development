% code/mesh/load_model.m
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

% In the functions below, 'triangle' refers to
% https://www.cs.cmu.edu/quake/triangle.html

function [model] = load_model(File)
    % Read triangle generated <>.node and
    % <>.ele files and return a struct with these.
    node_file = sprintf('%s.node', File);
    elem_file = sprintf('%s.ele' , File);
    model.vertices  = load_node_file(node_file);
    model.triangles = load_ele_file( elem_file);
end

function [points] = load_node_file(File)
    % Read a triangle generated <>.node file
    % and return an N x 2 array of coordinates.
    fh = fopen(File);
    header = strip(fgetl(fh));
    ndim = str2double(split(header));
    points = zeros(ndim(1), 2);
    while ~feof(fh)
        line = strip(fgetl(fh));
        if regexp(line,'^#')
            continue
        end
        % ixyn = str2double(split(line)); % slow
        ixyn = sscanf(line, '%d %g %g %d');
        points(ixyn(1), :) = [ixyn(2) ixyn(3)];
    end
    fclose(fh);
end

function [elem] = load_ele_file(File)
    % Read a triangle generated <>.ele file
    % and return an N x 3 array of vertex ID's.
    fh = fopen(File);
    header = strip(fgetl(fh));
    ndim = str2double(split(header));
    elem = zeros(ndim(1), 3);
    while ~feof(fh)
        line = strip(fgetl(fh));
        if regexp(line,'^#')
            continue
        end
        % iJKL = str2double(split(line)); % slow
        iJKL = sscanf(line, '%d %d %d %d');
        elem(iJKL(1), :) = [iJKL(2) iJKL(3) iJKL(4)];
    end
    fclose(fh);
end
