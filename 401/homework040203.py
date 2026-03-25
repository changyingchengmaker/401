#使用平方根法解对称正定线性方程组
import numpy as np

def square_method(A, b):
  n = len(A)
  L = np.zeros((n, n))
  for i in range(n):
    for j in range(i + 1):
      if i == j:
        L[i, j] = np.sqrt(A[i, i] - np.sum(L[i, :j] ** 2))
      else:
        L[i, j] = (A[i, j] - np.sum(L[i, :j] * L[j, :j])) / L[j, j]
  # 前向替换求解Ly = b
  y = np.zeros(n)
  for i in range(n):
    y[i] = b[i]
    for j in range(i):
      y[i] -= L[i, j] * y[j]
  # 后向替换求解Ux = y
  x = np.zeros(n)
  for i in range(n - 1, -1, -1):
    x[i] = y[i]
    for j in range(i + 1, n):
      x[i] -= L.T[i, j] * x[j]
    x[i] /= L[i, i]
  return x

A = np.array([[4,-1,1], [-1,4.25,2.75], [1,2.75,3.5]], dtype=float)
b = np.array([6, -0.5, 1.25], dtype=float)
solution = square_method(A, b)
print("解:", solution)
