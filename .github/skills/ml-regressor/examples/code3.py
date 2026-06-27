# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:47
    @file  : code3.py
"""

# pip install numpy scipy matplotlib

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import t

plt.rcParams['font.sans-serif'] = ['Kaiti']
plt.rcParams['axes.unicode_minus'] = False

# -----------------------------
# 1) 非线性模型：y = b0 * exp(b1 / x)
#    注意：curve_fit 需要 f(x, *params) 这种签名！
# -----------------------------
def volum(x, b0, b1):
    return b0 * np.exp(b1 / x)

# -----------------------------
# 2) 数据与初始值
# -----------------------------
x = np.arange(2, 17, 1, dtype=float)  # 2..16
y = np.array([6.42, 8.20, 9.58, 9.50, 9.70, 10.00, 9.93, 9.99, 10.49,
              10.59, 10.60, 10.80, 10.60, 10.90, 10.76], dtype=float)
beta0 = (8.0, 2.0)  # 初始值 (b0, b1)

# -----------------------------
# 3) 非线性最小二乘拟合
# -----------------------------
popt, pcov = curve_fit(volum, x, y, p0=beta0, maxfev=20000)
print("回归系数 beta =", popt)

# 残差与自由度
y_hat = volum(x, *popt)
resid = y - y_hat
n, p = len(y), len(popt)
dof = max(n - p, 1)
s2 = np.sum(resid**2) / dof
rmse = np.sqrt(s2)
print("RMSE =", rmse)

# -----------------------------
# 4) 预测与区间 (Δ法 + t 分布)
# -----------------------------
def jacobian_wrt_params(x0, theta, eps=1e-6):
    """
    数值近似: ∂f/∂theta at x0
    theta: (p,) -> (b0, b1)
    返回: (p,)
    """
    theta = np.asarray(theta, dtype=float)
    g = np.empty(theta.size, dtype=float)
    for k in range(theta.size):
        th_p = theta.copy(); th_m = theta.copy()
        th_p[k] += eps
        th_m[k] -= eps
        g[k] = (volum(x0, *th_p) - volum(x0, *th_m)) / (2 * eps)
    return g

t_val = t.ppf(0.975, dof)  # 95% 置信

y_mean = y_hat.copy()
ci_low_mean = np.empty_like(y_hat)
ci_high_mean = np.empty_like(y_hat)
pi_low = np.empty_like(y_hat)
pi_high = np.empty_like(y_hat)

for i, xi in enumerate(x):
    g = jacobian_wrt_params(xi, popt)
    # 注意：pcov 在 absolute_sigma=False 时已按残差方差刻度
    var_mean = g @ pcov @ g
    se_mean = np.sqrt(max(var_mean, 0.0))

    ci_low_mean[i]  = y_mean[i] - t_val * se_mean
    ci_high_mean[i] = y_mean[i] + t_val * se_mean

    # 个体预测区间：再加上残差方差 s2
    se_pred = np.sqrt(max(var_mean + s2, 0.0))
    pi_low[i]  = y_mean[i] - t_val * se_pred
    pi_high[i] = y_mean[i] + t_val * se_pred

# -----------------------------
# 5) 作图
# -----------------------------
plt.figure()
plt.plot(x, y, 'k+', label='观测')
plt.plot(x, y_hat, 'r-', label='拟合曲线')
plt.fill_between(x, ci_low_mean, ci_high_mean, alpha=0.2, label='均值95%CI')
plt.fill_between(x, pi_low, pi_high, alpha=0.15, label='个体95%PI')
plt.xlabel('x'); plt.ylabel('y')
plt.title('非线性最小二乘拟合与区间')
plt.legend()
plt.show()
