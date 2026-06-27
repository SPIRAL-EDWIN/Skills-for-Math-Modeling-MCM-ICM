# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:26
    @file  : beibao.py
"""

# pip install scipy

import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

# 利润（与 MATLAB 中 c 的相反数一致，这里直接用正利润便于理解）
profit = np.array([540, 200, 180, 350,  60, 150, 280, 450, 320, 120], dtype=float)

# 物品重量与容量
w = np.array([6, 3, 4, 5, 1, 2, 3, 5, 4, 2], dtype=float)
capacity = 30.0
n = len(profit)

# 目标：最大化 profit @ x  ⇔  最小化  (-profit) @ x
c = -profit

# 线性不等式约束：w @ x <= capacity
A = w[None, :]                      # 形状 (1, n)
b = np.array([capacity])
lin_con = LinearConstraint(A, lb=-np.inf, ub=b)

# 变量为 0/1
bounds = Bounds(lb=np.zeros(n), ub=np.ones(n))
integrality = np.ones(n, dtype=int)  # 全部是整数（1 表示整数变量；对于二进制配合0/1上下界即可）

res = milp(c=c, integrality=integrality,
           constraints=[lin_con], bounds=bounds)

if res.x is not None:
    x = np.round(res.x).astype(int)     # 取整到 0/1
    fval = res.fun
    best_profit = -fval                 # 还原为“最大化”的目标值

    print("最优选择 (0/1)：", x.tolist())
    print("总重量：", float(w @ x))
    print("最大总利润：", float(best_profit))
    print("选择的物品索引（从0计）：", np.where(x==1)[0].tolist())
else:
    print("未找到可行解：", res)

