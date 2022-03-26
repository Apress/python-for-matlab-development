# bridge_numpy_index.py
def ind(z, row, col):
    return z[int(row)-1, int(col)-1]
def nind(z, *i):
    int_minus_1 = tuple([int(_) - 1 for _ in i])
    return z[int_minus_1]
