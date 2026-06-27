---
name: sensitivity-master
description: Advanced sensitivity analysis for MCM/ICM competitions using global methods (Sobol indices, Morris screening). Use when simple one-factor-at-a-time analysis is insufficient for complex/nonlinear models. Produces spider plots and Sobol index visualizations identifying key parameter drivers. Essential for O-prize level analysis.
---

# Sensitivity-Master

Perform rigorous sensitivity analysis using global methods to identify which parameters truly drive model behavior.

## When to Use

- Model has 5+ parameters
- Nonlinear relationships between inputs and outputs
- Parameter interactions suspected (one parameter's effect depends on another)
- Want to demonstrate O-prize level rigor
- Need to prioritize data collection efforts

## Local vs. Global Sensitivity

| Method | When to Use | Limitations |
|--------|-------------|-------------|
| **Local (OFAT)** | Linear models, initial screening | Misses interactions, point-specific |
| **Global (Sobol/Morris)** | Nonlinear models, comprehensive | Computationally expensive |

**Key insight**: Local methods test one parameter at a time around a baseline. Global methods explore the entire parameter space simultaneously.

## Method 1: Morris Screening (Fast)

**Purpose**: Quickly identify which parameters matter most (computational budget: 100-500 model runs)

### Implementation

```python
from SALib.sample import morris as morris_sample
from SALib.analyze import morris as morris_analyze
import numpy as np

# Step 1: Define problem
problem = {
    'num_vars': 6,
    'names': ['growth_rate', 'decay_factor', 'carrying_capacity', 
              'initial_population', 'migration_rate', 'harvest_rate'],
    'bounds': [[0.01, 0.10],   # growth_rate
               [0.80, 0.95],   # decay_factor
               [1000, 5000],   # carrying_capacity
               [100, 500],     # initial_population
               [0, 50],        # migration_rate
               [0, 0.2]]       # harvest_rate
}

# Step 2: Generate sample points
param_values = morris_sample.sample(
    problem, 
    N=100,           # Number of trajectories
    num_levels=4     # Grid resolution
)

# Step 3: Run model for each parameter set
outputs = np.zeros(len(param_values))

for i, params in enumerate(param_values):
    # Convert array to dict for your model
    param_dict = {
        name: params[j] 
        for j, name in enumerate(problem['names'])
    }
    
    # Run your model
    result = run_model(param_dict)
    outputs[i] = result['final_population']  # Extract metric of interest

# Step 4: Analyze sensitivity
Si = morris_analyze.analyze(
    problem, 
    param_values, 
    outputs,
    print_to_console=False
)

# Step 5: Visualize results
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

# Plot mu* (overall effect) vs sigma (interaction/nonlinearity)
ax.scatter(Si['mu_star'], Si['sigma'], s=100, alpha=0.6)

for i, name in enumerate(problem['names']):
    ax.annotate(name, 
                (Si['mu_star'][i], Si['sigma'][i]),
                xytext=(5, 5), textcoords='offset points',
                fontsize=10, fontweight='bold')

ax.set_xlabel('μ* (Overall Effect)', fontsize=12, fontweight='bold')
ax.set_ylabel('σ (Interaction/Nonlinearity)', fontsize=12, fontweight='bold')
ax.set_title('Morris Sensitivity Analysis', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

# Add interpretation zones
ax.axhline(Si['sigma'].mean(), color='red', linestyle='--', alpha=0.5)
ax.axvline(Si['mu_star'].mean(), color='red', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('results/morris_screening.png', dpi=300)
```

**Interpretation:**
- **High μ*, Low σ**: Linear, important parameter → Priority for calibration
- **High μ*, High σ**: Nonlinear or interactive → Needs careful study
- **Low μ*, Low σ**: Negligible effect → Can fix or ignore
- **Low μ*, High σ**: Complex interactions → Investigate further

## Method 2: Sobol Indices (Rigorous)

**Purpose**: Quantify exact contribution of each parameter and interactions (computational budget: 1000-10000 model runs)

### Implementation

```python
from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import multiprocessing as mp

# Step 1: Define problem (same as Morris)
problem = {
    'num_vars': 6,
    'names': ['growth_rate', 'decay_factor', 'carrying_capacity', 
              'initial_population', 'migration_rate', 'harvest_rate'],
    'bounds': [[0.01, 0.10], [0.80, 0.95], [1000, 5000],
               [100, 500], [0, 50], [0, 0.2]]
}

# Step 2: Generate Saltelli sample
# Sample size = N * (2D + 2) where D = num_vars
# For N=1000, D=6: 1000 * (12 + 2) = 14,000 model evaluations
param_values = saltelli.sample(problem, N=1000)

# Step 3: Parallel model evaluation (CRITICAL for large samples)
def evaluate_model(params):
    """Wrapper for parallel execution"""
    param_dict = {
        name: params[j] 
        for j, name in enumerate(problem['names'])
    }
    result = run_model(param_dict)
    return result['final_population']

# Run in parallel
with mp.Pool(processes=mp.cpu_count()) as pool:
    outputs = np.array(pool.map(evaluate_model, param_values))

# Step 4: Calculate Sobol indices
Si = sobol.analyze(problem, outputs, print_to_console=False)

# Extract indices
first_order = Si['S1']      # Main effect of each parameter alone
total_order = Si['ST']      # Total effect including interactions
second_order = Si['S2']     # Pairwise interactions

# Step 5: Visualize with bar chart
fig, ax = plt.subplots(figsize=(12, 7))

x = np.arange(len(problem['names']))
width = 0.35

bars1 = ax.bar(x - width/2, first_order, width, 
               label='First Order (S₁)', 
               color='steelblue', alpha=0.8)
bars2 = ax.bar(x + width/2, total_order, width, 
               label='Total Order (Sᴛ)', 
               color='coral', alpha=0.8)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom', fontsize=9)

ax.set_ylabel('Sobol Index', fontsize=12, fontweight='bold')
ax.set_title('Sobol Sensitivity Analysis\n(First Order vs Total Effect)', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(problem['names'], rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('results/sobol_indices.png', dpi=300)

# Step 6: Interaction analysis
if second_order is not None:
    # Visualize pairwise interactions with heatmap
    import seaborn as sns
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # S2 is upper triangular matrix
    interaction_matrix = np.zeros((len(problem['names']), len(problem['names'])))
    idx = 0
    for i in range(len(problem['names'])):
        for j in range(i+1, len(problem['names'])):
            interaction_matrix[i, j] = second_order[idx]
            interaction_matrix[j, i] = second_order[idx]  # Symmetric
            idx += 1
    
    sns.heatmap(interaction_matrix, 
                xticklabels=problem['names'],
                yticklabels=problem['names'],
                annot=True, fmt='.3f',
                cmap='YlOrRd', cbar_kws={'label': 'S₂ (Interaction)'},
                ax=ax)
    
    ax.set_title('Pairwise Parameter Interactions (S₂)', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('results/sobol_interactions.png', dpi=300)
```

**Interpretation:**
- **S₁ (First Order)**: Direct effect of parameter alone
- **Sᴛ (Total Order)**: Total effect including all interactions
- **Sᴛ - S₁**: Interaction effect (if large, parameter interacts with others)
- **S₂**: Pairwise interaction strength

**Key Insight**: If Σ(S₁) ≈ 1, model is additive (no interactions). If Σ(S₁) << 1, strong interactions exist.

## Method 3: Spider Plot (OFAT Visualization)

**Purpose**: Visual representation of local sensitivity for presentations

```python
def spider_plot(model_func, base_params, output_metric, 
                perturbation_range=(-0.2, 0.2, 5)):
    """
    Create spider/radar plot showing output response to each parameter
    """
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Perturbation levels
    perturbations = np.linspace(perturbation_range[0], 
                                perturbation_range[1], 
                                perturbation_range[2])
    
    baseline_output = output_metric(model_func(base_params))
    
    for param_name, base_value in base_params.items():
        outputs = []
        
        for pert in perturbations:
            params = base_params.copy()
            params[param_name] = base_value * (1 + pert)
            result = model_func(params)
            outputs.append(output_metric(result))
        
        # Normalize to percentage change
        normalized = [(o - baseline_output) / baseline_output * 100 
                      for o in outputs]
        
        ax.plot(perturbations * 100, normalized, 
                marker='o', linewidth=2, label=param_name)
    
    ax.axhline(0, color='black', linestyle='--', linewidth=1)
    ax.axvline(0, color='black', linestyle='--', linewidth=1)
    
    ax.set_xlabel('Parameter Change (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Output Change (%)', fontsize=12, fontweight='bold')
    ax.set_title('Spider Plot: Local Sensitivity Analysis', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/spider_plot.png', dpi=300)
```

## Decision Guide: Which Method?

| Scenario | Recommended Method |
|----------|-------------------|
| Quick screening (< 10 params) | Morris |
| Need exact quantification | Sobol |
| Presentation visual | Spider Plot |
| Very expensive model (< 100 runs) | Spider Plot only |
| Nonlinear model | Morris + Sobol |
| Linear model | Spider Plot sufficient |

## Computational Considerations

**Morris**: N × (D + 1) model runs
- Example: 100 trajectories × 7 parameters = 800 runs

**Sobol**: N × (2D + 2) model runs
- Example: 1000 samples × 14 = 14,000 runs

**Optimization strategies:**
1. Use Morris first to eliminate unimportant parameters
2. Run Sobol only on important parameters (reduces D)
3. Parallelize with `multiprocessing`
4. Use surrogate models (Gaussian Process) if model is very slow

## Output Requirements

### For Paper

Include:
1. **Method description**: "We performed global sensitivity analysis using Sobol indices..."
2. **Ranking table**: List parameters by importance (S₁ or μ*)
3. **Visualization**: Sobol bar chart OR Morris scatter plot
4. **Interpretation**: "Parameter X is the key driver, accounting for 45% of output variance"

### Files

Save to `results/sensitivity/`:
- `sobol_indices.png` or `morris_screening.png`
- `spider_plot.png` (for presentations)
- `sensitivity_indices.csv` (numerical results)
- `sobol_interactions.png` (if interactions are significant)

## Common Pitfalls

- **Too few samples**: Sobol needs N ≥ 1000 for reliable results
- **Wrong bounds**: Unrealistic parameter ranges distort importance
- **Single output**: Run analysis for multiple outputs if model has several
- **No validation**: Compare Sobol results with Morris for sanity check
- **Ignoring interactions**: If Sᴛ >> S₁, interactions are critical
