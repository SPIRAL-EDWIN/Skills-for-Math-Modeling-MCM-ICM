# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:57
    @file  : GM_MAIN.py
"""

# -*- coding: utf-8 -*-
"""
灰色预测 GM(1,1) 全流程（Python 版）
- 画时间序列
- 数据合法性检查
- 准指数规律检验（光滑比）
- 训练/试验分组并对试验组预测与对比
- 用全量数据拟合与向后预测
- 相对残差与级比偏差检验 + 绘图
"""

import numpy as np
import matplotlib.pyplot as plt
from gm11 import gm11

# ========= 参数区 =========
AUTO_JUDGE = True          # 自动判定是否通过准指数规律检验
PREDICT_NUM = 5            # 往后预测期数（可修改）
SMOOTH_RATIO_TH1 = 0.60    # 指标1阈值（≥60%）
SMOOTH_RATIO_TH2 = 0.90    # 指标2阈值（≥90%）

# ========= 中文显示（避免乱码与负号问题）=========
plt.rcParams['font.sans-serif'] = ['Kaiti']
plt.rcParams['axes.unicode_minus'] = False


# ========= 1) 输入原始数据并作时间序列图 =========
year = np.arange(1995, 2005, 1, dtype=int)  # 1995..2004
x0 = np.array([174, 179, 183, 189, 207, 234, 220.5, 256, 270, 285], dtype=float)

plt.figure(1)
plt.plot(year, x0, 'o-', label='原始数据')
plt.grid(True)
plt.xticks(year)
plt.xlabel('年份'); plt.ylabel('排污总量')
plt.title('原始数据的时间序列图')
plt.legend(loc='best')

# ========= 2) 合法性检查 =========
ERROR = 0

if np.any(x0 < 0):
    print('亲，灰色预测的时间序列中不能有负数哦')
    ERROR = 1

n = len(x0)
print(f'原始数据的长度为 {n}')
if n <= 3:
    print('亲，数据量太小，我无能为力哦')
    ERROR = 1

if n > 10:
    print('亲，这么多数据量，一定要考虑使用其他的方法哦，例如 ARIMA，指数平滑等')

year = year.reshape(-1)
x0 = x0.reshape(-1)

# ========= 3) 准指数规律检验 =========
if ERROR == 0:
    print('------------------------------------------------------------')
    print('准指数规律检验')
    x1 = np.cumsum(x0)
    rho = x0[1:] / x1[:-1]  # 光滑度

    plt.figure(2)
    plt.plot(year[1:], rho, 'o-', label='光滑度')
    plt.plot([year[1], year[-1]], [0.5, 0.5], '-', label='临界线 0.5')
    plt.grid(True)
    plt.xticks(year[1:])
    plt.xlabel('年份'); plt.ylabel('原始数据的光滑度')
    plt.legend(loc='best')

    ind1 = 100 * np.mean(rho < 0.5)                     # 指标1：整体占比
    ind2 = 100 * np.mean(rho[2:] < 0.5) if n - 3 > 0 else np.nan  # 指标2：除前两期
    print(f'指标1：光滑比小于 0.5 的数据占比为 {ind1:.1f}%')
    if not np.isnan(ind2):
        print(f'指标2：除去前两个时期外，光滑比小于 0.5 的数据占比为 {ind2:.1f}%')
    print('参考标准：指标1一般要大于60%, 指标2要大于90%')

    if AUTO_JUDGE:
        passed = (ind1 >= 100 * SMOOTH_RATIO_TH1) and (np.isnan(ind2) or ind2 >= 100 * SMOOTH_RATIO_TH2)
        if not passed:
            print('【提示】准指数规律检验未达到参考标准，灰色模型可能不太适合，但这里继续后续步骤。')
        print('------------------------------------------------------------')
    else:
        print('（如需人工判断，请将 AUTO_JUDGE 设为 False，并自己添加交互逻辑。）')
        print('------------------------------------------------------------')

# ========= 4) 训练组 / 试验组划分 & 试验组预测对比 =========
if ERROR == 0:
    test_num = 3 if n > 7 else 2
    train_x0 = x0[:-test_num]
    test_x0 = x0[-test_num:]
    test_year = year[-test_num:]

    print('训练数据是:\n', train_x0)
    print('试验数据是:\n', test_x0)
    print('------------------------------------------------------------')
    print('***下面是 GM(1,1) 模型预测的详细过程***')

    result1, _, _, _ = gm11(train_x0, test_num, verbose=True)

    print('------------------------------------------------------------')

    # 试验组对比图
    plt.figure(3)
    plt.plot(test_year, test_x0, 'o-', label='试验组真实数据')
    plt.plot(test_year, result1, '*-', label='GM(1,1) 预测结果')
    plt.grid(True)
    plt.xticks(np.arange(test_year[0], test_year[-1] + 1))
    plt.xlabel('年份'); plt.ylabel('排污总量')
    plt.legend(loc='best')
    plt.title('试验组：真实 vs 预测')

# ========= 5) 用全量数据拟合并向后预测 =========
if ERROR == 0:
    predict_num = int(PREDICT_NUM)
    result, x0_hat, relative_residuals, eta = gm11(x0, predict_num, verbose=False)

    # 输出拟合与预测结果
    print('------------------------------------------------------------')
    print('对原始数据的拟合结果：')
    for yi, xi_hat in zip(year, x0_hat):
        print(f'{yi} ： {xi_hat:.6f}')
    print(f'往后预测 {predict_num} 期得到的结果：')
    for k in range(predict_num):
        print(f'{year[-1] + 1 + k} ： {result[k]:.6f}')

    # 相对残差与级比偏差图
    plt.figure(4)
    plt.subplot(2, 1, 1)
    plt.plot(year[1:], relative_residuals, '*-')
    plt.grid(True); plt.legend(['相对残差'], loc='best'); plt.xlabel('年份')
    plt.xticks(year[1:])

    plt.subplot(2, 1, 2)
    plt.plot(year[1:], eta, 'o-')
    plt.grid(True); plt.legend(['级比偏差'], loc='best'); plt.xlabel('年份')
    plt.xticks(year[1:])
    print(' ')
    print('****下面将输出对原数据拟合的评价结果***')

    # 残差检验
    average_relative_residuals = float(np.mean(relative_residuals))
    print(f'平均相对残差为 {average_relative_residuals:.6f}')
    if average_relative_residuals < 0.1:
        print('残差检验：模型拟合程度非常不错')
    elif average_relative_residuals < 0.2:
        print('残差检验：模型拟合程度达到一般要求')
    else:
        print('残差检验：模型拟合程度不太好，建议使用其他模型')

    # 级比偏差检验
    average_eta = float(np.mean(eta))
    print(f'平均级比偏差为 {average_eta:.6f}')
    if average_eta < 0.1:
        print('级比偏差检验：模型拟合程度非常不错')
    elif average_eta < 0.2:
        print('级比偏差检验：模型拟合程度达到一般要求')
    else:
        print('级比偏差检验：模型拟合程度不太好，建议使用其他模型')
    print(' ')
    print('------------------------------------------------------------')

    # 最终综合图
    plt.figure(5)
    plt.plot(year, x0, '-o', label='原始数据')
    plt.plot(year, x0_hat, '-*m', label='拟合数据')
    fut_year = np.arange(year[-1] + 1, year[-1] + 1 + predict_num)
    plt.plot(fut_year, result, '-*b', label='预测数据')
    # 连接最后一个已知点与首个预测点
    plt.plot([year[-1], fut_year[0]], [x0[-1], result[0]], '-*b')
    plt.grid(True)
    plt.xticks(np.arange(year[0], fut_year[-1] + 1))
    plt.xlabel('年份'); plt.ylabel('排污总量')
    plt.legend(loc='best')
    plt.title('GM(1,1) 拟合与预测')

plt.show()

