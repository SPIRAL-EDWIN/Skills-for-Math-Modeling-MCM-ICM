---
name: robustness-check
description: Model robustness and stability analysis for MCM/ICM competitions. Use to demonstrate that model results are reliable and don't collapse with small parameter changes. Produces tornado diagrams for sensitivity ranking and phase plane plots for dynamical system stability. Essential for convincing judges of model reliability.
---

# Robustness-Check

Validate model reliability by testing stability under parameter perturbations and analyzing system equilibrium behavior.

## When to Use

- After implementing core model, before finalizing results
- When model has multiple uncertain parameters
- For dynamical systems (differential equations, iterative maps)
- To demonstrate model quality to judges
- When results seem "too perfect" and need validation

## Core Techniques

### 1. Tornado Diagram (Parameter Sensitivity Ranking)

Shows which parameters have the largest impact on output.

**Workflow:**

```python
import numpy as np
import matplotlib.pyplot as plt

def tornado_analysis(model_func, base_params, output_metric, 
                     perturbation=0.2):
    """
    model_func: function that takes params dict and returns results
    base_params: dict of parameter names and baseline values
    output_metric: function to extract key metric from results
    perturbation: fractional change (0.2 = ±20%)
    """
    
    baseline_result = model_func(base_params)
    baseline_output = output_metric(baseline_result)
    
    sensitivities = []
    
    for param_name, base_value in base_params.items():
        # Test low value
        params_low = base_params.copy()
        params_low[param_name] = base_value * (1 - perturbation)
        result_low = model_func(params_low)
        output_low = output_metric(result_low)
        
        # Test high value
        params_high = base_params.copy()
        params_high[param_name] = base_value * (1 + perturbation)
        result_high = model_func(params_high)
        output_high = output_metric(result_high)
        
        # Calculate sensitivity range
        sensitivity_range = abs(output_high - output_low)
        
        sensitivities.append({
            'parameter': param_name,
            'baseline': baseline_output,
            'low': output_low,
            'high': output_high,
            'range': sensitivity_range
        })
    
    # Sort by sensitivity (largest impact first)
    sensitivities.sort(key=lambda x: x['range'], reverse=True)
    
    return sensitivities

# Visualization
def plot_tornado(sensitivities, output_name='Output Metric'):
    """Create tornado diagram"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    params = [s['parameter'] for s in sensitivities]
    baseline = sensitivities[0]['baseline']
    
    y_pos = np.arange(len(params))
    
    for i, s in enumerate(sensitivities):
        # Calculate bar widths (deviation from baseline)
        left_width = s['low'] - baseline
        right_width = s['high'] - baseline
        
        # Draw bars
        ax.barh(i, left_width, left=baseline, height=0.8, 
                color='steelblue', alpha=0.7)
        ax.barh(i, right_width, left=baseline, height=0.8, 
                color='coral', alpha=0.7)
        
        # Add value labels
        ax.text(s['low'], i, f"{s['low']:.2f}", 
                ha='right', va='center', fontsize=9)
        ax.text(s['high'], i, f"{s['high']:.2f}", 
                ha='left', va='center', fontsize=9)
    
    # Baseline line
    ax.axvline(baseline, color='black', linestyle='--', linewidth=2,
               label=f'Baseline: {baseline:.2f}')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(params)
    ax.set_xlabel(output_name, fontsize=12, fontweight='bold')
    ax.set_title('Tornado Diagram: Parameter Sensitivity Analysis\n(±20% variation)',
                 fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/tornado_diagram.png', dpi=300)
    
    return fig
```

**Usage Example:**

```python
# Define your model
def run_model(params):
    # Model simulation code
    revenue = params['price'] * params['demand'] * (1 - params['cost_ratio'])
    return {'revenue': revenue, 'profit': revenue * 0.2}

def extract_revenue(results):
    return results['revenue']

# Run analysis
base_params = {
    'price': 100,
    'demand': 1000,
    'cost_ratio': 0.6,
    'growth_rate': 0.05,
    'elasticity': 1.2
}

sensitivities = tornado_analysis(
    run_model, 
    base_params, 
    extract_revenue,
    perturbation=0.2
)

plot_tornado(sensitivities, output_name='Annual Revenue ($)')
```

### 2. Phase Plane Analysis (Dynamical Systems)

For systems with differential equations, analyze stability of equilibrium points.

**Applicable to:**
- Predator-prey models
- SIR/SEIR epidemic models
- Population dynamics
- Economic growth models

**Workflow:**

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def phase_plane_analysis(system_func, x_range, y_range, 
                         equilibria=None, n_trajectories=15):
    """
    system_func: function(state, t) returning [dx/dt, dy/dt]
    x_range: (min, max) for first variable
    y_range: (min, max) for second variable
    equilibria: list of (x, y) equilibrium points
    """
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create grid for vector field
    x = np.linspace(x_range[0], x_range[1], 20)
    y = np.linspace(y_range[0], y_range[1], 20)
    X, Y = np.meshgrid(x, y)
    
    # Calculate vector field
    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            derivatives = system_func([X[i,j], Y[i,j]], 0)
            U[i,j] = derivatives[0]
            V[i,j] = derivatives[1]
    
    # Normalize for better visualization
    M = np.hypot(U, V)
    M[M == 0] = 1  # Avoid division by zero
    U_norm = U / M
    V_norm = V / M
    
    # Plot vector field
    ax.quiver(X, Y, U_norm, V_norm, M, cmap='viridis', 
              alpha=0.6, scale=30)
    
    # Plot trajectories
    t = np.linspace(0, 50, 500)
    
    for _ in range(n_trajectories):
        # Random initial condition
        x0 = np.random.uniform(x_range[0], x_range[1])
        y0 = np.random.uniform(y_range[0], y_range[1])
        
        # Integrate ODE
        trajectory = odeint(system_func, [x0, y0], t)
        
        ax.plot(trajectory[:, 0], trajectory[:, 1], 
                'b-', alpha=0.4, linewidth=1.5)
        ax.plot(x0, y0, 'go', markersize=5)  # Starting point
    
    # Mark equilibrium points
    if equilibria:
        for eq in equilibria:
            ax.plot(eq[0], eq[1], 'r*', markersize=20, 
                   markeredgecolor='darkred', markeredgewidth=1.5,
                   label='Equilibrium' if eq == equilibria[0] else '')
    
    ax.set_xlabel('Variable X', fontsize=12, fontweight='bold')
    ax.set_ylabel('Variable Y', fontsize=12, fontweight='bold')
    ax.set_title('Phase Plane Analysis', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/phase_plane.png', dpi=300)
    
    return fig
```

**Example: Predator-Prey Model**

```python
def lotka_volterra(state, t, alpha=1.0, beta=0.1, delta=0.075, gamma=1.5):
    """
    Predator-prey dynamics
    x: prey population
    y: predator population
    """
    x, y = state
    dx_dt = alpha * x - beta * x * y
    dy_dt = delta * x * y - gamma * y
    return [dx_dt, dy_dt]

# Find equilibrium analytically
# dx/dt = 0: x(alpha - beta*y) = 0 → x=0 or y=alpha/beta
# dy/dt = 0: y(delta*x - gamma) = 0 → y=0 or x=gamma/delta
alpha, beta, delta, gamma = 1.0, 0.1, 0.075, 1.5
equilibria = [
    (0, 0),  # Trivial equilibrium
    (gamma/delta, alpha/beta)  # Coexistence equilibrium
]

phase_plane_analysis(
    lambda state, t: lotka_volterra(state, t, alpha, beta, delta, gamma),
    x_range=(0, 30),
    y_range=(0, 20),
    equilibria=equilibria,
    n_trajectories=20
)
```

### 3. Monte Carlo Robustness Test

Test stability under simultaneous random perturbations:

```python
def monte_carlo_robustness(model_func, base_params, n_samples=1000, 
                           perturbation_std=0.1):
    """
    Randomly perturb ALL parameters simultaneously
    perturbation_std: standard deviation of perturbation (0.1 = 10%)
    """
    
    baseline_result = model_func(base_params)
    
    perturbed_results = []
    
    for _ in range(n_samples):
        perturbed_params = {}
        for name, value in base_params.items():
            # Add Gaussian noise
            noise = np.random.normal(1.0, perturbation_std)
            perturbed_params[name] = value * noise
        
        result = model_func(perturbed_params)
        perturbed_results.append(result)
    
    return baseline_result, perturbed_results

# Visualization
def plot_robustness_distribution(baseline, perturbed_results, metric_name):
    """Show distribution of outcomes"""
    
    values = [r[metric_name] for r in perturbed_results]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(values, bins=50, alpha=0.7, color='steelblue', edgecolor='black')
    ax.axvline(baseline[metric_name], color='red', linestyle='--', 
               linewidth=2, label=f'Baseline: {baseline[metric_name]:.2f}')
    
    # Calculate statistics
    mean_val = np.mean(values)
    std_val = np.std(values)
    
    ax.axvline(mean_val, color='green', linestyle='--', 
               linewidth=2, label=f'Mean: {mean_val:.2f}')
    ax.axvspan(mean_val - 2*std_val, mean_val + 2*std_val, 
               alpha=0.2, color='green', label='95% CI')
    
    ax.set_xlabel(metric_name, fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax.set_title('Robustness Test: Output Distribution Under Parameter Uncertainty',
                 fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/robustness_distribution.png', dpi=300)
```

## Interpretation Guidelines

### Tornado Diagram
- **Wide bars** = High sensitivity (parameter needs careful calibration)
- **Narrow bars** = Low sensitivity (robust to this parameter)
- **Top parameters** = Priority for data collection/validation

### Phase Plane
- **Converging trajectories** = Stable equilibrium (good!)
- **Diverging trajectories** = Unstable equilibrium (problematic)
- **Closed loops** = Oscillatory behavior (cycles)
- **Spirals** = Damped or growing oscillations

### Robustness Distribution
- **Narrow distribution** = Robust model
- **Mean near baseline** = Unbiased
- **Wide distribution** = Sensitive to uncertainty (needs improvement)

## Output Location

Save to `results/robustness/`:
- `tornado_diagram.png`
- `phase_plane.png`
- `robustness_distribution.png`
- `sensitivity_report.txt`

## Requirements

1. Test at least 5 parameters in tornado analysis
2. Use ±20% perturbation as standard
3. For phase plane: show vector field + trajectories + equilibria
4. Include interpretation in paper ("Model is robust because...")
5. If model is NOT robust, explain mitigation strategy

## Common Pitfalls

- Testing only one parameter at a time (tornado is better than nothing, but Monte Carlo is more realistic)
- Not showing baseline in plots
- Phase plane without equilibrium points marked
- Claiming robustness without quantitative evidence
