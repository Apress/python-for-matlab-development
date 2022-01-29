#!/usr/bin/env python3
# code/plots/double_y_axis.py
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
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
yL = [68,    108, 112, 116, 193, 200]
yR = [9.86, 15.7, 16.2, 16.8, 28, 29]
yLmax = np.max(yL) * 1.1
materials = ['aluminum', 'zinc',
  'bronze', 'titanium',
  'iron', 'steel']
P = ax.bar(materials, yL)
ax.set_ylabel('GPa')
ax2 = ax.twinx()
ax2.set_ylabel('Mpsi')
ax.set_ylim(ymax=yLmax)
ax2.set_ylim(ymax=yLmax/6.8965)
ax.grid(True)
ax.set_axisbelow(True)
plt.title("Young's Modulus")
plt.show()
