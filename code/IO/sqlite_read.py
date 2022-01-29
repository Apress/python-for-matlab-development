#!/usr/bin/env python3
# code/IO/sqlite_read.py
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
import sqlite3
connection = sqlite3.connect('lat_lon_company.db')
cursor     = connection.cursor()
# read the contents of each row in descending order of revenue
query = 'select lat,name,revenue_mil from companies ' \
        'order by revenue_mil desc'
for row in cursor.execute(query):
    lat, name, revenue_mil = row
    print(f'lat={lat:9.2f} {name:20s} {revenue_mil:9.5f}')

# update the revenue of restaurants by 20%
cursor.execute("update companies set revenue_mil = " 
               "revenue_mil * 1.2 where industry = 'restaurant'");
# print updated restaurant values
query = "select lat,name,revenue_mil from companies " \
        "where industry = 'restaurant' order by revenue_mil desc"
for row in cursor.execute(query):
    lat, name, revenue_mil = row
    print(f'Updated: {name:20s} {revenue_mil:9.5f}')
connection.commit()   # necessary to preserve update
connection.close()
