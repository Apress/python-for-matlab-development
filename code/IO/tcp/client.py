#!/usr/bin/env python3
# code/IO/tcp/client.py
# {{{
# This code accompanies the book _Python for MATLAB Development:
# Extend MATLAB with 300,000+ Modules from the Python Package Index_ 
# ISBN 978-1-4842-7222-0 | ISBN 978-1-4842-7223-7 (eBook)
# DOI 10.1007/978-1-4842-7223-7
# https://github.com/Apress/python-for-matlab-development
# 
# Copyright © 2022 Albert Danial
# 
# MIT License:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# }}}
import socket
import numpy as np
import struct

def wait_for_nBytes(n, Sock):
    Bytes = b''
    received = 0
    block_size = 2048
    while received < n:
        data = Sock.recv(min(n-received, block_size))
        if not data:
            break
        Bytes += data
        received += len(data)
        if len(Bytes) == n:
            break
    return Bytes

def main():
    Host, Port = '127.0.0.1', 5006
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((Host, Port))
    for i in range(10):
        N = np.random.randint(3,10) # 3 <= N < 10
        A = np.random.rand(N,N)
        s.send(struct.pack('q',N))  # send N
        print(f'sending A ({N:2d} x {N:2d}) ',end='')
        s.send(A.tobytes())         # send A
        Bytes = wait_for_nBytes(8*N*N, s)
        Ainv = np.frombuffer(Bytes, dtype=np.float64)
        # could also do
        # Ainv = np.array(struct.unpack(f'{N*N}d',Bytes))
        Ainv = Ainv.reshape(N,N)
        err = np.max(np.eye(N) - A@Ainv)
        print(f'err = {err:e}')
    s.close()
if __name__ == "__main__": main()
