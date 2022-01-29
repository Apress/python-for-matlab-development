#!/usr/bin/env python3
# pythran/fem/load_node_ele.py
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
#import os.path
import numpy as np
# pythran export load_node_file(str)
def load_node_file(File): # {{{
    """
    Reads a triangle .node file.  First line is
      nPts 2 0 0
    followed by nPts lines having
      id  X  Y  \d
    (the last digit is ignored)
    Returns a list of (x,y) pairs.
    The id is ignored because entries appear
    in consecutive order starting at 1.
    Thus points[26] has x,y for id=27.
    """
####if not os.path.isfile(File):
####    print(f'load_node_file({File}): no such file')
####    return None
    points = []
#   with open(File, 'r') as fh:
    fh = open(File, 'r')
    if True:
        L = fh.readline()  # header line; don't need it
        for L in fh:
            L = L.rstrip().lstrip()
            if not L: continue  # blank line
            if L.startswith('#'): continue  # comment line
            words = L.split()
            if words[0].startswith('#'): continue
            x, y  = float(words[1]), float(words[2])
            points.append( (x,y) )
    fh.close()
    return np.array(points)
# }}}
# pythran export load_ele_file(str)
def load_ele_file(File):  # {{{
    """
    Reads a triangle .ele file.  First line is
      nElem 3 0 0
    followed by nElem lines having
      elem_id  node_id_1  node_id_2  node_id_3

    Returns either a list of triangular element node IDs:
        (nid1,nid2,nid3)
    or, if Rod=True, a set of rod element IDs where one
    triangular element yields three rod elements:
        (nid1,nid2)
        (nid1,nid3)
        (nid2,nid3)
    Only unique pairs are returned.

    elem_id is ignored.
    """
####if not os.path.isfile(File):
####    print(f'load_ele_file({File}): no such file')
####    return None
    known_rods = {} # keyed by a set of two nid ID's
    elements = []
#   with open(File, 'r') as fh:
    fh = open(File, 'r')
    if True:
        L = fh.readline()  # header line; don't need it
        for L in fh:
            L = L.rstrip().lstrip()
            if not L: continue  # blank line
            if L.startswith('#'): continue  # comment line
            words = L.split()
            if words[0].startswith('#'): continue
            nid1, nid2, nid3 = int(words[1]), int(words[2]), int(words[3])
            elements.append( (nid1, nid2, nid3) )
    fh.close()
    return np.array(elements)
# }}}
