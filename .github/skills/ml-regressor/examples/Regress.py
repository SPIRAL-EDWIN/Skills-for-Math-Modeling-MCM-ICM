# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:41
    @file  : Regress.py
"""

# pip install statsmodels matplotlib numpy

import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# 1) 输入数据
x = np.array([143,145,146,147,149,150,153,154,155,156,157,158,159,160,162,164], dtype=float)
y = np.array([ 88, 85, 88, 91, 92, 93, 93, 95, 96, 98, 97, 96, 98, 99,100,102], dtype=float)

X = sm.add_constant(x)  # 插入常数项列，相当于 [ones, x]

# 2) 回归分析
model = sm.OLS(y, X)
res = model.fit()

b0, b1 = res.params
ci = res.conf_int(alpha=0.05)     # 系数95%置信区间
r2 = res.rsquared
F = res.fvalue
pF = res.f_pvalue

print("b = ", res.params)
print("bint =\n", ci)             # [[b0_L, b0_U], [b1_L, b1_U]]
print("stats = [R^2, F, pF, s] = ",
      [r2, F, pF, np.sqrt(res.mse_resid)])  # s为残差标准差（RMSE）

# 3) 残差分析：学生化残差（近似 rcoplot）
influence = res.get_influence()
stud_resid = influence.resid_studentized_internal   # 学生化残差
fitted = res.fittedvalues

plt.figure()
plt.axhline(0, ls='--')
plt.axhline( 2, ls=':', lw=1)
plt.axhline(-2, ls=':', lw=1)
plt.scatter(fitted, stud_resid)
plt.xlabel('Fitted values')
plt.ylabel('Studentized residuals')
plt.title('Residual plot (±2 as reference)')
plt.show()

# 4) 预测及作图（拟合直线）
z = res.predict(X)  # b0 + b1*x

plt.figure()
plt.plot(x, y, 'k+', label='Observed')
plt.plot(x, z, 'r', label='Fitted line')
plt.xlabel('x'); plt.ylabel('y')
plt.legend(); plt.title('Linear fit')
plt.show()

# 可打印与示例中相近的结果
print(f"回归方程: y = {b0:.4f} + {b1:.4f} x")
print(f"R^2 = {r2:.4f}, F = {F:.4f}, p(F) = {pF:.4g}")
print(f"b0置信区间: [{ci[0,0]:.4f}, {ci[0,1]:.4f}]")
print(f"b1置信区间: [{ci[1,0]:.4f}, {ci[1,1]:.4f}]")

