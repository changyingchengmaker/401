import numpy as np
 
def phase_one(A, b):
    m, n = A.shape
    # 添加人工变量
    artificial = np.eye(m)
    new_A = np.hstack([A, artificial])
    # 第一阶段目标函数：最小化人工变量和
    c_phase1 = np.zeros(n + m)
    c_phase1[n:] = 1
    
    # 初始基变量是人工变量
    basis = list(range(n, n + m))
    return new_A, c_phase1, basis

def phase_two_transition(tableau, original_c, artificial_indices):
    # 删除人工变量列
    mask = np.ones(tableau.shape[1], dtype=bool)
    mask[artificial_indices] = False
    new_tableau = tableau[:, mask]
    
    # 替换目标函数行
    m = len(artificial_indices)
    new_tableau[-1, :-1] = original_c
    new_tableau[-1, -1] = 0  # 重置目标值
    
    # 重新计算检验数
    basis = [i for i in range(new_tableau.shape[1]-1) 
             if not np.allclose(new_tableau[:-1, i], 0)]
    return new_tableau, basis

def two_phase_solver(A, b, c, max_iter=100):
    # 第一阶段
    A_phase1, c_phase1, basis = phase_one(A, b)
    tableau = build_tableau(A_phase1, b, c_phase1)
    phase1_result = simplex(tableau, basis, max_iter)
    
    if not np.isclose(phase1_result[-1, -1], 0):
        raise ValueError("原问题无可行解")
    
    # 第二阶段转换
    artificial_indices = list(range(A.shape[1], A.shape[1]+A.shape[0]))
    phase2_tableau, basis = phase_two_transition(
        phase1_result, c, artificial_indices)
    
    # 第二阶段求解
    return simplex(phase2_tableau, basis, max_iter)

def build_tableau(A, b, c):
    m, n = A.shape
    tableau = np.zeros((m + 1, n + 1))
    tableau[:-1, :-1] = A
    tableau[:-1, -1] = b
    tableau[-1, :-1] = c
    return tableau

def simplex(tableau, basis, max_iter):
    m, n = tableau.shape
    for _ in range(max_iter):
        # 计算检验数
        c_B = tableau[-1, basis]
        z_B = c_B @ tableau[:-1, basis]
        tableau[-1, :-1] -= z_B
        
        # 找到最小检验数
        min_index = np.argmin(tableau[-1, :-1])
        if tableau[-1, min_index] >= 0:
            break  # 已经是最优解
        
        # 计算比率
        ratios = np.full(m-1, np.inf)
        for i in range(m-1):
            if tableau[i, min_index] > 0:
                ratios[i] = tableau[i, -1] / tableau[i, min_index]
        
        # 找到离开基变量
        leaving_index = np.argmin(ratios)
        
        # 更新基变量
        basis[leaving_index] = min_index
        
        # 高斯消元更新表格
        pivot = tableau[leaving_index, min_index]
        tableau[leaving_index] /= pivot
        
        for i in range(m):
            if i != leaving_index:
                factor = tableau[i, min_index]
                tableau[i] -= factor * tableau[leaving_index]
    
    return tableau

A = np.array([[1, 1, 1, 0], 
              [2, -1, 0, 1]])
b = np.array([4, 2])
c = np.array([-1, -2, 0, 0])  # min -x1-2x2
 
result = two_phase_solver(A, b, c)
print("最优解：", result[-1, -1])
print("基变量取值：", result[:-1, -1])