# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:45
    @file  : code2.py
"""

# pip install numpy statsmodels

import numpy as np
import statsmodels.api as sm

# 数据
x1 = np.array([1000, 600, 1200, 500, 300, 400, 1300, 1100, 1300, 300], dtype=float)
x2 = np.array([5, 7, 6, 6, 8, 7, 5, 4, 3, 9], dtype=float)
y  = np.array([100, 75, 80, 70, 50, 65, 90, 100, 110, 60], dtype=float)

# 设计矩阵：常数项、x1、x2、x1^2、x2^2（pure quadratic，无交互项）
X = np.column_stack([
    np.ones_like(x1),
    x1,
    x2,
    x1**2,
    x2**2
])

# 拟合
model = sm.OLS(y, X).fit()

# 系数与统计量
beta = model.params                   # 回归系数 [b0,b1,b2,b3,b4]
rmse = np.sqrt(model.mse_resid)       # 剩余标准差
r2   = model.rsquared
F    = model.fvalue
pF   = model.f_pvalue

print("beta =", beta)
print("RMSE =", rmse)
print("stats = [R^2, F, p(F)] =", [r2, F, pF])
print("\n95% CI:\n", model.conf_int())

# 预测（如需）
y_hat = model.predict(X)

print("\n回归模型：")
print(f"y = {beta[0]:.4f} + {beta[1]:.4f}*x1 + {beta[2]:.4f}*x2 "
      f"+ {beta[3]:.6f}*x1^2 + {beta[4]:.4f}*x2^2")

