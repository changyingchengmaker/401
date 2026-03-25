#use Doolittle's method to solve linar equations Ax = b
import numpy as np

def doolittle(A, b):
  n = len(A)
  L = np.zeros((n, n))
  U = np.zeros((n, n))
  
  for i in range(n):
    # 构建U矩阵
    for j in range(i, n):
      U[i, j] = A[i, j]
      for k in range(i):
        U[i, j] -= L[i, k] * U[k, j]
    
    # 构建L矩阵
    for j in range(i + 1, n):
      L[j, i] = A[j, i]
      for k in range(i):
        L[j, i] -= L[j, k] * U[k, i]
      L[j, i] /= U[i, i]
  
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
      x[i] -= U[i, j] * x[j]
    x[i] /= U[i, i]
  
  return x

A = np.array([[6,2,1,-1], [2,4,1,0], [1,1,4,-1], [-1,0,-1,3]], dtype=float)
b = np.array([6,-1,5,-5], dtype=float)
solution = doolittle(A, b)
print("解:", solution)