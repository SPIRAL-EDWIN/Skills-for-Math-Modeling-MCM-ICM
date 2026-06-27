# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:29
    @file  : zhipai.py
"""

# pip install scipy

import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

# 目标系数（总用时；指派问题为“最小化”）
# 列主序：每个人的4个泳姿依次排放（甲的4项、乙的4项、…、戊的4项）
c = np.array([
    66.8, 75.6, 87.0, 58.6,   # 甲：自由/蝶/仰/蛙
    57.2, 66.0, 66.4, 53.0,   # 乙
    78.0, 67.8, 84.6, 59.4,   # 丙
    70.0, 74.2, 69.6, 57.2,   # 丁
    67.4, 71.0, 83.8, 62.4    # 戊
], dtype=float)

n = 20

# 线性不等式：每个人最多选1个泳姿（5行，每行对应一人，连续4个变量为该人的4个泳姿）
A_ub = np.zeros((5, n))
for i in range(5):
    A_ub[i, 4*i:4*i+4] = 1.0
b_ub = np.ones(5)

# 线性等式：每种泳姿恰好1人参加（4行：自由/蝶/仰/蛙）
A_eq = np.zeros((4, n))
for stroke in range(4):
    A_eq[stroke, stroke::4] = 1.0   # 取第 stroke, stroke+4, stroke+8, ...（跨人取同一泳姿）
b_eq = np.ones(4)

# 变量 0/1
bounds = Bounds(lb=np.zeros(n), ub=np.ones(n))
integrality = np.ones(n, dtype=int)

# SciPy milp 需要把等式用两侧相同界的 LinearConstraint 表达
con_ub = LinearConstraint(A_ub, lb=-np.inf*np.ones_like(b_ub), ub=b_ub)
con_eq = LinearConstraint(A_eq, lb=b_eq, ub=b_eq)

res = milp(c=c, integrality=integrality,
           constraints=[con_ub, con_eq],
           bounds=bounds)

if res.x is None:
    raise RuntimeError(f"求解失败：{res}")

x = np.round(res.x).astype(int)  # 二进制
fval = res.fun                   # 最小总用时

print("最小总用时：", float(fval))

# 还原成 5x4（人 × 泳姿）
assign = x.reshape(5, 4, order='C')  # 因为我们构造时就是每人4列连在一起
persons = ['甲', '乙', '丙', '丁', '戊']
strokes = ['自由泳', '蝶泳', '仰泳', '蛙泳']

print("\n指派矩阵（行=人，列=泳姿，1表示被选中）：")
print(assign)

print("\n具体指派：")
for i, row in enumerate(assign):
    j = np.argmax(row)  # 每行恰好一个1
    print(f"{persons[i]} → {strokes[j]}  (用时 {c[4*i + j]})")

