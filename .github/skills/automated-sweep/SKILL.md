---
name: automated-sweep
description: Automated parameter sweeping and optimization for mathematical models in MCM/ICM competitions. Use when determining optimal model parameters (growth rates, coefficients, elasticity) through systematic exploration rather than manual assumption. Produces parameter heatmaps and optimal value identification with loss function evaluation.
---

# Automated-Sweep

Systematic parameter exploration for mathematical modeling competitions to identify optimal parameter values through automated sweeping rather than manual guessing.

## When to Use

- Determining optimal model parameters (growth rates, elasticity coefficients, etc.)
- When model has 1-3 key parameters that significantly affect results
- Need to validate parameter choices against historical data
- Want to demonstrate robustness of parameter selection to judges

## Workflow

### 1. Define Parameter Space

Identify parameters to sweep and establish reasonable bounds:

```python
# Define parameter ranges based on literature or data
parameters = {
    'growth_rate': (0.01, 0.10, 20),  # (min, max, steps)
    'decay_factor': (0.5, 0.95, 15),
    'elasticity': (0.1, 2.0, 20)
}
```

Base ranges on:
- Literature values from Phase 2 research
- Physical constraints (e.g., probabilities must be 0-1)
- Data-driven bounds (e.g., ±50% of observed values)

### 2. Implement Loss Function

Define metric to evaluate parameter quality:

```python
def loss_function(params, historical_data):
    """
    Calculate model error against historical data
    
    Returns: float (lower is better)
    Common choices:
    - RMSE: np.sqrt(np.mean((predicted - actual)**2))
    - MAE: np.mean(np.abs(predicted - actual))
    - R²: 1 - (SS_res / SS_tot)
    - Custom: weighted combination of metrics
    """
    predictions = run_model(params)
    return np.sqrt(np.mean((predictions - historical_data)**2))
```

### 3. Execute Sweep

**Single parameter (1D):**
```python
results = []
for value in np.linspace(min_val, max_val, steps):
    loss = loss_function({'param': value}, data)
    results.append((value, loss))

# Plot loss curve
plt.plot([r[0] for r in results], [r[1] for r in results])
plt.xlabel('Parameter Value')
plt.ylabel('Loss (RMSE)')
```

**Two parameters (2D heatmap):**
```python
from itertools import product
import multiprocessing as mp

def evaluate(params):
    return loss_function(params, historical_data)

# Generate parameter grid
p1_vals = np.linspace(p1_min, p1_max, 20)
p2_vals = np.linspace(p2_min, p2_max, 20)
param_grid = [{'p1': p1, 'p2': p2} 
              for p1, p2 in product(p1_vals, p2_vals)]

# Parallel evaluation
with mp.Pool() as pool:
    losses = pool.map(evaluate, param_grid)

# Reshape for heatmap
loss_matrix = np.array(losses).reshape(len(p1_vals), len(p2_vals))
```

**Three+ parameters (Latin Hypercube Sampling):**
```python
from scipy.stats import qmc

# Generate efficient sample points
sampler = qmc.LatinHypercube(d=3)  # 3 dimensions
sample = sampler.random(n=500)

# Scale to parameter bounds
scaled_sample = qmc.scale(sample, 
                          [p1_min, p2_min, p3_min],
                          [p1_max, p2_max, p3_max])
```

### 4. Visualization Requirements

**For 1D sweep:**
- Line plot: Parameter value vs. Loss
- Mark optimal value with vertical line
- Annotate: "Optimal: {value:.3f} (RMSE: {loss:.4f})"

**For 2D sweep (REQUIRED for O-prize level):**
```python
import seaborn as sns

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(loss_matrix, 
            xticklabels=np.round(p2_vals, 2),
            yticklabels=np.round(p1_vals, 2),
            cmap='viridis_r',  # Reverse so dark = better
            cbar_kws={'label': 'Loss (RMSE)'},
            ax=ax)

# Mark optimal point
opt_idx = np.unravel_index(loss_matrix.argmin(), loss_matrix.shape)
ax.plot(opt_idx[1], opt_idx[0], 'r*', markersize=20, 
        label=f'Optimal: ({p1_vals[opt_idx[0]]:.2f}, {p2_vals[opt_idx[1]]:.2f})')

ax.set_xlabel('Parameter 2')
ax.set_ylabel('Parameter 1')
ax.set_title('Parameter Sweep Results')
plt.legend()
plt.tight_layout()
plt.savefig('results/param_sweep.png', dpi=300)
```

### 5. Report Optimal Parameters

```python
# Find best parameters
best_idx = np.argmin(losses)
best_params = param_grid[best_idx]
best_loss = losses[best_idx]

print(f"Optimal Parameters:")
for name, value in best_params.items():
    print(f"  {name}: {value:.4f}")
print(f"Loss (RMSE): {best_loss:.4f}")
```

## Key Requirements

1. **Justify bounds**: Document why parameter ranges were chosen
2. **Loss function**: Must compare against historical/validation data
3. **Visualization**: Heatmap for 2D, annotated plot for 1D
4. **Robustness**: Show that optimal region is stable (not single sharp peak)
5. **Computation**: Use `multiprocessing` for >100 evaluations

## Output Location

Save results to `results/parameter_sweep/`:
- `heatmap.png` - Parameter space visualization
- `optimal_params.json` - Best parameter values
- `sweep_log.csv` - Full sweep results for reference

## Common Pitfalls

- **Too coarse grid**: Use at least 15-20 steps per dimension
- **Wrong loss metric**: RMSE for continuous, accuracy for classification
- **No validation**: Must test against data not used in sweep
- **Single run**: For stochastic models, average over multiple runs

---

## Related Skills

### When to Upgrade to Advanced Optimization
- **genetic-algorithm**: Use when discrete/combinatorial parameters (e.g., facility locations, schedules)
- **simulated-annealing**: Use when many local optima exist (multimodal objective)
- **particle-swarm**: Use for smooth continuous optimization with faster convergence than grid search
- **multi-objective-optimization**: Upgrade when problem has multiple conflicting objectives

### Validation & Analysis
- **sensitivity-master**: After finding optimal parameters, analyze their sensitivity (Sobol indices)
- **robustness-check**: Verify optimal parameters are stable (tornado diagram)
- **monte-carlo-engine**: Quantify uncertainty in predictions using optimal parameters

### Complementary Skills
- **pareto-frontier**: Visualize trade-offs if multiple objectives exist
- **visual-engineer**: Generate publication-quality heatmaps and convergence plots
