# code/matlab_py/bridge_geopandas.py
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
def row_filter(dframe, A, op, B):
    operation = {
            '==' : lambda DF, A, B : DF[DF[A] == B],
            '!=' : lambda DF, A, B : DF[DF[A] != B],
            '<=' : lambda DF, A, B : DF[DF[A] <= B],
            '>=' : lambda DF, A, B : DF[DF[A] >= B],
            '<'  : lambda DF, A, B : DF[DF[A] <  B],
            '>'  : lambda DF, A, B : DF[DF[A] >  B],
            }
    if op not in operation:
        print(f'bridge_geopandas.row_filter: "{op}" not recognized')
        return None
    return operation[op](dframe, A, B)
def col_filter(dframe, cols):
    return dframe[[*cols]]
def rename_col(dframe, A, B):
    dframe.rename(columns={A:B}, inplace=True)
def astype(dframe, col, new_type):
    if new_type == 'int':
        dframe[col] = dframe[col].astype(int)
    elif new_type == 'float':
        dframe[col] = dframe[col].astype(float)
    elif new_type == 'str':
        dframe[col] = dframe[col].astype(str)
    else:
        print(f'bridge_geopandas.astype: "{new_type}" not recognized')
def mult_by(dframe, col, scale):
    dframe[col] *= scale
def iterrows(dframe):
    i = -1
    n_rows = len(dframe)
    def increment():
        nonlocal i
        i += 1
        if i < n_rows:
            return dframe.iloc[i]
        else:
            return None
    return increment
