#!/usr/bin/env python3
# pythran/fem/triangle_utils.py
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
def write_file(lines, File): # {{{
    with open(File, 'w') as fh:
        fh.writelines([f'{L}\n' for L in lines])
    print(f'wrote {File}')
# }}}
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
    if not os.path.isfile(File):
        print(f'load_node_file({File}): no such file')
        return None
    points = []
    with open(File, 'r') as fh:
        L = fh.readline()  # header line; don't need it
        for L in fh:
            L = L.rstrip().lstrip()
            if not L: continue  # blank line
            if L.startswith('#'): continue  # comment line
            words = L.split()
            if words[0].startswith('#'): continue
            x, y  = float(words[1]), float(words[2])
            points.append( (x,y) )
    return np.array(points)
# }}}
def load_ele_file(File,  # {{{
                 Rod=False):
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
    if not os.path.isfile(File):
        print(f'load_ele_file({File}): no such file')
        return None
    known_rods = {} # keyed by a set of two nid ID's
    elements = []
    with open(File, 'r') as fh:
        L = fh.readline()  # header line; don't need it
        for L in fh:
            L = L.rstrip().lstrip()
            if not L: continue  # blank line
            if L.startswith('#'): continue  # comment line
            words = L.split()
            if words[0].startswith('#'): continue
            nid1, nid2, nid3 = int(words[1]), int(words[2]), int(words[3])
            if Rod:
                pair_1 = (nid1, nid2) if nid1 < nid2 else (nid2, nid1)
                pair_2 = (nid1, nid3) if nid1 < nid3 else (nid3, nid1)
                pair_3 = (nid2, nid3) if nid2 < nid3 else (nid3, nid2)
                if pair_1 not in known_rods:
                    known_rods[pair_1] = True
                    elements.append( pair_1 )
                if pair_2 not in known_rods:
                    known_rods[pair_2] = True
                    elements.append( pair_2 )
                if pair_3 not in known_rods:
                    known_rods[pair_3] = True
                    elements.append( pair_3 )
            else:
                elements.append( (nid1, nid2, nid3) )
    return np.array(elements)
# }}}
def load_model(base_file): # {{{
    """
    Reads <base_file>.node and <base_file>.ele files
    created by triangle and returns a dict of
    nodes and triangular elements.
    """

    node_file = f'{base_file}.node'
    elem_file = f'{base_file}.ele'

    return {
        'vertices'      : load_node_file(node_file),
        'triangles'     : load_ele_file( elem_file) - 1, # 0-based indexing
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
