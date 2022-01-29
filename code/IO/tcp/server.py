#!/usr/bin/env python3
# code/IO/tcp/server.py
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
import struct
import numpy as np
import socket
from client import wait_for_nBytes

def main():
    Host, Port = 'localhost', 5006

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((Host, Port))
    s.listen(1)

    conn, addr = s.accept()
    while True:
        try:
            Bytes = wait_for_nBytes(8, conn) # get bytes of N
            if not Bytes:
                break
            N = struct.unpack(f'q', Bytes)[0] # bytes -> N
            print(f'got N={N}')
            Bytes = wait_for_nBytes(8*N*N, conn) # get bytes of A
            A = np.frombuffer(Bytes, dtype=np.float64)
            # could also do
            # A = np.array(struct.unpack(f'{N*N}d', Bytes))
            A = A.reshape(N,N)
            print(f'received {N} x {N} from client')
            inv = np.linalg.inv(A)
            conn.send(inv.tobytes()) # send inv(A)
            print(f'sent inverse to client')
        except KeyboardInterrupt:
            break
    conn.close()
if __name__ == "__main__": main()
