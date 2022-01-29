#!/usr/bin/env python3
# code/IO/write_pickle.py
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
import pickle
import numpy as np

cm = np.array([[2., 3],[0, 1]]) - np.eye(2)*1j
a_list = ['this', 'is', 'a', 'complex', 'matrix', cm]
a_dict = { 1 : 1, 2 : 'two', 'three' : 3}
an_int = 42
some_bytes = b'1ee50ffe2fb5104144142f001a8ca94ae56b90cf'
X = np.arange(12,dtype=np.float16).reshape(3,4)

P = {
    'a_list'     : a_list,
    'a_dict'     : a_dict,
    'an_int'     : an_int,
    'some_bytes' : some_bytes,
    'X'          : X,
}

with open('data.pkl', 'wb') as fh:
    pickle.dump(P, fh, pickle.HIGHEST_PROTOCOL)
