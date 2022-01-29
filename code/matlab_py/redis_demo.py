#!/usr/bin/env python
# code/matlab_py/redis_demo.py
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
"""
https://tech.webinterpret.com/redis-notifications-python/

# start server:
    redis-server  [config file] [--port 12345]

# issue set/get from command line:
    redis-cli config set notify-keyspace-events KEA

# issue set/get from command line:
    redis-cli set price 3.21
    redis-cli get price
"""
import time
import sys
import redis
R = redis.Redis(host='localhost',port=6379) # defaults

try:
    R.ping()
except redis.exceptions.ConnectionError as e:
    print(f'Is Redis running?  Unable to connect {e}')
    sys.exit(1)

print(f'Connected to server.')

# modify configuration to enable keyspace notification
R.config_set('notify-keyspace-events', 'KEA')

retrieved_X     = R.get('X')
retrieved_month = R.get('month')

print(f'Got X = {retrieved_X}')
print(f'Got month = {retrieved_month}')

print('waiting for subscription events')
Sub = R.pubsub()  
Sub.psubscribe('__keyspace@0__:*')
while True:
    try:
        message = Sub.get_message()
    except redis.exceptions.ConnectionError:
        print('lost connection to server')
        sys.exit(1)
    if message is None:
        time.sleep(0.01)
        continue
    keyname = message['channel'].decode().replace('__keyspace@0__:','')
    if keyname == '*':
        # initial subscription value
        continue
    value = R.get(keyname)
    print(f'{keyname} = {value}')
