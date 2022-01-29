% code/IO/tcp/server.m
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
import py.list.*
import py.sys.path
append(py.sys.path, '.')
pyclient = py.importlib.import_module('client');

AF_INET = py.socket.AF_INET;
SOCK_STREAM = py.socket.SOCK_STREAM;
s = py.socket.socket(AF_INET,SOCK_STREAM);
addr = py.tuple([{"localhost"}, int64(5006)]); % host, port
s.bind(addr)
s.listen(int64(1))
conn_addr = s.accept();
conn = conn_addr{1};
while 1
    bytes = pyclient.wait_for_nBytes(int64(8), conn);
    N = typecast(uint8(bytes), 'int64');
    if isempty(N)
        break
    end
    bytes = pyclient.wait_for_nBytes(int64(8*N*N), conn);
    A = typecast(uint8(bytes), 'double');
    A = reshape(A, N,N);
    Ainv = inv(A);
    bytes = typecast(Ainv(:), 'uint8');
    conn.send(bytes);
end
conn.close()
