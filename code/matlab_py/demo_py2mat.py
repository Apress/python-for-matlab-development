# code/matlab_py/demo_py2mat.py
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
import numpy as np
def simple_vars():
    I = 42
    F = np.e
    S = 'Red'
    L = [1, 2.2, 'green']
    D = {'A' : 65, 'B' : 66, 'Z' : 90}
    T = (225, 'blue')
    N = F*np.arange(12).reshape(3,4)
    return I, F, S, L, D, T, N
def nested_var():
    N = np.arange(12).reshape(3,4)
    return [1, 2.2, 'green',
            {'A' : 65, 'B' : 66,
             'N' : N,
             'Z' : (225, 'blue')},
            27.8]
def arrays():
    arr_int8      = np.array([1, 2], dtype=np.int8)
    arr_uint8     = np.array([1, 2], dtype=np.uint8)
    arr_int16     = np.array([1, 2], dtype=np.int16)
    arr_uint16    = np.array([1, 2], dtype=np.uint16)
    arr_int32     = np.array([1, 2], dtype=np.int32)
    arr_uint32    = np.array([1, 2], dtype=np.uint32)
    arr_int64     = np.array([1, 2], dtype=np.int64)
    arr_uint64    = np.array([1, 2], dtype=np.uint64)
    arr_float16   = np.array([1, 2], dtype=np.float16)
    arr_float32   = np.array([1, 2], dtype=np.float32)
    arr_float64   = np.array([1, 2], dtype=np.float64)
    arr_complex64 = np.array([1-1j, 2-2j], dtype=np.complex64)
    arr_complex128 = np.array([1-1j, 2-2j], dtype=np.complex128)
    return arr_int8     , \
           arr_uint8    , \
           arr_int16    , \
           arr_uint16   , \
           arr_int32    , \
           arr_uint32   , \
           arr_int64    , \
           arr_uint64   , \
           arr_float16  , \
           arr_float32  , \
           arr_float64  , \
           arr_complex64, \
           arr_complex128
