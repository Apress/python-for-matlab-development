# A. Danial 2023-09-15
# Called in test_p2m.m
import numpy as np
from datetime import datetime
def a_tuple():
    return 12, "three", 4.4, datetime(2022, 3, 1, 12, 13, 14, 654321)
def a_list():
    return [12, "three", 4.4, datetime(2022, 3, 1, 12, 13, 14, 654321) ]
def a_dict():
    return { 'a' : 12, 'b' : "three", 'c' : 4.4, 
             'd' : datetime(2022, 3, 1, 12, 13, 14, 654321) }
def nested_dict():
    return { 'a' : a_tuple(),
             'b' : a_list(),
             'c' : a_dict() }
def i32_array():
    return np.reshape(np.arange(-12.5, 12.5, 2.1,dtype=np.int32),(3,4))
def i64_array():
    return np.reshape(np.arange(-12.5, 12.5, 2.1,dtype=np.int64),(3,4))
def f32_array():
    return np.reshape(np.arange(-12.5, 12.5, 2.1,dtype=np.float32),(3,4))
def f64_array():
    return np.reshape(np.arange(-12.5, 12.5, 2.1,dtype=np.float64),(3,4))
def c64_array():
    return f32_array() - 1j*f32_array()
def c128_array():
    return f64_array() - 1j*f64_array()