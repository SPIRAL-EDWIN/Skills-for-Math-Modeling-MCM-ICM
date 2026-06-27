---
name: pareto-frontier
description: Multi-objective optimization visualization for MCM/ICM competitions. Use when problems involve trade-offs (economic vs environmental, cost vs benefit, efficiency vs equity). Generates Pareto frontier plots showing non-dominated solution sets, demonstrating multiple optimal solutions for decision-maker preference.
---

# Pareto-Frontier

Visualize and analyze multi-objective optimization problems where trade-offs exist between competing goals.

## When to Use

- Problem explicitly involves trade-offs (e.g., "balance economic growth and environmental protection")
- Multiple stakeholders with conflicting interests
- No single "best" solution - optimal choice depends on priorities
- Want to demonstrate sophisticated understanding of optimization to judges

## Core Concept

**Pareto Optimality**: Solution A dominates solution B if A is better in at least one objective and no worse in all others. The Pareto frontier is the set of all non-dominated solutions.

```
Example: Maximize revenue, Minimize environmental damage
- Solution A: Revenue=$100k, Damage=10
- Solution B: Revenue=$80k, Damage=15
→ A dominates B (higher revenue, less damage)

- Solution C: Revenue=$120k, Damage=5
- Solution D: Revenue=$110k, Damage=8
→ Neither dominates (C has higher revenue but more damage)
→ Both are on Pareto frontier
```

## Implementation Methods

### Method 1: Weighted Sum (Simple)

For 2-3 objectives, systematically vary weights:

```python
import numpy as np
from scipy.optimize import minimize

def multi_objective(x, weights):
    """
    x: decision variables
    weights: [w1, w2] where w1 + w2 = 1
    """
    obj1 = calculate_revenue(x)      # Maximize (convert to minimize: -obj1)
    obj2 = calculate_damage(x)       # Minimize
    
    return -weights[0] * obj1 + weights[1] * obj2

# Generate Pareto frontier
pareto_solutions = []
weights_range = np.linspace(0, 1, 50)

for w1 in weights_range:
    w2 = 1 - w1
    result = minimize(
        multi_objective,
        x0=initial_guess,
        args=([w1, w2],),
        bounds=variable_bounds,
        method='SLSQP'
    )
    
    if result.success:
        obj1_val = calculate_revenue(result.x)
        obj2_val = calculate_damage(result.x)
        pareto_solutions.append({
            'revenue': obj1_val,
            'damage': obj2_val,
            'solution': result.x,
            'weight': w1
        })
```

### Method 2: NSGA-II (Advanced)

For complex problems or 3+ objectives:

```python
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.optimize import minimize as pymoo_minimize

class MultiObjectiveProblem(Problem):
    def __init__(self):
        super().__init__(
            n_var=5,           # Number of decision variables
            n_obj=2,           # Number of objectives
            n_constr=1,        # Number of constraints
            xl=np.array([0, 0, 0, 0, 0]),    # Lower bounds
            xu=np.array([10, 10, 10, 10, 10]) # Upper bounds
        )
    
    def _evaluate(self, x, out, *args, **kwargs):
        # Objective 1: Maximize revenue (minimize negative)
        f1 = -calculate_revenue(x)
        
        # Objective 2: Minimize environmental damage
        f2 = calculate_damage(x)
        
        # Constraint: Total budget <= 1000
        g1 = np.sum(x * costs) - 1000
        
        out["F"] = np.column_stack([f1, f2])
        out["G"] = g1

# Run optimization
problem = MultiObjectiveProblem()
algorithm = NSGA2(pop_size=100)

res = pymoo_minimize(
    problem,
    algorithm,
    ('n_gen', 200),
    verbose=True
)

# Extract Pareto frontier
pareto_front = res.F
pareto_solutions = res.X
```

### Method 3: Grid Search (Brute Force)

When optimization is fast, exhaustively explore:

```python
from itertools import product

# Define ranges for each decision variable
var1_range = np.linspace(0, 10, 30)
var2_range = np.linspace(0, 10, 30)
var3_range = np.linspace(0, 10, 30)

# Evaluate all combinations
all_solutions = []
for v1, v2, v3 in product(var1_range, var2_range, var3_range):
    x = np.array([v1, v2, v3])
    
    # Check constraints
    if not satisfies_constraints(x):
        continue
    
    obj1 = calculate_revenue(x)
    obj2 = calculate_damage(x)
    
    all_solutions.append({
        'revenue': obj1,
        'damage': obj2,
        'solution': x
    })

# Filter to Pareto frontier
pareto_solutions = filter_pareto_optimal(all_solutions)

def filter_pareto_optimal(solutions):
    """Keep only non-dominated solutions"""
    pareto = []
    for candidate in solutions:
        is_dominated = False
        for other in solutions:
            if (other['revenue'] >= candidate['revenue'] and 
                other['damage'] <= candidate['damage'] and
                (other['revenue'] > candidate['revenue'] or 
                 other['damage'] < candidate['damage'])):
                is_dominated = True
                break
        if not is_dominated:
            pareto.append(candidate)
    return pareto
```

## Visualization Requirements

### Standard 2D Pareto Plot

```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 7))

# Plot all feasible solutions (gray)
all_x = [s['revenue'] for s in all_solutions]
all_y = [s['damage'] for s in all_solutions]
ax.scatter(all_x, all_y, c='lightgray', s=20, alpha=0.3, 
           label='Feasible Solutions')

# Plot Pareto frontier (highlighted)
pareto_x = [s['revenue'] for s in pareto_solutions]
pareto_y = [s['damage'] for s in pareto_solutions]

# Sort for line connection
sorted_pareto = sorted(zip(pareto_x, pareto_y), key=lambda p: p[0])
pareto_x_sorted = [p[0] for p in sorted_pareto]
pareto_y_sorted = [p[1] for p in sorted_pareto]

ax.plot(pareto_x_sorted, pareto_y_sorted, 'r-', linewidth=2, 
        label='Pareto Frontier', zorder=3)
ax.scatter(pareto_x, pareto_y, c='red', s=100, marker='o', 
           edgecolors='darkred', linewidth=1.5, zorder=4)

# Annotate key points
max_revenue_sol = max(pareto_solutions, key=lambda s: s['revenue'])
min_damage_sol = min(pareto_solutions, key=lambda s: s['damage'])

ax.annotate('Max Revenue\n({:.1f}k, {:.1f})'.format(
    max_revenue_sol['revenue']/1000, max_revenue_sol['damage']),
    xy=(max_revenue_sol['revenue'], max_revenue_sol['damage']),
    xytext=(20, 20), textcoords='offset points',
    bbox=dict(boxstyle='round', fc='yellow', alpha=0.7),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

ax.annotate('Min Damage\n({:.1f}k, {:.1f})'.format(
    min_damage_sol['revenue']/1000, min_damage_sol['damage']),
    xy=(min_damage_sol['revenue'], min_damage_sol['damage']),
    xytext=(-80, -30), textcoords='offset points',
    bbox=dict(boxstyle='round', fc='lightgreen', alpha=0.7),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

ax.set_xlabel('Total Revenue ($1000s)', fontsize=12, fontweight='bold')
ax.set_ylabel('Environmental Damage Index', fontsize=12, fontweight='bold')
ax.set_title('Pareto Frontier: Revenue vs. Environmental Impact', 
             fontsize=14, fontweight='bold')
ax.legend(loc='best', fontsize=11)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/pareto_frontier.png', dpi=300)
```

### 3D Pareto Surface (for 3 objectives)

```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Plot Pareto surface
ax.scatter([s['obj1'] for s in pareto_solutions],
           [s['obj2'] for s in pareto_solutions],
           [s['obj3'] for s in pareto_solutions],
           c='red', s=50, marker='o', alpha=0.6)

ax.set_xlabel('Objective 1')
ax.set_ylabel('Objective 2')
ax.set_zlabel('Objective 3')
ax.set_title('3D Pareto Frontier')

plt.savefig('results/pareto_3d.png', dpi=300)
```

## Narrative for Paper

Include this type of explanation in your paper:

> We recognize that this problem involves inherent trade-offs between economic development and environmental preservation. Rather than imposing arbitrary weights, we present the **Pareto frontier** of optimal solutions (Figure X). Each point on this frontier represents a configuration where improving one objective necessarily worsens another.
>
> Decision-makers can select from this set based on their priorities:
> - **Point A** maximizes revenue ($XXX) at the cost of higher environmental impact (YY units)
> - **Point B** minimizes environmental damage (ZZ units) while maintaining acceptable revenue ($WWW)
> - **Point C** represents a balanced compromise
>
> We recommend Point C as it achieves 85% of maximum revenue while keeping environmental damage below the critical threshold of QQ units.

## Key Requirements

1. **Show both**: Plot all feasible solutions (gray) + Pareto frontier (colored)
2. **Annotate extremes**: Label max/min points for each objective
3. **Provide recommendations**: Suggest 2-3 specific solutions with rationale
4. **Verify non-dominance**: Ensure no frontier point dominates another
5. **Multiple objectives**: Must have at least 2 competing objectives

## Output Location

Save to `results/pareto_analysis/`:
- `pareto_frontier.png` - Main visualization
- `pareto_solutions.csv` - All Pareto-optimal solutions
- `recommended_solution.json` - Top 3 recommended configurations

## Common Pitfalls

- **Fake trade-off**: Both objectives move in same direction (not multi-objective)
- **Dominated solutions**: Frontier includes points that aren't truly optimal
- **No context**: Plot without explaining what solutions mean
- **Single solution**: Presenting one "optimal" solution defeats the purpose

---

## Related Skills

### Optimization Algorithms
- **multi-objective-optimization**: Advanced NSGA-II/III implementation for generating Pareto fronts (use this for complex problems with 3+ objectives or constraints)
- **genetic-algorithm**: Single-objective GA that can be extended to multi-objective with Pareto selection
- **particle-swarm**: Fast continuous optimization (can be adapted for multi-objective)
- **simulated-annealing**: Global search for multimodal problems

### Validation & Analysis
- **sensitivity-master**: Analyze which parameters most affect Pareto frontier shape
- **robustness-check**: Verify Pareto solutions are stable under uncertainty
- **automated-sweep**: Simple grid search for single-objective problems (upgrade to Pareto when trade-offs exist)

### Visualization
- **visual-engineer**: Generate publication-quality Pareto frontier plots
