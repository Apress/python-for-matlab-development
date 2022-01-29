#!/usr/bin/env python3
# pythran/fem/main_load_node_ele.py
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
"""
Code to read/write files related to the 'triangle' mesh generator.
"""
import sys
import os.path
import numpy as np
import load_node_ele as LNE
def load_model(base_file): # {{{
    """
    Reads <base_file>.node and <base_file>.ele files
    created by triangle and returns a dict of
    nodes and triangular elements.
    """

    node_file = f'{base_file:s}.node'
    elem_file = f'{base_file:s}.ele'

    return {
        'vertices'      : LNE.load_node_file(node_file),
        'triangles'     : LNE.load_ele_file( elem_file) - 1, # 0-based indexing
        'constrained_x' : np.array([]),
        'constrained_y' : np.array([]),
        }
# }}}
def main(): # {{{
    if len(sys.argv) < 2:
        print("Usage:  %s <file>" % sys.argv[0])
        print("   where <file>.ele and <file>.node exist")
        print("   ./triangle_utils.py beam.1 beam.2 beam.3 beam.4")

        raise SystemExit

    for F in sys.argv[1:]:
        model = load_model(F)
        print(f"{F:<10s} "
              f"{len(model['vertices']):7d} nodes, "
              f"{len(model['triangles']):7d} triangles")
        print('Nodes:')
        print(model['vertices'])
        print('Elements:')
        print(model['triangles'])
# }}}
if __name__ == "__main__": main()
