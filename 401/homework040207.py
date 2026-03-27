#use jacobi method to solve the linar eqation Ax = b

import numpy as np

#无穷范数
def norm(x):
    return np.max(np.abs(x))
    
def jacobi_guass_seidel_method(A, b, x0, epsilon = 1e-3):
    n = len(b)
    times = 0 
    s = 1
    while s > epsilon:
        x1 = np.copy(x0)
        for i in range(n):
            sum1 = np.dot(A[i, :i], x1[:i])
            sum2 = np.dot(A[i, i+1:], x0[i+1:])
            x1[i] = (b[i] - sum1 - sum2) / A[i, i]
        s = norm(x1 - x0)
        x0 = np.copy(x1)
        times += 1
        print(f"迭代次数: {times}, 当前解: {x1}")
    return x1

def jacobi_method(A, b, x0, epsilon = 1e-3):
    n = len(b)
    times = 0 
    s = 1
    while s > epsilon:
        x1 = np.copy(x0)
        for i in range(n):
            sum = np.dot(A[i], x0)-A[i, i]*x0[i]
            x1[i] = (b[i] - sum) / A[i, i]
        s = norm(x1 - x0)
        x0 = np.copy(x1)
        times += 1
        print(f"迭代次数: {times}, 当前解: {x1}")
    return x1

A = np.array([[5,2,1], [-1,4,2], [2,-3,10]])
b = np.array([-12,20,3])
x0 = np.array([0,0,0], dtype = float)
print("="*50)
print("Jacobi-Guass-Seidel method:")
solution1 = jacobi_guass_seidel_method(A, b, x0)
print("="*50)
print("jacobi method:")
solution2 = jacobi_method(A, b, x0)


