#!/usr/bin/env python3
# code/geopandas/LA_home_prices.py
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
from matplotlib.transforms import Bbox
import geopandas as gp
import pandas as pd

zipcode_geom = gp.read_file('usa_zip/tl_2019_us_zcta510.shp')
home_prices  = pd.read_csv('Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_mon.csv')
# rename zip code columns to enable join
zipcode_geom.rename(columns={'ZCTA5CE10':'ZipCode'}, inplace=True)
home_prices.rename(columns={'RegionName':'ZipCode'}, inplace=True)
# change type from 'object' to 'int64'
zipcode_geom['ZipCode'] = zipcode_geom['ZipCode'].astype(int)
# subset to just LA County
LA_prices = home_prices[
                  home_prices['CountyName'] == 'Los Angeles County'][
                  ['ZipCode','2020-05-31','2021-05-31']]
LA_price_map = zipcode_geom.merge(LA_prices,on='ZipCode')
LA_price_map['2020-05-31'] /= 1.0e6  # change units to million dollars
LA_price_map.plot(column='2020-05-31',cmap='plasma',
        legend=True,figsize=(10,14))
plt.xlim(left=-118.55,right=-118.17)
plt.ylim(top=34.14,bottom=33.7)
plt.title('Los Angeles County Home Prices 2020-05-31, $M')
plt.ylabel('Latitude [deg]')
plt.xlabel('Longitude [deg]')
# label each zip code
for i,row in LA_price_map.iterrows():
    center = row['geometry'].centroid.xy
    xy = center[0][0], center[1][0]
    plt.annotate(text=row['ZipCode'], xy=xy,
                 horizontalalignment='center')
plt.savefig('LA_home_prices.png', bbox_inches=Bbox([[0.9,0.9],[9,13]]),
            transparent=True)
plt.show()
