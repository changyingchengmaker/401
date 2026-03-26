#使用追赶法解对角线性方程组

import numpy as np

def thomas_algorithm(a, b, c, d):
    n = len(d)
    # 前向消去
    for i in range(1, n):
        w = a[i-1] / b[i-1]
        b[i] = b[i] - w * c[i-1]
        d[i] = d[i] - w * d[i-1]
    
    # 回代
    x = np.zeros(n)
    x[-1] = d[-1] / b[-1]
    for i in range(n-2, -1, -1):
        x[i] = (d[i] - c[i] * x[i+1]) / b[i]
    
    return x

a = np.array([1,1,2], dtype = float)
b = np.array([2,3,1,1], dtype = float)
c = np.array([1,1,1], dtype = float)
d = np.array([1,2,2,0], dtype = float)
solution = thomas_algorithm(a, b, c, d)
print("解:", solution)