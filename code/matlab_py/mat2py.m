% Convert a MATLAB variable to an equivalent Python-native variable.
% py_var = mat2py(mat_var);
% py_var = mat2py(mat_var, 'bytes');  % char mapped to Python bytes
% py_var = mat2py(mat_var, 'string'); % char mapped to Python string
function [x_py] = mat2py(x_mat, char_to)
    arguments
        x_mat
        char_to = 'string';
    end

% {{{ code/matlab_py/mat2py.m
% This code accompanies the book _Python for MATLAB Development:
% Extend MATLAB with 300,000+ Modules from the Python Package Index_
% ISBN 978-1-4842-7222-0 | ISBN 978-1-4842-7223-7 (eBook)
% DOI 10.1007/978-1-4842-7223-7
% https://github.com/Apress/python-for-matlab-development
%
% Copyright © 2022-2023 Albert Danial
%
% Contributions by:
%   - https://github.com/hcommin (performance enhancements)
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

    x_py = py.numpy.array({});
    switch class(x_mat)
        case 'char'
            if strcmp(char_to,'bytes')
                x_py = py.bytes(x_mat,'ASCII');
            else
                x_py = py.str(x_mat);
            end
        case 'string'
            x_py = py.str(x_mat);
        case 'datetime'
            int_sec = int64(floor(x_mat.Second));
            milli_sec = x_mat.Second - double(int_sec);
            micro_sec = int64(round(1e6 * milli_sec));
            if ~isempty(x_mat.TimeZone)
                tzinfo = py.dateutil.tz.gettz(x_mat.TimeZone);
            else
                tzinfo = py.None;
            end
            x_py = py.datetime.datetime(int64(x_mat.Year), int64(x_mat.Month), ...
                               int64(x_mat.Day) , int64(x_mat.Hour) , ...
                               int64(x_mat.Minute), int_sec, ...
                               micro_sec, tzinfo);
        case {'double', 'single', ...
              'uint8', 'uint16', 'uint32', 'uint64', ...
              'int8',  'int16',  'int32',  'int64'}
            if issparse(x_mat)
                if ndims(x_mat) ~= 2
                    fprintf('mat2py:  can only convert 2D sparse matrices\n')
                    return
                end
                [nR,nC] = size(x_mat);
                [i,j,vals] = find(x_mat);
                % subtract 1 to go from 1-based to 0-based indices
                py_I    = py.numpy.array(int64(i)-1);
                py_J    = py.numpy.array(int64(j)-1);
                py_vals = mat2py(vals);
                py_dims = py.tuple({int64(nR), int64(nC)});
                py_IJ   = py.tuple({py_I, py_J});
                V_IJ    = py.tuple({py_vals, py_IJ});
                x_py = py.scipy.sparse.coo_matrix(V_IJ,py_dims);
            elseif ismatrix(x_mat)
                if numel(x_mat) == 1
                    x_py = x_mat;  % scalar numeric value
                elseif isreal(x_mat)
                    x_py = py.numpy.array(x_mat);
                else
                    x_py = py.numpy.array(real(x_mat)) + 1j*py.numpy.array(imag(x_mat));
                end
            end
        case 'logical'
            if x_mat
                x_py = py.True;
            else
                x_py = py.False;
            end
        case 'cell'
            x_py = py.list();
            dims = size(x_mat);
            if prod(dims) == max(size(x_mat))
                % 1D cell array
                for i = 1:numel(x_mat)
                    x_py.append(mat2py(x_mat{i}, char_to));
                end
            else
                if length(dims) > 2
                    fprintf('mat2py:  %d-dimensional cell array conversion ' + ...
                            'is not implemented\n', length(dims));
                    return
                end
                nR = dims(1,1); nC = dims(1,2);
                for r = 1:nR
                    this_row = py.list();
                    for c = 1:nC
                      this_row.append(mat2py(x_mat{r,c}, char_to));
                    end
                    x_py.append(this_row);
                end
            end
        case 'struct'
            x_py = py.dict();
            F = fieldnames(x_mat);
            if (length(x_mat) > 1) && ...
               (class(x_mat) == "struct")
                % struct array
                x_py = py.list();
                for j = 1:length(x_mat)
                    x_py.append( mat2py(x_mat(j)) );
                end
            else
                for i = 1:length(F)
                    if (length(x_mat.(F{i})) > 1) && ...
                       (class(x_mat.(F{i})) == "struct")
                        % struct of struct array
                        List = py.list();
                        for j = 1:length(x_mat.(F{i}))
                            List.append( mat2py(x_mat.(F{i})(j)) );
                        end
                        x_py.update(pyargs(F{i}, List));
                    else
                        x_py.update(pyargs(F{i}, mat2py(x_mat.(F{i}))));
                    end
                end
            end
        otherwise
            fprintf('mat2py:  %s conversion is not implemented\n', class(x_mat))
    end % switch
end
