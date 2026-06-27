# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:22
    @file  : fun2.py
"""

import numpy as np


def fun2(x):
    # 工地坐标
    a1 = np.array([1.25, 8.75, 0.5, 5.75, 3.0, 7.25])
    b1 = np.array([1.25, 0.75, 4.75, 5.0, 6.5, 7.75])

    # 第一个料场坐标
    x13, x14 = x[12], x[13]
    # 第二个料场坐标
    x15, x16 = x[14], x[15]

    # 第一个料场到各工地的距离
    dist1 = np.sqrt((x13 - a1) ** 2 + (x14 - b1) ** 2)
    # 第二个料场到各工地的距离
    dist2 = np.sqrt((x15 - a1) ** 2 + (x16 - b1) ** 2)

    # f1: 第一个料场的吨千米数
    f1 = np.dot(dist1, x[0:6])
    # f2: 第二个料场的吨千米数
    f2 = np.dot(dist2, x[6:12])

    # 总运输量
    return f1 + f2

