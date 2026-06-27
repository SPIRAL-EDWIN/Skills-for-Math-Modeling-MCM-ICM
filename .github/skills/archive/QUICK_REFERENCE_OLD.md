# MCM/ICM Skills Quick Reference Card

## 📊 Evaluation & Decision-Making (4 skills)

### entropy-weight-method
**One-liner**: Objective weights from data variance  
**Trigger**: "Need data-driven weights without bias"  
**Time**: 10-15 min

### ahp-method
**One-liner**: Subjective weights from expert pairwise comparisons  
**Trigger**: "Need expert judgment weights"  
**Time**: 20-30 min

### topsis-scorer
**One-liner**: Rank alternatives by closeness to ideal solution  
**Trigger**: "Which alternative is best overall?"  
**Time**: 10-15 min

### pca-analyzer
**One-liner**: Reduce 10+ indicators to principal components  
**Trigger**: "Too many correlated indicators"  
**Time**: 15-25 min

---

## 📈 Time Series & Forecasting (3 skills)

### arima-forecaster
**One-liner**: ARIMA/SARIMA for large samples (50+ points)  
**Trigger**: "Forecast with trend/seasonality"  
**Time**: 30-45 min

### grey-forecaster
**One-liner**: GM(1,1) for small samples (4-10 points)  
**Trigger**: "Only have 6 data points"  
**Time**: 15-20 min

### lstm-forecaster
**One-liner**: Deep learning for complex patterns (500+ points)  
**Trigger**: "Nonlinear, long-term dependencies"  
**Time**: 1-2 hours

---

## 🤖 Machine Learning (1 skill)

### ml-regressor
**One-liner**: Random Forest/XGBoost with feature importance  
**Trigger**: "Predict with complex interactions"  
**Time**: 30-60 min

---

## 🔬 Differential Equations (4 skills)

### differential-equations
**One-liner**: Unified ODE/PDE solver framework  
**Trigger**: "Solve any continuous-time system"  
**Time**: 20-40 min

### logistic-growth
**One-liner**: Single-species population with carrying capacity  
**Trigger**: "S-curve growth model"  
**Time**: 10-15 min

### lotka-volterra
**One-liner**: Predator-prey or competition dynamics  
**Trigger**: "Two-species interaction"  
**Time**: 20-30 min

### reaction-diffusion
**One-liner**: Spatiotemporal PDEs (pattern formation)  
**Trigger**: "Spatial spread + local reactions"  
**Time**: 30-60 min

---

## 🌐 Network & Graph Theory (2 skills)

### shortest-path
**One-liner**: Dijkstra/Floyd-Warshall for optimal routing  
**Trigger**: "Find shortest path in network"  
**Time**: 15-30 min

### network-centrality
**One-liner**: Identify critical nodes (degree/betweenness/closeness/eigenvector)  
**Trigger**: "Find key nodes, influencers, bottlenecks"  
**Time**: 20-35 min

---

## 🎯 Optimization Algorithms (4 skills)

### genetic-algorithm
**One-liner**: GA for discrete/combinatorial problems  
**Trigger**: "Optimize discrete choices (TSP, scheduling)"  
**Time**: 30-60 min

### simulated-annealing
**One-liner**: SA for multimodal continuous optimization  
**Trigger**: "Many local optima, need global search"  
**Time**: 20-40 min

### particle-swarm
**One-liner**: PSO for smooth continuous optimization  
**Trigger**: "Fast convergence on smooth objectives"  
**Time**: 15-30 min

### multi-objective-optimization
**One-liner**: NSGA-II for Pareto frontier  
**Trigger**: "Multiple conflicting objectives"  
**Time**: 1-2 hours

---

## ✅ Validation & Analysis (6 skills)

### automated-sweep
**One-liner**: Grid search for optimal parameters  
**Trigger**: "What's the best parameter value?"  
**Time**: 30-60 min

### sensitivity-master
**One-liner**: Global sensitivity (Sobol/Morris)  
**Trigger**: "Which parameters matter most?"  
**Time**: 1-3 hours

### robustness-check
**One-liner**: Stability under uncertainty  
**Trigger**: "How reliable is this model?"  
**Time**: 30-60 min

### pareto-frontier
**One-liner**: Visualize multi-objective trade-offs  
**Trigger**: "Show cost vs quality trade-off"  
**Time**: 1-2 hours

### monte-carlo-engine
**One-liner**: Uncertainty quantification  
**Trigger**: "What's the confidence interval?"  
**Time**: 30-90 min

### modular-modeler
**One-liner**: OOP architecture for complex models  
**Trigger**: "Too many moving parts"  
**Time**: 2-4 hours

---

## 🔧 Basic Tools (3 skills)

### data-cleaner
**One-liner**: Clean CSV/Excel data  
**Trigger**: "Missing values and outliers"  
**Time**: 10-20 min

### visual-engineer
**One-liner**: Publication-quality figures (300 DPI)  
**Trigger**: "Make paper figures"  
**Time**: 5-15 min

### latex-transformer
**One-liner**: Markdown → LaTeX  
**Trigger**: "Format for paper"  
**Time**: 5-10 min

---

## 🚀 Quick Decision Tree

```
START: What do you need?

├─ "Clean data"
│  ├─ Basic cleaning → data-cleaner
│  └─ Reduce dimensions → pca-analyzer
│
├─ "Forecast time series"
│  ├─ Large sample (50+) → arima-forecaster
│  ├─ Small sample (4-10) → grey-forecaster
│  └─ Complex patterns (500+) → lstm-forecaster
│
├─ "Make decision / rank alternatives"
│  ├─ Objective weights → entropy-weight-method
│  ├─ Subjective weights → ahp-method
│  └─ Final ranking → topsis-scorer
│
├─ "Predict with ML"
│  └─ → ml-regressor
│
├─ "Model dynamics"
│  ├─ Single species → logistic-growth
│  ├─ Two species → lotka-volterra
│  ├─ Spatial spread → reaction-diffusion
│  └─ General solver → differential-equations
│
├─ "Find shortest path / routing"
│  ├─ Single source, non-negative weights → shortest-path (Dijkstra)
│  ├─ All pairs distances → shortest-path (Floyd-Warshall)
│  ├─ Negative weights allowed → shortest-path (Bellman-Ford)
│  └─ With heuristic (geographic) → shortest-path (A*)
│
├─ "Identify key nodes / influencers"
│  ├─ Direct connections (popularity) → network-centrality (degree)
│  ├─ Bridges / bottlenecks → network-centrality (betweenness)
│  ├─ Spreading efficiency → network-centrality (closeness)
│  ├─ Influence by association → network-centrality (eigenvector/PageRank)
│  └─ Comprehensive analysis → network-centrality (all metrics)
│
├─ "Optimize"
│  ├─ Discrete/combinatorial → genetic-algorithm
│  ├─ Continuous (multimodal) → simulated-annealing
│  ├─ Continuous (smooth) → particle-swarm
│  ├─ Multiple objectives → multi-objective-optimization
│  └─ Simple grid search → automated-sweep
│
├─ "Validate model"
│  ├─ Find best parameters → automated-sweep
│  ├─ Which params matter? → sensitivity-master
│  ├─ Stability check → robustness-check
│  ├─ Uncertainty bounds → monte-carlo-engine
│  └─ Trade-off analysis → pareto-frontier
│
├─ "Build complex model"
│  └─ → modular-modeler
│
├─ "Make figures"
│  └─ → visual-engineer
│
└─ "Write paper"
   └─ → latex-transformer
```

---

## 📊 Typical Competition Workflow

### Day 1 (Data & Model Selection)
1. **data-cleaner** - Clean raw data (30 min)
2. **pca-analyzer** - Reduce dimensions if needed (20 min)
3. **visual-engineer** - Exploratory plots (1 hour)
4. **Choose model type**:
   - Time series? → arima/grey/lstm-forecaster
   - Decision? → entropy/ahp/topsis
   - Dynamics? → differential-equations family
   - Prediction? → ml-regressor
   - Optimization? → GA/SA/PSO/NSGA-II

### Day 2 (Model Development & Initial Results)
5. **Implement chosen model** (3-4 hours)
6. **automated-sweep** OR **genetic-algorithm** - Parameter tuning (1-2 hours)
7. **visual-engineer** - Initial result plots (1 hour)

### Day 3 (Validation & Refinement)
8. **sensitivity-master** - Identify key drivers (2 hours)
9. **robustness-check** - Prove stability (1 hour)
10. **monte-carlo-engine** - Quantify uncertainty (1-2 hours)
11. **pareto-frontier** - Trade-off analysis (if multi-objective, 1 hour)

### Day 4 (Paper Writing & Final Figures)
12. **visual-engineer** - All publication figures (2-3 hours)
13. **latex-transformer** - Format paper sections (1 hour)
14. **Final review** - Proofread and polish (2 hours)

---

## 💡 Pro Tips

### When to Use Multiple Skills Together

**Time Series Forecasting Package**:
```python
load_skills=["arima-forecaster", "monte-carlo-engine", "visual-engineer"]
# Forecast + Uncertainty bounds + Publication figures
```

**Decision-Making Complete Suite**:
```python
load_skills=["entropy-weight-method", "ahp-method", "topsis-scorer", "visual-engineer"]
# Objective + Subjective weights → Ranking → Visualization
```

**Population Dynamics Analysis**:
```python
load_skills=["lotka-volterra", "differential-equations", "sensitivity-master", "visual-engineer"]
# Model + Solve + Sensitivity + Phase portraits
```

**Transportation Network Optimization**:
```python
load_skills=["shortest-path", "genetic-algorithm", "sensitivity-master", "visual-engineer"]
# Shortest paths + Vehicle routing + Bottleneck analysis + Network diagrams
```

**Social Network Analysis**:
```python
load_skills=["network-centrality", "visual-engineer"]
# Identify influencers + Critical nodes + Network visualization
```

**Optimization with Validation**:
```python
load_skills=["genetic-algorithm", "sensitivity-master", "robustness-check", "visual-engineer"]
# Optimize + Sensitivity + Stability + Figures
```

**Multi-Objective Complete Package**:
```python
load_skills=["multi-objective-optimization", "pareto-frontier", "sensitivity-master", "visual-engineer"]
# NSGA-II + Frontier plot + Parameter analysis + Figures
```

**Data-to-Paper Pipeline**:
```python
load_skills=["data-cleaner", "pca-analyzer", "visual-engineer", "latex-transformer"]
# Clean → Reduce → Visualize → Format
```

### Time Budgets (Realistic)

| Skill | Minimum | Typical | With Iteration |
|-------|---------|---------|----------------|
| **Basic Tools** | | | |
| data-cleaner | 10 min | 20 min | 30 min |
| visual-engineer | 5 min | 10 min | 20 min |
| latex-transformer | 5 min | 10 min | 15 min |
| **Evaluation** | | | |
| entropy-weight-method | 10 min | 15 min | 25 min |
| ahp-method | 15 min | 25 min | 40 min |
| topsis-scorer | 10 min | 15 min | 20 min |
| pca-analyzer | 15 min | 20 min | 30 min |
| **Forecasting** | | | |
| grey-forecaster | 10 min | 15 min | 25 min |
| arima-forecaster | 20 min | 35 min | 60 min |
| lstm-forecaster | 45 min | 90 min | 2 hours |
| **ML & Dynamics** | | | |
| ml-regressor | 30 min | 50 min | 90 min |
| logistic-growth | 10 min | 15 min | 20 min |
| lotka-volterra | 15 min | 25 min | 40 min |
| reaction-diffusion | 30 min | 50 min | 90 min |
| differential-equations | 20 min | 35 min | 60 min |
| **Network & Graph** | | | |
| shortest-path | 15 min | 25 min | 40 min |
| network-centrality | 20 min | 30 min | 50 min |
| **Optimization** | | | |
| automated-sweep | 30 min | 1 hour | 2 hours |
| particle-swarm | 15 min | 25 min | 45 min |
| simulated-annealing | 20 min | 35 min | 60 min |
| genetic-algorithm | 30 min | 50 min | 90 min |
| multi-objective-optimization | 1 hour | 1.5 hours | 3 hours |
| **Validation** | | | |
| robustness-check | 30 min | 45 min | 1.5 hours |
| monte-carlo-engine | 30 min | 1 hour | 2 hours |
| sensitivity-master | 1 hour | 2 hours | 4 hours |
| pareto-frontier | 1 hour | 1.5 hours | 3 hours |
| modular-modeler | 2 hours | 3 hours | 6 hours |

### Computational Requirements

| Skill | Model Runs | Parallelizable? | Speed Critical? |
|-------|------------|-----------------|-----------------|
| **Optimization** | | | |
| automated-sweep | 100-1000 | ✅ Yes | ⚠️ Medium |
| genetic-algorithm | 1000-5000 | ✅ Yes | ⚠️ High |
| simulated-annealing | 500-2000 | ❌ No (sequential) | ⚠️ Medium |
| particle-swarm | 500-2000 | ✅ Yes | ⚠️ Medium |
| multi-objective-optimization | 2000-10000 | ✅ Yes | ⚠️ High |
| **Validation** | | | |
| sensitivity-master | 1000-10000 | ✅ Yes | ⚠️ High |
| monte-carlo-engine | 10000+ | ✅ Yes | ⚠️ High |
| robustness-check | 50-200 | ✅ Yes | ✅ Low |
| pareto-frontier | 100-500 | ✅ Yes | ⚠️ Medium |
| **Forecasting** | | | |
| lstm-forecaster | 1000+ epochs | ✅ GPU | ⚠️ High |
| arima-forecaster | 50-200 | ❌ No | ✅ Low |
| grey-forecaster | <10 | ❌ No | ✅ Low |

**Optimization Strategy**: If model is slow (>1 sec/run):
1. Vectorize computations (NumPy/Pandas)
2. Use multiprocessing for parallel evaluation
3. Consider surrogate models (Gaussian Process)
4. Use PSO instead of GA (fewer evaluations needed)

---

## 🎓 O-Prize Checklist

To maximize chances of Outstanding Winner:

### Must Have (80% of O-Prize papers)
- [ ] **Model Selection Justified**: Use decision tree to pick appropriate model type
- [ ] **Uncertainty Quantification**: monte-carlo-engine OR lstm-forecaster confidence intervals
- [ ] **Sensitivity Analysis**: sensitivity-master (Sobol) OR robustness-check (tornado)
- [ ] **Publication-Quality Figures**: visual-engineer (300 DPI, Times New Roman)
- [ ] **Clean, Documented Code**: modular-modeler for complex systems

### Strong Plus (50% of O-Prize papers)
- [ ] **Parameter Optimization**: automated-sweep OR genetic-algorithm with convergence proof
- [ ] **Multi-Objective Analysis**: multi-objective-optimization + pareto-frontier
- [ ] **Mechanistic Foundation**: differential-equations (not just black-box ML)
- [ ] **Feature Importance**: ml-regressor OR pca-analyzer showing key drivers
- [ ] **Comprehensive Evaluation**: entropy + AHP + TOPSIS for decisions

### Nice to Have (20% of O-Prize papers)
- [ ] **Hybrid Modeling**: Combine mechanistic (ODE) + data-driven (ML)
- [ ] **Spatial Dynamics**: reaction-diffusion for epidemic/ecology problems
- [ ] **Advanced Optimization**: NSGA-II for Pareto-optimal policies
- [ ] **Small-Sample Techniques**: grey-forecaster when data is limited
- [ ] **Comparison with Baselines**: Show your model outperforms simpler alternatives

---

## 🔗 Related Files

- **Detailed Guide**: `README.md` (full documentation)
- **Strategy Manual**: `../../MCM_AI_Strategy_Guide.md`
- **Skill Creator**: `skill-creator/SKILL.md`

---

*Print this reference card and keep it handy during competition!*
