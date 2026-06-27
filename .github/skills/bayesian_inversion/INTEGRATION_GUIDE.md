# Bayesian Inversion 技能集成指南

## 技能位置

**路径**: `.github/skills/bayesian_inversion/`

**状态**: ✅ 已集成到MCM技能库 (版本 2.1)

---

## 快速索引

| 文档 | 用途 | 阅读时间 |
|------|------|---------|
| `README.md` | 完整技术文档（数学理论、API参考、竞赛策略） | 15-20分钟 |
| `QUICKSTART.md` | 5分钟快速上手教程 | 5分钟 |
| `example_stair_wear.py` | 完整工作示例（台阶磨损问题） | 运行2-5分钟 |
| `INTEGRATION_GUIDE.md` (本文档) | 技能库集成说明 | 3分钟 |

---

## 在技能库中的定位

### 分类
**F. 反问题与参数估计类 (Inverse Problems & Parameter Estimation)**

### 决策树位置
```
├─ "反问题求解" (Inverse Problems) ⭐ NEW
│  └─ 从观测数据反推模型参数 (带不确定性量化) → bayesian-inversion
```

### 时间预算
- **MAP Grid 方法**: 15分钟（快速）→ 30分钟（典型）→ 1小时（含调试）
- **PSO+MCMC 方法**: 45分钟（快速）→ 1.5小时（典型）→ 3小时（含调优）

---

## 何时使用此技能

### 核心场景识别

**你需要使用 `bayesian-inversion` 当你的问题包含以下特征：**

1. **已知结果，未知原因**
   - ✅ 观测到磨损深度 → 推断使用年限
   - ✅ 测量到污染浓度 → 推断排放源强度
   - ✅ 记录到感染人数 → 推断传播率

2. **参数不确定性重要**
   - ✅ 需要报告"参数 ± 误差范围"
   - ✅ 论文要求置信区间
   - ✅ 决策需要考虑风险

3. **传统优化不够**
   - ❌ 单纯最小化误差 → 只得到点估计
   - ✅ 贝叶斯推断 → 得到完整后验分布

### 典型问题类型

| 问题领域 | 观测数据 | 待推断参数 | 前向模型 |
|---------|---------|-----------|---------|
| **材料科学** | 磨损深度分布 | 材料硬度、使用时间 | Archard磨损定律 |
| **流行病学** | 感染人数时序 | 传播率β、接触率 | SIR/SEIR模型 |
| **地球物理** | 地震波到达时间 | 地下结构参数 | 波动方程 |
| **考古学** | 文物磨损程度 | 年代、使用频率 | 物理磨损模型 |
| **环境科学** | 污染物浓度场 | 排放源位置、强度 | 扩散方程 |

---

## 与其他技能的协同

### 经典工作流

#### 场景：材料磨损反问题（MCM 2025 Problem A）

```
Day 1 (0-24h):
├─ data-cleaner          清洗3D扫描点云数据
├─ visual-engineer       可视化原始磨损分布
└─ 构建前向模型          编写Archard磨损定律代码

Day 2 (24-48h):
├─ bayesian-inversion    反推参数（MAP快速测试）
├─ bayesian-inversion    升级到PSO+MCMC（完整不确定性）
└─ visual-engineer       绘制后验分布图

Day 3 (48-72h):
├─ sensitivity-master    分析哪个参数最重要
├─ robustness-check      测试极端条件
└─ monte-carlo-engine    验证不确定性传播

Day 4 (72-96h):
├─ latex-coauthoring     撰写论文
├─ web-artifacts-builder 制作模型流程图
└─ pdf                   组装提交文件
```

### 技能组合建议

**组合1：完整反问题分析**
```python
data-cleaner → bayesian-inversion → sensitivity-master → visual-engineer
```

**组合2：快速参数估计**
```python
bayesian-inversion (MAP) → automated-sweep (验证) → robustness-check
```

**组合3：深度不确定性量化**
```python
bayesian-inversion (MCMC) → monte-carlo-engine → pareto-frontier
```

---

## 竞赛策略集成

### 在README主决策树中的位置

已添加到 `.github/skills/README.md` 的以下位置：

1. **快速决策树** (第29行)
   ```
   ├─ "反问题求解" (Inverse Problems) ⭐ NEW
   │  └─ 从观测数据反推模型参数 (带不确定性量化) → bayesian-inversion
   ```

2. **时间预算表** (第120行)
   ```
   | **反问题类** ⭐ | | | |
   | bayesian-inversion (MAP) | 15 min | 30 min | 1 hour |
   | bayesian-inversion (PSO+MCMC) | 45 min | 1.5 hours | 3 hours |
   ```

3. **模型构建阶段** (第238行)
   - 新增 **F. 反问题与参数估计类** 章节
   - 详细说明技能定位、数学框架、使用场景

4. **经典调用流程** (第395行)
   - 新增 **场景4：材料磨损反问题** 示例

5. **O奖检查清单** (第410行)
   - 添加反问题场景的特殊要求
   - 强调贝叶斯推断的论文加分点

---

## O奖差异化要点

### 为什么这是关键技能

**数据来源**: 分析MCM 2025 Problem A 的5篇O奖论文

| 论文编号 | 使用贝叶斯推断 | 报告置信区间 | 收敛诊断 |
|---------|--------------|------------|---------|
| 2504218 | ✅ PSO+MCMC | ✅ 95% CI | ✅ R-hat |
| 2511565 | ✅ MAP估计 | ✅ 后验分布 | ❌ |
| 2501909 | ❌ | ❌ | ❌ |
| 其他队伍 | ❌ (仅点估计) | ❌ | ❌ |

**关键发现**:
- ✅ **O奖队伍**: 2/5 明确使用贝叶斯框架
- ✅ **关键差异**: 量化不确定性（95% CI）
- ❌ **普通队伍**: 仅报告最优参数值

### 论文写作模板

**Methods 章节**:
```latex
\subsection{Bayesian Parameter Inversion}

To estimate parameters $\theta = (\alpha, N, T)$ from observed wear data, 
we employ Bayesian inference with a two-step strategy:

1. **Particle Swarm Optimization (PSO)**: Locates global optimum in parameter space
2. **Markov Chain Monte Carlo (MCMC)**: Quantifies posterior uncertainty

Prior distributions based on material science literature:
\begin{align}
\alpha &\sim \text{LogUniform}(10^{-10}, 10^{-7}) \\
N &\sim \text{Uniform}(100, 1000) \\
T &\sim \text{Uniform}(50, 200)
\end{align}

Convergence diagnostics: acceptance rate = 0.28, $\hat{R} = 1.02 < 1.1$ ✓
```

**Results 章节**:
```latex
\subsection{Parameter Estimates}

\begin{itemize}
\item Wear coefficient: $\alpha = 5.2 \times 10^{-9}$ [4.8, 5.6] $\times 10^{-9}$ (95\% CI)
\item Daily foot traffic: $N = 487$ [450, 520] people/day (95\% CI)
\item Age: $T = 98$ [92, 105] years (95\% CI)
\end{itemize}

The credible intervals indicate high confidence in our estimates, 
with uncertainty primarily driven by measurement noise ($\sigma = 5$ mm).
```

---

## 快速启动检查清单

### 第一次使用（5分钟）

- [ ] 阅读 `QUICKSTART.md`
- [ ] 运行 `python example_stair_wear.py`
- [ ] 观察输出：参数估计 + 95% CI + 收敛诊断
- [ ] 确认理解：先验 → 似然 → 后验

### 应用到竞赛问题（1小时）

- [ ] 识别问题类型（观测数据 → 待推断参数）
- [ ] 构建前向模型（物理方程）
- [ ] 定义先验分布（基于文献或常识）
- [ ] 运行MAP快速测试（验证流程）
- [ ] 升级到PSO+MCMC（完整分析）
- [ ] 检查收敛（R-hat < 1.1，接受率 20-40%）
- [ ] 报告结果（参数 ± 95% CI）

### 论文撰写（30分钟）

- [ ] Methods: 说明先验、似然、后验
- [ ] Results: 报告MAP估计 + 置信区间
- [ ] Validation: 展示收敛诊断
- [ ] Discussion: 解释不确定性来源

---

## 技术支持

### 常见问题

**Q1: 我的前向模型很慢，MCMC运行要很久怎么办？**
- A: 先用MAP Grid方法（快速），验证流程后再升级到MCMC
- A: 减少MCMC采样数（`n_samples=2000` → `1000`）
- A: 使用PSO找到好的初始点，减少MCMC burn-in

**Q2: 收敛诊断失败（R-hat > 1.1）？**
- A: 增加采样数（`n_samples=5000` → `10000`）
- A: 调整步长（`step_size=0.01` → `0.005`）
- A: 检查先验是否太窄（MCMC被困在边界）

**Q3: 置信区间太宽，不确定性太大？**
- A: 这是真实的不确定性！不要人为收窄
- A: 增加观测数据量
- A: 使用更强的先验（如果有专家知识）

### 调试技巧

1. **先验检查**: 
   ```python
   prior.sample(100)  # 采样100次，看看范围是否合理
   ```

2. **前向模型验证**:
   ```python
   theta_test = {'alpha': 5e-9, 'N': 500, 'T': 100}
   h_sim = forward_model(x, y, theta_test)
   plt.imshow(h_sim)  # 看起来合理吗？
   ```

3. **后验可视化**:
   ```python
   plt.hist(result.posterior_samples['alpha'], bins=50)
   # 应该是单峰、光滑的分布
   ```

---

## 文件清单

```
.github/skills/bayesian_inversion/
├── __init__.py                 # 包初始化 (19行)
├── README.md                   # 技术文档 (326行)
├── QUICKSTART.md              # 快速教程 (261行)
├── INTEGRATION_GUIDE.md       # 本文档
├── requirements.txt           # 依赖 (3个包)
├── core.py                    # BayesianInverter类 (362行)
├── priors.py                  # 先验分布 (262行)
├── optimizers.py              # PSO实现 (227行)
├── samplers.py                # MCMC采样器 (294行)
└── example_stair_wear.py      # 完整示例 (241行)

总计: 1992行代码 + 文档
```

---

## 版本信息

- **技能版本**: 1.0.0
- **集成日期**: 2026年1月28日
- **技能库版本**: 2.1
- **来源**: MCM 2025 O奖论文分析（Papers 2504218, 2511565）

---

## 下一步

1. **立即行动**: 运行 `python example_stair_wear.py` 验证安装
2. **深入学习**: 阅读 `README.md` 理解数学理论
3. **实战演练**: 在模拟赛中使用此技能
4. **扩展技能库**: 考虑添加 GMM (高斯混合模型) 技能

---

**最后更新**: 2026年1月28日 15:30 CST  
**状态**: 生产就绪 ✅
