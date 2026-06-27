# pip install numpy scipy

import numpy as np
from scipy.optimize import minimize
from fun import Fun

# === 构建最小化 t 的问题：变量 z = [x1, x2, t] ===
def obj(z):
    return z[2]  # 最小化 t

# 不等式约束：t - Fun(x) >= 0  （逐分量）
def make_con(i):
    return {'type': 'ineq',
            'fun': lambda z, i=i: z[2] - Fun(z[:2])[i]}

cons = [make_con(i) for i in range(10)]

# 变量边界：x1∈[3,8], x2∈[4,10], t≥0（上界给 None）
bounds = [(3, 8), (4, 10), (0, None)]

# 初值（对应 MATLAB x0=[6,6]，给 t 一个宽松初值）
z0 = np.array([6.0, 6.0, 50.0])

res = minimize(obj, z0, method='SLSQP', bounds=bounds, constraints=cons,
               options=dict(maxiter=2000, ftol=1e-9, disp=False))

if not res.success:
    raise RuntimeError(res.message)

x1, x2, t_opt = res.x
d = Fun([x1, x2])

print(f"x* = ({x1:.4f}, {x2:.4f})")
print("feval（各分量）=", np.round(d, 4))
print("max(feval) =", d.max(), "  = 最优 t =", round(t_opt, 4))
