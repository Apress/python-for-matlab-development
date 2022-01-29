#!/usr/bin/env python
# code/bin/patch_cartopy.py
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
# Change the active cartopy installation so that:
#  1. Replace urllib with requests to download image tiles in
#     cartopy/io/img_tiles.py
#  2. [Windows only] Replace variable sys.prefix with expanded
#     string in shapely/geos.py when searching for geos_c.dll
#     so it can be found by MATLAB.

import sys
import pathlib
import shutil
import re
import cartopy.io
import shapely

def fix_geos():                                             # {{{
    """
    On Windows, modify shapely/geos.py when the CONDA_PREFIX
    string is empty so that
        sys.prefix
    is hardcoded to the correct virtual environment path
    to load the geos_c.dll.
    """
    if sys.platform != 'win32':
        print('fix_geos() exit since this is not Windows')
        return

    shapely_dir = shapely.__path__

    if not shapely_dir:
        print(f"Unable to determine shapely's location, exit")
        return

    P = pathlib.Path(shapely_dir[0]) / 'geos.py'
    if not P.exists():
        print(f"{str(P)} doesn't exist, exit")
        return

    lines_in  = P.read_text().split('\n')
    found_win = False
    for L in lines_in:
        if re.search(r'_lgeos\s*=.*?sys\.prefix,.*?geos_c\.dll', L):
            found_win = True
    if not found_win:
        print(f"{str(P)} does not use sys.prefix to determine "
              f"geos_c.dll path, nothing done.")
        return

    shutil.copy(str(P), f'{str(P)}.bak') # backup the original version
    print(f'Wrote backup {str(P)}.bak')

    lines_out = []
    found_win = False
    did_fix   = False
    for L in lines_in:
        if did_fix:
            lines_out.append( L )
            continue
        if re.search(r"\s*==\s*'win32':", L):
            found_win = True
            lines_out.append( L )
        elif found_win and L.endswith("'geos_c.dll'))"):
            did_fix = True
            lines_out.append( f'#{L}' )
            lines_out.append( L.replace('sys.prefix', f"r'{sys.prefix}'") )
        else:
            lines_out.append(L)

    P.write_text('\n'.join(lines_out))
    print(f'Wrote updated {str(P)}')
# }}}
def fix_img_tiles():                                        # {{{
    """
    Modify cartopy/io/img_tiles.py to use
        requests.get()
    instead of
        urllib.request.Request()
    to download an image tile.
    """
    cartopy_io_dir = cartopy.io.__path__

    if not cartopy_io_dir:
        print(f"Unable to determine cartopy.io's location, exit")
        return

    P = pathlib.Path(cartopy_io_dir[0]) / 'img_tiles.py'
    if not P.exists():
        print(f"{str(P)} doesn't exist, exit")
        return

    lines_in  = P.read_text().split('\n')
    if 'import requests' in lines_in:
        print(f'{str(P)} already uses requests module, nothing done')
        return

    shutil.copy(str(P), f'{str(P)}.bak') # backup the original version
    print(f'Wrote backup {str(P)}.bak')

    New = [
        'request = requests.get(url, stream=True)',
        'request.raw.decode_content = True',
        'img = Image.open(request.raw)',
        ]

    lines_out = []
    request_start = 0
    for L in lines_in:
        if re.search(r'^import\s+cartopy\s*$', L):
            lines_out.append('import requests')
            lines_out.append(L)
        elif re.search(r'^\s+request\s+=\s*', L):
            request_start = 1
            lines_out.append(f'#{L}')
            spaces = ' ' * L.find('r')  # 12
            lines_out.append(f'{spaces}{New[0]}')
            lines_out.append(f'{spaces}{New[1]}')
            lines_out.append(f'{spaces}{New[2]}')
        elif 0 < request_start < 5:
            request_start += 1
            lines_out.append(f'#{L}')
        else:
            lines_out.append(L)
    P.write_text('\n'.join(lines_out))
    print(f'Wrote updated {str(P)}')
# }}}
def main():
    fix_geos()
    fix_img_tiles()
    pass

if __name__ == "__main__": main()
