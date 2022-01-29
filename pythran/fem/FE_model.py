#!/usr/bin/env python3
# pythran/fem/FE_model.py
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
import scipy.sparse as sp
import rod

class FE_model:
    def ascending(self, i,j):                               # {{{
        return (i,j) if i < j else (j,i)
    # }}}
    def connectivity(self, triangle_mesh):                  # {{{
        """
        Given a mesh from triangle, returns nodes, (mesh's ['vertices'])
        and conn, a set of elements defined by their node ID's, eg,
          nodes = [[ 0.0, 0.0],
               [10.0, 0.0],
               [10.0, 1.0], ... ]
          conn = {(0, 3),
              (0, 18),
              (1, 2),
              (1, 30), ... }
        Node ID's begin with 0.
        """
        conn = []
        for i,j,k in triangle_mesh['triangles']:
            conn.append( self.ascending(i, j) ) # add node ID tuples in
            conn.append( self.ascending(j, k) ) # ascending order so that
            conn.append( self.ascending(i, k) ) # set() removes duplicates
        conn = set(conn) # remove duplicates
        return triangle_mesh['vertices'], conn
    # }}}
    def __init__(self, triangle_mesh):                      # {{{
        self.E     = 10.0e6  # psi
        self.R     = 0.1     # radius, inches
        self.rho   = 0.1     # density, lb/inches**3
        nodes, conn = self.connectivity(triangle_mesh)

        self.node  = []
        for nid,(x,y) in enumerate(nodes):
            self.node.append( rod.Node(id=nid, x=x, y=y) )
        # store coordinate min/max to set plot frame,
        # help with autoscaling
        self.xmin = min([_.x for _ in self.node])
        self.xmax = max([_.x for _ in self.node])
        self.ymin = min([_.y for _ in self.node])
        self.ymax = max([_.y for _ in self.node])

        self.constrained_dof = []
        for nid in triangle_mesh['constrained_x']:
            self.constrained_dof.append( 2*nid )
        for nid in triangle_mesh['constrained_y']:
            self.constrained_dof.append( 2*nid + 1 )
        self.constrained_dof = set( self.constrained_dof )
       #print('INIT: constrained_dof=',self.constrained_dof)

        _elem = {}
        for eid,(i,j) in enumerate(conn):
            nA = rod.Node(id=i, x=nodes[i,0], y=nodes[i,1])
            nB = rod.Node(id=j, x=nodes[j,0], y=nodes[j,1])
            _elem[eid] = rod.Rod_Elem(eid, self.node[i], self.node[j],
                                     self.R, self.E, self.rho)
        self.elem = _elem
        self.nDof = 2*len(self.node)
    # }}}
    #pythran export add_element(str, int, float list, int list, int list)
    def add_element(self, eid, kV, I, J, M):                # {{{
        E = self.elem[eid]
        nAx = 2*E.node_a.id; nAy = nAx + 1
        nBx = 2*E.node_b.id; nBy = nBx + 1

        I.append(nAx); J.append(nAx)
        I.append(nAx); J.append(nAy)
        I.append(nAx); J.append(nBx)
        I.append(nAx); J.append(nBy)

        I.append(nAy); J.append(nAx)
        I.append(nAy); J.append(nAy)
        I.append(nAy); J.append(nBx)
        I.append(nAy); J.append(nBy)

        I.append(nBx); J.append(nAx)
        I.append(nBx); J.append(nAy)
        I.append(nBx); J.append(nBx)
        I.append(nBx); J.append(nBy)

        I.append(nBy); J.append(nAx)
        I.append(nBy); J.append(nAy)
        I.append(nBy); J.append(nBx)
        I.append(nBy); J.append(nBy)

        kV.extend(E.stiffness_matrix().ravel())
        dof = np.array([2*E.node_a.id, 2*E.node_a.id+1,
                        2*E.node_b.id, 2*E.node_b.id+1,])
        M[np.ix_(dof)] += E.mass_matrix()
    # }}}
    def __str__(self):                                      # {{{
        S  = self.print_summary(str=True)
        S += f'E: {self.E:7.4e}  R: {self.R:7.4f}  rho: {self.rho:7.4f}\n'
        S += 'Elements:\n'
        for eid in self.elem:
            E = self.elem[eid]
            S += f'    E[{eid:3d}]: N[{E.node_a.id:3d}], N[{E.node_b.id:3d}]\n'
        S += 'Nodes:\n'
        for N in self.node:
            S += f'    N[{N.id:3d}]:  {N.x: 18.12f}  {N.y: 18.12f}\n'
        if self.constrained_dof:
            S += 'Constrained DOF: ' + \
                ' '.join([f'{_:d}' for _ in sorted(self.constrained_dof)]) + '\n'
        else:
            S += 'Constrained DOF: -none-'
        return S
    def __repr__(self):
        return str(self)
    # }}}
    def KM(self, dense=False):                              # {{{
        """
        Return this model's stiffness and mass matrices.
        """
        nD = self.nDof
        M = np.zeros(nD)
        if dense:
            K = np.zeros((nD,nD))
            for eid in self.elem:
                E = self.elem[eid]
                dof = np.array([2*E.node_a.id, 2*E.node_a.id+1,
                                2*E.node_b.id, 2*E.node_b.id+1,])
                K[np.ix_(dof, dof)] += E.stiffness_matrix()
                M[np.ix_(dof)] += E.mass_matrix()
            # apply constraints
            for dof in sorted(self.constrained_dof):
                M[dof]   = 0
                K[dof, : ] = 0
                K[ : ,dof] = 0
                K[dof,dof] = 1
        else:
            # sparse K in COO (coordinate) form
            I, J, kV = [], [], []
            for eid in self.elem:
                self.add_element(eid, kV, I, J, M)
            # Apply constraints by zeroing out the value.
            # Keep track of diagonal terms so as to not
            # double-book 1's.
            did_diag = {}
            for i,(i_dof,j_dof) in enumerate(zip(I,J)):
                if (i_dof in self.constrained_dof) or \
                   (j_dof in self.constrained_dof):
                   #print(f'DOF {i_dof} or {j_dof} is constrained')
                    if i_dof == j_dof and i_dof not in did_diag:
                        # the diagonal
                        kV[i]    = 1.0  # stiffness term
                        M[i_dof] = 0.0  # mass term
                        did_diag[i_dof] = True
                    else:
                        kV[i] = 0

            K = sp.coo_matrix((kV,(I,J)),shape=(nD,nD))
            M = sp.diags(M)

        return K, M
    # }}}
    def print_summary(self, str=False):                     # {{{
        S  = f'nDof : {self.nDof}    elem : {len(self.elem)}   '
        S +=  'mass : %8.5f lb  ' % sum(self.elem[_].mass   for _ in self.elem)
        S +=  '   '
        S +=  'length : %6.2f in' % sum(self.elem[_].length for _ in self.elem)
        if str:
            return S
        else:
            print(S)
    # }}}
    def deform(self, dV,                                    # {{{
               scale=None):
        """
        dV is a linear list or array of deformations to
        apply to the nodal coordinates.
        Even indices are the x component, odd are y.

        scale = None means autoscale so that deformations
                are 30% of the model's max dimension.
        """
        if scale is None:
            model_len = np.sqrt((self.xmax - self.xmin)**2 +
                                (self.ymax - self.ymin)**2)
            S = 0.1 * model_len / np.max(np.abs(dV))
        else:
            S = scale

       #print(f'max dV {np.max(np.abs(dV))}, model_len {model_len}  S {S}')
        for dX, dY, N in zip(dV[0::2],
                             dV[1::2],
                             self.node):
            N.x += S*dX
            N.y += S*dY

        # update the bounding box to the deformed shape
        self.xmin = min([_.x for _ in self.node])
        self.xmax = max([_.x for _ in self.node])
        self.ymin = min([_.y for _ in self.node])
        self.ymax = max([_.y for _ in self.node])
    # }}}
