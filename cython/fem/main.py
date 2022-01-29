#!/usr/bin/env python3
# cython/fem/main.py
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
import sys
import numpy as np
import scipy.linalg as la
import scipy.sparse as sp
from   scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt
import copy
from timeit import default_timer
import triangle_utils
import rod
from FE_model import FE_model

def print_tight(M, title=None):                             # {{{1
    nR,nC = M.shape
    if title:
        print(f'{title} -------')
    for r in range(nR):
        for c in range(nC):
            print(' % 8.3e' % M[r,c], end='')
        print()
# 1}}}
def box_model(elsize='qa0.4'):                              # {{{
    A = dict(vertices=np.array(((0, 0), (1, 0), (1, 1), (0, 1))))
    B = tr.triangulate(A, elsize)
    B['constrained_x'] = [] # nodes with x dof fixed
    B['constrained_y'] = [] # nodes with y dof fixed
    return B
# }}}
def equitriangle_model(elsize='qa1',                        # {{{
                       constrain=None):
    A = dict(vertices=np.array(((0, 0), (1, 0), (0.5, 0.866))))
    B = tr.triangulate(A, elsize)
    if constrain == 'bottom_edge':
        node_ids = np.argwhere(B['vertices'][:,1] == 0)
        B['constrained_x'] = node_ids.squeeze() # nodes with x dof fixed
        B['constrained_y'] = node_ids.squeeze() # nodes with y dof fixed
    else:
        B['constrained_x'] = [] # nodes with x dof fixed
        B['constrained_y'] = [] # nodes with y dof fixed
    return B
# }}}
def beam_model(elsize='qa0.4',                              # {{{
               constrain=None):
    A = dict(vertices=np.array(((0, 0), (10, 0), (10, 1), (0, 1))))
    B = tr.triangulate(A, elsize)
    if constrain is None:
        B['constrained_x'] = [] # nodes with x dof fixed
        B['constrained_y'] = [] # nodes with y dof fixed
        return B
    if constrain == 'left_edge':
        node_ids = np.argwhere(B['vertices'][:,0] == 0)
    elif constrain == 'right_edge':
        max_x = np.max(B['vertices'][:,0])
        node_ids = np.argwhere(np.abs(B['vertices'][:,0] - max_x) < 1.0e-7)
    else:
        node_L = np.argwhere(B['vertices'][:,0] == 0)
        max_x = np.max(B['vertices'][:,0])
        node_R = np.argwhere(np.abs(B['vertices'][:,0] - max_x) < 1.0e-7)
        node_ids = np.vstack([node_L, node_R])
    B['constrained_x'] = node_ids.squeeze() # nodes with x dof fixed
    B['constrained_y'] = node_ids.squeeze() # nodes with y dof fixed
    return B
# }}}
def torus_model(elsize='qpa0.05'):                          # {{{
    # https://rufat.be/triangle/examples.html
    # effective: qpa0.1
    def circle(N, R):
        i = np.arange(N)
        theta = i * 2 * np.pi / N
        pts = np.stack([np.cos(theta), np.sin(theta)], axis=1) * R
        seg = np.stack([i, i + 1], axis=1) % N
        return pts, seg

    pts0, seg0 = circle(30, 1.4)
    pts1, seg1 = circle(16, 0.6)
    pts = np.vstack([pts0, pts1])
    seg = np.vstack([seg0, seg1 + seg0.shape[0]])

    A = dict(vertices=pts, segments=seg, holes=[[0, 0]])
    B = tr.triangulate(A, elsize)
    B['constrained_x'] = [] # nodes with x dof fixed
    B['constrained_y'] = [] # nodes with y dof fixed
    return B
# }}}

def main():
    tri_model = 'code/mesh/beam.4'
    if len(sys.argv) == 1:
        print(f'using default "triangle" model {tri_model}')
    else:
        tri_model = sys.argv[1]

    T_top = default_timer()
    T_s = default_timer()
    #Model = box_model(elsize='qa=0.8')
    #Model = torus_model(elsize='qpa0.3')
    #Model = equitriangle_model(elsize='qa0.005', constrain='bottom_edge')
    #Model = beam_model(elsize='qa0.0005', constrain='left_edge')
    #Model = triangle_utils.load_model('code/mesh/simple.1')
    Model = triangle_utils.load_model(tri_model)
    T_e = default_timer()
    print(f'read model file             : {T_e-T_s:.6f} s '
          f'({tri_model})')

    T_s = default_timer()
    m = FE_model(Model)
    T_e = default_timer()
    print(f'FE_model tri->rod   {len(m.elem)} elem : {T_e-T_s:.6f} s')
    #m.show()
    m.print_summary()
    #print(m)

    T_s = default_timer()
    K,M = m.KM()
    T_e = default_timer()
    print(f'FE_model K, M     {m.nDof:7} dof : {T_e-T_s:.6f} s')
    #print('exit before modal solution'); sys.exit(0)

    T_s = default_timer()
    w,v = eigsh(K, k=6, M=M, which='LM', sigma=0)
    T_e = default_timer()
    print(f'Eigensolution for {m.nDof:7} dof : {T_e-T_s:.6f} s')
    print(f'Total                          : {T_e-T_top:.6f} s')

    iSorted = np.argsort( np.abs(w) )

    print(f'First 6 eigenvalues')
    for i in range(6):
        J = iSorted[i]
        Hz = np.sqrt( np.abs(w[J]) )/(2*np.pi)
        print(f'{i+1:2d}. {np.real(w[J]):20.3f}  {Hz:20.3f} Hz')
    #   mode_shape = m.copy_and_deform(v[:,J])
    #   m.show_comparison(mode_shape, title=f'Mode {i+1}  {Hz:.2f} Hz')

if __name__ == "__main__": main()
