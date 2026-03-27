from homework040207 import jacobi_method
import numpy as np

A = np.array([[1,2,-2], [1,1,1], [2,2,1]], dtype = float)
b = np.array([-3,1,1], dtype = float)
x0 = np.array([0,0,0], dtype = float)
print("Jacobi method:")
solution = jacobi_method(A, b, x0, epsilon = 1e-5)
print(f"解向量: {solution}")