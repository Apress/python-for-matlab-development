#!/usr/bin/env python3
# code/os/job_shepherd.py
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
import os
import psutil
import time

refresh_sec = 1.0
max_L1  = 1.5  # 1 minute load average
max_mem_fraction = 0.5
min_cpu_pct = 50.0

ignore = {
    'chrome', 'dbus-daemon', 'dconf-service', 'firefox',
    'gnome-terminal-server', 'ssh-agent', 'systemd', 'vim', 'Xorg', 'top'}

uid_me  = psutil.Process( os.getpid() ).uids().real  # my user ID #

while True:
    L1, L5, L15 = psutil.getloadavg()
    mem = psutil.virtual_memory()
    if L1 < max_L1:
        time.sleep(refresh_sec)
        continue
    # under heavy system load
    if mem.used/mem.total < max_mem_fraction:
        time.sleep(refresh_sec)
        continue
    # under heavy system and memory load
    for proc in psutil.process_iter(['pid', 'name', 'uids']):
        if proc.name() in ignore:
            continue
        if uid_me != proc.uids().real:
            # process doesn't belong to me, can't do anything about it
            continue
        info = psutil.Process(proc.pid)
        try:
            cpu_pct = info.cpu_percent(interval=0.2)
        except:
            # process ended before cpu measurement finished
            continue
        if cpu_pct < min_cpu_pct:
            # not doing anything, ignore
            continue
        try:
            pmem = info.memory_full_info()
        except psutil.AccessDenied:
            # parent must own it, can't control this
            continue
        print(f'pid={proc.pid} name={proc.name()} CPU={cpu_pct} '
              f'pmem={pmem.rss} swap={pmem.swap}')
        if pmem.rss/mem.total > 0.5 or pmem.swap > 0:
            print(f'-> kill {proc.pid} name={proc.name()}')
            proc.kill()
    time.sleep(refresh_sec)
