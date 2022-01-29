#!/usr/bin/env python3
# code/IO/sqlite_create.py
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
import os
import os.path
# create the database file lat_lon_company.db
db_file = 'lat_lon_company.db'
if os.path.exists(db_file):
    os.remove(db_file)
connection = sqlite3.connect(db_file)
cursor     = connection.cursor()
# add a table called 'companies' with five fields
cursor.execute('''create table companies(
                            lon float,
                            lat float,
                            name text,
                            industry text,
                            revenue_mil float);''')
data = [
    [-106.52, 35.079, "Acme,  Inc.", "cosmetics",  12.3],
    [-86.17, 41.717, "FlexMex", "restaurant", 0.5],
    [-80.75, 41.214, "Titan Hercules, LLP", "sporting goods",  45.3],
    [-95.54, 29.783, "The Chicken Palace",  "restaurant",  22.3],
    [-98.48, 29.355, "Joe's Diner",  "restaurant",  0.0045],
    [-78.99, 33.784, "Amalgamated Powders", "cosmetics",  1.9],
    [-122.68, 45.525, "Pie and Cake", "restaurant", 2.2],
    ]
# insert the first row
cursor.execute('insert into companies values (?,?,?,?,?)', data[0])
# insert a bunch of rows at once
cursor.executemany('insert into companies values (?,?,?,?,?)', data[1:])
# commit the pending transactions
connection.commit()
connection.close()
