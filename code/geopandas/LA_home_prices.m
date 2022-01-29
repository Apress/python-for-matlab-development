% code/geopandas/LA_home_prices.m
% {{{
% This code accompanies the book _Python for MATLAB Development:
% Extend MATLAB with 300,000+ Modules from the Python Package Index_ 
% ISBN 978-1-4842-7222-0 | ISBN 978-1-4842-7223-7 (eBook)
% DOI 10.1007/978-1-4842-7223-7
% https://github.com/Apress/python-for-matlab-development
% 
% Copyright © 2022 Albert Danial
% 
% MIT License:
% Permission is hereby granted, free of charge, to any person obtaining a copy
% of this software and associated documentation files (the "Software"), to deal
% in the Software without restriction, including without limitation the rights
% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
% copies of the Software, and to permit persons to whom the Software is
% furnished to do so, subject to the following conditions:
% 
% The above copyright notice and this permission notice shall be included in
% all copies or substantial portions of the Software.
% 
% THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
% THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
% FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
% DEALINGS IN THE SOFTWARE.
% }}}
Im  = @py.importlib.import_module;
pd  = Im('pandas');
gp  = Im('geopandas');  
BG  = Im('bridge_geopandas');  
plt = Im('matplotlib.pyplot');
trx = Im('matplotlib.transforms');
mpl = Im('matplotlib');
if ispc
    mpl.use('WXAgg')    
else
    mpl.use('TkAgg')
end

zipcode_geom = gp.read_file('usa_zip/tl_2019_us_zcta510.shp');

% zipcode_geom.rename(columns={'ZCTA5CE10':'ZipCode'}, inplace=True)
BG.rename_col(zipcode_geom, 'ZCTA5CE10','ZipCode');

% zipcode_geom['ZipCode'] = zipcode_geom['ZipCode'].astype(int)
BG.astype(zipcode_geom, 'ZipCode', 'int');

% zipcode_geom = zipcode_geom[ zipcode_geom['ZipCode'] > 90000]
BG.row_filter(zipcode_geom, 'ZipCode', '>', 90000);

home_prices = pd.read_csv('Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_mon.csv');

% home_prices.rename(columns={'RegionName':'ZipCode'}, inplace=True)
BG.rename_col(home_prices, 'RegionName', 'ZipCode');

% home_prices = home_prices[['ZipCode','2020-05-31','2021-05-31']]
home_prices = BG.col_filter(home_prices, py.list({'ZipCode',...
                            'CountyName','2020-05-31','2021-05-31'}));

% LA_prices = home_prices[home_prices['CountyName'] == 'Los Angeles County']]
LA_prices = BG.row_filter(home_prices, 'CountyName', '==', 'Los Angeles County');

LA_price_map = zipcode_geom.merge(LA_prices,pyargs('on','ZipCode'));

% LA_price_map['2020-05-31'] /= 1.0e6  # change units to million dollars
BG.mult_by(LA_price_map, '2020-05-31', 1.0/1.0e6);

size_10_14 = py.tuple([10,14]);
LA_price_map.plot(pyargs('column','2020-05-31','cmap','plasma',...
        'legend',py.True,'figsize',size_10_14));

plt.xlim(pyargs('left',-118.55,'right',-118.17));
plt.ylim(pyargs('top',34.14,'bottom',33.7));
plt.title('Los Angeles County Home Prices 2020-05-31, $M');
plt.ylabel('Latitude [deg]');
plt.xlabel('Longitude [deg]');
% label each zip code
next_row = BG.iterrows(LA_price_map);
while 1
    row = next_row();
    if strcmp(class(row), 'py.NoneType')
        break
    end
    geo = row.get('geometry');
    xy = py.tuple([geo.centroid.x, geo.centroid.y]);
    plt.annotate(pyargs('text',row.get('ZipCode'),'xy',xy,...
                 'horizontalalignment','center'));
end
bbox = trx.Bbox([0.9 0.9; 9 13]);
plt.savefig('LA_m.png', pyargs('bbox_inches',bbox,'transparent',py.True));
plt.show()
