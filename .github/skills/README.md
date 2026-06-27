# MCM/ICM 2026 Competition Modeling Skills Master Guide

**Version:** 3.2

**Scope:** 42 reusable skill definitions plus one Bayesian inversion support module

**Audience:** MCM/ICM teams, mathematical modeling learners, and builders of competition-oriented modeling workflows

This guide is the central reference for selecting, combining, and applying the modeling skills in this repository. It is designed for fast decision-making during a competition: start from the problem type, choose an appropriate method family, implement a credible model, validate it, and translate the result into a polished paper.

Since 2024, COMAP has required teams to disclose AI-tool use. The `ai-report-writer` skill is therefore treated as a mandatory competition support skill rather than an optional writing utility.

---

## Table of Contents

1. [Decision Tree](#decision-tree)
2. [Time Budgets](#time-budgets)
3. [Stage 1: Data Preparation](#stage-1-data-preparation)
4. [Stage 2: Model Construction](#stage-2-model-construction)
5. [Stage 3: Validation and Analysis](#stage-3-validation-and-analysis)
6. [Stage 4: Paper Production](#stage-4-paper-production)
7. [Typical Workflows](#typical-workflows)
8. [Outstanding-Winner Checklist](#outstanding-winner-checklist)

---

## Decision Tree

```text
Start: What do you need to do?

Clean or prepare data
  Basic missing-value and outlier handling -> data-cleaner
  Too many correlated indicators -> pca-analyzer
  Spreadsheet-heavy raw data -> xlsx

Forecast future values
  Short positive series with limited samples -> grey-forecaster
  Long enough stationary or seasonal time series -> arima-forecaster
  Large nonlinear sequence data -> lstm-forecaster
  Tabular prediction with feature importance -> ml-regressor

Rank alternatives or make a decision
  Objective data-driven weights -> entropy-weight-method
  Expert or judgment-based weights -> ahp-method
  Qualitative or fuzzy indicators -> fuzzy-evaluation
  Small-sample association analysis -> grey-relation
  Final ranking from weighted indicators -> topsis-scorer

Build a mechanism-based model
  Single-population constrained growth -> logistic-growth
  Two interacting populations or competitors -> lotka-volterra
  Spatial spread over time -> reaction-diffusion
  Custom ODE or PDE model -> differential-equations

Analyze networks or paths
  Graph representation and traversal -> graph-theory
  Shortest route or emergency path -> shortest-path
  Minimum-cost network design -> minimum-spanning-tree
  Influential nodes or vulnerability -> network-centrality

Optimize decisions
  Linear objective and constraints -> linear-programming
  Nonlinear objective or constraints -> nonlinear-programming
  Integer or binary decisions -> integer-programming
  Worst-case or robust objective -> minimax-programming
  Multi-stage decisions -> dynamic-programming
  Combinatorial search -> genetic-algorithm
  Continuous multimodal search -> simulated-annealing
  Fast continuous parameter search -> particle-swarm
  Conflicting objectives -> multi-objective-optimization
  Simple parameter sweep -> automated-sweep

Solve an inverse problem
  Infer parameters from observations with uncertainty -> bayesian_inversion

Validate a model
  Find best parameters -> automated-sweep
  Identify important parameters -> sensitivity-master
  Test stability under extreme assumptions -> robustness-check
  Quantify uncertainty intervals -> monte-carlo-engine
  Inspect objective trade-offs -> pareto-frontier

Communicate results
  Publication-quality figures -> visual-engineer
  Custom web-based diagrams or interactive visuals -> web-artifacts-builder
  LaTeX collaboration and paper structure -> latex-coauthoring
  Markdown-to-LaTeX conversion -> latex-transformer
  PDF extraction or final submission assembly -> pdf
  Mandatory AI-use disclosure -> ai-report-writer
```

---

## Time Budgets

These estimates are practical competition-time budgets, not theoretical runtime guarantees.

| Skill or task | Fast pass | Typical pass | With debugging |
| --- | ---: | ---: | ---: |
| data-cleaner | 10 min | 20 min | 30 min |
| xlsx | 10 min | 30 min | 60 min |
| visual-engineer | 5 min | 10 min | 20 min |
| web-artifacts-builder | 20 min | 45 min | 90 min |
| latex-coauthoring | 2 hours | 15 hours | 30 hours |
| latex-transformer | 5 min | 10 min | 15 min |
| pdf extraction | 10 min | 30 min | 60 min |
| pdf submission assembly | 15 min | 30 min | 60 min |
| ai-report-writer logging | 2-3 min per interaction | 1-2 hours total | spread across the contest |
| ai-report-writer final report | 45 min | 1 hour | 1.5 hours |
| entropy-weight-method / topsis-scorer | 10 min | 15 min | 25 min |
| ahp-method | 15 min | 25 min | 40 min |
| pca-analyzer | 15 min | 20 min | 30 min |
| fuzzy-evaluation | 20 min | 30 min | 50 min |
| grey-relation | 15 min | 25 min | 40 min |
| grey-forecaster | 10 min | 15 min | 25 min |
| arima-forecaster | 20 min | 35 min | 60 min |
| lstm-forecaster | 45 min | 90 min | 2 hours |
| logistic-growth / lotka-volterra | 10-15 min | 25 min | 40 min |
| reaction-diffusion | 30 min | 50 min | 90 min |
| differential-equations | 20 min | 35 min | 60 min |
| graph-theory | 20 min | 30 min | 50 min |
| shortest-path | 15 min | 25 min | 40 min |
| minimum-spanning-tree | 15 min | 25 min | 40 min |
| network-centrality | 20 min | 30 min | 50 min |
| linear-programming | 20 min | 40 min | 1 hour |
| nonlinear-programming | 30 min | 50 min | 1.5 hours |
| integer-programming | 30 min | 50 min | 1.5 hours |
| minimax-programming | 25 min | 40 min | 1 hour |
| dynamic-programming | 30 min | 1 hour | 2 hours |
| automated-sweep | 30 min | 1 hour | 2 hours |
| particle-swarm | 15 min | 25 min | 45 min |
| simulated-annealing | 20 min | 35 min | 60 min |
| genetic-algorithm | 30 min | 50 min | 90 min |
| multi-objective-optimization | 1 hour | 1.5 hours | 3 hours |
| bayesian_inversion MAP prototype | 15 min | 30 min | 1 hour |
| bayesian_inversion PSO + MCMC | 45 min | 1.5 hours | 3 hours |
| robustness-check | 30 min | 45 min | 1.5 hours |
| monte-carlo-engine | 30 min | 1 hour | 2 hours |
| sensitivity-master | 1 hour | 2 hours | 4 hours |

---

## Stage 1: Data Preparation

### `data-cleaner`

Use this skill when the raw data contains missing values, outliers, inconsistent units, duplicate records, or fields that need normalization before modeling. The expected output is a modeling-ready dataset plus a concise cleaning report that explains the treatment of missing values and abnormal observations.

Recommended techniques include interpolation, deletion with justification, 3-sigma screening, interquartile-range filtering, unit conversion, and vectorized Pandas operations.

### `pca-analyzer`

Use this skill when the problem has many correlated indicators and the model would otherwise suffer from multicollinearity or weak interpretability. A credible PCA workflow should report explained variance ratios, cumulative variance, loading matrices, and a plain-language interpretation of the retained principal components.

For contest work, a common threshold is to retain enough components to explain at least 85 percent of the cumulative variance, unless the problem statement gives a stronger reason to choose a different cutoff.

### `xlsx`

Use this skill for Excel- or CSV-heavy preprocessing. It supports cleaning, normalization for decision models, descriptive statistics, feature engineering, and conversion into model-ready tables.

---

## Stage 2: Model Construction

### A. Evaluation and Decision Models

#### `entropy-weight-method`

Entropy weighting is an objective weighting method based on variation in the observed data. It is useful when the team wants to reduce subjective judgment in indicator weights. It is commonly paired with `topsis-scorer`.

#### `ahp-method`

The Analytic Hierarchy Process converts expert pairwise comparisons into weights. A credible AHP result must report the consistency ratio and should satisfy CR < 0.1. Use it when qualitative judgment is unavoidable, such as policy strength, social acceptability, or strategic priority.

#### `topsis-scorer`

TOPSIS ranks alternatives by their distance to the ideal and negative-ideal solutions. It is often used as the final ranking layer after AHP, entropy weighting, PCA, or fuzzy evaluation.

#### `fuzzy-evaluation`

Fuzzy comprehensive evaluation is useful for qualitative or ambiguous indicators. The standard workflow is to define the factor set, define the evaluation set, build a membership matrix, assign weights, and perform fuzzy aggregation.

Typical applications include environmental quality, education quality, risk assessment, and service satisfaction.

#### `grey-relation`

Grey relational analysis measures association under small-sample or incomplete-information conditions. It does not require a large sample or a strict linear relationship, which makes it useful for factor screening and small-sample decision analysis.

### B. Forecasting and Time-Series Models

#### `grey-forecaster`

Use GM(1,1) when data are scarce, positive, and relatively smooth. It is particularly useful when only four to ten observations are available and the team still needs a defensible trend forecast.

#### `arima-forecaster`

ARIMA is a classical statistical forecasting method for time series with sufficient length. A complete ARIMA workflow should include stationarity checks, differencing if needed, order selection, residual diagnostics, and forecast intervals.

#### `lstm-forecaster`

Use LSTM models for large nonlinear sequence data where classical time-series models are too restrictive. Because LSTMs require more data and tuning, they are best used when the dataset is large enough and predictive performance is central to the paper.

#### `ml-regressor`

Use machine-learning regression when tabular features drive a target variable. Random forest, gradient boosting, or related models can provide both prediction and feature-importance analysis, which improves interpretability in the final paper.

### C. Mechanistic and Differential-Equation Models

#### `logistic-growth`

Use logistic growth for single-population or adoption processes constrained by a carrying capacity. The model should estimate or justify the carrying capacity and explain the saturation mechanism.

#### `lotka-volterra`

Use Lotka-Volterra models for predator-prey, competition, or other two-population interactions. A strong analysis should include phase portraits, equilibrium points, and stability interpretation.

#### `reaction-diffusion`

Use reaction-diffusion models for spatiotemporal spread, such as disease transmission, pollution diffusion, invasive species, or heat-like propagation. Good outputs include two-dimensional or three-dimensional evolution plots and parameter sensitivity checks.

#### `differential-equations`

Use this skill as the general ODE/PDE solver framework when the standard named models do not fit. It should help define the state variables, equations, initial conditions, numerical method, and validation strategy.

### D. Network and Graph-Theory Models

#### `graph-theory`

Use this skill to define graph representations, adjacency matrices, adjacency lists, traversal algorithms, connected components, and basic network properties.

#### `shortest-path`

Use shortest-path methods for logistics, emergency routing, evacuation, communication networks, or route planning. Common algorithms include Dijkstra, Floyd-Warshall, Bellman-Ford, and A*.

#### `minimum-spanning-tree`

Use minimum spanning trees for network design when all nodes must be connected at minimum total cost. Typical algorithms include Prim and Kruskal.

#### `network-centrality`

Use centrality metrics to identify important nodes in a network. Degree, betweenness, closeness, and eigenvector centrality each answer a different version of "importance"; the paper should state which meaning is relevant.

### E. Optimization and Planning Models

#### `linear-programming`

Use linear programming when both the objective function and constraints are linear. Typical applications include resource allocation, production planning, transportation, blending, and scheduling approximations.

#### `nonlinear-programming`

Use nonlinear programming when the objective or constraints are nonlinear. Since local optima can occur, report initial guesses, solver settings, and robustness checks where appropriate.

#### `integer-programming`

Use integer programming when decisions must be integer-valued or binary, such as assignment, facility location, knapsack, crew scheduling, and selection problems.

#### `minimax-programming`

Use minimax programming to optimize worst-case performance. It is especially useful for robust decision-making, risk control, game-theoretic settings, and designs that must remain acceptable under adverse scenarios.

#### `dynamic-programming`

Use dynamic programming for multi-stage decisions with optimal substructure. The paper should clearly define states, decisions, transitions, boundary conditions, and the objective recurrence.

#### `genetic-algorithm`

Genetic algorithms are useful for global search in discrete, combinatorial, or encoding-friendly problems such as routing, layout, selection, and scheduling.

#### `simulated-annealing`

Simulated annealing is useful for multimodal landscapes where the solver must escape local optima. It is relatively simple to implement and explain, but the cooling schedule should be justified.

#### `particle-swarm`

Particle swarm optimization is a fast and intuitive method for continuous parameter search. It is useful for fitting, calibration, and smooth optimization when gradients are unavailable or inconvenient.

#### `multi-objective-optimization`

Use multi-objective optimization when goals conflict, such as minimizing cost while maximizing service quality. NSGA-II, MOEA/D, and MOPSO are common approaches. The expected output is a Pareto frontier and a principled final selection rule, often using `topsis-scorer`.

#### `automated-sweep`

Use automated parameter sweeps for quick grid search, calibration, ablation, and sensitivity-oriented exploration. It is not always the most elegant optimizer, but it is transparent and highly useful under time pressure.

### F. Inverse Problems and Parameter Estimation

#### `bayesian_inversion`

This repository includes `bayesian_inversion` as a support module rather than a standard skill definition. It is designed for parameter inversion from observed data with uncertainty quantification.

The core workflow is:

```text
prior(theta) x likelihood(observations | theta) -> posterior(theta | observations)
```

Typical use cases include material-wear inference, archaeological stair-wear reconstruction, geophysical parameter estimation, and epidemiological rate inference.

A strong Bayesian inversion result should report point estimates, 95 percent credible intervals, convergence diagnostics, and the assumptions behind the prior and likelihood. Compared with reporting only point estimates, uncertainty quantification can make a paper substantially more convincing.

---

## Stage 3: Validation and Analysis

### `sensitivity-master`

Use global sensitivity analysis, such as Sobol or Morris methods, to identify which parameters truly drive the result. Strong contest papers rarely stop at one-factor-at-a-time tests.

### `robustness-check`

Use robustness checks to test whether the model remains credible under extreme or perturbed assumptions. Tornado diagrams are often effective for communicating which assumptions matter most.

### `monte-carlo-engine`

Use Monte Carlo simulation when inputs are uncertain or stochastic. Report confidence intervals, credible intervals, or empirical distributions rather than only a single deterministic output.

### `pareto-frontier`

Use Pareto-frontier visualization to explain trade-offs among objectives. It is especially useful after multi-objective optimization or policy analysis.

### `modular-modeler`

Use modular modeling when the codebase becomes large, multiple teammates are contributing, or the model contains several interacting subsystems. A modular architecture makes validation and revision easier.

---

## Stage 4: Paper Production

### `visual-engineer`

Use this skill for publication-quality figures. Contest figures should have readable labels, consistent typography, clean color use, and enough resolution for PDF submission.

### `web-artifacts-builder`

Use this skill when a standard Matplotlib or Excel figure cannot communicate the system clearly. It is well suited for model architecture diagrams, custom network views, Sankey diagrams, chord diagrams, and interactive prototypes that can be exported as high-quality images.

### `latex-transformer`

Use this skill to convert Markdown-style derivations, formulas, tables, and references into LaTeX. It is useful when moving from draft notes to the final paper.

### `latex-coauthoring`

Use this skill for the full LaTeX paper-writing workflow, including structure, mathematical exposition, section drafting, and Summary Sheet refinement. In MCM/ICM, the Summary Sheet is often the most important page of the paper.

### `pdf`

Use this skill for literature extraction, table extraction, PDF inspection, and final submission assembly. It can support both early research and late-stage compliance checks.

### `ai-report-writer`

Use this skill throughout the competition to record AI-tool interactions and generate the required AI-use report.

A complete AI-use report should include:

1. A summary of all AI tools used
2. Detailed records of LLM interactions
3. Translation-tool disclosure and proofreading notes
4. Code-assistance locations and verification notes
5. A formal integrity statement describing human supervision and responsibility

Record prompts, outputs, and verification notes as work happens. Reconstructing the report from memory at the end is risky and often incomplete.

---

## Typical Workflows

### Epidemic-control problem

1. Clean case data with `data-cleaner`.
2. Build an SIR-style model with `differential-equations`.
3. Fit infection or recovery parameters with `automated-sweep`.
4. Analyze parameter sensitivity with `sensitivity-master`.
5. Produce final figures with `visual-engineer`.

### Logistics or facility-location problem

1. Use `data-cleaner` and `shortest-path` to build a distance matrix.
2. Use `network-centrality` to identify candidate hubs.
3. Use `genetic-algorithm` or `integer-programming` for location optimization.
4. Use `topsis-scorer` to rank final alternatives.
5. Create a clear map or network diagram with `visual-engineer` or `web-artifacts-builder`.

### Policy-design problem

1. Use `pca-analyzer` to reduce correlated indicators.
2. Use `lstm-forecaster` or `arima-forecaster` to forecast key variables.
3. Use `multi-objective-optimization` to explore economic, social, and environmental trade-offs.
4. Use `pareto-frontier` and `robustness-check` to justify the final policy recommendation.

### Inverse material-wear problem

1. Clean observed scan or measurement data with `data-cleaner`.
2. Define the forward physical model.
3. Use `bayesian_inversion` to infer material parameters, traffic intensity, or service duration.
4. Report posterior intervals and convergence diagnostics.
5. Validate assumptions with `sensitivity-master`.

---

## Outstanding-Winner Checklist

- [ ] The model choice is justified using problem structure, data availability, and assumptions.
- [ ] Uncertainty is quantified with Monte Carlo simulation, confidence intervals, credible intervals, or Bayesian inference.
- [ ] Sensitivity analysis identifies the parameters that matter most.
- [ ] Robustness checks show how conclusions change under disturbed assumptions.
- [ ] Figures are publication-quality and directly support the paper's claims.
- [ ] Code is readable, modular, and reproducible.
- [ ] Any inverse problem reports posterior distributions or interval estimates, not only point estimates.
- [ ] The AI-use report is complete, specific, and consistent with COMAP requirements.
- [ ] All citations, AI-generated statements, and numerical results are verified by humans.
- [ ] The Summary Sheet states the core idea, the model pathway, and the final recommendation clearly.

---
