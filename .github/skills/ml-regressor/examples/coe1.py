# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:44
    @file  : coe1.py
"""

# pip install numpy matplotlib statsmodels

import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

plt.rcParams['font.sans-serif'] = ['Kaiti']
plt.rcParams['axes.unicode_minus'] = False

# ------------------------------
# 数据
# ------------------------------
t = np.arange(1/30, 15/30, 1/30)  # 1/30:1/30:14/30，共14个点
s = np.array([11.86, 15.67, 20.6, 26.69, 33.71, 41.93, 51.13,
              61.49, 72.9, 85.44, 99.08, 113.77, 129.54, 146.48], dtype=float)

# =========================================================
# 1) 二次多项式回归（polyfit 对应 polyfit/polyconf 的核心功能）
# =========================================================
# 拟合 s ≈ p2*t^2 + p1*t + p0
p = np.polyfit(t, s, deg=2)         # 返回 [p2, p1, p0]
Y = np.polyval(p, t)                # 预测值（对应 polyconf 的均值预测）

# 作图
plt.figure()
plt.plot(t, s, 'k+', label='原始数据')
plt.plot(t, Y, 'r', label='拟合曲线')
plt.xlabel('t'); plt.ylabel('s'); plt.title('二次多项式回归')
plt.legend(); plt.show()

print("polyfit 系数（p2, p1, p0）:", p)

# 说明：MATLAB 的 polyconf 还能给出预测区间；若需要区间，可用 statsmodels 下方做法获取。

# =========================================================
# 2) 化为多元线性回归（对应 regress）
# =========================================================
# 构建设计矩阵 T = [1, t, t^2]
T = np.column_stack([np.ones_like(t), t, t**2])

model = sm.OLS(s, T).fit()
print(model.summary())  # 含系数、置信区间、R²、F、p值等

# 系数与区间（对应 b, bint）
b = model.params
bint = model.conf_int(alpha=0.05)   # 95% CI
print("b =", b)
print("bint =\n", bint)

# 拟合值与残差（可按需做残差图）
z = model.predict(T)
plt.figure()
plt.plot(t, s, 'k+', label='原始数据')
plt.plot(t, z, 'r', label='线性化拟合（t, t^2）')
plt.xlabel('t'); plt.ylabel('s'); plt.title('二次多项式 → 线性回归')
plt.legend(); plt.show()

