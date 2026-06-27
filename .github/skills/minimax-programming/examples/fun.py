# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:34
    @file  : fun.py
"""

import numpy as np


def Fun(x):
    a = np.array([1, 4, 3, 5, 9, 12, 6, 20, 17, 8])
    b = np.array([2, 10, 8, 18, 1, 4, 5, 10, 8, 9])

    x1, x2 = x
    f = np.abs(x1 - a) + np.abs(x2 - b)  # 向量化计算
    return f

