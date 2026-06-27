# MCM/ICM 2026 竞赛模型库完全指南 (Master Guide)

**版本**: 3.1 (2026年1月29日 - 新增AI报告技能)  
**包含技能**: 45个核心技能 (+10个新增，含强制性AI报告)  
**整合教程**: 23课完整教程（数模加油站）  
**适用对象**: MCM/ICM 参赛队伍、数学建模爱好者

⚠️ **重要更新**: 新增 `ai-report-writer` 技能 - COMAP从2024年起强制要求所有队伍提交AI工具使用报告！

本文档整合了 **模型列表 (MODELS LIST)**、**速查卡 (QUICK REFERENCE)** 和 **优化集成指南 (OPTIMIZATION INTEGRATION)**，是比赛期间的唯一核心参考文档。

---

## 目录 (Table of Contents)

1. [⚡ 快速决策树 (Decision Tree)](#-快速决策树-decision-tree)
2. [⏱️ 时间预算表 (Time Budgets)](#-时间预算表-time-budgets)
3. [📅 第一阶段：前期数据处理](#-第一阶段前期数据处理-data-pre-processing)
4. [⚙️ 第二阶段：中期模型构建](#-第二阶段中期模型构建-mid-stage-modeling)
   - [A. 评价与决策](#a-评价与决策类-evaluation--decision)
   - [B. 预测与时序](#b-预测与时间序列类-forecasting--time-series)
   - [C. 机理与微分方程](#c-机理与微分方程类-mechanistic--differential-equations)
   - [D. 网络与图论](#d-网络与图论类-network--graph-theory)
   - [E. 优化与规划 (含深度集成指南)](#e-优化与规划类-optimization--planning)
5. [✅ 第三阶段：验证与分析](#-第三阶段后期验证与分析-validation--analysis)
6. [📝 第四阶段：论文产出](#-第四阶段论文产出-post-processing)
7. [🚀 经典调用流程](#-经典调用流程示例)
8. [🏆 O奖检查清单](#-o奖检查清单-o-prize-checklist)

---

## ⚡ 快速决策树 (Decision Tree)

```text
开始: 你需要做什么？

├─ "清洗数据" (Clean data)
│  ├─ 基础清洗 (缺失/异常) → data-cleaner
│  └─ 降维 (指标太多) → pca-analyzer
│
├─ "预测未来" (Forecast)
│  ├─ 大样本 (>50点) → arima-forecaster
│  ├─ 小样本 (4-10点) → grey-forecaster
│  └─ 复杂非线性 (>500点) → lstm-forecaster
│
├─ "做决策 / 排名" (Decision/Rank)
│  ├─ 客观权重 (数据驱动) → entropy-weight-method (第3课)
│  ├─ 主观权重 (专家经验) → ahp-method (第1课)
│  ├─ 模糊评价 (定性指标) → fuzzy-evaluation (第4课) 🆕
│  ├─ 灰色关联 (小样本关联) → grey-relation (第5课) 🆕
│  └─ 最终排名 → topsis-scorer (第2课)
│
├─ "机器学习预测" (Predict with ML)
│  └─ 回归/特征重要性 → ml-regressor (第17-20课)
│
├─ "机理建模" (Dynamics)
│  ├─ 单一种群增长 → logistic-growth
│  ├─ 双种群互动 (捕食/竞争) → lotka-volterra
│  ├─ 空间传播 (传染病/污染) → reaction-diffusion
│  └─ 通用方程求解 → differential-equations
│
├─ "网络与路径" (Network)
│  ├─ 图论基础 (概念/遍历) → graph-theory (第14课) 🆕
│  ├─ 找最短路径/路由 → shortest-path (Dijkstra/Floyd) (第15课)
│  ├─ 最小生成树 (网络设计) → minimum-spanning-tree (第16课) 🆕
│  └─ 找关键节点/影响力 → network-centrality
│
├─ "优化求解" (Optimize)
│  ├─ 线性规划 (LP) → linear-programming (第7课) 🆕
│  ├─ 非线性规划 (NLP) → nonlinear-programming (第9课) 🆕
│  ├─ 整数规划 (IP/0-1) → integer-programming (第10课) 🆕
│  ├─ 最大最小化 (Minimax) → minimax-programming (第11课) 🆕
│  ├─ 动态规划 (DP) → dynamic-programming (第13课) 🆕
│  ├─ 离散/组合问题 (TSP/排班) → genetic-algorithm (第23课)
│  ├─ 连续多峰 (易陷局部最优) → simulated-annealing (第23课)
│  ├─ 连续光滑 (追求速度) → particle-swarm (第23课)
│  ├─ 多目标 (既要又要) → multi-objective-optimization (第12课)
│  └─ 简单参数搜索 → automated-sweep
│
├─ "反问题求解" (Inverse Problems) ⭐ NEW
│  └─ 从观测数据反推模型参数 (带不确定性量化) → bayesian-inversion
│
├─ "验证模型" (Validate)
│  ├─ 寻找最佳参数 → automated-sweep
│  ├─ 哪个参数最重要？→ sensitivity-master
│  ├─ 模型稳不稳定？→ robustness-check
│  ├─ 结果的不确定性范围？→ monte-carlo-engine
│  └─ 多目标权衡分析 → pareto-frontier
│
├─ "构建复杂系统" (Build)
│  └─ → modular-modeler
│
├─ "画图" (Figures)
│  ├─ 传统图表 (matplotlib) → visual-engineer
│  └─ 现代Web图表 (流程图/自定义) → web-artifacts-builder
│
├─ "写论文" (Write)
│  ├─ LaTeX协作写作 → latex-coauthoring
│  ├─ Markdown转LaTeX → latex-transformer
│  └─ AI工具使用报告 → ai-report-writer 🆕
│
├─ "处理Excel数据" (Excel/CSV)
│  └─ → xlsx
│
└─ "处理PDF" (PDF)
   ├─ 提取文献信息 → pdf
   └─ 合并提交文件 → pdf
```

---

## ⏱️ 时间预算表 (Time Budgets)

| 技能 | 最快耗时 | 典型耗时 | 包含调试 |
|------|---------|---------|---------|
| **基础工具** | | | |
| data-cleaner | 10 min | 20 min | 30 min |
| xlsx | 10 min | 30 min | 60 min |
| visual-engineer | 5 min | 10 min | 20 min |
| web-artifacts-builder | 20 min | 45 min | 90 min |
| latex-coauthoring | 2 hours | 15 hours | 30 hours |
| latex-transformer | 5 min | 10 min | 15 min |
| pdf (文献提取) | 10 min | 30 min | 60 min |
| pdf (提交组装) | 15 min | 30 min | 60 min |
| ai-report-writer (日志记录) | 2-3 min/次 | 累计1-2 hours | 分散4天 |
| ai-report-writer (报告组装) | 45 min | 1 hour | 1.5 hours |
| **评价类** | | | |
| entropy/topsis | 10 min | 15 min | 25 min |
| ahp-method | 15 min | 25 min | 40 min |
| pca-analyzer | 15 min | 20 min | 30 min |
| fuzzy-evaluation | 20 min | 30 min | 50 min |
| grey-relation | 15 min | 25 min | 40 min |
| **预测类** | | | |
| grey-forecaster | 10 min | 15 min | 25 min |
| arima-forecaster | 20 min | 35 min | 60 min |
| lstm-forecaster | 45 min | 90 min | 2 hours |
| **机理类** | | | |
| logistic/lotka | 10-15 min | 25 min | 40 min |
| reaction-diffusion | 30 min | 50 min | 90 min |
| differential-eqn | 20 min | 35 min | 60 min |
| **网络类** | | | |
| graph-theory | 20 min | 30 min | 50 min |
| shortest-path | 15 min | 25 min | 40 min |
| minimum-spanning-tree | 15 min | 25 min | 40 min |
| network-centrality | 20 min | 30 min | 50 min |
| **优化类** | | | |
| linear-programming | 20 min | 40 min | 1 hour |
| nonlinear-programming | 30 min | 50 min | 1.5 hours |
| integer-programming | 30 min | 50 min | 1.5 hours |
| minimax-programming | 25 min | 40 min | 1 hour |
| dynamic-programming | 30 min | 1 hour | 2 hours |
| automated-sweep | 30 min | 1 hour | 2 hours |
| particle-swarm | 15 min | 25 min | 45 min |
| simulated-annealing | 20 min | 35 min | 60 min |
| genetic-algorithm | 30 min | 50 min | 90 min |
| multi-objective | 1 hour | 1.5 hours | 3 hours |
| **反问题类** ⭐ | | | |
| bayesian-inversion (MAP) | 15 min | 30 min | 1 hour |
| bayesian-inversion (PSO+MCMC) | 45 min | 1.5 hours | 3 hours |
| **验证类** | | | |
| robustness-check | 30 min | 45 min | 1.5 hours |
| monte-carlo | 30 min | 1 hour | 2 hours |
| sensitivity | 1 hour | 2 hours | 4 hours |

---

## 📅 第一阶段：前期数据处理 (Data Pre-processing)

### 1. **data-cleaner** (数据清洗专家)
- **技能定位**: 自动化数据预处理工具，处理脏数据、缺失值和异常值。
- **核心要求**: 必须处理缺失值（插值/删除）和异常值（3-sigma/IQR）。
- **适用数据**: 原始的、未清洗的CSV/Excel文件。
- **使用场景**: 刚下载原始数据，需要生成 `processed.csv` 作为后续输入。
- **实现策略**: Pandas 向量化操作，自动生成清洗报告。

### 2. **pca-analyzer** (主成分分析器)
- **技能定位**: 降维工具，消除多重共线性。
- **核心要求**: 保留85%以上累计方差，并解释主成分含义。
- **适用数据**: 指标过多（>10个）且存在相关性的高维数据。
- **使用场景**: 评价指标太多，担心模型过拟合或难以解释。
- **实现策略**: sklearn PCA，输出特征值和载荷矩阵。

---

## ⚙️ 第二阶段：中期模型构建 (Mid-stage Modeling)

### A. 评价与决策类 (Evaluation & Decision)

#### 3. **entropy-weight-method** (熵权法)
- **定位**: 客观赋权，基于数据变异程度。
- **场景**: 不希望主观因素干扰权重时。常与 TOPSIS 连用。

#### 4. **ahp-method** (层次分析法)
- **定位**: 主观赋权，基于专家两两比较。
- **要求**: 一致性比例 CR < 0.1。
- **场景**: 处理难以量化的定性指标（如"政策力度"）。

#### 5. **topsis-scorer** (优劣解距离法)
- **定位**: 综合排名工具。
- **经典组合**: Entropy + AHP + TOPSIS (主客观点综合赋权)。
- **输出**: 各方案的相对贴近度得分及排名。

#### 6. **fuzzy-evaluation** (模糊综合评价) 🆕
- **定位**: 定性指标量化评价。
- **核心步骤**: 因素集 → 评语集 → 隶属度矩阵 → 权重 → 模糊运算。
- **场景**: 环境质量、教学质量、风险评估等模糊指标。
- **教程**: 第4课

#### 7. **grey-relation** (灰色关联分析) 🆕
- **定位**: 小样本关联度分析。
- **核心步骤**: 无量纲化 → 关联系数 → 关联度 → 排序。
- **场景**: 影响因素分析、小样本决策。
- **与相关系数区别**: 不要求大样本、不要求线性。
- **教程**: 第5课

### B. 预测与时间序列类 (Forecasting & Time Series)

#### 6. **grey-forecaster** (灰色预测 GM(1,1))
- **定位**: 贫信息预测，小样本神器。
- **要求**: 样本量 4-10 个，数据全为正。
- **场景**: 历史数据极少（如仅有5年），需预测未来趋势。

#### 7. **arima-forecaster** (ARIMA 时序)
- **定位**: 经典统计预测，捕捉趋势和季节性。
- **要求**: 样本量 > 50，通过平稳性检验。
- **场景**: 数据量充足的经济、气象指标预测。

#### 8. **lstm-forecaster** (深度学习 LSTM)
- **定位**: 处理复杂非线性长序列。
- **要求**: 数据量 > 500，需划分训练/测试集。
- **场景**: 传统模型失效，需要高精度拟合复杂模式。

#### 9. **ml-regressor** (机器学习回归)
- **定位**: 随机森林/XGBoost 回归。
- **亮点**: 输出特征重要性 (Feature Importance)，增加可解释性。
- **场景**: 预测房价、销量，并找出关键驱动因素。

### C. 机理与微分方程类 (Mechanistic & Differential Equations)

#### 10. **logistic-growth** (Logistic 增长)
- **定位**: 资源受限的单一种群增长（S型）。
- **要求**: 估计环境承载力 K 值。
- **场景**: 人口、传染病早期、产品扩散。

#### 11. **lotka-volterra** (捕食者-猎物)
- **定位**: 双种群竞争或捕食关系。
- **要求**: 绘制相图 (Phase Portrait) 分析稳定性。
- **场景**: 生态平衡、商业竞争 (A公司 vs B公司)。

#### 12. **reaction-diffusion** (反应扩散)
- **定位**: 时空演化模型（时间+空间）。
- **输出**: 2D/3D 动态演化热力图。
- **场景**: 传染病空间传播、污染物扩散、生态入侵。

#### 13. **differential-equations** (通用求解器)
- **定位**: 统一的 ODE/PDE 数值解框架。
- **场景**: 标准模型无法满足，需自定义方程组时。

### D. 网络与图论类 (Network & Graph Theory)

#### 14. **graph-theory** (图论基础) 🆕
- **定位**: 图的基本概念和算法（DFS/BFS/连通性）。
- **核心内容**: 邻接矩阵、邻接表、图遍历、连通分量。
- **场景**: 社交网络分析、依赖关系、交通网络基础。
- **教程**: 第14课

#### 15. **shortest-path** (最短路径)
- **定位**: Dijkstra / Floyd / Bellman-Ford / A* 算法库。
- **场景**: 物流配送、应急救援、路由规划。
- **流程**: 构建邻接矩阵 → 算距离 → 输入优化模型。
- **教程**: 第15课

#### 16. **minimum-spanning-tree** (最小生成树) 🆕
- **定位**: 连接所有节点的最小权重树（Prim/Kruskal）。
- **场景**: 网络设计、道路建设、管道铺设。
- **教程**: 第16课

#### 17. **network-centrality** (中心性分析)
- **定位**: 识别网络中的关键节点 (Key Nodes)。
- **指标**: 度 (Degree)、介数 (Betweenness)、接近 (Closeness)、特征向量 (Eigenvector)。
- **场景**: 找社交网络意见领袖、电网脆弱节点、超级传播者。

### E. 优化与规划类 (Optimization & Planning)

#### 18. **linear-programming** (线性规划) 🆕
- **定位**: 线性目标函数 + 线性约束。
- **场景**: 资源分配、生产计划、运输问题。
- **工具**: Python (scipy.linprog), MATLAB (linprog)。
- **教程**: 第7课

#### 19. **nonlinear-programming** (非线性规划) 🆕
- **定位**: 非线性目标函数或约束。
- **场景**: 工程设计、最优控制、参数拟合。
- **工具**: Python (scipy.minimize), MATLAB (fmincon)。
- **注意**: 需要初始猜测值，可能有局部最优。
- **教程**: 第9课

#### 20. **integer-programming** (整数规划) 🆕
- **定位**: 决策变量必须是整数（0-1决策、离散数量）。
- **场景**: 背包问题、指派问题、排班、选址。
- **工具**: Python (scipy.milp, pulp), MATLAB (intlinprog)。
- **教程**: 第10课

#### 21. **minimax-programming** (最大最小化规划) 🆕
- **定位**: 优化最坏情况（鲁棒优化）。
- **场景**: 风险管理、博弈论、最坏情况设计。
- **技巧**: 转化为标准优化（引入辅助变量）。
- **教程**: 第11课

#### 22. **dynamic-programming** (动态规划) 🆕
- **定位**: 多阶段决策，最优子结构。
- **场景**: 背包、最优路径、资源分配、换硬币。
- **核心**: 状态定义 + 状态转移方程。
- **教程**: 第13课

#### 24. **genetic-algorithm** (遗传算法)
- **特点**: 全局搜索，适合离散编码。
- **场景**: 选址、排班、路径规划。
- **教程**: 第23课

#### 25. **simulated-annealing** (模拟退火)
- **特点**: 原理简单，擅长跳出局部最优。
- **场景**: 复杂函数寻优。
- **教程**: 第23课

#### 26. **particle-swarm** (粒子群)
- **特点**: 收敛快，实现简单。
- **场景**: 连续参数拟合。
- **教程**: 第23课

#### 27. **multi-objective-optimization** (多目标 NSGA-II)
- **定位**: 寻找 Pareto 前沿面。
- **场景**: "既要成本低，又要质量高" 的冲突目标优化。
- **教程**: 第12课

### F. 反问题与参数估计类 (Inverse Problems & Parameter Estimation) ⭐ NEW

#### 20. **bayesian-inversion** (贝叶斯参数反演) 🔥 O-Award Differentiator
- **技能定位**: 从观测数据反推模型参数，并量化不确定性（95%置信区间）。
- **核心算法**: 
  - **PSO + MCMC**: 粒子群全局搜索 + 马尔可夫链蒙特卡洛局部采样
  - **MAP Grid**: 最大后验估计（快速原型）
- **数学框架**:
  ```
  先验: p(θ) = p(α) × p(N) × p(T)
  似然: p(h_obs | θ) ∝ exp(-E(θ))
  后验: p(θ | h_obs) ∝ p(θ) × p(h_obs | θ)
  ```
- **适用场景**:
  - **材料科学**: 观测磨损深度 → 推断材料硬度、使用年限
  - **考古学**: 台阶磨损分布 → 推断人流量、使用方向
  - **地球物理**: 地震波数据 → 推断地下结构参数
  - **流行病学**: 感染数据 → 推断传播率、接触率
- **输出示例**:
  ```
  α = 5.2×10⁻⁹ [4.8×10⁻⁹, 5.6×10⁻⁹] (95% CI)
  N = 487 [450, 520] 人/天
  T = 98 [92, 105] 年
  收敛诊断: 接受率=0.28, R-hat=1.02 < 1.1 ✓
  ```
- **为什么这是O奖关键**:
  - ✅ **MCM 2025 O奖论文分析**: 5篇O奖论文中，2篇明确使用贝叶斯框架
  - ✅ **关键差异**: 大多数队伍只报告点估计，O奖队伍量化不确定性
  - ✅ **论文加分点**: "We quantify parameter uncertainty using Bayesian inference"
- **时间预算**:
  - 快速原型 (MAP Grid): 10-20分钟
  - 完整分析 (PSO+MCMC): 1-2小时（含参数调优）
- **使用流程**:
  1. Day 1: 构建前向模型（物理方程）
  2. Day 2: 集成bayesian-inversion，运行PSO+MCMC
  3. Day 3: 报告参数估计值 ± 95% CI
  4. Day 4: 论文中展示收敛诊断、敏感度分析
- **依赖**: numpy, scipy, matplotlib
- **关键文件**: 
  - `README.md`: 完整技术文档（数学理论、API参考）
  - `QUICKSTART.md`: 5分钟快速上手
  - `example_stair_wear.py`: 完整工作示例（合成数据验证）

---

#### 🔧 优化算法深度集成指南 (Deep Dive)

> **如何选择算法?**
> - **离散/组合问题** (TSP, 0/1规划) → **genetic-algorithm**
> - **多峰连续问题** (易陷局部最优) → **simulated-annealing**
> - **光滑连续问题** (追求速度) → **particle-swarm**
>
> **多目标算法原理**:
> - **NSGA-II** = 遗传算法 (GA) + Pareto 排序
>   - 使用 GA 的交叉变异 + 非支配排序 + 拥挤度距离
> - **MOEA/D** = 分解法 + 模拟退火 (SA) 接受准则
> - **MOPSO** = 粒子群 (PSO) + Pareto 档案集
>
> **推荐使用模式**:
> 1. 先用单目标算法 (GA/PSO) 跑通流程。
> 2. 如果发现有权衡 (Trade-off)，升级为多目标 (NSGA-II)。
> 3. 最后使用 `topsis-scorer` 从 Pareto 前沿中选出最优解。

---

## ✅ 第三阶段：后期验证与分析 (Validation & Analysis)

### 20. **sensitivity-master** (灵敏度分析)
- **定位**: Sobol / Morris 全局分析。
- **目的**: 识别关键参数，证明模型对参数扰动不敏感（鲁棒性）。
- **O奖标准**: 必须做。不仅仅是单因素分析。

### 21. **robustness-check** (鲁棒性检验)
- **定位**: 极端条件测试。
- **输出**: 龙卷风图 (Tornado Diagram)。
- **场景**: "如果我的假设稍微不成立，模型会崩溃吗？"

### 22. **monte-carlo-engine** (蒙特卡洛模拟)
- **定位**: 不确定性量化。
- **输出**: 95% 置信区间。
- **场景**: 输入参数带有随机性时。

### 23. **automated-sweep** (参数扫描)
- **定位**: 暴力网格搜索最优参数。
- **场景**: 模型参数未知，反向拟合历史数据。

### 24. **pareto-frontier** (Pareto 可视化)
- **定位**: 多目标权衡图。
- **场景**: 直观展示目标间的制约关系。

### 25. **modular-modeler** (模块化架构)
- **定位**: 复杂系统 OOP 框架。
- **场景**: 代码量大，需多人协作开发时使用。

---

## 📝 第四阶段：论文产出 (Post-processing)

### 26. **visual-engineer** (可视化专家)
- **定位**: 生成出版级 (300 DPI, Times New Roman) 图表。
- **场景**: 替换 Python 默认丑陋图表。

### 27. **latex-transformer** (LaTeX 转换)
- **定位**: Markdown 转 LaTeX 代码。
- **场景**: 快速生成公式、表格、引用。

### 28. **xlsx** (Excel数据处理专家)
- **定位**: MCM/ICM专用数据预处理工具，处理原始Excel/CSV数据。
- **核心功能**: 数据清洗（缺失值、异常值）、归一化（TOPSIS/AHP准备）、统计分析、特征工程。
- **场景**: 比赛初期快速处理原始数据，生成建模就绪的数据集。
- **时间预算**: 快速清洗10-30分钟，完整处理30-60分钟。

### 29. **latex-coauthoring** (LaTeX协作写作专家)
- **定位**: MCM/ICM论文LaTeX写作全流程指导，特别强化Summary Sheet（摘要页）。
- **核心功能**: 论文结构搭建、数学公式格式化、Summary Sheet打磨、学术语言规范。
- **关键特色**: 三阶段写作流程（结构蓝图→章节起草→Summary Sheet打磨），Summary Sheet为王的策略。
- **场景**: 论文起草（60-80小时）、Summary Sheet最终打磨（84-92小时）。
- **时间预算**: 结构搭建2-4小时，章节起草10-20小时，Summary Sheet打磨4-8小时。

### 30. **web-artifacts-builder** (Web可视化设计师)
- **定位**: 创建出版级、有区别度的图表和流程图，超越Excel/Matplotlib默认样式。
- **核心功能**: 模型架构流程图、系统动力学图、自定义数据可视化（Sankey、Chord、Network图）。
- **技术栈**: HTML/CSS/SVG/React + D3.js/Chart.js/Recharts。
- **输出方式**: 生成Web artifact，用户截图后导入LaTeX（\includegraphics）。
- **场景**: 需要专业、现代、有视觉冲击力的图表时使用。
- **时间预算**: 简单流程图20-30分钟，自定义图表30-60分钟，复杂D3.js图表60-90分钟。

### 31. **pdf** (PDF处理与提交专家)
- **定位**: 文献综述支持（PDF信息提取）+ 最终提交组装（PDF合并与验证）。
- **核心功能**: 从学术论文提取文本/表格/公式、合并最终提交PDF（Control Sheet + Main Paper + Code Appendix）、验证提交合规性（页数、字体、格式）。
- **关键时间节点**: 文献综述（0-24小时）、提交组装（90-96小时）。
- **场景**: 快速从参考文献提取关键信息、确保最终提交符合MCM/ICM规则。
- **时间预算**: 批量文献提取30分钟，提交组装与验证30-60分钟。

### 32. **ai-report-writer** (AI工具使用报告生成器) 🆕 🚨 MANDATORY
- **技能定位**: COMAP MCM/ICM强制要求的"AI工具使用报告"生成工具。从2024年起，所有队伍必须提交AI使用报告作为附录，否则可能取消资格。
- **核心功能**: 
  - **实时日志记录**: 比赛期间记录所有AI交互（提示词+输出+验证）
  - **合规报告生成**: 自动生成符合COMAP要求的LaTeX报告
  - **透明度保证**: 确保所有AI使用都被披露并验证
  - **引用格式**: 提供主论文中AI工具的正确引用格式
- **报告结构** (5个必需部分):
  1. **使用概览**: 所有AI工具的汇总表
  2. **LLM详细记录**: 每次交互的完整提示词、输出、验证笔记
  3. **翻译工具**: 使用声明和校对说明
  4. **代码辅助**: 文件位置和验证说明
  5. **诚信声明**: 正式的人工监督和责任声明
- **COMAP政策要点**:
  - ✅ **必须披露**: ChatGPT、Claude、DeepL、GitHub Copilot等所有AI工具
  - ✅ **完整记录**: 提示词必须是原文（不能改写），输出必须完整
  - ✅ **验证笔记**: 必须具体说明检查了什么、修改了什么
  - ❌ **取消资格触发器**: 未披露AI使用、假引用、未验证内容
- **两阶段工作流**:
  - **阶段1（0-92小时）**: 实时日志记录（每次交互2-3分钟）
  - **阶段2（92-96小时）**: 报告组装（1小时转换日志为LaTeX）
- **时间预算**: 
  - 日志记录：1-2小时（分散在4天内）
  - 报告组装：1小时（第92-93小时）
  - 总计：2-3小时
- **关键时间节点**: 
  - 第0小时：创建日志模板
  - 第0-92小时：持续记录
  - 第92小时：开始报告组装（不要等到第95小时！）
  - 第94小时：将AI引用添加到主论文
  - 第96小时：提交
- **输出文件**:
  - `ai_usage_log.md` - 实时工作日志
  - `ai_report.tex` - 正式LaTeX报告
  - `ai_report.pdf` - 编译后的报告（合并到主论文后）
- **包含资源**:
  - `references/comap-policy.md` - COMAP官方政策详解
  - `references/log-template.md` - 详细日志模板和示例
  - `references/quick-reference.md` - 快速参考卡
  - `assets/ai_report_template.tex` - 完整LaTeX模板
- **专业提示**:
  - 📝 **立即记录**: 不要依赖记忆，每次AI交互后立即记录
  - 🔍 **具体验证**: 避免"我们检查过了"这种泛泛的说法
  - 📋 **指定角色**: 指定一名队员作为"AI日志员"执行记录纪律
  - ⏰ **提前开始**: 第92小时开始报告组装，不要等到最后30分钟
  - 🎯 **过度报告**: 有疑问时就报告，过度报告比漏报安全
- **为什么这是强制性的**:
  - COMAP从2024年开始要求所有队伍提交AI报告
  - 透明度建立信任 - 诚实披露的队伍更受评委信任
  - 这不是惩罚 - 这是展示诚信和人工监督的机会
  - 未报告AI使用 = 学术不诚信 = 取消资格

---

## 🚀 经典调用流程示例

**场景 1：传染病防控 (Epidemic Control)**
1. **Data**: `data-cleaner` 清洗数据。
2. **Model**: `differential-equations` 建立 SIR 模型。
3. **Param**: `automated-sweep` 拟合感染率。
4. **Validation**: `sensitivity-master` 分析 R0 敏感性。
5. **Output**: `visual-engineer` 绘制预测曲线。

**场景 2：物流选址 (Logistics)**
1. **Network**: `data-cleaner` + `shortest-path` 构建距离矩阵。
2. **Analysis**: `network-centrality` 找候选中心。
3. **Optimize**: `genetic-algorithm` 求解最小成本选址。
4. **Eval**: `topsis-scorer` 综合评估方案。
5. **Output**: 选址地图。

**场景 3：政策制定 (Policy Making)**
1. **Index**: `pca-analyzer` 降维指标。
2. **Forecast**: `lstm-forecaster` 预测趋势。
3. **Optimize**: `multi-objective-optimization` 寻找经济/环境平衡点。
4. **Decision**: `pareto-frontier` + `robustness-check` 验证政策。

**场景 4：材料磨损反问题 (Inverse Problem - Stair Wear)** ⭐ NEW
1. **Data**: `data-cleaner` 清洗3D扫描点云数据。
2. **Forward**: 构建Archard磨损定律前向模型。
3. **Inversion**: `bayesian-inversion` 反推材料系数、人流量、使用年限。
4. **Output**: 报告参数估计 ± 95% CI，展示后验分布。
5. **Validation**: `sensitivity-master` 分析参数敏感性。

---

## 🏆 O奖检查清单 (O-Prize Checklist)

- [ ] **模型选择有理有据**: 使用决策树证明为什么选这个模型。
- [ ] **不确定性量化**: 必须有 Monte Carlo 或置信区间。
  - ⭐ **反问题场景**: 使用 `bayesian-inversion` 报告 95% 置信区间
  - ⭐ **论文关键句**: "We quantify parameter uncertainty using Bayesian inference"
- [ ] **灵敏度分析**: 必须有 Sensitivity Analysis (Sobol/Robustness)。
- [ ] **图表质量**: 必须是出版级 (visual-engineer)。
- [ ] **代码规范**: 清晰、模块化。
- [ ] **参数估计**: 如涉及反问题，必须报告后验分布和收敛诊断（R-hat, 接受率）。
- [ ] **AI使用报告**: 🚨 **强制要求** - 必须提交完整的AI工具使用报告（`ai-report-writer`）
  - ✅ 所有AI交互已记录（提示词+输出+验证）
  - ✅ 报告包含所有5个必需部分
  - ✅ 验证笔记具体详细（不是泛泛而谈）
  - ✅ 所有AI生成的引用已验证真实性
  - ✅ 诚信声明已签署
  - ❌ 未报告AI使用 = 可能取消资格

---