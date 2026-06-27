# Bayesian Parameter Inversion - Quick Start

## Installation

```bash
cd code/skills/bayesian_inversion
pip install -r requirements.txt
```

## 5-Minute Tutorial

### Step 1: Define Your Forward Model

```python
def forward_model(x, y, theta):
    """
    Compute predicted observations given parameters
    
    Args:
        x, y: Observation coordinates (arrays)
        theta: Dict of parameters, e.g., {'alpha': 1e-9, 'N': 500}
    
    Returns:
        Predicted values (array same shape as x)
    """
    # Your physics model here
    # Example: Linear model
    return theta['slope'] * x + theta['intercept'] * y
```

### Step 2: Set Up Priors

```python
from bayesian_inversion import UniformPrior, LogUniformPrior

priors = {
    'slope': UniformPrior(0.0, 10.0),
    'intercept': UniformPrior(-5.0, 5.0)
}
```

**Prior Types**:
- `UniformPrior(low, high)`: Flat prior, use when you have bounded but no preferred value
- `LogUniformPrior(low, high)`: For scale parameters spanning orders of magnitude (e.g., wear coefficient: 1e-10 to 1e-6)
- `GaussianPrior(mu, sigma)`: When you have expert knowledge about the parameter value

### Step 3: Create Inverter and Run

```python
from bayesian_inversion import BayesianInverter

# Create inverter
inverter = BayesianInverter(
    forward_model=forward_model,
    params=priors,
    method='pso_mcmc'  # or 'map_grid' for faster but less accurate
)

# Run inversion
result = inverter.invert(
    observed_data=your_data,           # Shape (n_obs,) or (ny, nx)
    observation_points=your_coords,    # Shape (n_obs, 2) with (x, y) pairs
    sigma=0.01,                        # Measurement noise std
    smooth_lambda=0.1                  # Smoothness penalty (0 = no smoothing)
)

# View results
print(result.summary())
```

### Step 4: Extract Results

```python
# MAP estimates
alpha_est = result.theta_map['alpha']
N_est = result.theta_map['N']

# 95% credible intervals
alpha_ci = result.credible_intervals['alpha']
print(f"alpha: {alpha_est:.2e} [{alpha_ci[0]:.2e}, {alpha_ci[1]:.2e}]")

# Posterior samples (for plotting, correlations, etc.)
if result.posterior_samples is not None:
    alpha_samples = result.posterior_samples['alpha']
    # Plot histogram, corner plots, etc.
```

## Complete Example: Stair Wear

See `example_stair_wear.py` for a full working example with:
- Synthetic data generation
- Forward model implementation (Archard wear law)
- PSO + MCMC inversion
- MAP grid search (single parameter)
- Validation against ground truth

Run it:
```bash
python example_stair_wear.py
```

## Method Selection Guide

| Scenario | Method | Config |
|----------|--------|--------|
| **1-2 parameters, need quick estimate** | `map_grid` | Default |
| **3+ parameters, need uncertainty** | `pso_mcmc` | `n_particles=30, max_iter=100` |
| **High-dimensional (5+ params)** | `pso_mcmc` | `n_particles=50, max_iter=200` |
| **Debugging/testing** | `map_grid` | Fast iteration |

## Configuration Tips

### PSO Configuration
```python
pso_config = {
    'n_particles': 30,      # More particles = better global search, slower
    'max_iter': 100,        # More iterations = better convergence
    'w': 0.7,               # Inertia (0.4-0.9, higher = more exploration)
    'c1': 1.5,              # Personal best weight
    'c2': 1.5,              # Global best weight
    'patience': 10          # Stop if no improvement for N iterations
}
```

### MCMC Configuration
```python
mcmc_config = {
    'n_samples': 5000,      # More samples = better posterior estimate
    'n_burnin': 1000,       # Discard initial samples (typically 20% of n_samples)
    'step_size': 0.01,      # Proposal step size (auto-tuned during burnin)
    'n_chains': 1,          # Use >1 to compute R-hat convergence diagnostic
    'adapt_step': True,     # Auto-tune step size during burnin
    'target_accept': 0.234  # Target acceptance rate (0.234 optimal for Gaussian)
}
```

## Interpreting Results

### Convergence Diagnostics

**Acceptance Rate** (MCMC):
- **Too low (<10%)**: Step size too large, chain stuck
- **Good (20-40%)**: Optimal mixing
- **Too high (>70%)**: Step size too small, slow exploration

**R-hat** (multiple chains):
- **R-hat < 1.1**: Converged ✓
- **R-hat > 1.1**: Not converged, run longer or check model

**Effective Sample Size (ESS)**:
- **ESS > 1000**: Good
- **ESS < 100**: High autocorrelation, need more samples

### Credible Intervals

95% credible interval: "There's a 95% probability the true parameter lies in this range"

**Wide CI**: High uncertainty, need more data or stronger priors
**Narrow CI**: Low uncertainty, parameter well-constrained by data

### Checking Your Results

1. **Plot posterior samples**: Should look smooth, not spiky
2. **Check if CI includes true value** (if known from synthetic data)
3. **Run forward model with MAP estimate**: Should match observed data
4. **Sensitivity analysis**: Vary sigma, smooth_lambda, check if results stable

## Common Issues

### Issue: "Forward model failed"
**Cause**: Parameters outside valid range (e.g., negative values where positive required)
**Fix**: Tighten priors to physically valid ranges

### Issue: PSO finds poor solution
**Cause**: Stuck in local minimum
**Fix**: Increase `n_particles` or `max_iter`, or use wider priors

### Issue: MCMC low acceptance rate
**Cause**: Step size too large
**Fix**: Decrease `step_size` or enable `adapt_step=True`

### Issue: Results don't match observed data
**Cause**: Wrong forward model or poor prior specification
**Fix**: Validate forward model independently, check prior bounds

## Competition Workflow

### Day 1: Build Forward Model
```python
# Test forward model with known parameters
theta_test = {'alpha': 5e-9, 'N': 500, 'T': 100}
h_sim = forward_model(x, y, theta_test)
# Visualize, check if reasonable
```

### Day 2: Add Bayesian Inversion
```python
# Start with MAP grid search (fast)
result = inverter.invert(..., method='map_grid')
# If works, upgrade to PSO+MCMC for uncertainty
```

### Day 3: Write Paper
```python
# Report: "We estimate α = 5.2e-9 [4.8e-9, 5.6e-9] (95% CI)"
# Include: Prior specification, convergence diagnostics, sensitivity analysis
```

## Paper Writing Template

```latex
\subsection{Bayesian Parameter Inversion}

To estimate parameters $\theta = (\alpha, N, T)$ from observed wear data $h_{obs}$, 
we employ Bayesian inference. We specify prior distributions based on material 
science literature:

\begin{align}
\alpha &\sim \text{LogUniform}(10^{-10}, 10^{-7}) \\
N &\sim \text{Uniform}(100, 1000) \\
T &\sim \text{Uniform}(50, 200)
\end{align}

The likelihood function is constructed from the residual between observed and 
simulated wear:

\begin{equation}
p(h_{obs} | \theta) \propto \exp\left(-\frac{1}{2\sigma^2} \sum_i [h_{sim}(x_i, y_i; \theta) - h_{obs}(x_i, y_i)]^2\right)
\end{equation}

We use a two-step optimization strategy: (1) Particle Swarm Optimization (PSO) 
locates the global optimum, (2) Markov Chain Monte Carlo (MCMC) refines the 
posterior distribution and quantifies uncertainty.

\subsection{Results}

Our inversion yields the following parameter estimates with 95% credible intervals:

\begin{itemize}
\item Wear coefficient: $\alpha = 5.2 \times 10^{-9}$ [4.8, 5.6] $\times 10^{-9}$
\item Daily foot traffic: $N = 487$ [450, 520] people/day
\item Age: $T = 98$ [92, 105] years
\end{itemize}

Convergence diagnostics: acceptance rate 0.28, $\hat{R} = 1.02 < 1.1$ ✓
```

## Next Steps

1. **Run the example**: `python example_stair_wear.py`
2. **Adapt to your problem**: Modify `forward_model` and `priors`
3. **Validate**: Test with synthetic data where you know the true parameters
4. **Apply to real data**: Run inversion on competition dataset
5. **Write paper**: Report MAP ± 95% CI, include convergence diagnostics

## References

- Paper 2504218 (MCM 2025): PSO + MCMC hybrid approach
- Paper 2511565 (MCM 2025): MAP estimation with Bayesian framework
- Gelman et al. (2013): "Bayesian Data Analysis" - MCMC theory
- Kennedy & Eberhart (1995): Original PSO paper
