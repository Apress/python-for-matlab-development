% code/IO/demo_openpxl.m
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
OP = Im('openpyxl');
styles = Im('openpyxl.styles');
OP_bridge = Im('bridge_openpyxl');
Workbook = OP.Workbook; 
Font        = styles.Font;
Alignment   = styles.Alignment;
PatternFill = styles.PatternFill;
book = Workbook();
sheet = book.active;
sheet.title = "Pets by weight";

% font styles, background color
ft_title = Font(pyargs('name','Arial','size',int64(14),'bold',py.True));
ft_red   = Font(pyargs('color','00FF0000'));
ft_italics = Font(pyargs('bold',py.True,'italic',py.True));
bg_green = PatternFill(pyargs('fgColor','C5FD2F','fill_type','solid'));

sheet.merge_cells('B2:D3')
OP_bridge.set(sheet, pyargs('loc','B2','value','My Pets'));
OP_bridge.set(sheet, pyargs('loc','B2','font',ft_title));
alignment = Alignment(pyargs('horizontal','center',...
                             'vertical','center'));
OP_bridge.set(sheet, pyargs('loc','B2','align',alignment));

% column headings
category = {'Name', 'Animal', 'weight [kg]'};
row = int64(4); col = int64(1);
for i = 1:length(category)
    OP_bridge.set(sheet, pyargs('row',row,'col',col+i,'value',category{i}));
    OP_bridge.set(sheet, pyargs('row',row,'col',col+i,'fill',bg_green));
end

pets = {{'Nutmeg', 'Rabbit', 2.5}, ...
        {'Annabel', 'Dog', 4.3},   ...
        {'Sunny', 'Bird', 0.02},   ...
        {'Harley', 'Dog', 17.1},   ...
        {'Toby', 'Dog', 24.0},     ...
        {'Mr Socks', 'Cat', 3.9}};
for P = pets
    row = row + 1;
    for j = 1:length(category)
        OP_bridge.set(sheet, pyargs('row',row,'col',col+j,...
                                    'value',P{1}{j}));
        if j == 3 && P{1}{j} < 0.1
            OP_bridge.set(sheet, pyargs('row',row,'col',col+j,...
                                       'font',ft_red));
        end
    end
end

% equation to sum all weights
eqn = sprintf("=SUM(D4:D%d)", row);
loc = sprintf("D%d", row + 1);
OP_bridge.set(sheet, pyargs('loc',loc,'value',eqn));

row = row + 1;
sheet.merge_cells(sprintf("B%d:C%d",row,row));
Brow = sprintf("B%d",row);
OP_bridge.set(sheet, pyargs('loc',Brow,'value','Total weight:'));
OP_bridge.set(sheet, pyargs('loc',Brow,'font',ft_italics));

book.save("pets.xlsx")
