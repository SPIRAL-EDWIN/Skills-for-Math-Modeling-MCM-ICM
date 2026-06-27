# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:48
    @file  : gm11.py
"""

import numpy as np

def gm11(x0, predict_num, verbose=True):
    """
    传统 GM(1,1) 模型
    参数：
        x0 : (n,) 原始数据（1D 可迭代/ndarray）
        predict_num : 向后预测期数（int）
        verbose : 是否打印中间信息（bool）
    返回：
        result : (predict_num,) 未来预测值
        x0_hat : (n,) 对原始数据的拟合值
        relative_residuals : (n-1,) 相对残差（从第2项开始）
        eta : (n-1,) 级比偏差
    """
    x0 = np.asarray(x0, dtype=float).reshape(-1)
    n = x0.size
    if n < 2:
        raise ValueError("x0 的长度至少为 2")

    # 1) 一次累加生成
    x1 = np.cumsum(x0)

    # 2) 紧邻均值生成数列 z1（长度 n-1）
    z1 = 0.5 * (x1[:-1] + x1[1:])

    # 3) 最小二乘拟合白化方程：x0(k) + a*z1(k) = b
    #    你的推导里用的是斜截式：y = kx + b 且 k = -a
    y = x0[1:]
    x = z1
    nn = n - 1

    denom = (nn * np.sum(x * x) - np.sum(x) ** 2)
    if abs(denom) < 1e-12:
        raise ZeroDivisionError("最小二乘拟合时分母过小，可能数据退化。")

    k = (nn * np.sum(x * y) - np.sum(x) * np.sum(y)) / denom
    b = (np.sum(x * x) * np.sum(y) - np.sum(x) * np.sum(x * y)) / denom
    a = -k  # 注意：k = -a

    if verbose:
        print("现在进行 GM(1,1) 预测的原始数据是:")
        print(x0)
        print(f"最小二乘法拟合得到的发展系数为 {-a:.6f} ，灰作用量是 {b:.6f}")

    # 4) 还原公式得到对原始序列的拟合值（x0_hat）
    x0_hat = np.zeros(n)
    x0_hat[0] = x0[0]
    # 避免 a 接近 0 时的数值不稳
    for m in range(1, n):
        x0_hat[m] = (1 - np.exp(a)) * (x0[0] - b / a) * np.exp(-a * (m - 1))

    # 5) 向后预测 predict_num 期
    result = np.zeros(predict_num)
    for i in range(predict_num):
        m = n + i  # 对应公式中的 m（从 n 起算）
        result[i] = (1 - np.exp(a)) * (x0[0] - b / a) * np.exp(-a * (m - 1))

    # 6) 残差与相对残差（从第2项开始）
    absolute_residuals = x0[1:] - x0_hat[1:]
    relative_residuals = np.abs(absolute_residuals) / x0[1:]

    # 7) 级比与级比偏差
    class_ratio = x0[1:] / x0[:-1]
    # 避免分母 1+0.5*a 为 0
    denom_eta = (1 + 0.5 * a)
    if abs(denom_eta) < 1e-12:
        denom_eta = np.sign(denom_eta) * 1e-12
    eta = np.abs(1 - (1 - 0.5 * a) / denom_eta * (1.0 / class_ratio))

    return result, x0_hat, relative_residuals, eta

