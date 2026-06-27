# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:31
    @file  : code12.py
"""

# pip install numpy scipy matplotlib

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

plt.rcParams['font.sans-serif'] = ['Kaiti']
plt.rcParams['axes.unicode_minus'] = False

# =========================
# 一、单次求解（设置权重 w1,w2）
# =========================
# 你在 MATLAB 里最后一次设置的是 w1=0.3, w2=0.7
w1, w2 = 0.3, 0.7

# 目标函数系数：c = [w1/30*2 + w2/2*0.4,  w1/30*5 + w2/2*0.3]
c = np.array([w1/30*2 + w2/2*0.4,  w1/30*5 + w2/2*0.3], dtype=float)

# 线性不等式：A_ub x <= b_ub （原式 -x1 - x2 <= -7 ）
A_ub = np.array([[-1.0, -1.0]])
b_ub = np.array([-7.0])

# 上下界：0 <= x1 <= 5,  0 <= x2 <= 6
bounds = [(0, 5), (0, 6)]

res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

if not res.success:
    raise RuntimeError(res.message)

x = res.x
fval = res.fun
f1 = 2*x[0] + 5*x[1]
f2 = 0.4*x[0] + 0.3*x[1]

print("单次求解（w1=%.3f, w2=%.3f）" % (w1, w2))
print("x* =", x)
print("f1 =", f1)
print("f2 =", f2)
print("综合指标值（加权和） =", fval)

# =========================
# 二、敏感性分析（扫描 w1∈[0.1,0.5]）
# =========================
W1 = np.arange(0.1, 0.5001, 0.001)
W2 = 1.0 - W1
n  = len(W1)

F1   = np.zeros(n)
F2   = np.zeros(n)
X1   = np.zeros(n)
X2   = np.zeros(n)
FVAL = np.zeros(n)

A_ub = np.array([[-1.0, -1.0]])
b_ub = np.array([-7.0])
bounds = [(0, 5), (0, 6)]

for i in range(n):
    w1, w2 = W1[i], W2[i]
    c = np.array([w1/30*2 + w2/2*0.4,  w1/30*5 + w2/2*0.3], dtype=float)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if not res.success:
        # 理论上该简单 LP 都可行/有界；为稳妥处理异常
        F1[i] = F2[i] = X1[i] = X2[i] = np.nan
        FVAL[i] = np.nan
        continue
    x = res.x
    X1[i], X2[i] = x[0], x[1]
    F1[i] = 2*x[0] + 5*x[1]
    F2[i] = 0.4*x[0] + 0.3*x[1]
    FVAL[i] = res.fun

# =========================
# 三、绘图
# =========================
plt.figure(1)
plt.plot(W1, F1, label='f1')
plt.plot(W1, F2, label='f2')
plt.xlabel('f1 的权重')
plt.ylabel('f1 与 f2 的取值')
plt.legend()
plt.title('目标函数值随权重变化')

plt.figure(2)
plt.plot(W1, X1, label='x1')
plt.plot(W1, X2, label='x2')
plt.xlabel('f1 的权重')
plt.ylabel('x1 与 x2 的取值')
plt.legend()
plt.title('最优解分量随权重变化')

plt.figure(3)
plt.plot(W1, FVAL)
plt.xlabel('f1 的权重')
plt.ylabel('综合指标（加权和）')
plt.title('综合指标随权重变化')
plt.show()

