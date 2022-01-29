#!/usr/bin/env python3
# cython/fem/rod.pyx
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
from dataclasses import dataclass, field
import numpy as np

@dataclass
class Node:
    ID : str
    x  : float
    y  : float

@dataclass
class Rod_Elem:
    ID    : str
    node_a: Node
    node_b: Node
    radius: float
    E     : float # Young's modulus of elasticity
    rho   : float # density
    # Internal values computed in __post_init__()
    # These are not supplied by the caller when
    # creating a new Rod_Elem; instead they are
    # computed from the above inputs.
    dX             : float
    dY             : float
    length         : float
    cross_sect_area: float
    mass           : float
#   dX             : float = field(init=False)
#   dY             : float = field(init=False)
#   length         : float = field(init=False)
#   cross_sect_area: float = field(init=False)
#   mass           : float = field(init=False)

    def __post_init__(self):
        """
        Called when a new Rod_Elem is defined via
           element = Rod_Elem(ID, node_a, node_b, E, rho)
        """
        self.dX = self.node_b.x - self.node_a.x
        self.dY = self.node_b.y - self.node_a.y
        self.length = np.sqrt( self.dX**2 + self.dY**2 )
        self.cross_sect_area = np.pi * self.radius**2
        self.mass = self.rho * self.length * self.cross_sect_area

    def stiffness_matrix(self):
        """
        http://www.ita.uni-heidelberg.de/~dullemond/lectures/num_phys_2010/Chapter_FiniteElements.pdf
        """
        K      = self.E * self.cross_sect_area / self.length
        cos    = self.dX/self.length
        sin    = self.dY/self.length
        cos2   = cos**2
        sin2   = sin**2
        sincos = sin*cos
        return K*np.array([[ cos2  ,  sincos, -cos2  , -sincos  ],
                           [ sincos,  sin2  , -sincos, -sin2    ],
                           [-cos2  , -sincos,  cos2  ,  sincos, ],
                           [-sincos, -sin2  ,  sincos,  sin2  , ],])

    def mass_matrix(self):
        """
        Lumped mass, returned as the diagonal of the matrix.
        http://kis.tu.kielce.pl/mo/COLORADO_FEM/colorado/IFEM.Ch31.pdf, p 31-7
        """
        return 0.5 * self.mass * np.array([1.0, 1.0, 1.0, 1.0])
