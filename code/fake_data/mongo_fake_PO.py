#!/usr/bin/env python
# code/fake_data/mongo_fake_PO.py
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
from pymongo import MongoClient
from urllib.parse import quote_plus
from faker import Faker
from datetime import datetime
import time

fake = Faker()
Faker.seed(123)  # for reproducibility
start_date = datetime(1997, 1, 31, 12, 0, 0)
end_date   = datetime(2025, 1, 31, 12, 0, 0)

def start_new_order():
    PO = {}
    PO['customer_name'] = fake.name()
    PO['customer_phone'] = fake.phone_number()
    PO['order_number'] = fake.uuid4()
    PO['order_date'] = fake.date_time_between_dates(
                            start_date, end_date)
    return PO

def order_items(price):
    n_items = fake.random_int(min=1,max=len(price))
    order = []
    total_price = 0
    for i in range(n_items):
        item = fake.random_element(price.keys())
        quantity = fake.random_int(min=1,max=8)
        order.append({'item' : item, 'quantity' : quantity})
        total_price += price[item]*quantity
    return order, total_price

def main():
    T_start = time.time()
    n_orders = 10_000
    price = { 'bike' : 80.00, 'golf club' : 120.00,
              'ball' : 4.50, 'glove' : 25.00, 'hat' : 8.25}
    local = True
    if local:
        client = MongoClient('localhost:27017')
    else:
        uri = "mongodb://%s:%s@%s/purchase_orders" % (
                quote_plus('al'),
                quote_plus('SuperSecret'),
                quote_plus('413.198.231.158:27027'))
        client = MongoClient(uri)
    db = client.purchase_orders
    all_PO = []
    for i in range(n_orders):
        PO = start_new_order()
        PO['order'], PO['total_price'] = order_items(price)
        all_PO.append( PO )
    db.purchase_orders.insert_many( all_PO )
    print(f'added {n_orders} orders in {time.time()-T_start:.3f} s')
 
if __name__ == "__main__": main()
