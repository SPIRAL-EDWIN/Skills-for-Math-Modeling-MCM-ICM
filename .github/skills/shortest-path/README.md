# Shortest Path Skill - Quick Start

## 快速使用指南

### 何时使用此技能

- 🚗 **交通运输网络**: 道路网络、航线规划、物流配送
- 📦 **物流优化**: 最优配送路径、供应链路径
- 🌐 **网络分析**: 通信网络、社交网络、基础设施
- 🚑 **应急响应**: 最快疏散路线、救护车调度
- 🏙️ **城市规划**: 交通流优化、公共交通设计

---

## 算法选择速查表

| 需求 | 推荐算法 | 复杂度 |
|------|---------|--------|
| **单源最短路径** (非负权重) | Dijkstra | O((V+E) log V) |
| **单源最短路径** (有负权重) | Bellman-Ford | O(VE) |
| **所有点对最短路径** | Floyd-Warshall | O(V³) |
| **启发式搜索** (如地图导航) | A* | O(E) 最佳情况 |

---

## 快速示例

### 示例 1: 城市配送最短路径 (Dijkstra)

```python
from shortest_path import dijkstra, reconstruct_path

# 城市道路网络 (节点: 路口, 边权重: 行驶时间/分钟)
city_network = {
    '仓库': [('路口A', 5), ('路口B', 8)],
    '路口A': [('路口C', 3), ('客户', 15)],
    '路口B': [('路口C', 4), ('路口D', 6)],
    '路口C': [('路口D', 2), ('客户', 10)],
    '路口D': [('客户', 5)],
    '客户': []
}

# 查找最短路径
distances, predecessors = dijkstra(city_network, '仓库', '客户')
path = reconstruct_path(predecessors, '仓库', '客户')

print(f"最优配送路线: {' -> '.join(path)}")
print(f"总行驶时间: {distances['客户']} 分钟")
```

**输出**:
```
最优配送路线: 仓库 -> 路口B -> 路口C -> 路口D -> 客户
总行驶时间: 21 分钟
```

---

### 示例 2: 多城市距离矩阵 (Floyd-Warshall)

```python
import numpy as np
from shortest_path import floyd_warshall

# 城市列表
cities = ['北京', '上海', '广州', '成都', '武汉']
n = len(cities)

# 创建邻接矩阵 (距离/公里)
adj_matrix = np.array([
    [0,    1200, 1900, 1500, 1100],  # 北京
    [1200, 0,    1400, 1900, 800],   # 上海
    [1900, 1400, 0,    1700, 1000],  # 广州
    [1500, 1900, 1700, 0,    1200],  # 成都
    [1100, 800,  1000, 1200, 0]      # 武汉
])

# 计算所有点对最短距离
all_distances, next_node = floyd_warshall(adj_matrix, cities)

# 打印距离矩阵
print("所有城市间最短距离 (公里):")
for i, city in enumerate(cities):
    print(f"{city}: {all_distances[i]}")
```

---

## 与其他技能集成

### 运输网络优化完整流程

```python
# 加载多个技能协同工作
load_skills=[
    "shortest-path",           # 最短路径算法
    "genetic-algorithm",       # 车辆路径优化 (VRP)
    "sensitivity-master",      # 瓶颈分析
    "visual-engineer"          # 网络可视化
]
```

**工作流程**:
1. 使用 `shortest-path` 计算所有点对距离矩阵
2. 使用 `genetic-algorithm` 优化多车辆配送路线 (VRP)
3. 使用 `sensitivity-master` 分析关键路段 (瓶颈)
4. 使用 `visual-engineer` 生成网络图和路径可视化

---

## 论文写作模板

### MCM/ICM 论文中的表述

```markdown
## 3.2 最短路径分析

为优化[运输/物流/路径规划]问题，我们采用 **Dijkstra算法** 求解从[起点]到[终点]的最短路径。

### 3.2.1 网络建模

我们将[系统]建模为加权有向图 G = (V, E)，其中：
- **节点 (V)**: [路口、城市、设施] (|V| = N)
- **边 (E)**: [道路、航线、连接] (|E| = M)  
- **权重**: [行驶时间、距离、成本]，单位为[分钟/公里/元]

### 3.2.2 算法选择

我们选择 **Dijkstra算法**，理由如下：
1. 所有边权重非负 (行驶时间 ≥ 0)
2. 仅需单源最短路径 (从仓库出发)
3. 稀疏图 (V=100, E=300)，时间复杂度 O((V+E) log V) 可接受

### 3.2.3 结果

从[起点]到[终点]的最优路径为：
- **路径**: A → B → C → D
- **总距离**: X 公里
- **计算时间**: Y 秒

图X展示了网络结构及最短路径（红色高亮）。

### 3.2.4 敏感性分析

通过对边权重进行 ±20% 扰动分析鲁棒性：
- **最优情况** (所有边 -20%): 距离 = X1 (变化 Z1%)
- **最差情况** (所有边 +20%): 距离 = X2 (变化 Z2%)
- **路径稳定性**: 在 95% 的扰动场景中路径保持不变

结果表明我们的解对[边权重]的中等变化具有**鲁棒性**。
```

---

## 常见陷阱

❌ **错误使用 Dijkstra 处理负权重**: Dijkstra 不支持负权重，需使用 Bellman-Ford  
❌ **忘记设置自环为0**: Floyd-Warshall 中对角线必须初始化为 0  
❌ **无向图只添加单向边**: 无向图需双向添加边: `graph[u].append((v, w))` 和 `graph[v].append((u, w))`  
❌ **未存储前驱节点**: 只计算距离无法重构路径，需同时维护 predecessors  
❌ **未检查路径是否存在**: 距离为 `inf` 表示不可达，需判断后再重构路径

---

## 输出文件位置

结果保存至 `results/shortest_path/`:
- `optimal_path.json` - 路径节点和总距离
- `distance_matrix.csv` - 所有点对距离 (Floyd-Warshall)
- `network_diagram.png` - 网络图及路径高亮
- `sensitivity_analysis.csv` - 边权重变化影响分析

---

## 相关技能

- **genetic-algorithm**: 车辆路径问题 (VRP) 中使用最短路径作为子程序
- **multi-objective-optimization**: 平衡距离、时间、成本的多目标路径优化
- **sensitivity-master**: 分析关键边 (瓶颈) 对网络的影响
- **robustness-check**: 测试路径在边失效情况下的稳定性
- **visual-engineer**: 生成出版级网络图

---

完整文档请参阅 **SKILL.md**
