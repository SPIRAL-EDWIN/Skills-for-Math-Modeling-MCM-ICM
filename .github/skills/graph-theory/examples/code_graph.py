# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:33
    @file  : code_graph.py
"""

# pip install networkx matplotlib numpy

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Kaiti']
plt.rcParams['axes.unicode_minus'] = False

# 统一的辅助：隐藏坐标轴
def hide_axes(ax=None):
    ax = ax or plt.gca()
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

# =========================
# （1）无向图：无权重（默认权重=1）
# =========================
s1 = [1, 2, 3, 4]
t1 = [2, 3, 1, 1]
G1 = nx.Graph()
G1.add_edges_from(zip(s1, t1))

plt.figure()
pos = nx.spring_layout(G1, seed=42)  # 随机但可复现的布局
nx.draw(G1, pos, with_labels=True, node_size=800, width=1.5)
hide_axes()
plt.title("Undirected, unweighted")

# =========================
# 字符串节点（中文标签）
# =========================
s2 = ['学校','电影院','网吧','酒店']
t2 = ['电影院','酒店','酒店','KTV']  # KTV 节点会被自动加入
G2 = nx.Graph()
G2.add_edges_from(zip(s2, t2))

plt.figure()
pos = nx.spring_layout(G2, seed=42)
nx.draw(G2, pos, with_labels=True, node_size=900, width=2)
hide_axes()
plt.title("Undirected with string nodes")

# =========================
# （2）无向图：有权重（s,t,w）
# =========================
s = [1, 2, 3, 4]
t = [2, 3, 1, 1]
w = [3, 8, 9, 2]
G = nx.Graph()
for u, v, wt in zip(s, t, w):
    G.add_edge(u, v, weight=wt)

plt.figure()
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=800, width=2)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
hide_axes()
plt.title("Undirected, weighted (edge labels)")

# =========================
# 无向图：由邻接矩阵构造
# （非零即有边，值为权重）
# =========================
a = np.array([
    [0, 3, 9, 2],
    [3, 0, 8, 0],
    [9, 8, 0, 0],
    [2, 0, 0, 0],
], dtype=float)

# 无向图：只取上三角避免重复（类似 MATLAB 的 graph(a) 默认对称）
G_adj = nx.Graph()
n = a.shape[0]
for i in range(n):
    for j in range(i+1, n):       # 上三角
        if a[i, j] != 0:
            G_adj.add_edge(i+1, j+1, weight=a[i, j])

plt.figure()
pos = nx.spring_layout(G_adj, seed=42)
nx.draw(G_adj, pos, with_labels=True, node_size=800, width=2)
nx.draw_networkx_edge_labels(G_adj, pos, edge_labels=nx.get_edge_attributes(G_adj, 'weight'))
hide_axes()
plt.title("Undirected from adjacency (upper triangle)")

# =========================
# （3）有向图：无权 digraph(s,t)
# =========================
s = [1, 2, 3, 4, 1]
t = [2, 3, 1, 1, 4]
DG = nx.DiGraph()
DG.add_edges_from(zip(s, t))

plt.figure()
pos = nx.spring_layout(DG, seed=42)
nx.draw(DG, pos, with_labels=True, node_size=800, width=1.8, arrows=True, arrowstyle='->', arrowsize=18)
hide_axes()
plt.title("Directed, unweighted")

# =========================
# 有向图：有权 digraph(s,t,w)
# =========================
s = [1, 2, 3, 4]
t = [2, 3, 1, 1]
w = [3, 8, 9, 2]
DGw = nx.DiGraph()
for u, v, wt in zip(s, t, w):
    DGw.add_edge(u, v, weight=wt)

plt.figure()
pos = nx.spring_layout(DGw, seed=42)
nx.draw(DGw, pos, with_labels=True, node_size=800, width=2, arrows=True, arrowstyle='->', arrowsize=18)
nx.draw_networkx_edge_labels(DGw, pos, edge_labels=nx.get_edge_attributes(DGw, 'weight'))
hide_axes()
plt.title("Directed, weighted (edge labels)")

# =========================
# 有向图：由邻接矩阵构造
# （非零即有向边，值为权重）
# =========================
a_dir = np.array([
    [0, 3, 0, 0],
    [0, 0, 8, 0],
    [9, 0, 0, 0],
    [2, 0, 0, 0],
], dtype=float)

DG_adj = nx.DiGraph()
n = a_dir.shape[0]
for i in range(n):
    for j in range(n):
        if a_dir[i, j] != 0:
            DG_adj.add_edge(i+1, j+1, weight=a_dir[i, j])

plt.figure()
pos = nx.spring_layout(DG_adj, seed=42)
nx.draw(DG_adj, pos, with_labels=True, node_size=800, width=2, arrows=True, arrowstyle='->', arrowsize=18)
nx.draw_networkx_edge_labels(DG_adj, pos, edge_labels=nx.get_edge_attributes(DG_adj, 'weight'))
hide_axes()
plt.title("Directed from adjacency")

plt.show()

