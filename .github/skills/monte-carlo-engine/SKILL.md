---
name: monte-carlo-engine
description: Monte Carlo simulation for uncertainty quantification and risk analysis in MCM/ICM competitions. Use when dealing with randomness, incomplete data, or need to show probability distributions rather than single predictions. Produces confidence interval plots, distribution histograms, and convergence diagnostics. Essential for stochastic models.
---

# Monte-Carlo-Engine

Quantify uncertainty and assess risk through large-scale random sampling simulations.

## When to Use

- Model has inherent randomness (weather, human behavior, arrivals)
- Parameters are uncertain (only know ranges, not exact values)
- Need to report "probability of success" rather than single prediction
- Want to show confidence intervals on forecasts
- Data is insufficient (use distributions to fill gaps)
- O-prize level: Always prefer probabilistic results over deterministic

## Core Concept

Instead of running model once with "best guess" parameters, run it thousands of times with randomly sampled parameters from probability distributions. This produces a distribution of possible outcomes.

```
Traditional: "Population will be 5,432 in 2030"
Monte Carlo: "Population will be 4,800-6,100 (95% CI) in 2030, 
              with 85% probability of exceeding 5,000"
```

## Workflow

### Step 1: Define Parameter Distributions

**CRITICAL**: Choose distributions based on physical meaning, not convenience.

```python
import numpy as np
from scipy import stats

# Common distributions and when to use them

# 1. Normal (Gaussian): Natural measurement errors, central limit theorem
growth_rate = stats.norm(loc=0.05, scale=0.01)  # mean=5%, std=1%

# 2. Lognormal: Positive quantities (money, population, time)
initial_capital = stats.lognorm(s=0.5, scale=100000)  # Right-skewed

# 3. Uniform: No information except min/max bounds
elasticity = stats.uniform(loc=0.5, scale=1.5)  # Range [0.5, 2.0]

# 4. Triangular: Know min, max, and most likely value
cost_estimate = stats.triang(c=0.6, loc=1000, scale=2000)  
# min=1000, max=3000, mode=1000+0.6*2000=2200

# 5. Beta: Bounded on [0,1], flexible shape (e.g., probabilities)
success_rate = stats.beta(a=8, b=2)  # Skewed toward 1

# 6. Poisson: Count data (arrivals, events per time)
daily_visitors = stats.poisson(mu=150)  # Average 150/day

# 7. Exponential: Time between events, lifetimes
failure_time = stats.expon(scale=5)  # Mean time = 5 years

# 8. Gamma: Positive, flexible shape (waiting times, rainfall)
project_duration = stats.gamma(a=2, scale=3)  # shape=2, scale=3
```

**Distribution Selection Guide:**

| Data Type | Suggested Distribution |
|-----------|----------------------|
| Measurement error | Normal |
| Money, population | Lognormal |
| Probability | Beta |
| Count (events/time) | Poisson |
| Time until event | Exponential, Gamma |
| Unknown (bounded) | Uniform, Triangular |

### Step 2: Implement Vectorized Simulation

**BAD (slow):**
```python
results = []
for i in range(10000):
    param1 = np.random.normal(5, 1)
    param2 = np.random.uniform(0, 10)
    result = run_model(param1, param2)  # Python loop
    results.append(result)
```

**GOOD (fast):**
```python
# Generate all samples at once (vectorized)
n_simulations = 10000

param1_samples = np.random.normal(5, 1, size=n_simulations)
param2_samples = np.random.uniform(0, 10, size=n_simulations)

# Vectorized model evaluation
results = run_model_vectorized(param1_samples, param2_samples)

# OR parallel processing for complex models
from multiprocessing import Pool

def run_single(params):
    return run_model(params[0], params[1])

param_pairs = list(zip(param1_samples, param2_samples))

with Pool() as pool:
    results = pool.map(run_single, param_pairs)
```

### Step 3: Core Simulation Pattern

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def monte_carlo_simulation(n_simulations=10000, random_seed=42):
    """
    Template for Monte Carlo simulation
    """
    np.random.seed(random_seed)  # Reproducibility
    
    # Define parameter distributions
    distributions = {
        'growth_rate': stats.norm(0.05, 0.01),
        'initial_pop': stats.lognorm(s=0.2, scale=1000),
        'carrying_capacity': stats.uniform(5000, 5000),  # [5000, 10000]
        'harvest_rate': stats.beta(a=2, b=5)
    }
    
    # Pre-allocate results array
    results = {
        'final_population': np.zeros(n_simulations),
        'peak_time': np.zeros(n_simulations),
        'sustainability': np.zeros(n_simulations, dtype=bool)
    }
    
    # Run simulations
    for i in range(n_simulations):
        # Sample parameters
        params = {
            name: dist.rvs() 
            for name, dist in distributions.items()
        }
        
        # Run model
        outcome = run_model(params)
        
        # Store results
        results['final_population'][i] = outcome['population'][-1]
        results['peak_time'][i] = outcome['peak_time']
        results['sustainability'][i] = outcome['is_sustainable']
    
    return results

# Execute simulation
results = monte_carlo_simulation(n_simulations=10000)
```

### Step 4: Statistical Analysis

```python
def analyze_results(results, metric='final_population'):
    """Extract statistics from simulation results"""
    
    data = results[metric]
    
    analysis = {
        'mean': np.mean(data),
        'median': np.median(data),
        'std': np.std(data),
        'min': np.min(data),
        'max': np.max(data),
        'ci_95': np.percentile(data, [2.5, 97.5]),
        'ci_90': np.percentile(data, [5, 95]),
        'ci_50': np.percentile(data, [25, 75]),  # IQR
        'skewness': stats.skew(data),
        'kurtosis': stats.kurtosis(data)
    }
    
    # Print summary
    print(f"Monte Carlo Results for {metric}:")
    print(f"  Mean: {analysis['mean']:.2f}")
    print(f"  Median: {analysis['median']:.2f}")
    print(f"  Std Dev: {analysis['std']:.2f}")
    print(f"  95% CI: [{analysis['ci_95'][0]:.2f}, {analysis['ci_95'][1]:.2f}]")
    print(f"  Range: [{analysis['min']:.2f}, {analysis['max']:.2f}]")
    
    return analysis
```

## Visualization Requirements

### 1. Confidence Interval Bands (Time Series)

```python
def plot_confidence_bands(time_series_results, time_points):
    """
    Show mean trajectory with uncertainty bands
    time_series_results: shape (n_simulations, n_timepoints)
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Calculate percentiles at each time point
    mean_trajectory = np.mean(time_series_results, axis=0)
    ci_95_lower = np.percentile(time_series_results, 2.5, axis=0)
    ci_95_upper = np.percentile(time_series_results, 97.5, axis=0)
    ci_50_lower = np.percentile(time_series_results, 25, axis=0)
    ci_50_upper = np.percentile(time_series_results, 75, axis=0)
    
    # Plot bands
    ax.fill_between(time_points, ci_95_lower, ci_95_upper, 
                    alpha=0.2, color='steelblue', 
                    label='95% Confidence Interval')
    ax.fill_between(time_points, ci_50_lower, ci_50_upper, 
                    alpha=0.4, color='steelblue', 
                    label='50% Confidence Interval (IQR)')
    
    # Plot mean
    ax.plot(time_points, mean_trajectory, 'b-', linewidth=2.5, 
            label='Mean Prediction')
    
    # Optional: Show sample trajectories
    n_samples_to_show = 50
    for i in range(n_samples_to_show):
        ax.plot(time_points, time_series_results[i, :], 
                'gray', alpha=0.05, linewidth=0.5)
    
    ax.set_xlabel('Time', fontsize=12, fontweight='bold')
    ax.set_ylabel('Population', fontsize=12, fontweight='bold')
    ax.set_title('Monte Carlo Forecast with Uncertainty', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/monte_carlo_forecast.png', dpi=300)
```

### 2. Distribution Histogram

```python
def plot_distribution(results, metric='final_population'):
    """Show probability distribution of outcomes"""
    
    data = results[metric]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Histogram
    n, bins, patches = ax.hist(data, bins=50, density=True, 
                               alpha=0.7, color='steelblue', 
                               edgecolor='black')
    
    # Fit and overlay normal distribution (for comparison)
    mu, sigma = np.mean(data), np.std(data)
    x = np.linspace(data.min(), data.max(), 100)
    ax.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', linewidth=2,
            label=f'Normal fit (μ={mu:.1f}, σ={sigma:.1f})')
    
    # Mark percentiles
    ci_95 = np.percentile(data, [2.5, 97.5])
    ax.axvline(ci_95[0], color='red', linestyle='--', linewidth=2,
               label='95% CI')
    ax.axvline(ci_95[1], color='red', linestyle='--', linewidth=2)
    
    # Mark mean and median
    ax.axvline(np.mean(data), color='green', linestyle='-', linewidth=2,
               label=f'Mean: {np.mean(data):.1f}')
    ax.axvline(np.median(data), color='orange', linestyle='-', linewidth=2,
               label=f'Median: {np.median(data):.1f}')
    
    # Annotate statistics
    textstr = f'Skewness: {stats.skew(data):.2f}\nKurtosis: {stats.kurtosis(data):.2f}'
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, 
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax.set_xlabel(metric.replace('_', ' ').title(), fontsize=12, fontweight='bold')
    ax.set_ylabel('Probability Density', fontsize=12, fontweight='bold')
    ax.set_title('Monte Carlo Output Distribution', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/monte_carlo_distribution.png', dpi=300)
```

### 3. Convergence Diagnostic

**CRITICAL**: Prove that N=10,000 is sufficient (results have stabilized)

```python
def plot_convergence(results, metric='final_population'):
    """Show that mean converges with sample size"""
    
    data = results[metric]
    n_simulations = len(data)
    
    # Calculate running mean
    sample_sizes = np.arange(100, n_simulations, 100)
    running_means = [np.mean(data[:n]) for n in sample_sizes]
    running_stds = [np.std(data[:n]) for n in sample_sizes]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Mean convergence
    ax1.plot(sample_sizes, running_means, 'b-', linewidth=2)
    final_mean = np.mean(data)
    ax1.axhline(final_mean, color='red', linestyle='--', linewidth=2,
                label=f'Final Mean: {final_mean:.2f}')
    ax1.fill_between(sample_sizes, 
                     final_mean - 0.01*final_mean,
                     final_mean + 0.01*final_mean,
                     alpha=0.2, color='red', label='±1% band')
    ax1.set_ylabel('Running Mean', fontsize=11, fontweight='bold')
    ax1.set_title('Convergence Diagnostic', fontsize=13, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Std convergence
    ax2.plot(sample_sizes, running_stds, 'g-', linewidth=2)
    final_std = np.std(data)
    ax2.axhline(final_std, color='red', linestyle='--', linewidth=2,
                label=f'Final Std: {final_std:.2f}')
    ax2.set_xlabel('Number of Simulations', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Running Std Dev', fontsize=11, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/monte_carlo_convergence.png', dpi=300)
```

## Advanced: Variance Reduction Techniques

### Latin Hypercube Sampling (More efficient than pure random)

```python
from scipy.stats import qmc

def latin_hypercube_sampling(distributions, n_samples=10000):
    """
    More efficient sampling than pure random
    Ensures better coverage of parameter space
    """
    n_params = len(distributions)
    
    # Generate LHS samples in [0,1]
    sampler = qmc.LatinHypercube(d=n_params, seed=42)
    unit_samples = sampler.random(n=n_samples)
    
    # Transform to actual distributions
    samples = {}
    for i, (name, dist) in enumerate(distributions.items()):
        samples[name] = dist.ppf(unit_samples[:, i])  # Inverse CDF
    
    return samples
```

## Output Requirements

### For Paper

1. **Method description**: "We performed Monte Carlo simulation with 10,000 runs..."
2. **Distribution justification**: "Growth rate assumed Normal based on historical data..."
3. **Confidence intervals**: Report 95% CI, not just mean
4. **Convergence proof**: Include convergence plot in appendix
5. **Risk metrics**: "85% probability of exceeding target"

### Files

Save to `results/monte_carlo/`:
- `forecast_with_ci.png` - Confidence band plot
- `distribution.png` - Histogram of outcomes
- `convergence.png` - Diagnostic plot
- `simulation_results.csv` - Raw results (for reproducibility)
- `summary_statistics.json` - Mean, CI, percentiles

## Common Pitfalls

- **Too few runs**: N < 1,000 is unreliable, N ≥ 10,000 is standard
- **Wrong distributions**: Using Uniform for everything (lazy!)
- **No convergence check**: Must prove results are stable
- **Single output**: Run MC for multiple metrics, not just one
- **Ignoring correlations**: If parameters are correlated, use copulas
- **No seed**: Always set `np.random.seed()` for reproducibility
- **Python loops**: Must vectorize or parallelize for speed

## Performance Benchmarks

Target: 10,000 simulations in < 5 minutes

- **Vectorized NumPy**: 10,000 runs in seconds
- **Python loop**: 10,000 runs in hours (1000x slower!)
- **Multiprocessing**: Linear speedup with CPU cores
