#!/usr/bin/env python3
# code/IO/postgres_crud.py
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
import psycopg2
import random
import time

def record():
    """Return a random integer, float, and pet type."""
    n = random.randint(1,15)
    price = 10.0 + 30*random.random()
    pet = random.choice(['dog', 'cat',
            'bunny', 'fish', 'horse'])
    return (n, price, pet)

def populate_table(conn, cur):
    T_start = time.time()
    cur.execute("""create table myvalues (id serial primary key,
                n integer, price float, pet varchar)""")
    batch_size = 3_0
    n_records  = 10_0
    batch = []
    insert = "insert into myvalues (n,price,pet) values(%s,%s,%s)"
    for i in range(n_records):
        n,price,pet = record()
        batch.append((n, price, pet))
        if len(batch) < batch_size:
            continue
        cur.executemany(insert, batch)
        conn.commit()
        batch = []
    if batch:
        cur.executemany(insert, batch)
        conn.commit()
    print(f'inserted {n_records} rows in {time.time()-T_start:.3} sec')

def query_results(cursor):
    query = "select sum(price), sum(n), pet from myvalues group by pet"
    cursor.execute(query)
    print(f'Result of {query}:')
    for sum_price, sum_n, pet in cursor.fetchall():
        print(f'  {sum_price:.2f}  {sum_n:6d}  {pet:>7s}')
    print('-' * 60)

def rename_pets(cursor, before, after):
    update_cmd = f"update myvalues set pet='{after}' where pet='{before}'"
    cursor.execute(update_cmd)
    print(f'Did:  {update_cmd}')

def remove_pets(cursor, pet):
    delete_cmd = f"delete from myvalues where pet='{pet}'"
    cursor.execute(delete_cmd)
    print(f'Did:  {delete_cmd}')

def main():
    try:
        conn = psycopg2.connect( host="413.198.155.245",
            user="al", password="SuperSecret",
            database="pet_store")
    except psycopg2.OperationalError as e:
        print(f'Failed to connect: {e}')
        return
    cur = conn.cursor()

    # drop the table 'myvalues' if it already exists
    try:
        cur.execute('drop table myvalues')
    except:
        pass

    populate_table(conn, cur)
    query_results(cur)

    rename_pets(cur, 'bunny', 'rabbit')
    query_results(cur)

    remove_pets(cur, 'cat')
    query_results(cur)

    cur.execute('drop table myvalues')

    conn.close()
if __name__ == "__main__": main()
