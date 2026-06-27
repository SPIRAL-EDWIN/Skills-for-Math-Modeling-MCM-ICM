# Bayesian Parameter Inversion Skill

## Overview
A reusable framework for inverting model parameters from observed data using Bayesian inference. This skill implements two O-award winning approaches from MCM 2025 Problem A.

## Purpose
Convert observed wear patterns (effects) into hidden parameters (causes) with quantified uncertainty:
- **Input**: Observed data (e.g., wear depth matrix, point cloud)
- **Output**: Parameter estimates + uncertainty (credible intervals, posterior distributions)

## Key Features
1. **Hybrid PSO+MCMC** (Paper 2504218 approach)
   - Global optimization via Particle Swarm Optimization
   - Local uncertainty quantification via MCMC sampling
   - Full posterior distributions with credible intervals

2. **MAP Estimation** (Paper 2511565 approach)
   - Grid search over parameter space
   - Maximum a posteriori point estimates
   - Faster for low-dimensional problems

3. **Smoothness Regularization**
   - Second-order gradient penalty for smooth solutions
   - Prevents overfitting to noisy data

## Mathematical Framework

### Bayesian Formulation
```
Prior:       p(θ) = p(α) × p(N) × p(T) × ...
Likelihood:  p(h_obs | θ) ∝ exp(-E(θ))
Posterior:   p(θ | h_obs) ∝ p(θ) × p(h_obs | θ)
```

### Energy Function
```
E(θ) = (1/2σ²) Σ[h_sim(x_i, y_i; θ) - h_obs(x_i, y_i)]² + λ·E_smooth
       └────────────── Data misfit ──────────────┘   └─ Regularization ─┘
```

### Smoothness Penalty
```
E_smooth = Σ[∇²h_sim(x_i, y_i; θ)]²
```

## Implementation Approaches

### Method 1: PSO + MCMC (Recommended for high accuracy)
**Use when**: Need full uncertainty quantification, multiple parameters (3+)

**Algorithm**:
1. **PSO Global Search**
   - Initialize particle swarm in prior bounds
   - Optimize: `min[E(θ) - ln p(θ)]`
   - Output: Near-global optimum θ*

2. **MCMC Local Sampling**
   - Initialize at θ*
   - Metropolis-Hastings sampling around θ*
   - Output: Posterior samples {θ^(s)}

3. **Credible Intervals**
   - Sort samples, extract quantiles
   - 95% CI: [θ_0.025, θ_0.975]

**Pros**:
- Handles high-dimensional spaces
- Full posterior distribution
- Quantifies parameter correlations

**Cons**:
- Computationally expensive
- Requires tuning (PSO parameters, MCMC step size)

### Method 2: MAP Estimation (Recommended for speed)
**Use when**: Need quick estimates, low-dimensional (1-2 parameters)

**Algorithm**:
1. Define prior: `p(θ) = Uniform(θ_min, θ_max)`
2. Compute likelihood: `L(θ) = exp(-(V_model(θ) - V_obs)² / 2σ²)`
3. Grid search: `θ_MAP = argmax[p(θ) × L(θ)]`

**Pros**:
- Fast and simple
- No tuning required
- Works well for 1-2 parameters

**Cons**:
- No uncertainty quantification (point estimate only)
- Struggles with high dimensions

## API Design

### Core Class: `BayesianInverter`

```python
class BayesianInverter:
    """
    Bayesian parameter inversion framework
    """
    def __init__(self, 
                 forward_model: Callable,
                 params: Dict[str, Prior],
                 method: str = 'pso_mcmc'):
        """
        Args:
            forward_model: Function that computes h_sim(x, y; θ)
            params: Dictionary of parameter priors
                    e.g., {'alpha': UniformPrior(0.1, 1.0),
                           'N': UniformPrior(100, 1000)}
            method: 'pso_mcmc' or 'map_grid'
        """
        
    def invert(self, 
               observed_data: np.ndarray,
               observation_points: np.ndarray,
               sigma: float = 0.01,
               smooth_lambda: float = 0.1) -> InversionResult:
        """
        Perform Bayesian inversion
        
        Args:
            observed_data: h_obs values at observation points
            observation_points: (x_i, y_i) coordinates
            sigma: Observation noise std
            smooth_lambda: Smoothness penalty weight
            
        Returns:
            InversionResult with:
                - theta_map: MAP estimate
                - posterior_samples: MCMC samples (if method='pso_mcmc')
                - credible_intervals: 95% CI for each parameter
                - convergence_diagnostics: R-hat, ESS, etc.
        """
```

### Prior Distributions

```python
class Prior(ABC):
    @abstractmethod
    def log_prob(self, theta: float) -> float:
        pass
    
    @abstractmethod
    def sample(self, n: int) -> np.ndarray:
        pass

class UniformPrior(Prior):
    def __init__(self, low: float, high: float):
        self.low, self.high = low, high
    
    def log_prob(self, theta):
        return 0.0 if self.low <= theta <= self.high else -np.inf
    
class GaussianPrior(Prior):
    def __init__(self, mu: float, sigma: float):
        self.mu, self.sigma = mu, sigma
    
    def log_prob(self, theta):
        return -0.5 * ((theta - self.mu) / self.sigma)**2
```

## Usage Examples

### Example 1: Stair Wear Parameter Estimation (PSO+MCMC)

```python
from bayesian_inversion import BayesianInverter, UniformPrior
import numpy as np

# Define forward model (Archard wear law)
def wear_model(x, y, theta):
    """
    theta = [alpha, N, T]
    alpha: wear coefficient
    N: daily foot traffic
    T: time (years)
    """
    alpha, N, T = theta
    # Simplified Archard: h = (k·N·T·P·d) / (H·A)
    h = alpha * N * T * foot_pressure(x, y) / material_hardness
    return h

# Set up priors
priors = {
    'alpha': UniformPrior(1e-10, 1e-8),
    'N': UniformPrior(100, 1000),
    'T': UniformPrior(50, 200)
}

# Create inverter
inverter = BayesianInverter(
    forward_model=wear_model,
    params=priors,
    method='pso_mcmc'
)

# Run inversion
result = inverter.invert(
    observed_data=wear_depth_matrix,
    observation_points=grid_points,
    sigma=0.005,  # 5mm measurement noise
    smooth_lambda=0.1
)

# Extract results
print(f"MAP Estimate: alpha={result.theta_map['alpha']:.2e}")
print(f"95% CI: [{result.ci['alpha'][0]:.2e}, {result.ci['alpha'][1]:.2e}]")

# Visualize posterior
result.plot_posterior('alpha')
result.plot_corner()  # Pair plot of all parameters
```

### Example 2: Quick Age Estimation (MAP)

```python
# Simpler approach for single parameter
inverter = BayesianInverter(
    forward_model=lambda t: archard_volume(t, N=500),
    params={'T': UniformPrior(50, 200)},
    method='map_grid'
)

result = inverter.invert(
    observed_data=total_wear_volume,
    observation_points=None,  # Scalar observation
    sigma=0.1
)

print(f"Estimated age: {result.theta_map['T']:.1f} years")
```

## Implementation Modules

```
bayesian_inversion/
├── __init__.py
├── README.md
├── core.py              # BayesianInverter class
├── priors.py            # Prior distribution classes
├── optimizers.py        # PSO implementation
├── samplers.py          # MCMC (Metropolis-Hastings, NUTS)
├── diagnostics.py       # Convergence checks (R-hat, ESS)
├── visualization.py     # Posterior plots
└── tests/
    ├── test_pso_mcmc.py
    ├── test_map.py
    └── synthetic_data.py
```

## Dependencies

```python
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
emcee>=3.1.0          # MCMC sampler (optional)
pymc>=5.0.0           # Alternative MCMC backend (optional)
```

## Validation Strategy

1. **Synthetic Data Tests**
   - Generate data with known θ_true
   - Run inversion, check if θ_true ∈ 95% CI
   - Repeat 100 times, expect ~95% coverage

2. **Convergence Diagnostics**
   - Gelman-Rubin R-hat < 1.1
   - Effective Sample Size (ESS) > 1000
   - Trace plots show mixing

3. **Sensitivity Analysis**
   - Vary σ (noise level): Check CI width scales properly
   - Vary λ (smoothness): Check bias-variance tradeoff

## References

1. **Paper 2504218** (MCM 2025 O-Award): "Where Footsteps Collide"
   - Section 4: Bayesian inference with PSO+MCMC
   - Equations (20)-(23): Smoothness regularization

2. **Paper 2511565** (MCM 2025 O-Award): Bayesian MAP estimation
   - Section 3.2.3: Grid search approach
   - Equations (9)-(12): Prior, likelihood, posterior

## Competition Usage Tips

### Day 1-2: Build Forward Model First
- Don't start with Bayesian inversion
- First implement deterministic forward model
- Validate it produces reasonable outputs

### Day 2-3: Add Bayesian Inversion
- Start with MAP (faster to implement)
- If time permits, upgrade to PSO+MCMC
- Always include credible intervals in paper

### Paper Writing
- **Methods section**: Show the Bayesian formulation (prior, likelihood, posterior)
- **Results section**: Report MAP ± 95% CI
- **Sensitivity section**: Show how CI width changes with noise
- **Key phrase**: "We quantify parameter uncertainty using Bayesian inference"

## Common Pitfalls

1. **Prior too narrow**: MCMC gets stuck, fails to explore
   - Fix: Use wider priors, check posterior doesn't hit bounds

2. **Smoothness λ too large**: Over-smoothed, biased estimates
   - Fix: Cross-validation to tune λ

3. **MCMC not converged**: R-hat > 1.1, poor mixing
   - Fix: Run longer, adjust step size, use multiple chains

4. **PSO stuck in local minimum**: Poor starting point for MCMC
   - Fix: Increase PSO iterations, use multiple swarms

## Future Enhancements

- [ ] Hierarchical Bayesian models (multi-level priors)
- [ ] Adaptive MCMC (auto-tune step size)
- [ ] Parallel tempering for multimodal posteriors
- [ ] Variational inference (faster alternative to MCMC)
