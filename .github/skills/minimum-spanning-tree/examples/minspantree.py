# -*- coding: utf-8 -*-
"""
    @author: 数模加油站
    @time  : 2025/8/23 15:40
    @file  : minspantree.py
"""

# pip install networkx matplotlib numpy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# —— 邻接矩阵（不存在的边=0），仅上三角有权重 ——
a = np.zeros((6, 6), dtype=float)
a[0, [1, 2]] = [14, 18]
a[1, [2, 3, 4]] = [13, 18, 16]
a[2, [3, 4]] = [12, 16]
a[3, [4, 5]] = [14, 19]
a[4, 5] = 10

# —— 用上三角构造无向图（等价于 MATLAB: graph(a, s, 'upper')）——
G = nx.Graph()
labels = {i+1: f"城市{i+1}" for i in range(6)}  # 节点名称
for i in range(6):
    G.add_node(i+1, label=labels[i+1])

for i in range(6):
    for j in range(i+1, 6):
        if a[i, j] != 0:
            G.add_edge(i+1, j+1, weight=float(a[i, j]))

# —— 绘图并标注权重 ——
pos = nx.spring_layout(G, seed=42)  # 可复现布局
plt.figure()
nx.draw(G, pos, with_labels=True, labels=labels, node_size=900, width=2)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.gca().set_xticks([]); plt.gca().set_yticks([])
plt.title("原图（带边权）")

# —— 最小生成树（可选算法：'prim' 或 'kruskal'）——
T_prim = nx.minimum_spanning_tree(G, algorithm="prim", weight="weight")
T_kruskal = nx.minimum_spanning_tree(G, algorithm="kruskal", weight="weight")

# 计算权重和
L_prim = sum(d["weight"] for *_, d in T_prim.edges(data=True))
L_kruskal = sum(d["weight"] for *_, d in T_kruskal.edges(data=True))
print("Prim 最小生成树总权重 L =", L_prim)
print("Kruskal 最小生成树总权重 L =", L_kruskal)

# —— 高亮最小生成树（以 Prim 为例）——
plt.figure()
nx.draw(G, pos, with_labels=True, labels=labels, node_size=900, width=1.5)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.draw_networkx_edges(
    G, pos,
    edgelist=list(T_prim.edges()),
    width=2.5, edge_color="red"
)
plt.gca().set_xticks([]); plt.gca().set_yticks([])
plt.title("最小生成树（红色高亮）")
plt.show()

