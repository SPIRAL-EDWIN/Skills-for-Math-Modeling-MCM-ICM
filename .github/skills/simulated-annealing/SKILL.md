---
name: simulated-annealing
description: Simulated Annealing (SA) for global optimization of multimodal functions. Inspired by metal annealing physics. Probabilistically accepts worse solutions to escape local optima. Best for continuous optimization with many local minima in MCM/ICM.
---

# Simulated Annealing (SA)

Physics-inspired optimization algorithm that escapes local optima through controlled randomness.

## When to Use

- **Multi-Modal Functions**: Many local optima in objective landscape.
- **Continuous Optimization**: Real-valued decision variables.
- **Global Optimization**: Need to avoid getting stuck in local minima.
- **Non-Differentiable**: Black-box functions without gradients.
- **Simplicity Preferred**: Fewer parameters than **`genetic-algorithm`** or **`particle-swarm`**.

## When NOT to Use

- **Convex Problems**: Use gradient-based methods (much faster).
- **Discrete/Combinatorial**: Use **`genetic-algorithm`** (better suited).
- **Fast Convergence Needed**: SA is typically slower than **`particle-swarm`**.
- **Very High Dimensions**: SA struggles with dimensionality (>50 variables).

## Algorithm Overview

### Physical Metaphor
**Metal Annealing**: Heat metal to high temperature → slowly cool → atoms settle into low-energy (optimal) state.

### Key Idea
Accept worse solutions with probability $P = e^{-\Delta E / T}$ to escape local optima.

### Components
1.  **Temperature $T$**: Controls acceptance probability (high $T$ = more exploration).
2.  **Cooling Schedule**: How temperature decreases over time.
3.  **Neighbor Generation**: How to perturb current solution.
4.  **Acceptance Criterion**: Metropolis criterion from statistical mechanics.

### Pseudo-Code
```
1. Initialize: random solution x, high temperature T
2. REPEAT until T < T_final:
   a. Generate neighbor x' by perturbing x
   b. Calculate ΔE = f(x') - f(x)
   c. IF ΔE < 0 OR random() < exp(-ΔE/T):
      Accept x' (x = x')
   d. Cool down: T = T * alpha
3. Return best solution found
```

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

class SimulatedAnnealing:
    """
    Simulated Annealing for optimization
    """
    
    def __init__(self, objective_func, bounds, T_initial=100, T_final=1e-3,
                 alpha=0.95, constraints=None, maximize=False, seed=42):
        """
        Args:
            objective_func (callable): f(x) -> float
            bounds (list of tuples): [(x1_min, x1_max), ...]
            T_initial (float): Initial temperature (10-1000)
            T_final (float): Final temperature (0.001-0.1)
            alpha (float): Cooling rate (0.85-0.99)
            constraints (list): [g1(x), g2(x), ...] where g(x) <= 0
            maximize (bool): If True, maximize; else minimize
            seed (int): Random seed
        """
        self.objective_func = objective_func
        self.bounds = np.array(bounds)
        self.n_dim = len(bounds)
        self.T_initial = T_initial
        self.T_final = T_final
        self.alpha = alpha
        self.constraints = constraints if constraints else []
        self.maximize = maximize
        
        np.random.seed(seed)
        
        # Initialize solution
        self.current_solution = np.random.uniform(
            self.bounds[:, 0], 
            self.bounds[:, 1]
        )
        self.current_fitness = self._evaluate_fitness(self.current_solution)
        
        self.best_solution = self.current_solution.copy()
        self.best_fitness = self.current_fitness
        
        # History tracking
        self.best_fitness_history = []
        self.current_fitness_history = []
        self.temperature_history = []
        self.acceptance_rate_history = []
        
    def _evaluate_fitness(self, solution):
        """Evaluate fitness with constraint penalty"""
        # Base objective
        f = self.objective_func(solution)
        
        # Constraint penalty
        penalty = 0
        for constraint in self.constraints:
            violation = max(0, constraint(solution))
            penalty += 1000 * violation**2
        
        # Convert to minimization
        if self.maximize:
            f = -f
        
        return f + penalty
    
    def _generate_neighbor_gaussian(self, x, T):
        """
        Generate neighbor using Gaussian perturbation
        Step size adapts with temperature
        """
        # Adaptive step size (decreases with temperature)
        step_size = (self.bounds[:, 1] - self.bounds[:, 0]) * 0.1 * (T / self.T_initial)
        
        neighbor = x + np.random.normal(0, step_size, self.n_dim)
        
        # Clip to bounds
        neighbor = np.clip(neighbor, self.bounds[:, 0], self.bounds[:, 1])
        
        return neighbor
    
    def _generate_neighbor_uniform(self, x, T):
        """
        Generate neighbor using uniform perturbation
        """
        step_size = (self.bounds[:, 1] - self.bounds[:, 0]) * 0.05 * (T / self.T_initial)
        
        neighbor = x + np.random.uniform(-step_size, step_size, self.n_dim)
        neighbor = np.clip(neighbor, self.bounds[:, 0], self.bounds[:, 1])
        
        return neighbor
    
    def _generate_neighbor_cauchy(self, x, T):
        """
        Generate neighbor using Cauchy distribution (heavier tails)
        Better for escaping local minima
        """
        step_size = (self.bounds[:, 1] - self.bounds[:, 0]) * 0.05 * (T / self.T_initial)
        
        # Cauchy distribution (scale parameter = step_size)
        perturbation = np.random.standard_cauchy(self.n_dim) * step_size
        
        neighbor = x + perturbation
        neighbor = np.clip(neighbor, self.bounds[:, 0], self.bounds[:, 1])
        
        return neighbor
    
    def _acceptance_probability(self, current_fitness, new_fitness, T):
        """
        Metropolis criterion
        
        Returns:
            float: Acceptance probability [0, 1]
        """
        if new_fitness < current_fitness:
            return 1.0  # Always accept better solutions
        else:
            # Accept worse solutions with probability exp(-ΔE/T)
            return np.exp(-(new_fitness - current_fitness) / T)
    
    def _cooling_schedule_geometric(self, T):
        """Geometric cooling: T_new = alpha * T_old"""
        return self.alpha * T
    
    def _cooling_schedule_logarithmic(self, T, iteration):
        """Logarithmic cooling: T = T0 / log(1 + iteration)"""
        return self.T_initial / np.log(2 + iteration)
    
    def _cooling_schedule_exponential(self, T, iteration):
        """Exponential cooling: T = T0 * exp(-k * iteration)"""
        k = -np.log(self.T_final / self.T_initial) / 1000  # Assuming 1000 iterations
        return self.T_initial * np.exp(-k * iteration)
    
    def optimize(self, n_iterations=1000, neighbor_type='gaussian', 
                 cooling_schedule='geometric', verbose=True):
        """
        Run simulated annealing
        
        Args:
            n_iterations (int): Maximum iterations
            neighbor_type (str): 'gaussian', 'uniform', 'cauchy'
            cooling_schedule (str): 'geometric', 'logarithmic', 'exponential'
            verbose (bool): Print progress
            
        Returns:
            dict: {
                'best_solution': array,
                'best_fitness': float,
                'fitness_history': list,
                'temperature_history': list
            }
        """
        # Select neighbor generation method
        neighbor_funcs = {
            'gaussian': self._generate_neighbor_gaussian,
            'uniform': self._generate_neighbor_uniform,
            'cauchy': self._generate_neighbor_cauchy
        }
        generate_neighbor = neighbor_funcs[neighbor_type]
        
        # Select cooling schedule
        cooling_funcs = {
            'geometric': lambda T, i: self._cooling_schedule_geometric(T),
            'logarithmic': lambda T, i: self._cooling_schedule_logarithmic(T, i),
            'exponential': lambda T, i: self._cooling_schedule_exponential(T, i)
        }
        cool_down = cooling_funcs[cooling_schedule]
        
        T = self.T_initial
        accepted_count = 0
        
        for iteration in range(n_iterations):
            # Generate neighbor
            neighbor = generate_neighbor(self.current_solution, T)
            neighbor_fitness = self._evaluate_fitness(neighbor)
            
            # Acceptance decision
            accept_prob = self._acceptance_probability(
                self.current_fitness, neighbor_fitness, T
            )
            
            if np.random.rand() < accept_prob:
                self.current_solution = neighbor
                self.current_fitness = neighbor_fitness
                accepted_count += 1
                
                # Update best
                if self.current_fitness < self.best_fitness:
                    self.best_solution = self.current_solution.copy()
                    self.best_fitness = self.current_fitness
            
            # Track history
            self.best_fitness_history.append(self.best_fitness)
            self.current_fitness_history.append(self.current_fitness)
            self.temperature_history.append(T)
            
            # Track acceptance rate (every 100 iterations)
            if iteration % 100 == 99:
                acceptance_rate = accepted_count / 100
                self.acceptance_rate_history.append(acceptance_rate)
                accepted_count = 0
            
            # Cool down
            T = cool_down(T, iteration)
            
            if T < self.T_final:
                if verbose:
                    print(f"Iteration {iteration}: Reached final temperature")
                break
            
            if verbose and iteration % 100 == 0:
                print(f"Iteration {iteration}: T = {T:.4f}, Best = {self.best_fitness:.6f}, Current = {self.current_fitness:.6f}")
        
        return {
            'best_solution': self.best_solution,
            'best_fitness': self.best_fitness if not self.maximize else -self.best_fitness,
            'fitness_history': self.best_fitness_history,
            'temperature_history': self.temperature_history,
            'current_fitness_history': self.current_fitness_history
        }
    
    def plot_convergence(self, title='SA Convergence'):
        """Plot convergence and temperature curves"""
        fig, axes = plt.subplots(2, 1, figsize=(10, 10))
        
        # Fitness convergence
        ax1 = axes[0]
        ax1.plot(self.best_fitness_history, 'b-', linewidth=2, label='Best Fitness')
        ax1.plot(self.current_fitness_history, 'r-', linewidth=1, alpha=0.5, label='Current Fitness')
        ax1.set_xlabel('Iteration', fontsize=12)
        ax1.set_ylabel('Fitness', fontsize=12)
        ax1.set_title('Fitness Evolution', fontsize=13, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Temperature schedule
        ax2 = axes[1]
        ax2.plot(self.temperature_history, 'g-', linewidth=2)
        ax2.set_xlabel('Iteration', fontsize=12)
        ax2.set_ylabel('Temperature', fontsize=12)
        ax2.set_title('Temperature Schedule', fontsize=13, fontweight='bold')
        ax2.set_yscale('log')
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('sa_convergence.png', dpi=300)
        plt.show()
    
    def plot_acceptance_rate(self):
        """Plot acceptance rate over time"""
        if not self.acceptance_rate_history:
            print("No acceptance rate data available")
            return
        
        plt.figure(figsize=(10, 6))
        plt.plot(np.arange(len(self.acceptance_rate_history)) * 100, 
                self.acceptance_rate_history, 'purple', linewidth=2)
        plt.xlabel('Iteration', fontsize=12)
        plt.ylabel('Acceptance Rate', fontsize=12)
        plt.title('Acceptance Rate Over Time', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('sa_acceptance_rate.png', dpi=300)
        plt.show()

# --- Usage Example ---
if __name__ == "__main__":
    # Example: Minimize Ackley function
    def ackley(x):
        n = len(x)
        return (-20 * np.exp(-0.2 * np.sqrt(np.sum(x**2) / n)) 
                - np.exp(np.sum(np.cos(2 * np.pi * x)) / n) 
                + 20 + np.e)
    
    # Setup
    n_dim = 5
    bounds = [(-5, 5)] * n_dim
    
    sa = SimulatedAnnealing(
        ackley, 
        bounds, 
        T_initial=100,
        T_final=1e-3,
        alpha=0.95
    )
    
    # Run
    result = sa.optimize(n_iterations=1000, neighbor_type='gaussian', cooling_schedule='geometric')
    
    print(f"\nBest solution: {result['best_solution']}")
    print(f"Best fitness: {result['best_fitness']:.6f}")
    
    # Plot
    sa.plot_convergence()
    sa.plot_acceptance_rate()
```

## Cooling Schedules Comparison

| Schedule | Formula | Convergence | Best For |
|----------|---------|-------------|----------|
| **Geometric** | $T_{k+1} = \alpha T_k$ | Fast | Most problems (default) |
| **Logarithmic** | $T_k = T_0 / \log(1+k)$ | Slow, guaranteed | Theoretical optimality |
| **Exponential** | $T_k = T_0 e^{-\lambda k}$ | Medium | When iterations known |

## Parameter Tuning Guide

| Parameter | Typical Range | Effect | Recommendation |
|-----------|--------------|--------|----------------|
| `T_initial` | 10-1000 | Higher = more exploration | 10-100 × objective range |
| `T_final` | 0.001-0.1 | Lower = finer search | 0.001 (standard) |
| `alpha` | 0.85-0.99 | Higher = slower cooling | 0.95 (good balance) |
| `n_iterations` | 500-5000 | More = better convergence | Until T < T_final |

### Rule of Thumb for T_initial
Set $T_0$ such that initial acceptance probability ≈ 80%:
$$T_0 \approx \frac{\Delta E_{avg}}{-\ln(0.8)} \approx 0.45 \times \Delta E_{avg}$$

Where $\Delta E_{avg}$ is average difference between random neighbors.

## Advanced Variants

### 1. Adaptive SA (Fast SA)

```python
def adaptive_step_size(self, accepted_ratio):
    """Adjust step size based on acceptance rate"""
    if accepted_ratio > 0.6:
        self.step_size *= 1.1  # Increase exploration
    elif accepted_ratio < 0.4:
        self.step_size *= 0.9  # Decrease exploration
```

### 2. Parallel SA (Multiple Chains)

```python
def parallel_sa(objective, bounds, n_chains=4):
    """Run multiple SA chains in parallel"""
    results = []
    for _ in range(n_chains):
        sa = SimulatedAnnealing(objective, bounds)
        result = sa.optimize()
        results.append(result)
    
    # Return best across all chains
    best = min(results, key=lambda r: r['best_fitness'])
    return best
```

## Integration with Other Skills

### Connection to Multi-Objective Optimization

SA can be extended to multi-objective problems using **simulated annealing with archive** (similar to MOEA/D):

```python
# Single-objective SA (this skill)
from simulated_annealing import SimulatedAnnealing
sa = SimulatedAnnealing(objective, bounds)
result = sa.optimize()

# Multi-objective (multi-objective-optimization)
from multi_objective_optimization import MOEAD
# MOEA/D uses decomposition + SA-like acceptance
```

### Use with Differential Equations

```python
# Optimize parameters of ODE model
from differential_equations import LogisticModel
from simulated_annealing import SimulatedAnnealing

model = LogisticModel()

def objective(params):
    model.params = {'r': params[0], 'K': params[1]}
    predictions = model.solve([10], t_data)
    return np.sum((predictions - observed_data)**2)

sa = SimulatedAnnealing(objective, bounds=[(0.1, 2.0), (50, 200)])
result = sa.optimize()
```

## Common Pitfalls

1.  **T_initial Too Low**: Algorithm behaves like hill climbing (gets stuck).
    *   **Fix**: Increase T_initial (test with 80% initial acceptance).

2.  **Cooling Too Fast**: Premature convergence.
    *   **Fix**: Increase alpha (0.95 → 0.99) or use logarithmic cooling.

3.  **Cooling Too Slow**: Wastes computation time.
    *   **Fix**: Decrease alpha or use exponential cooling.

4.  **Step Size Too Large/Small**: Poor exploration or exploitation.
    *   **Fix**: Use adaptive step size based on acceptance rate.

## Output Requirements for Paper

1.  **Algorithm Description**:
    > "We employed Simulated Annealing with geometric cooling (α=0.95), Gaussian neighbor generation, and Metropolis acceptance criterion."

2.  **Parameter Justification**:
    > "Initial temperature T₀=100 was set to achieve 80% initial acceptance rate. Final temperature Tₑ=0.001 ensures fine-tuning."

3.  **Convergence Plots**: Show both fitness and temperature curves.

4.  **Acceptance Rate**: Plot acceptance rate over time (should decrease from ~80% to ~5%).

5.  **Performance**:
    > "After 1000 iterations, SA converged to f(x*) = 0.0045. The algorithm successfully escaped 3 local minima (Figure X)."

## Decision Guide: SA vs Other Algorithms

| Problem Type | Use SA? | Alternative |
|--------------|---------|-------------|
| Continuous, multimodal | ✅ Yes | **`particle-swarm`** (faster) |
| Discrete/Combinatorial | ⚠️ Possible | **`genetic-algorithm`** (better) |
| Smooth, unimodal | ❌ No | Gradient-based |
| Need simplicity | ✅ Yes | Fewest parameters |
| High-dimensional (>50) | ⚠️ Slow | **`particle-swarm`** |

## Summary

This **`simulated-annealing`** skill:
1.  Provides complete SA implementation with multiple cooling schedules.
2.  Best for continuous optimization with many local minima.
3.  Simplest algorithm (only 3 main parameters).
4.  Integrates with **`differential-equations`** for parameter fitting.
5.  Can be extended to multi-objective (MOEA/D connection).
