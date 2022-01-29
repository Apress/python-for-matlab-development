% code/matlab_py/mongo_fake_PO.m
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
pymongo = Im('pymongo');
fake_PO = Im('mongo_fake_PO');
bridge_mongo = Im('bridge_mongo');

tic;
price.bike      = 80.00;
price.golf_club = 120.00;
price.ball      = 4.50;
price.glove     = 25.00;
price.hat       = 8.25;
price_items = fieldnames(price);

local = true;

if local
    client = pymongo.MongoClient('localhost:27017');
else
    db_user = 'al';
    db_passwd = 'SuperSecret';
    db_host = '413.198.231.158';
    db_port = 27027;
    uri = sprintf("mongodb://%s:%s@%s:%d/purchase_orders", ...
            db_user, db_passwd, db_host, db_port);
    client = pymongo.MongoClient(uri);
end
db = client.get_database('purchase_orders');
n_orders = 10000;
all_PO = py.list();
for i = 1:n_orders
    PO = fake_PO.start_new_order();
    [order, total_price] = order_items(price, price_items);
    PO.update(pyargs('order', order));
    PO.update(pyargs('total_price', total_price));
    all_PO.append( PO );
end
bridge_mongo.insert_many( db, 'purchase_orders', all_PO );
fprintf('added %d orders in %.3f s\n', n_orders, toc)

function [order, total_price] = order_items(price, price_items)
    n_prices = length(price_items);
    n_items = randi(n_prices,1,1);
    order = py.list();
    total_price = 0;
    for i = 1:n_items
        i_item = randi(n_prices,1,1);
        item = price_items{i_item};
        quantity = randi(8,1,1);
        this_order = py.dict(pyargs('item',item,'quantity',quantity));
        order.append(this_order);
        total_price = total_price + price.(item)*quantity;
    end
end
