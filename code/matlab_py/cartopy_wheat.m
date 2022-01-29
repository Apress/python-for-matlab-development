% code/matlab_py/cartopy_wheat.m
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
Im = @py.importlib.import_module;
np    = Im('numpy');
ccrs  = Im('cartopy.crs');
cfeat = Im('cartopy.feature');
shape = Im('cartopy.io.shapereader');
poly  = Im('shapely.geometry.polygon');
plt   = Im('matplotlib.pyplot');
col   = Im('matplotlib.colors'); % from_levels_and_colors
axes  = Im('mpl_toolkits.axes_grid1'); % make_axes_locatable
mpl   = Im('matplotlib');
if ispc
    mpl.use('WXAgg')    
else
    mpl.use('TkAgg')
end
i1 = int64(1);

wheat_tons.Argentina = 13930078;
wheat_tons.Brazil    =  6261895;
wheat_tons.Chile     =  1358128;
wheat_tons.Uruguay   =  1076000;
wheat_tons.Paraguay  =   840000;
wheat_tons.Bolivia   =   263076;
wheat_tons.Peru      =   214533;
wheat_tons.Colombia  =     9718;
wheat_tons.Ecuador   =     6584;
wheat_tons.Venezuela =      161;

Countries = shape.Reader('nat_earth/ne_110m_admin_0_countries.shp');
shp = py.dict(); % country shape indexed by name
for geom_meta = py.list(py.zip(...
        Countries.geometries(), Countries.records()))
    name = geom_meta{1}{2}.attributes.get('NAME_EN'); % {1}{2} = meta
    shp.update(pyargs(name, geom_meta{1}{1}));        % {1}{1} = geom
end
PC = ccrs.PlateCarree();
fig_ax = plt.subplots(i1, i1, pyargs('subplot_kw',...
                      py.dict(pyargs('projection',PC))));
fig = fig_ax{1};
ax  = fig_ax{2};
ax.set_extent([-85, -33, ... % lon
               -55,  14])    % lat

ton_intervals = [0, 10000, 100000, 1000000, 10000000, 15000000];
fraction_interval = linspace(0.12, 1, length(ton_intervals));
colors = plt.cm.BuPu(fraction_interval(1:end-1));
col_ind = np.arange(4, pyargs('dtype',np.int64));

country_names = fieldnames(wheat_tons);
for i = 1:numel(country_names)
    ctry = country_names{i};
    w_tons = wheat_tons.(ctry);
    color_row = np.searchsorted(ton_intervals, w_tons) - 1;
    fprintf('%20s %10d tons, color=%d\n', ctry, w_tons, int32(color_row))
    color = colors.take(col_ind + int64(4)*color_row);
    if py.isinstance(shp.get(ctry), poly.Polygon)
        shape = py.list({shp.get(ctry)});
    else
        shape = shp.get(ctry);
    end
    ax.add_geometries(shape, pyargs('crs',PC,'facecolor',color));
end

ax.add_feature(cfeat.BORDERS);
ax.add_feature(cfeat.COASTLINE);
ax.set_title('Wheat Production, 2014 [10$^6$ tons]');

% colorbar
divider = axes.make_axes_locatable(ax);
ax_cb = divider.new_horizontal(pyargs('size',"5%",'pad',0.1,...
                                      'axes_class',plt.Axes));
fig.add_axes(ax_cb);
cmap_norm = col.from_levels_and_colors(ton_intervals/1.0e+6, colors);
cmap = cmap_norm{1};
norm = cmap_norm{2};
sm = plt.cm.ScalarMappable(pyargs('cmap',cmap,'norm',norm));
plt.colorbar(sm, pyargs('cax',ax_cb));
plt.savefig('SA_wheat_2014.png', pyargs('bbox_inches','tight',...
            'pad_inches',0,'transparent','True'));
plt.show()
