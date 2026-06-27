# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:30
    @file  : youxi.py
"""

# pip install scipy
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

# 最大化 20 x1 + 30 x2 + 40 x3  ⇔  最小化  -20 x1 - 30 x2 - 40 x3
c = -np.array([20.0, 30.0, 40.0])

# 约束：[[4, 8, 10],
#        [1, 1, 1]] @ x <= [100, 20]
A = np.array([[4.0, 8.0, 10.0],
              [1.0, 1.0, 1.0]])
b = np.array([100.0, 20.0])
con = LinearConstraint(A, lb=-np.inf*np.ones_like(b), ub=b)

# 非负整数（注意：这里是整数≥0，不是二进制；如需二进制把上界设为1）
bounds = Bounds(lb=np.zeros(3), ub=np.array([np.inf, np.inf, np.inf]))
integrality = np.ones(3, dtype=int)

res = milp(c=c, integrality=integrality, constraints=[con], bounds=bounds)

x = np.round(res.x).astype(int)
fval = res.fun
y = -fval  # 还原为最大化
print("A、B、C三图分别通关的次数为：", x.tolist())
print("最终获得的经验为：", float(y))

