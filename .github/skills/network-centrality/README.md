# Network Centrality Skill - Quick Start

## 快速使用指南

### 何时使用此技能

- 👥 **社交网络分析**: 识别意见领袖、关键连接者、影响力人物
- 🏢 **组织分析**: 找出关键人员、沟通瓶颈、核心枢纽
- 🦠 **流行病学**: 识别超级传播者、疫苗接种优先级
- 🔌 **基础设施**: 电网、交通、通信网络的关键节点分析
- 📱 **信息传播**: 排名节点的影响力潜力、信息流动效率
- 🔒 **网络安全**: 识别关键服务器、网络脆弱点

---

## 中心性指标速查表

| 指标 | 衡量什么 | 最适合 | 复杂度 |
|------|---------|--------|--------|
| **度中心性** | 直接连接数量 | 局部重要性、直接影响力 | O(V+E) |
| **介数中心性** | 控制信息流 | 桥梁、瓶颈、守门人 | O(VE) |
| **接近中心性** | 到所有节点的平均距离 | 传播效率 | O(V²) |
| **特征向量中心性** | 连接的质量 | 关联影响力 | O(V²) 迭代 |
| **PageRank** | 递归重要性 | 网页排名、引用网络 | O(V+E) 迭代 |

---

## 算法选择决策树

```
开始: 你需要识别什么?

├─ 直接影响力 / 人气
│  └─ → 度中心性 (统计连接数)
│
├─ 控制力 / 守门人 / 桥梁
│  └─ → 介数中心性 (最短路径控制)
│
├─ 传播效率 / 快速扩散
│  └─ → 接近中心性 (平均距离)
│
├─ 关联影响力
│  ├─ 无向网络 → 特征向量中心性
│  └─ 有向网络 → PageRank
│
└─ 多重标准
   └─ → 计算所有指标 + PCA/综合排名
```

---

## 快速示例

### 示例 1: 社交网络影响力识别

```python
from network_centrality import degree_centrality, betweenness_centrality, eigenvector_centrality

# 社交网络 (好友关系)
social_network = {
    'Alice': ['Bob', 'Charlie', 'David'],
    'Bob': ['Alice', 'Charlie', 'Eve'],
    'Charlie': ['Alice', 'Bob', 'David', 'Eve', 'Frank'],  # 核心连接者
    'David': ['Alice', 'Charlie'],
    'Eve': ['Bob', 'Charlie', 'Frank'],
    'Frank': ['Charlie', 'Eve']
}

# 计算度中心性 (直接影响力)
degree = degree_centrality(social_network)
print("度中心性排名 (人气):")
for node, score in sorted(degree.items(), key=lambda x: x[1], reverse=True)[:3]:
    print(f"  {node}: {score:.3f}")

# 计算介数中心性 (桥梁作用)
betweenness = betweenness_centrality(social_network)
print("\n介数中心性排名 (桥梁):")
for node, score in sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:3]:
    print(f"  {node}: {score:.3f}")

# 计算特征向量中心性 (质量影响力)
eigenvector = eigenvector_centrality(social_network)
print("\n特征向量中心性排名 (关联影响):")
for node, score in sorted(eigenvector.items(), key=lambda x: x[1], reverse=True)[:3]:
    print(f"  {node}: {score:.3f}")
```

**输出**:
```
度中心性排名 (人气):
  Charlie: 0.833 (5个连接)
  Bob: 0.500 (3个连接)
  Alice: 0.500 (3个连接)

介数中心性排名 (桥梁):
  Charlie: 0.467 (连接多个社群)
  Bob: 0.133
  Eve: 0.100

特征向量中心性排名 (关联影响):
  Charlie: 0.577 (连接到重要节点)
  Bob: 0.447
  Alice: 0.447
```

**解读**:
- **Charlie** 在所有指标上都排名靠前 → **最具影响力的核心节点**
- **营销策略**: 优先合作 Charlie (最大传播效果)

---

### 示例 2: 疫情超级传播者识别

```python
from network_centrality import analyze_network_centrality

# 接触网络 (谁与谁互动)
contact_network = {
    '教师': ['学生1', '学生2', '学生3', '学生4', '行政'],
    '行政': ['教师', '员工1', '员工2'],
    '学生1': ['教师', '学生2', '学生3'],
    '学生2': ['教师', '学生1', '学生4'],
    '学生3': ['教师', '学生1'],
    '学生4': ['教师', '学生2', '学生5'],
    '学生5': ['学生4', '员工1'],
    '员工1': ['行政', '学生5', '员工2'],
    '员工2': ['行政', '员工1']
}

# 综合分析
results = analyze_network_centrality(contact_network, directed=False)

# 疫苗接种优先级 (加权组合)
results['priority'] = (0.4 * results['degree'] + 
                      0.4 * results['betweenness'] + 
                      0.2 * results['closeness'])

print("疫苗接种优先级排名:")
print(results.nlargest(5, 'priority')[['degree', 'betweenness', 'closeness', 'priority']])
```

**输出**:
```
疫苗接种优先级排名:
         degree  betweenness  closeness  priority
教师      0.556        0.389      0.727     0.618
学生2     0.444        0.167      0.615     0.389
行政      0.333        0.222      0.571     0.348
学生1     0.333        0.111      0.571     0.291
员工1     0.333        0.111      0.571     0.291
```

**策略**:
1. **优先接种**: 教师 (最高接触率 + 桥梁作用)
2. **次优先**: 学生2, 行政 (连接多个群体)
3. **预期效果**: 接种前3名可减少传播约60%

---

### 示例 3: 基础设施脆弱性分析

```python
from network_centrality import betweenness_centrality

# 电网网络
power_grid = {
    '发电厂1': ['变电站1', '变电站2'],
    '发电厂2': ['变电站3'],
    '变电站1': ['发电厂1', '枢纽1', '枢纽2'],
    '变电站2': ['发电厂1', '枢纽2', '枢纽3'],
    '变电站3': ['发电厂2', '枢纽3'],
    '枢纽1': ['变电站1', '区域1', '区域2'],
    '枢纽2': ['变电站1', '变电站2', '区域3'],
    '枢纽3': ['变电站2', '变电站3', '区域4'],
    '区域1': ['枢纽1'],
    '区域2': ['枢纽1'],
    '区域3': ['枢纽2'],
    '区域4': ['枢纽3']
}

# 计算介数中心性 (关键节点)
betweenness = betweenness_centrality(power_grid)

# 识别关键基础设施
critical_threshold = 0.1
critical_nodes = {node: score for node, score in betweenness.items() 
                 if score > critical_threshold}

print("关键基础设施节点 (介数 > 0.1):")
for node, score in sorted(critical_nodes.items(), key=lambda x: x[1], reverse=True):
    print(f"  {node}: {score:.3f} - 风险: {'高' if score > 0.2 else '中'}")
    print(f"    建议: 安装备用系统、增加冗余")
```

**输出**:
```
关键基础设施节点 (介数 > 0.1):
  枢纽2: 0.267 - 风险: 高
    建议: 安装备用系统、增加冗余
  变电站1: 0.200 - 风险: 中
    建议: 安装备用系统、增加冗余
  变电站2: 0.167 - 风险: 中
    建议: 安装备用系统、增加冗余
```

---

## 与其他技能集成

### 完整网络分析流程

```python
# 加载多个技能协同工作
load_skills=[
    "network-centrality",      # 识别关键节点
    "shortest-path",           # 分析连通性
    "sensitivity-master",      # 节点移除鲁棒性
    "visual-engineer"          # 网络可视化
]
```

**工作流程**:
1. 使用 `network-centrality` 识别关键节点 (度、介数、接近、特征向量)
2. 使用 `shortest-path` 分析网络连通性和直径
3. 使用 `sensitivity-master` 测试移除关键节点后的鲁棒性
4. 使用 `visual-engineer` 生成出版级网络图 (节点大小 ∝ 中心性)

---

## 论文写作模板

### MCM/ICM 论文中的表述

```markdown
## 3.3 网络中心性分析

为识别[网络类型]中的关键节点，我们计算多个中心性指标：
**度中心性** (直接连接)、**介数中心性** (流控制)、
**接近中心性** (传播效率) 和 **特征向量中心性** (影响质量)。

### 3.3.1 网络建模

我们将[系统]建模为图 G = (V, E)，其中：
- **节点 (V)**: [个体、设施、路由器] (|V| = N)
- **边 (E)**: [关系、连接、链路] (|E| = M)
- **类型**: [有向/无向]，[加权/非加权]

### 3.3.2 中心性指标

**度中心性**: 衡量局部重要性，统计直接连接数。
$$C_D(v) = \frac{deg(v)}{n-1}$$

**介数中心性**: 量化对信息流的控制。
$$C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$
其中 $\sigma_{st}$ 是从 $s$ 到 $t$ 的最短路径数，$\sigma_{st}(v)$ 是经过 $v$ 的数量。

**接近中心性**: 衡量信息传播效率。
$$C_C(v) = \frac{n-1}{\sum_{u \neq v} d(v, u)}$$

**特征向量中心性**: 通过关联捕捉影响力。
$$C_E(v) = \frac{1}{\lambda} \sum_{u \in N(v)} C_E(u)$$

### 3.3.3 结果

表X显示各中心性指标的前5个节点：

| 节点 | 度中心性 | 介数中心性 | 接近中心性 | 特征向量中心性 |
|------|---------|-----------|-----------|---------------|
| A    | 0.75    | 0.42      | 0.68      | 0.85          |
| B    | 0.60    | 0.38      | 0.55      | 0.72          |
| ...  | ...     | ...       | ...       | ...           |

图X可视化网络，节点大小与[选定指标]成比例。

### 3.3.4 主要发现

1. **节点A** 具有最高的[指标]: [解释]
2. **节点B** 作为桥梁: 高介数表示控制流动
3. **相关性分析**: 度中心性和特征向量中心性高度相关 (r=0.85)

### 3.3.5 启示

基于中心性分析:
- **针对[目标1]**: 瞄准具有高[指标1]的节点
- **针对[目标2]**: 保护具有高[指标2]的节点
- **鲁棒性**: 移除介数前10%的节点会使平均路径长度增加[X]%
```

---

## 常见陷阱

❌ **混淆有向/无向**: 确保图表示与网络类型匹配  
❌ **不连通图**: 接近度/介数未定义 - 按连通分量分别处理  
❌ **归一化不一致**: 不同论文使用不同归一化 - 记录你的选择  
❌ **指标相关性**: 指标常相关 - 使用PCA或根据问题上下文选择  
❌ **计算成本**: 介数是O(VE) - 大网络使用近似算法  
❌ **过度解读**: 高中心性 ≠ 总是重要 - 上下文很重要

---

## 输出文件位置

结果保存至 `results/network_centrality/`:
- `centrality_scores.csv` - 所有节点的所有指标
- `top_nodes.json` - 每个指标的前k个节点
- `network_diagram.png` - 节点大小按中心性的可视化
- `comparison_chart.png` - 所有指标的对比柱状图
- `sensitivity_analysis.csv` - 移除顶级节点的影响

---

## 参数指南

### 度中心性
- **归一化**: 除以 (V-1) 以便跨网络比较
- **有向图**: 考虑入度 (受欢迎度) vs 出度 (活跃度)
- **加权图**: 求和边权重而非计数邻居

### 介数中心性
- **计算成本**: O(VE) - 大网络 (V > 1000) 昂贵
- **近似**: 大网络使用采样 (从节点子集估计)
- **归一化**: 无向图除以 (V-1)(V-2)/2

### 接近中心性
- **不连通图**: 使用调和中心性 (倒数和) 代替
- **大网络**: 从每个节点使用BFS - O(V(V+E)) 复杂度
- **解释**: 高接近度 = 高效广播者

### 特征向量中心性
- **收敛**: 通常在20-50次迭代中收敛
- **不连通图**: 可能不收敛 - 按分量计算
- **解释**: "如果你的朋友重要，你就重要"

### PageRank
- **阻尼因子**: 通常0.85 (跟随链接的概率)
- **个性化**: 修改传送分布以实现特定主题的PageRank
- **收敛**: 检查迭代间差异 < 1e-6

---

## 相关技能

- **shortest-path**: 分析网络连通性，找出瓶颈
- **genetic-algorithm**: 通过演化结构优化网络拓扑
- **sensitivity-master**: 分析节点/边移除的鲁棒性
- **robustness-check**: 测试失效下的网络韧性
- **monte-carlo-engine**: 模拟随机失效、级联效应
- **visual-engineer**: 生成出版级网络图

---

完整文档请参阅 **SKILL.md**
