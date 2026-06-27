---
name: particle-swarm
description: Particle Swarm Optimization (PSO) for fast continuous optimization. Inspired by bird flocking and fish schooling. Balances exploration and exploitation with few parameters. Best for smooth continuous functions in MCM/ICM. Fastest convergence among metaheuristics.
---

# Particle Swarm Optimization (PSO)

Swarm intelligence algorithm inspired by social behavior of birds and fish.

## When to Use

- **Continuous Optimization**: Real-valued decision variables.
- **Smooth Functions**: Differentiable or nearly differentiable objectives.
- **Fast Convergence Needed**: PSO typically converges faster than **`genetic-algorithm`** or **`simulated-annealing`**.
- **Few Parameters**: Only 4 main parameters to tune (vs. 5+ for GA).
- **High-Dimensional**: Works well up to 50-100 dimensions.

## When NOT to Use

- **Discrete/Combinatorial**: Use **`genetic-algorithm`** instead.
- **Highly Discontinuous**: PSO assumes some smoothness.
- **Convex Problems**: Use gradient-based methods (much faster).
- **Need Global Guarantee**: PSO can get stuck in local optima (though rare).

## Algorithm Overview

### Social Metaphor
**Bird Flocking**: Birds share information about food location; each bird adjusts flight based on:
1.  **Personal experience**: Where it found best food.
2.  **Social knowledge**: Where the swarm found best food.

### Key Components
1.  **Particles**: Candidate solutions moving through search space.
2.  **Velocity**: Speed and direction of particle movement.
3.  **Personal Best ($p_i$)**: Best position this particle has found.
4.  **Global Best ($g$)**: Best position any particle has found.
5.  **Inertia Weight ($w$)**: Balance between exploration and exploitation.

### Update Equations
$$v_i(t+1) = w \cdot v_i(t) + c_1 r_1 (p_i - x_i(t)) + c_2 r_2 (g - x_i(t))$$
$$x_i(t+1) = x_i(t) + v_i(t+1)$$

Where:
- $w$: Inertia weight (0.4-0.9)
- $c_1$: Cognitive coefficient (1.0-2.0)
- $c_2$: Social coefficient (1.0-2.0)
- $r_1, r_2$: Random numbers in [0, 1]

### Pseudo-Code
```
1. Initialize: random positions and velocities for all particles
2. Evaluate fitness of all particles
3. Set personal best = current position, global best = best particle
4. REPEAT until convergence:
   a. For each particle:
      - Update velocity using equation above
      - Update position: x = x + v
      - Clip to bounds
      - Evaluate fitness
      - Update personal best if improved
   b. Update global best across all particles
5. Return global best
```

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

class ParticleSwarmOptimization:
    """
    Particle Swarm Optimization
    """
    
    def __init__(self, objective_func, bounds, n_particles=30, 
                 w=0.7, c1=1.5, c2=1.5, constraints=None, 
                 maximize=False, seed=42):
        """
        Args:
            objective_func (callable): f(x) -> float
            bounds (list of tuples): [(x1_min, x1_max), ...]
            n_particles (int): Number of particles (20-50)
            w (float): Inertia weight (0.4-0.9)
            c1 (float): Cognitive coefficient (1.0-2.0)
            c2 (float): Social coefficient (1.0-2.0)
            constraints (list): [g1(x), g2(x), ...] where g(x) <= 0
            maximize (bool): If True, maximize; else minimize
            seed (int): Random seed
        """
        self.objective_func = objective_func
        self.bounds = np.array(bounds)
        self.n_dim = len(bounds)
        self.n_particles = n_particles
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.constraints = constraints if constraints else []
        self.maximize = maximize
        
        np.random.seed(seed)
        
        # Initialize swarm
        self.positions = np.random.uniform(
            self.bounds[:, 0], 
            self.bounds[:, 1],
            size=(n_particles, self.n_dim)
        )
        
        # Initialize velocities (20% of search space)
        v_max = (self.bounds[:, 1] - self.bounds[:, 0]) * 0.2
        self.velocities = np.random.uniform(-v_max, v_max, 
                                           size=(n_particles, self.n_dim))
        self.v_max = v_max
        
        # Personal best
        self.personal_best_positions = self.positions.copy()
        self.personal_best_fitness = np.array([
            self._evaluate_fitness(p) for p in self.positions
        ])
        
        # Global best
        best_idx = np.argmin(self.personal_best_fitness)
        self.global_best_position = self.personal_best_positions[best_idx].copy()
        self.global_best_fitness = self.personal_best_fitness[best_idx]
        
        # History tracking
        self.global_best_fitness_history = []
        self.avg_fitness_history = []
        self.diversity_history = []
        
    def _evaluate_fitness(self, position):
        """Evaluate fitness with constraint penalty"""
        # Base objective
        f = self.objective_func(position)
        
        # Constraint penalty
        penalty = 0
        for constraint in self.constraints:
            violation = max(0, constraint(position))
            penalty += 1000 * violation**2
        
        # Convert to minimization
        if self.maximize:
            f = -f
        
        return f + penalty
    
    def _calculate_diversity(self):
        """
        Calculate swarm diversity (average distance to centroid)
        """
        centroid = np.mean(self.positions, axis=0)
        distances = np.linalg.norm(self.positions - centroid, axis=1)
        return np.mean(distances)
    
    def optimize(self, n_iterations=100, adaptive_inertia=False, verbose=True):
        """
        Run PSO
        
        Args:
            n_iterations (int): Number of iterations
            adaptive_inertia (bool): Use linearly decreasing inertia weight
            verbose (bool): Print progress
            
        Returns:
            dict: {
                'best_solution': array,
                'best_fitness': float,
                'fitness_history': list,
                'positions': array (final swarm positions)
            }
        """
        for iteration in range(n_iterations):
            # Adaptive inertia weight (linearly decreasing)
            if adaptive_inertia:
                w = 0.9 - (0.9 - 0.4) * iteration / n_iterations
            else:
                w = self.w
            
            for i in range(self.n_particles):
                # Evaluate fitness
                fitness = self._evaluate_fitness(self.positions[i])
                
                # Update personal best
                if fitness < self.personal_best_fitness[i]:
                    self.personal_best_fitness[i] = fitness
                    self.personal_best_positions[i] = self.positions[i].copy()
                
                # Update global best
                if fitness < self.global_best_fitness:
                    self.global_best_fitness = fitness
                    self.global_best_position = self.positions[i].copy()
            
            # Track statistics
            self.global_best_fitness_history.append(self.global_best_fitness)
            self.avg_fitness_history.append(np.mean(self.personal_best_fitness))
            self.diversity_history.append(self._calculate_diversity())
            
            # Update velocities and positions
            for i in range(self.n_particles):
                r1 = np.random.rand(self.n_dim)
                r2 = np.random.rand(self.n_dim)
                
                # Velocity update
                cognitive = self.c1 * r1 * (self.personal_best_positions[i] - self.positions[i])
                social = self.c2 * r2 * (self.global_best_position - self.positions[i])
                
                self.velocities[i] = w * self.velocities[i] + cognitive + social
                
                # Velocity clamping
                self.velocities[i] = np.clip(self.velocities[i], -self.v_max, self.v_max)
                
                # Position update
                self.positions[i] += self.velocities[i]
                
                # Boundary handling (reflection)
                for d in range(self.n_dim):
                    if self.positions[i, d] < self.bounds[d, 0]:
                        self.positions[i, d] = self.bounds[d, 0]
                        self.velocities[i, d] *= -0.5  # Reflect with damping
                    elif self.positions[i, d] > self.bounds[d, 1]:
                        self.positions[i, d] = self.bounds[d, 1]
                        self.velocities[i, d] *= -0.5
            
            if verbose and iteration % 10 == 0:
                diversity = self.diversity_history[-1]
                print(f"Iteration {iteration}: Best = {self.global_best_fitness:.6f}, "
                      f"Avg = {self.avg_fitness_history[-1]:.6f}, Diversity = {diversity:.4f}")
        
        return {
            'best_solution': self.global_best_position,
            'best_fitness': self.global_best_fitness if not self.maximize else -self.global_best_fitness,
            'fitness_history': self.global_best_fitness_history,
            'avg_fitness_history': self.avg_fitness_history,
            'positions': self.positions
        }
    
    def plot_convergence(self, title='PSO Convergence'):
        """Plot convergence curve"""
        fig, axes = plt.subplots(2, 1, figsize=(10, 10))
        
        # Fitness convergence
        ax1 = axes[0]
        ax1.plot(self.global_best_fitness_history, 'b-', linewidth=2, label='Global Best')
        ax1.plot(self.avg_fitness_history, 'r--', linewidth=1.5, label='Average Fitness')
        ax1.set_xlabel('Iteration', fontsize=12)
        ax1.set_ylabel('Fitness', fontsize=12)
        ax1.set_title('Fitness Evolution', fontsize=13, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Diversity
        ax2 = axes[1]
        ax2.plot(self.diversity_history, 'g-', linewidth=2)
        ax2.set_xlabel('Iteration', fontsize=12)
        ax2.set_ylabel('Swarm Diversity', fontsize=12)
        ax2.set_title('Diversity (Exploration vs Exploitation)', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('pso_convergence.png', dpi=300)
        plt.show()
    
    def plot_swarm_2d(self, iteration_snapshots=[0, 25, 50, 100]):
        """
        Visualize swarm movement in 2D (only if n_dim == 2)
        """
        if self.n_dim != 2:
            print("Swarm visualization only available for 2D problems")
            return
        
        # This requires storing position history during optimization
        # Simplified version: just show final positions
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create contour plot of objective function
        x = np.linspace(self.bounds[0, 0], self.bounds[0, 1], 100)
        y = np.linspace(self.bounds[1, 0], self.bounds[1, 1], 100)
        X, Y = np.meshgrid(x, y)
        Z = np.array([[self.objective_func([xi, yi]) for xi, yi in zip(xrow, yrow)] 
                      for xrow, yrow in zip(X, Y)])
        
        ax.contour(X, Y, Z, levels=20, cmap='viridis', alpha=0.6)
        
        # Plot particles
        ax.scatter(self.positions[:, 0], self.positions[:, 1], 
                  c='red', s=50, alpha=0.8, edgecolors='black', label='Particles')
        
        # Plot global best
        ax.scatter(self.global_best_position[0], self.global_best_position[1],
                  c='yellow', s=200, marker='*', edgecolors='black', 
                  linewidth=2, label='Global Best', zorder=5)
        
        ax.set_xlabel('x1', fontsize=12)
        ax.set_ylabel('x2', fontsize=12)
        ax.set_title('PSO Swarm Distribution', fontsize=14, fontweight='bold')
        ax.legend()
        plt.tight_layout()
        plt.savefig('pso_swarm_2d.png', dpi=300)
        plt.show()

# --- Usage Example ---
if __name__ == "__main__":
    # Example: Minimize Rosenbrock function
    def rosenbrock(x):
        return np.sum(100 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)
    
    # Setup
    n_dim = 5
    bounds = [(-5, 5)] * n_dim
    
    pso = ParticleSwarmOptimization(
        rosenbrock, 
        bounds, 
        n_particles=30,
        w=0.7,
        c1=1.5,
        c2=1.5
    )
    
    # Run
    result = pso.optimize(n_iterations=100, adaptive_inertia=True)
    
    print(f"\nBest solution: {result['best_solution']}")
    print(f"Best fitness: {result['best_fitness']:.6f}")
    
    # Plot
    pso.plot_convergence()
```

## Advanced Variants

### 1. Constriction PSO (Clerc & Kennedy)

```python
def constriction_coefficient(c1, c2):
    """
    Calculate constriction coefficient χ
    Ensures convergence without velocity clamping
    """
    phi = c1 + c2
    if phi <= 4:
        return 1.0
    else:
        return 2 / abs(2 - phi - np.sqrt(phi**2 - 4*phi))

# Usage:
chi = constriction_coefficient(c1=2.05, c2=2.05)
v_new = chi * (v + c1*r1*(p - x) + c2*r2*(g - x))
```

### 2. Adaptive PSO (APSO)

```python
def adaptive_parameters(diversity, diversity_threshold=0.1):
    """
    Adapt w, c1, c2 based on swarm diversity
    """
    if diversity < diversity_threshold:
        # Low diversity: increase exploration
        w = 0.9
        c1 = 2.0
        c2 = 1.0
    else:
        # High diversity: increase exploitation
        w = 0.4
        c1 = 1.0
        c2 = 2.0
    return w, c1, c2
```

### 3. Multi-Swarm PSO

```python
def multi_swarm_pso(objective, bounds, n_swarms=3):
    """
    Run multiple independent swarms, exchange information periodically
    """
    swarms = [ParticleSwarmOptimization(objective, bounds) 
              for _ in range(n_swarms)]
    
    for iteration in range(100):
        for swarm in swarms:
            swarm.optimize(n_iterations=10, verbose=False)
        
        # Exchange global best every 10 iterations
        if iteration % 10 == 0:
            all_bests = [s.global_best_fitness for s in swarms]
            best_swarm = swarms[np.argmin(all_bests)]
            for swarm in swarms:
                if swarm != best_swarm:
                    swarm.global_best_position = best_swarm.global_best_position.copy()
                    swarm.global_best_fitness = best_swarm.global_best_fitness
```

## Parameter Tuning Guide

| Parameter | Typical Range | Effect | Recommendation |
|-----------|--------------|--------|----------------|
| `n_particles` | 20-50 | More = better coverage | 30 (standard) |
| `w` | 0.4-0.9 | Lower = exploitation, higher = exploration | 0.7 or adaptive |
| `c1` | 1.0-2.0 | Cognitive (personal experience) | 1.5 |
| `c2` | 1.0-2.0 | Social (swarm knowledge) | 1.5 |

### Standard Parameter Sets

1.  **Balanced (Default)**: $w=0.7, c_1=1.5, c_2=1.5$
2.  **Exploration**: $w=0.9, c_1=2.0, c_2=1.0$
3.  **Exploitation**: $w=0.4, c_1=1.0, c_2=2.0$
4.  **Constriction**: $\chi=0.729, c_1=2.05, c_2=2.05$

## Integration with Other Skills

### Connection to Multi-Objective Optimization

PSO can be extended to multi-objective problems:

```python
# Single-objective PSO (this skill)
from particle_swarm import ParticleSwarmOptimization
pso = ParticleSwarmOptimization(objective, bounds)
result = pso.optimize()

# Multi-objective (multi-objective-optimization)
# MOPSO: PSO with Pareto dominance and archive
from multi_objective_optimization import MOPSO  # If implemented
```

### Use with Differential Equations

```python
# Optimize ODE model parameters
from differential_equations import PredatorPreyModel
from particle_swarm import ParticleSwarmOptimization

model = PredatorPreyModel()

def objective(params):
    model.params = {
        'alpha': params[0], 'beta': params[1],
        'delta': params[2], 'gamma': params[3]
    }
    pred, prey = model.solve([10, 5], t_data)
    error = np.sum((pred - observed_pred)**2 + (prey - observed_prey)**2)
    return error

pso = ParticleSwarmOptimization(objective, bounds)
result = pso.optimize()
```

## Common Pitfalls

1.  **Premature Convergence**: All particles cluster around local optimum.
    *   **Fix**: Increase $w$ or use adaptive inertia.

2.  **Slow Convergence**: Takes too many iterations.
    *   **Fix**: Increase $c_2$ (social component) or particle count.

3.  **Particles Leave Bounds**: Velocities too large.
    *   **Fix**: Implement velocity clamping or boundary reflection.

4.  **Loss of Diversity**: Swarm collapses to single point.
    *   **Fix**: Monitor diversity, restart if < threshold.

## Output Requirements for Paper

1.  **Algorithm Description**:
    > "We employed Particle Swarm Optimization with 30 particles, inertia weight $w=0.7$, cognitive coefficient $c_1=1.5$, and social coefficient $c_2=1.5$."

2.  **Parameter Justification**:
    > "Parameters follow the standard balanced configuration recommended by Clerc & Kennedy (2002). Adaptive inertia weight was used to improve convergence."

3.  **Convergence Plot**: Show global best and average fitness over iterations.

4.  **Diversity Plot**: Show swarm diversity to demonstrate exploration-exploitation balance.

5.  **Performance**:
    > "PSO converged to f(x*) = 0.0023 after 80 iterations (Figure X). Swarm diversity decreased smoothly from 2.5 to 0.1, indicating healthy convergence without premature stagnation."

## Decision Guide: PSO vs Other Algorithms

| Problem Type | Use PSO? | Alternative |
|--------------|---------|-------------|
| Continuous, smooth | ✅ Yes (best choice) | **`simulated-annealing`** |
| Discrete/Combinatorial | ❌ No | **`genetic-algorithm`** |
| Multi-modal | ✅ Yes | **`simulated-annealing`** (also good) |
| High-dimensional (50+) | ✅ Yes | Best among metaheuristics |
| Need fast convergence | ✅ Yes | Fastest metaheuristic |
| Need simplicity | ✅ Yes | Only 4 parameters |

## Summary

This **`particle-swarm`** skill:
1.  Provides complete PSO implementation with adaptive variants.
2.  **Fastest convergence** among metaheuristics for continuous problems.
3.  **Fewest parameters** (4 vs. 5+ for GA).
4.  Best for **smooth, continuous, high-dimensional** optimization.
5.  Integrates with **`differential-equations`** for parameter fitting.
6.  Can be extended to multi-objective (MOPSO).
