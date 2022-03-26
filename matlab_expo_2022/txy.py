# txy.py
import numpy as np
from datetime import datetime
def F():
    return { 't' : datetime.now(),
             'x' : np.arange(12).reshape(2,6),
             'y' : ['a list', 'with strings']}
