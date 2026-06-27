# MCM/ICM Competition Skills

This directory contains specialized skills for Mathematical Contest in Modeling (MCM) and Interdisciplinary Contest in Modeling (ICM) competitions.

## Skill Categories

### 1. Evaluation & Decision-Making Models

#### **entropy-weight-method**
- **Purpose**: Objective weighting based on data variance
- **Use When**: Need data-driven weights without subjective judgment
- **Key Output**: Objective weights for each indicator
- **Method**: Information entropy to quantify indicator differentiation

#### **ahp-method**
- **Purpose**: Subjective weighting via pairwise comparisons
- **Use When**: Expert judgment needed, qualitative factors involved
- **Key Output**: Consistent weight vector with CR < 0.1
- **Method**: Analytic Hierarchy Process with consistency check

#### **topsis-scorer**
- **Purpose**: Comprehensive evaluation and ranking
- **Use When**: Multiple alternatives with multiple criteria
- **Key Output**: Ranked alternatives with closeness scores
- **Integration**: Works with entropy-weight-method and ahp-method

#### **pca-analyzer**
- **Purpose**: Dimensionality reduction and feature extraction
- **Use When**: High-dimensional data (10+ indicators), multicollinearity present
- **Key Output**: Principal components explaining 85%+ variance
- **Method**: Eigenvalue decomposition with Kaiser criterion

---

### 2. Time Series & Forecasting Models

#### **arima-forecaster**
- **Purpose**: ARIMA/SARIMA for stationary time series
- **Use When**: Large sample (50+ points), clear trend/seasonality
- **Key Output**: Forecast with confidence intervals
- **Method**: Auto ARIMA with AIC/BIC selection

#### **grey-forecaster**
- **Purpose**: GM(1,1) for small-sample prediction
- **Use When**: Limited data (4-10 points), exponential growth pattern
- **Key Output**: Short-term forecast (1-3 steps ahead)
- **Method**: Grey differential equation with least squares

#### **lstm-forecaster**
- **Purpose**: LSTM/GRU for complex temporal patterns
- **Use When**: Nonlinear dependencies, long-term memory needed, large dataset (500+ points)
- **Key Output**: Multi-step forecast with attention weights
- **Method**: Deep learning with early stopping

---

### 3. Machine Learning Models

#### **ml-regressor**
- **Purpose**: Random Forest & XGBoost for nonlinear regression
- **Use When**: Complex feature interactions, need feature importance
- **Key Output**: Predictions with feature importance ranking
- **Method**: Ensemble learning with cross-validation

---

### 4. Differential Equations & Mechanistic Models

#### **differential-equations** (Unified Framework)
- **Purpose**: Comprehensive ODE/PDE solver integrating all mechanistic models
- **Use When**: Any continuous-time dynamic system
- **Key Output**: Time series solutions, phase portraits, bifurcation diagrams
- **Integrates**: logistic-growth, lotka-volterra, reaction-diffusion

#### **logistic-growth**
- **Purpose**: Single-species population dynamics
- **Use When**: Growth with carrying capacity constraint
- **Key Output**: S-curve growth trajectory
- **Method**: Logistic ODE with analytical/numerical solution

#### **lotka-volterra**
- **Purpose**: Predator-prey and competition models
- **Use When**: Two-species interaction dynamics
- **Key Output**: Phase portraits showing cyclic behavior
- **Method**: Coupled ODEs with stability analysis

#### **reaction-diffusion**
- **Purpose**: Spatiotemporal PDEs (pattern formation)
- **Use When**: Spatial spread + local reactions (epidemics, ecology)
- **Key Output**: 2D/3D spatiotemporal patterns
- **Method**: Finite difference with stability constraints

---

### 5. Network & Graph Theory

#### **shortest-path**
- **Purpose**: Dijkstra, Floyd-Warshall, Bellman-Ford, A* algorithms
- **Use When**: Transportation networks, logistics routing, network optimization
- **Key Output**: Optimal paths, distance matrices, route visualization
- **Method**: Graph algorithms for weighted shortest paths

#### **network-centrality**
- **Purpose**: Centrality analysis (degree, betweenness, closeness, eigenvector, PageRank)
- **Use When**: Social network analysis, infrastructure vulnerability, epidemic modeling, influence ranking
- **Key Output**: Critical node identification, centrality scores, network visualization
- **Method**: Graph centrality metrics for identifying key nodes

---

### 6. Optimization Algorithms

#### **genetic-algorithm**
- **Purpose**: GA for discrete/combinatorial optimization
- **Use When**: Discrete variables, combinatorial problems (TSP, scheduling)
- **Key Output**: Near-optimal solution with convergence curve
- **Method**: Selection, crossover, mutation with elitism

#### **simulated-annealing**
- **Purpose**: SA for multimodal continuous optimization
- **Use When**: Many local optima, need global search
- **Key Output**: Global optimum with cooling schedule
- **Method**: Metropolis criterion with exponential cooling

#### **particle-swarm**
- **Purpose**: PSO for smooth continuous optimization
- **Use When**: Continuous variables, smooth objective, fast convergence needed
- **Key Output**: Optimal solution with swarm trajectory
- **Method**: Velocity update with inertia weight

#### **multi-objective-optimization**
- **Purpose**: NSGA-II/III for Pareto frontier analysis
- **Use When**: Multiple conflicting objectives (cost vs quality)
- **Key Output**: Pareto front with non-dominated solutions
- **Method**: Non-dominated sorting with crowding distance

---

### 7. Validation & Analysis Skills (O-Prize Level)

#### **automated-sweep**
- **Purpose**: Automated parameter sweeping and optimization
- **Use When**: Determining optimal model parameters through systematic exploration
- **Key Output**: Parameter heatmaps, optimal value identification with loss function evaluation
- **Computational Budget**: 100-1000 model evaluations

#### **modular-modeler**
- **Purpose**: Object-oriented architecture for complex system models
- **Use When**: Building multi-component models (System Dynamics, Agent-Based Models)
- **Key Output**: Maintainable, testable, swappable model components
- **Benefits**: Mid-competition model changes without breaking entire codebase

#### **pareto-frontier**
- **Purpose**: Multi-objective optimization visualization
- **Use When**: Problems involve trade-offs (economic vs. environmental, cost vs. benefit)
- **Key Output**: Pareto frontier plots showing non-dominated solution sets
- **Narrative**: "We provide multiple optimal solutions for different stakeholder preferences"

#### **robustness-check**
- **Purpose**: Model stability and reliability validation
- **Use When**: Need to prove model results are stable under parameter uncertainty
- **Key Output**: Tornado diagrams, phase plane plots, Monte Carlo robustness tests
- **Critical**: Demonstrates model quality to judges

#### **sensitivity-master**
- **Purpose**: Advanced global sensitivity analysis
- **Use When**: Complex/nonlinear models with 5+ parameters
- **Key Output**: Sobol indices, Morris screening, spider plots identifying key drivers
- **Methods**: Morris (fast screening), Sobol (rigorous quantification)

#### **monte-carlo-engine**
- **Purpose**: Uncertainty quantification and risk analysis
- **Use When**: Dealing with randomness, incomplete data, stochastic models
- **Key Output**: Confidence interval plots, probability distributions, convergence diagnostics
- **Standard**: 10,000+ simulations with proper distribution selection

---

### 8. Basic Skills

Essential tools for data processing, visualization, and document preparation.

#### **data-cleaner**
- **Purpose**: Automated data cleaning and preprocessing
- **Use When**: Loading raw CSV/Excel data before modeling
- **Key Output**: Clean datasets with statistical quality reports
- **Pipeline**: Missing values → Outliers → Type conversion → Normalization

#### **visual-engineer**
- **Purpose**: Academic-quality visualization
- **Use When**: Creating figures for papers requiring publication standards
- **Key Output**: 300 DPI figures with Times New Roman, proper colormaps
- **Standards**: Colorblind-friendly, LaTeX integration, consistent styling

#### **latex-transformer**
- **Purpose**: Convert Markdown to LaTeX format
- **Use When**: Drafting content in Markdown, need LaTeX for paper
- **Key Output**: Properly formatted LaTeX (equations, tables, citations, figures)
- **Handles**: Three-line tables, equation environments, bibliography integration

---

## Usage Workflow

### Phase 1: Data Preparation & Exploration (Hours 0-12)
1. **data-cleaner**: Clean raw data from web scraping or downloads
2. **pca-analyzer**: Reduce dimensions if 10+ indicators (optional)
3. **visual-engineer**: Create exploratory plots to understand data

### Phase 2: Model Selection & Development (Day 1-2)

**For Time Series Problems:**
- **arima-forecaster** (if 50+ points, stationary)
- **grey-forecaster** (if 4-10 points)
- **lstm-forecaster** (if 500+ points, complex patterns)

**For Decision-Making Problems:**
- **entropy-weight-method** + **ahp-method** → **topsis-scorer**

**For Mechanistic Models:**
- **differential-equations** (unified interface) with:
  - **logistic-growth** (single species)
  - **lotka-volterra** (predator-prey)
  - **reaction-diffusion** (spatial dynamics)

**For Optimization Problems:**
- **genetic-algorithm** (discrete/combinatorial)
- **simulated-annealing** (multimodal continuous)
- **particle-swarm** (smooth continuous)
- **multi-objective-optimization** (multiple objectives)

**For Prediction Problems:**
- **ml-regressor** (Random Forest/XGBoost)

### Phase 3: Parameter Tuning & Optimization (Day 2-3)
4. **automated-sweep**: Find optimal parameters through systematic search
5. **genetic-algorithm** / **particle-swarm** / **simulated-annealing**: Advanced optimization
6. **monte-carlo-engine**: Quantify uncertainty in stochastic models

### Phase 4: Validation & Analysis (Day 3-4)
7. **sensitivity-master**: Identify key parameter drivers (Sobol/Morris)
8. **robustness-check**: Prove model stability (tornado, phase plane)
9. **pareto-frontier**: Visualize multi-objective trade-offs (if applicable)

### Phase 5: Paper Writing (Day 4)
10. **visual-engineer**: Generate all publication-quality figures
11. **latex-transformer**: Convert Markdown drafts to LaTeX sections

---

## Skill Selection Guide

| Problem Type | Recommended Skills |
|--------------|-------------------|
| **Population Dynamics** | logistic-growth OR lotka-volterra, differential-equations, automated-sweep, robustness-check |
| **Epidemic Spread (Spatial)** | reaction-diffusion, differential-equations, sensitivity-master, visual-engineer |
| **Time Series Forecasting** | arima-forecaster (large sample) OR grey-forecaster (small sample) OR lstm-forecaster (complex), monte-carlo-engine |
| **Multi-Criteria Decision** | entropy-weight-method + ahp-method + topsis-scorer, visual-engineer |
| **Dimensionality Reduction** | pca-analyzer, visual-engineer, ml-regressor |
| **Nonlinear Regression** | ml-regressor, sensitivity-master, robustness-check |
| **Transportation & Routing** | shortest-path (Dijkstra/Floyd), genetic-algorithm (VRP), visual-engineer |
| **Network Optimization** | shortest-path, network-centrality, sensitivity-master (bottleneck analysis), robustness-check |
| **Social Network Analysis** | network-centrality (influencer identification), visual-engineer |
| **Infrastructure Vulnerability** | network-centrality (critical nodes), shortest-path, robustness-check |
| **Discrete Optimization** | genetic-algorithm, simulated-annealing (if many local optima), sensitivity-master |
| **Continuous Optimization** | particle-swarm (smooth) OR simulated-annealing (multimodal), automated-sweep |
| **Multi-Objective Optimization** | multi-objective-optimization, pareto-frontier, sensitivity-master |
| **Stochastic/Uncertain Systems** | monte-carlo-engine, sensitivity-master, robustness-check |
| **Multi-Agent Systems** | modular-modeler, genetic-algorithm (emergent behavior), visual-engineer |
| **Policy Analysis** | topsis-scorer, pareto-frontier, sensitivity-master, visual-engineer |

---

## Quality Standards

### For O-Prize Recognition

A winning solution typically demonstrates:
- ✅ **Rigorous parameter validation** (automated-sweep or sensitivity-master)
- ✅ **Uncertainty quantification** (monte-carlo-engine with confidence intervals)
- ✅ **Robustness analysis** (robustness-check with multiple diagnostics)
- ✅ **Publication-quality figures** (visual-engineer at 300 DPI)
- ✅ **Clean, modular code** (modular-modeler for complex systems)
- ✅ **Multi-objective awareness** (pareto-frontier when applicable)

### Minimum Requirements

Every submission should include:
- ✅ Clean data with documented preprocessing (data-cleaner)
- ✅ At least one validation technique (robustness-check OR sensitivity-master)
- ✅ Professional figures (visual-engineer)
- ✅ Properly formatted LaTeX paper (latex-transformer)

---

## Complete Skill Catalog (26 Skills)

### By Domain

| Domain | Skills | Count |
|--------|--------|-------|
| **Evaluation & Decision** | entropy-weight-method, ahp-method, topsis-scorer, pca-analyzer | 4 |
| **Time Series & Forecasting** | arima-forecaster, grey-forecaster, lstm-forecaster | 3 |
| **Machine Learning** | ml-regressor | 1 |
| **Differential Equations** | differential-equations, logistic-growth, lotka-volterra, reaction-diffusion | 4 |
| **Network & Graph Theory** | shortest-path, network-centrality | 2 |
| **Optimization** | genetic-algorithm, simulated-annealing, particle-swarm, multi-objective-optimization | 4 |
| **Validation & Analysis** | automated-sweep, sensitivity-master, robustness-check, pareto-frontier, monte-carlo-engine, modular-modeler | 6 |
| **Basic Tools** | data-cleaner, visual-engineer, latex-transformer | 3 |
| **Meta** | skill-creator | 1 |

### Integration with MCM AI Strategy Guide

Core skills implement techniques from `MCM_AI_Strategy_Guide.md`:

| Strategy Guide Section | Corresponding Skill |
|------------------------|---------------------|
| Automated-Sweep (Section III.1) | automated-sweep |
| Modular-Modeler (Section III.2) | modular-modeler |
| Pareto-Frontier (Section III.3) | pareto-frontier |
| Robustness-Check (Section III.4) | robustness-check |
| Sensitivity-Master (Section III.5) | sensitivity-master |
| Monte-Carlo-Engine (Section III.6) | monte-carlo-engine |
| Data-Cleaner (Section IV.1) | data-cleaner |
| Visual-Engineer (Section IV.2) | visual-engineer |
| LaTeX-Transformer (Section IV.3) | latex-transformer |

**Extended Skills** (built in 2026 session):
- Evaluation models: entropy-weight-method, ahp-method, topsis-scorer, pca-analyzer
- Forecasting models: arima-forecaster, grey-forecaster, lstm-forecaster
- ML models: ml-regressor
- Mechanistic models: differential-equations, logistic-growth, lotka-volterra, reaction-diffusion
- Optimization algorithms: genetic-algorithm, simulated-annealing, particle-swarm, multi-objective-optimization

---

## Loading Skills in OpenCode

To use these skills with the Sisyphus agent:

```python
# Example 1: Time series forecasting with small sample
delegate_task(
    category="unspecified-high",
    load_skills=["grey-forecaster", "visual-engineer"],
    prompt="""
    Use Grey GM(1,1) model to forecast next 3 years based on 6 historical 
    data points: [100, 120, 145, 175, 210, 250]. Generate forecast plot 
    with 95% confidence intervals.
    """,
    run_in_background=False
)

# Example 2: Multi-criteria decision making
delegate_task(
    category="unspecified-high",
    load_skills=["entropy-weight-method", "ahp-method", "topsis-scorer", "visual-engineer"],
    prompt="""
    Evaluate 5 policy alternatives using 8 indicators. First calculate 
    objective weights (entropy) and subjective weights (AHP). Then use 
    TOPSIS to rank alternatives. Generate comparison radar chart.
    """,
    run_in_background=False
)

# Example 3: Population dynamics modeling
delegate_task(
    category="unspecified-high",
    load_skills=["lotka-volterra", "differential-equations", "sensitivity-master", "visual-engineer"],
    prompt="""
    Model predator-prey dynamics with Lotka-Volterra equations. Perform 
    Sobol sensitivity analysis on 4 parameters. Generate phase portrait 
    and sensitivity spider plot.
    """,
    run_in_background=False
)

# Example 4: Multi-objective optimization
delegate_task(
    category="unspecified-high",
    load_skills=["multi-objective-optimization", "pareto-frontier", "visual-engineer"],
    prompt="""
    Optimize production planning with 2 objectives: minimize cost, maximize 
    quality. Use NSGA-II with 100 generations. Generate Pareto frontier 
    plot and recommend 3 representative solutions.
    """,
    run_in_background=False
)

# Example 5: Discrete optimization problem
delegate_task(
    category="unspecified-high",
    load_skills=["genetic-algorithm", "sensitivity-master", "visual-engineer"],
    prompt="""
    Solve facility location problem with 20 cities using genetic algorithm. 
    Population size 100, 200 generations. Analyze sensitivity to crossover 
    and mutation rates. Generate convergence curve.
    """,
    run_in_background=False
)

# Example 6: Comprehensive validation suite
delegate_task(
    category="unspecified-high",
    load_skills=["automated-sweep", "sensitivity-master", "robustness-check", "monte-carlo-engine", "visual-engineer"],
    prompt="""
    Full validation of epidemic model: 1) Parameter sweep for R0 and recovery 
    rate, 2) Sobol sensitivity analysis, 3) Tornado diagram for robustness, 
    4) Monte Carlo with 10000 runs. Generate publication-quality figures.
    """,
    run_in_background=False
)
```

---

## Output Organization

Skills follow standardized output locations:

```
results/
├── data/
│   ├── processed.csv                    # data-cleaner
│   ├── processed_report.json
│   └── pca_components.csv               # pca-analyzer
├── figures/                              # visual-engineer (all skills)
│   ├── fig1_time_series.png
│   ├── fig2_heatmap.png
│   └── ...
├── evaluation/
│   ├── entropy_weights.csv              # entropy-weight-method
│   ├── ahp_weights.csv                  # ahp-method
│   └── topsis_ranking.csv               # topsis-scorer
├── forecasts/
│   ├── arima_forecast.csv               # arima-forecaster
│   ├── grey_forecast.csv                # grey-forecaster
│   └── lstm_forecast.csv                # lstm-forecaster
├── ml_models/
│   ├── rf_predictions.csv               # ml-regressor
│   └── feature_importance.png
├── ode_solutions/
│   ├── logistic_trajectory.csv          # logistic-growth
│   ├── lotka_volterra_phase.png         # lotka-volterra
│   └── reaction_diffusion_2d.mp4        # reaction-diffusion
├── optimization/
│   ├── ga_best_solution.json            # genetic-algorithm
│   ├── sa_convergence.png               # simulated-annealing
│   ├── pso_trajectory.png               # particle-swarm
│   └── nsga2_pareto_front.csv           # multi-objective-optimization
├── parameter_sweep/
│   ├── heatmap.png                      # automated-sweep
│   └── optimal_params.json
├── sensitivity/
│   ├── sobol_indices.png                # sensitivity-master
│   └── morris_screening.png
├── robustness/
│   ├── tornado_diagram.png              # robustness-check
│   └── phase_plane.png
├── pareto_analysis/
│   ├── pareto_frontier.png              # pareto-frontier
│   └── pareto_solutions.csv
└── monte_carlo/
    ├── forecast_with_ci.png             # monte-carlo-engine
    └── distribution.png
```

---

## Contributing

When creating new skills:
1. Follow the structure in `skill-creator/SKILL.md`
2. Include clear "When to Use" section in frontmatter description
3. Provide code templates with proper documentation
4. Specify output requirements and file locations
5. List common pitfalls to avoid

---

## References

- **MCM AI Strategy Guide**: `../../MCM_AI_Strategy_Guide.md`
- **Skill Creation Guide**: `skill-creator/SKILL.md`
- **Project Structure**: `../../README.md`

---

*Created for MCM/ICM 2026 Competition*  
*Zhejiang University Team*
