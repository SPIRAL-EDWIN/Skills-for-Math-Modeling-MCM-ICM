# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:39
    @file  : shortestpath.py
"""

# pip install networkx matplotlib numpy

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# ----- 数据：边与权重 -----
s = [9, 9, 1, 1, 3, 3, 3, 2, 2, 5, 5, 7, 7, 8]  # 起点
t = [1, 2, 2, 3, 4, 6, 7, 4, 5, 4, 7, 6, 8, 6]  # 终点
w = [4, 8, 3, 8, 2, 7, 4, 1, 6, 6, 2, 14, 10, 9]  # 权重

# ----- 无向加权图 -----
G = nx.Graph()
for u, v, wt in zip(s, t, w):
    G.add_edge(u, v, weight=wt)

# ----- 绘制并显示权重 -----
plt.figure()
pos = nx.spring_layout(G, seed=42)  # 可复现布局
nx.draw(G, pos, with_labels=True, node_size=800, width=2)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.gca().set_xticks([]); plt.gca().set_yticks([])
plt.title("Weighted undirected graph")

# ----- 最短路径：9 到 8 -----
path = nx.shortest_path(G, source=9, target=8, weight='weight')
dist = nx.shortest_path_length(G, source=9, target=8, weight='weight')
print("P (9→8 的最短路径) =", path)
print("d (最短路径长度) =", dist)

# 高亮最短路径（加粗并改为红色）
path_edges = list(zip(path[:-1], path[1:]))
plt.figure()
nx.draw(G, pos, with_labels=True, node_size=800, width=2)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color='r')
plt.gca().set_xticks([]); plt.gca().set_yticks([])
plt.title("Shortest path 9→8 highlighted")

# ----- 全对最短路距离矩阵（按节点升序排列） -----
nodes_sorted = sorted(G.nodes())
index = {n: i for i, n in enumerate(nodes_sorted)}
D = np.full((len(nodes_sorted), len(nodes_sorted)), np.inf)

for src in nodes_sorted:
    lengths = nx.single_source_dijkstra_path_length(G, source=src, weight='weight')
    for dst, L in lengths.items():
        D[index[src], index[dst]] = L

print("\nD 矩阵（按节点升序 1..n 顺序）：\n", D)

# 对应 MATLAB 的 D(1,2) 与 D(9,4)
print("\nD(1,2) =", D[index[1], index[2]])
print("D(9,4) =", D[index[9], index[4]])

# ----- 距离节点 2 不超过 10 的所有节点及其距离 -----
within = nx.single_source_dijkstra_path_length(G, source=2, cutoff=10, weight='weight')
#（包含源点 2 本身，按需要可去掉）
nodeIDs = sorted(within.keys())
distances = [within[n] for n in nodeIDs]
print("\n距离节点 2 不超过 10 的节点：", nodeIDs)
print("对应距离：", distances)

plt.show()

