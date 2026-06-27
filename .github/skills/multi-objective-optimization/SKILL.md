---
name: multi-objective-optimization
description: Comprehensive multi-objective optimization framework for MCM/ICM. Handles 2-10+ conflicting objectives using NSGA-II/III, MOEA/D, weighted sum methods. Generates Pareto frontiers, computes quality metrics (hypervolume, spacing), and integrates with TOPSIS for decision support. Essential for trade-off analysis in policy, engineering, and resource allocation problems.
---

# Multi-Objective Optimization (MOO)

A unified framework for solving optimization problems with multiple conflicting objectives, finding Pareto-optimal solutions, and supporting decision-making under trade-offs.

## When to Use

- **Conflicting Objectives**: Maximize profit AND minimize cost (impossible to optimize both simultaneously).
- **Trade-off Analysis**: Economic growth vs. environmental protection, efficiency vs. equity.
- **Stakeholder Conflicts**: Different groups prioritize different objectives.
- **Policy Design**: Need to present multiple options for decision-makers.
- **No Single "Best"**: Optimal solution depends on subjective preferences.

## When NOT to Use

- **Single Objective**: Use standard optimization (**`automated-sweep`**).
- **Objectives Align**: Both can be improved together (not truly multi-objective).
- **Lexicographic Priorities**: One objective strictly dominates others (use hierarchical optimization).

## Core Concepts

### Pareto Dominance
Solution $A$ **dominates** solution $B$ if:
1. $A$ is **no worse** than $B$ in all objectives.
2. $A$ is **strictly better** than $B$ in at least one objective.

### Pareto Frontier (Pareto Front)
The set of all **non-dominated** solutions. No solution on the frontier can improve one objective without worsening another.

```
Example: Maximize Revenue (f1), Minimize Pollution (f2)
┌─────────────────────────────────────┐
│   Pollution (f2) ↓                  │
│   │                                 │
│ 20│  ●  Dominated solutions         │
│   │     ●                           │
│ 15│        ● ●                      │
│   │          ● ●                    │
│ 10│   Pareto → ◆─◆─◆─◆ ← Frontier  │
│   │              ●                  │
│  5│                ●                │
│   └─────────────────────────────►  │
│     50   100  150  200  Revenue    │
└─────────────────────────────────────┘
```

## Algorithm Library

### 1. NSGA-II (Recommended for 2-3 objectives)

**Non-dominated Sorting Genetic Algorithm II** - Industry standard for MOO.

```python
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
import numpy as np

class CustomMOOProblem(Problem):
    """
    Define your multi-objective problem
    """
    def __init__(self, n_var=5, n_obj=2, n_constr=0):
        super().__init__(
            n_var=n_var,
            n_obj=n_obj,
            n_constr=n_constr,
            xl=np.array([0] * n_var),  # Lower bounds
            xu=np.array([10] * n_var)  # Upper bounds
        )
    
    def _evaluate(self, X, out, *args, **kwargs):
        """
        X: Decision variables (n_samples, n_var)
        out["F"]: Objectives to MINIMIZE (n_samples, n_obj)
        out["G"]: Constraints g(x) <= 0 (n_samples, n_constr)
        """
        # Example: Two objectives
        f1 = np.sum(X**2, axis=1)  # Minimize sum of squares
        f2 = np.sum((X - 5)**2, axis=1)  # Minimize distance from 5
        
        out["F"] = np.column_stack([f1, f2])
        
        # Optional: Add constraints
        # g1 = np.sum(X, axis=1) - 20  # Sum <= 20
        # out["G"] = g1

# Run NSGA-II
problem = CustomMOOProblem(n_var=5, n_obj=2)
algorithm = NSGA2(
    pop_size=100,      # Population size
    eliminate_duplicates=True
)

res = minimize(
    problem,
    algorithm,
    ('n_gen', 200),    # Number of generations
    seed=42,
    verbose=False
)

# Extract Pareto frontier
pareto_front = res.F  # Objective values (n_solutions, n_obj)
pareto_solutions = res.X  # Decision variables (n_solutions, n_var)

print(f"Found {len(pareto_front)} Pareto-optimal solutions")
```

### 2. NSGA-III (For 4+ objectives)

**NSGA-III** handles many-objective problems better than NSGA-II.

```python
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.util.ref_dirs import get_reference_directions

# Generate reference directions for many objectives
ref_dirs = get_reference_directions("das-dennis", n_dim=4, n_partitions=12)

algorithm = NSGA3(
    ref_dirs=ref_dirs,
    pop_size=100
)

# Use same problem definition and minimize() call
```

### 3. MOEA/D (Decomposition-based)

**Multi-Objective Evolutionary Algorithm based on Decomposition** - Fast for 2-3 objectives.

```python
from pymoo.algorithms.moo.moead import MOEAD

algorithm = MOEAD(
    ref_dirs=get_reference_directions("uniform", n_dim=2, n_points=100),
    n_neighbors=15,
    prob_neighbor_mating=0.7
)
```

### 4. Weighted Sum Method (Simple, for 2 objectives)

Convert multi-objective to single-objective using weights.

```python
from scipy.optimize import minimize as scipy_minimize

def weighted_objective(x, weights):
    """
    weights: [w1, w2, ...] where sum(weights) = 1
    """
    # Calculate objectives (convert maximize to minimize with negative)
    f1 = -calculate_revenue(x)  # Maximize revenue
    f2 = calculate_pollution(x)  # Minimize pollution
    
    return weights[0] * f1 + weights[1] * f2

# Sweep over different weights
pareto_solutions = []
weights_range = np.linspace(0, 1, 50)

for w1 in weights_range:
    w2 = 1 - w1
    
    result = scipy_minimize(
        weighted_objective,
        x0=np.array([5, 5, 5]),
        args=([w1, w2],),
        bounds=[(0, 10)] * 3,
        method='SLSQP'
    )
    
    if result.success:
        f1_val = -result.fun * w1 / (w1 if w1 > 0 else 1e-9)
        f2_val = result.fun * w2 / (w2 if w2 > 0 else 1e-9)
        
        pareto_solutions.append({
            'x': result.x,
            'f1': f1_val,
            'f2': f2_val,
            'weight': w1
        })
```

**Limitation**: Cannot find non-convex parts of Pareto frontier.

### 5. ε-Constraint Method (Guaranteed complete frontier)

Fix all but one objective as constraints, sweep constraint values.

```python
def epsilon_constraint_method(objective_to_optimize, constraint_objectives, 
                              epsilon_ranges):
    """
    objective_to_optimize: Index of objective to minimize (e.g., 0)
    constraint_objectives: Indices of objectives to constrain (e.g., [1, 2])
    epsilon_ranges: List of arrays for each constraint
    """
    pareto_solutions = []
    
    for epsilons in itertools.product(*epsilon_ranges):
        # Define problem with constraints
        def objective(x):
            return calculate_objective(x, objective_to_optimize)
        
        def constraints(x):
            return [
                calculate_objective(x, i) - epsilons[j]
                for j, i in enumerate(constraint_objectives)
            ]
        
        # Solve
        result = scipy_minimize(
            objective, x0, 
            constraints={'type': 'ineq', 'fun': constraints},
            bounds=bounds
        )
        
        if result.success:
            pareto_solutions.append(result.x)
    
    return pareto_solutions
```

## Quality Metrics

### Hypervolume (HV)
Volume of objective space dominated by the Pareto set. **Higher is better.**

```python
from pymoo.indicators.hv import HV

# Define reference point (nadir point, worst values)
ref_point = np.array([1.0, 1.0])  # For normalized objectives

# Calculate hypervolume
ind = HV(ref_point=ref_point)
hv_value = ind(pareto_front)

print(f"Hypervolume: {hv_value:.4f}")
```

### Spacing (SP)
Uniformity of solution distribution. **Lower is better** (0 = perfectly uniform).

```python
def spacing_metric(pareto_front):
    """
    Measure uniformity of Pareto front distribution
    """
    n = len(pareto_front)
    if n < 2:
        return 0
    
    # Calculate distances to nearest neighbor
    distances = []
    for i in range(n):
        min_dist = np.inf
        for j in range(n):
            if i != j:
                dist = np.linalg.norm(pareto_front[i] - pareto_front[j])
                min_dist = min(min_dist, dist)
        distances.append(min_dist)
    
    # Spacing metric
    d_mean = np.mean(distances)
    sp = np.sqrt(np.sum((distances - d_mean)**2) / n)
    
    return sp
```

### Spread (Δ)
Extent of coverage along Pareto front. **Lower is better** (0 = full coverage).

```python
from pymoo.indicators.igd import IGD

# Requires true Pareto front (or approximation)
ind = IGD(true_pareto_front)
igd_value = ind(pareto_front)
```

## Visualization

### 2D Pareto Frontier (Standard)

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_pareto_2d(all_solutions, pareto_solutions, 
                   obj_names=['Objective 1', 'Objective 2'],
                   title='Pareto Frontier'):
    """
    all_solutions: List of dicts with 'f1', 'f2' keys
    pareto_solutions: Subset that are Pareto-optimal
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # All feasible solutions (background)
    all_f1 = [s['f1'] for s in all_solutions]
    all_f2 = [s['f2'] for s in all_solutions]
    ax.scatter(all_f1, all_f2, c='lightgray', s=20, alpha=0.3, 
               label='Feasible Solutions', zorder=1)
    
    # Pareto frontier
    pareto_f1 = [s['f1'] for s in pareto_solutions]
    pareto_f2 = [s['f2'] for s in pareto_solutions]
    
    # Sort for line connection
    sorted_pareto = sorted(zip(pareto_f1, pareto_f2))
    pf1_sorted = [p[0] for p in sorted_pareto]
    pf2_sorted = [p[1] for p in sorted_pareto]
    
    ax.plot(pf1_sorted, pf2_sorted, 'r-', linewidth=2.5, 
            label='Pareto Frontier', zorder=3)
    ax.scatter(pareto_f1, pareto_f2, c='red', s=100, 
               edgecolors='darkred', linewidth=2, zorder=4,
               label='Pareto-Optimal Solutions')
    
    # Annotate extremes
    max_f1_sol = max(pareto_solutions, key=lambda s: s['f1'])
    min_f2_sol = min(pareto_solutions, key=lambda s: s['f2'])
    
    ax.annotate(f'Max {obj_names[0]}\n({max_f1_sol["f1"]:.1f}, {max_f1_sol["f2"]:.1f})',
                xy=(max_f1_sol['f1'], max_f1_sol['f2']),
                xytext=(20, 20), textcoords='offset points',
                bbox=dict(boxstyle='round', fc='yellow', alpha=0.8),
                arrowprops=dict(arrowstyle='->', lw=1.5))
    
    ax.annotate(f'Min {obj_names[1]}\n({min_f2_sol["f1"]:.1f}, {min_f2_sol["f2"]:.1f})',
                xy=(min_f2_sol['f1'], min_f2_sol['f2']),
                xytext=(-80, -30), textcoords='offset points',
                bbox=dict(boxstyle='round', fc='lightgreen', alpha=0.8),
                arrowprops=dict(arrowstyle='->', lw=1.5))
    
    ax.set_xlabel(obj_names[0], fontsize=12, fontweight='bold')
    ax.set_ylabel(obj_names[1], fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/pareto_analysis/pareto_frontier_2d.png', dpi=300)
    plt.show()
```

### 3D Pareto Surface

```python
from mpl_toolkits.mplot3d import Axes3D

def plot_pareto_3d(pareto_front, obj_names=['Obj 1', 'Obj 2', 'Obj 3']):
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(pareto_front[:, 0], pareto_front[:, 1], pareto_front[:, 2],
               c=pareto_front[:, 0], cmap='viridis', s=50, alpha=0.8)
    
    ax.set_xlabel(obj_names[0], fontsize=11)
    ax.set_ylabel(obj_names[1], fontsize=11)
    ax.set_zlabel(obj_names[2], fontsize=11)
    ax.set_title('3D Pareto Frontier', fontsize=14, fontweight='bold')
    
    plt.savefig('results/pareto_analysis/pareto_frontier_3d.png', dpi=300)
    plt.show()
```

### Parallel Coordinates (For 4+ objectives)

```python
from pandas.plotting import parallel_coordinates

def plot_parallel_coordinates(pareto_solutions, obj_names):
    """
    pareto_solutions: DataFrame with columns for each objective
    """
    import pandas as pd
    
    df = pd.DataFrame(pareto_solutions, columns=obj_names)
    df['Solution'] = range(len(df))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    parallel_coordinates(df, 'Solution', colormap='viridis', ax=ax)
    
    ax.set_title('Pareto Solutions (Parallel Coordinates)', 
                 fontsize=14, fontweight='bold')
    ax.legend().remove()
    plt.tight_layout()
    plt.savefig('results/pareto_analysis/parallel_coordinates.png', dpi=300)
    plt.show()
```

## Decision Support Integration

### TOPSIS for Pareto Solution Selection

After finding Pareto frontier, use **TOPSIS** to rank solutions based on decision-maker preferences.

```python
# Assume pareto_front is (n_solutions, n_objectives) array

# Step 1: Define weights (can use entropy-weight-method or ahp-method)
from entropy_weight_method import entropy_weight_method
weights, _ = entropy_weight_method(pd.DataFrame(pareto_front), 
                                   negative_indicators=[1])  # Obj 2 is cost

# Step 2: Apply TOPSIS
from topsis_scorer import topsis_scorer
results = topsis_scorer(pd.DataFrame(pareto_front), weights, 
                       negative_indicators=[1])

# Step 3: Recommend top solutions
top_3 = results.nsmallest(3, 'Rank')
print("Recommended Solutions:")
print(top_3[['TOPSIS_Score', 'Rank']])
```

## Integration Workflow

### Complete MOO Pipeline

```python
# Step 1: Data preparation
from data_cleaner import clean_data
data = clean_data('input_data.csv')

# Step 2: Define problem
problem = CustomMOOProblem(n_var=10, n_obj=2)

# Step 3: Run optimization
from multi_objective_optimization import run_nsga2
pareto_front, pareto_solutions = run_nsga2(problem, n_gen=200)

# Step 4: Quality metrics
hv = calculate_hypervolume(pareto_front)
sp = spacing_metric(pareto_front)
print(f"Hypervolume: {hv:.4f}, Spacing: {sp:.4f}")

# Step 5: Sensitivity analysis
from sensitivity_master import sobol_analyze
# Analyze how problem parameters affect Pareto front

# Step 6: Visualization
plot_pareto_2d(all_solutions, pareto_solutions)

# Step 7: Decision support
from topsis_scorer import topsis_scorer
ranked_solutions = topsis_scorer(pareto_front, weights)

# Step 8: Robustness check
from robustness_check import test_robustness
# Perturb parameters, verify Pareto front stability
```

## Common Pitfalls

1.  **Fake Trade-off**: Both objectives improve together (check correlation).
2.  **Dominated Solutions in Frontier**: Verify non-dominance with `is_pareto_optimal()` function.
3.  **Poor Convergence**: Increase `n_gen` or `pop_size` in evolutionary algorithms.
4.  **Ignoring Constraints**: Always include feasibility checks.
5.  **Single Solution**: Presenting one "optimal" defeats the purpose of MOO.
6.  **No Normalization**: Objectives with different scales need normalization.

## Output Requirements for Paper

1.  **Problem Formulation**:
    $$\begin{aligned}
    \text{minimize} \quad & f_1(x), f_2(x), \ldots, f_k(x) \\
    \text{subject to} \quad & g_i(x) \leq 0, \quad i = 1, \ldots, m \\
    & h_j(x) = 0, \quad j = 1, \ldots, p \\
    & x \in \mathbb{R}^n
    \end{aligned}$$

2.  **Algorithm Specification**: "We used NSGA-II with population size 100, 200 generations."

3.  **Pareto Frontier Plot**: Show all feasible + Pareto-optimal solutions.

4.  **Quality Metrics**: "Hypervolume = 0.85, Spacing = 0.03 (uniform distribution)."

5.  **Decision Analysis**: "We recommend Solution C, which achieves 90% of max revenue while keeping pollution below threshold."

6.  **Comparison Table**:
    | Solution | Revenue ($k) | Pollution | Employment | Score (TOPSIS) |
    |----------|-------------|-----------|------------|----------------|
    | A | 500 | 20 | 1000 | 0.85 |
    | B | 450 | 15 | 1200 | 0.92 |
    | C | 480 | 12 | 1100 | **0.95** |

## Advanced Topics

### Constraint Handling

```python
# Penalty method
def penalized_objective(x, penalty_factor=1000):
    f = original_objective(x)
    violation = max(0, constraint(x))  # g(x) <= 0
    return f + penalty_factor * violation**2
```

### Dynamic Weights (Interactive MOO)

```python
# Allow decision-maker to adjust weights iteratively
weights = ask_decision_maker()  # Interactive input
re-optimize with new weights
```

### Robust Pareto Frontier

```python
# Use monte-carlo-engine to propagate uncertainty
from monte_carlo_engine import run_monte_carlo

uncertain_params = {'demand': (100, 120), 'cost': (10, 15)}
robust_pareto = []

for _ in range(1000):
    sampled_params = sample(uncertain_params)
    pf = solve_moo(sampled_params)
    robust_pareto.append(pf)

# Find solutions that appear in most samples
```

## Decision Guide: Algorithm Selection

| Scenario | Algorithm | Reason |
|----------|-----------|--------|
| 2-3 objectives, smooth | NSGA-II | Industry standard, reliable |
| 4-10 objectives | NSGA-III | Designed for many objectives |
| Fast convergence needed | MOEA/D | Decomposition is efficient |
| Non-convex frontier | NSGA-II or ε-constraint | Weighted sum fails here |
| Simple problem, 2 objectives | Weighted sum | Fast, interpretable |
| Guaranteed complete frontier | ε-Constraint | Systematic, no gaps |

## Integration with Single-Objective Metaheuristics

### NSGA-II as Multi-Objective Genetic Algorithm

**NSGA-II is essentially GA + Multi-Objective Selection**:

```python
# Single-objective GA (genetic-algorithm skill)
from genetic_algorithm import GeneticAlgorithm
ga = GeneticAlgorithm(objective, bounds, pop_size=50)
result = ga.optimize(n_generations=100)

# Multi-objective NSGA-II (this skill)
# Uses GA's operators + non-dominated sorting + crowding distance
from pymoo.algorithms.moo.nsga2 import NSGA2
algorithm = NSGA2(pop_size=100)
res = minimize(problem, algorithm, ('n_gen', 200))
```

**Key Differences**:
| Component | GA (Single-Objective) | NSGA-II (Multi-Objective) |
|-----------|----------------------|---------------------------|
| **Selection** | Tournament (fitness-based) | Non-dominated sorting |
| **Diversity** | Mutation | Crowding distance |
| **Output** | Single best solution | Pareto frontier (set of solutions) |

### When to Upgrade from Single to Multi-Objective

```
Problem Evolution:
1. Start: "Minimize cost"
   → Use genetic-algorithm, simulated-annealing, or particle-swarm

2. Realization: "But we also care about quality"
   → Upgrade to multi-objective-optimization (NSGA-II)

3. Decision: "Which solution to implement?"
   → Use topsis-scorer with entropy-weight-method
```

### Connection Table

| Single-Objective Skill | Multi-Objective Extension | Relationship |
|------------------------|---------------------------|--------------|
| **`genetic-algorithm`** | NSGA-II, NSGA-III | GA with Pareto ranking |
| **`particle-swarm`** | MOPSO | PSO with archive + crowding |
| **`simulated-annealing`** | MOEA/D | Decomposition + SA acceptance |

## Summary: Skill Integration

This **`multi-objective-optimization`** skill:
1.  **Extends** the existing **`pareto-frontier`** skill with more algorithms and metrics.
2.  **Builds upon** single-objective metaheuristics:
    *   **`genetic-algorithm`** → NSGA-II/III
    *   **`particle-swarm`** → MOPSO (if implemented)
    *   **`simulated-annealing`** → MOEA/D (decomposition-based)
3.  **Integrates** with **`topsis-scorer`**, **`entropy-weight-method`**, **`ahp-method`** for decision support.
4.  **Connects** to **`sensitivity-master`** for robustness analysis.
5.  **Uses** **`visual-engineer`** for publication-quality plots.
6.  **Complements** **`automated-sweep`** (single-objective) and **`differential-equations`** (constrained dynamics).

**When to use each:**
- **Single objective**: Use **`genetic-algorithm`**, **`simulated-annealing`**, or **`particle-swarm`**
- **Quick multi-objective visualization**: Use **`pareto-frontier`** directly (simpler templates)
- **Advanced multi-objective analysis**: Use **`multi-objective-optimization`** (full framework)
- **Decision support**: Combine MOO + TOPSIS + sensitivity analysis
