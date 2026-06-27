---
name: genetic-algorithm
description: Genetic Algorithm (GA) for combinatorial and discrete optimization problems. Inspired by biological evolution with selection, crossover, mutation, and elitism. Foundation for NSGA-II multi-objective optimization. Best for TSP, scheduling, assignment problems in MCM/ICM.
---

# Genetic Algorithm (GA)

Evolution-inspired optimization algorithm for discrete, combinatorial, and complex nonlinear problems.

## When to Use

- **Combinatorial Optimization**: TSP, knapsack, scheduling, assignment problems.
- **Discrete Variables**: Integer programming, binary decisions.
- **Non-Differentiable**: Objective function has discontinuities or is black-box.
- **Multi-Modal**: Multiple local optima in search space.
- **Constraint Handling**: Complex constraints that violate convexity.

## When NOT to Use

- **Convex Problems**: Use gradient-based methods (faster).
- **Continuous Smooth Functions**: Use **`particle-swarm`** or **`simulated-annealing`** (faster convergence).
- **Small Search Space**: Use **`automated-sweep`** (exhaustive search).
- **Real-Time Optimization**: GA is computationally expensive.

## Algorithm Overview

### Biological Metaphor
Natural selection: "Survival of the fittest"

### Key Components
1.  **Population**: Set of candidate solutions (chromosomes).
2.  **Fitness**: Evaluation function (how good is each solution).
3.  **Selection**: Choose parents based on fitness (tournament, roulette wheel).
4.  **Crossover**: Combine parent genes to create offspring.
5.  **Mutation**: Random changes to maintain diversity.
6.  **Elitism**: Preserve best individuals across generations.

### Pseudo-Code
```
1. Initialize random population
2. Evaluate fitness of all individuals
3. REPEAT until convergence:
   a. Select parents (tournament selection)
   b. Apply crossover to create offspring
   c. Apply mutation to offspring
   d. Evaluate offspring fitness
   e. Replace population (elitism + offspring)
   f. Track best solution
4. Return best solution found
```

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

class GeneticAlgorithm:
    """
    Genetic Algorithm for optimization
    """
    
    def __init__(self, objective_func, bounds, pop_size=50, 
                 crossover_rate=0.8, mutation_rate=0.1, elitism=2,
                 constraints=None, maximize=False, seed=42):
        """
        Args:
            objective_func (callable): f(x) -> float
            bounds (list of tuples): [(x1_min, x1_max), ...]
            pop_size (int): Population size
            crossover_rate (float): Probability of crossover (0.6-0.9)
            mutation_rate (float): Probability of mutation per gene (0.01-0.1)
            elitism (int): Number of best individuals to preserve (1-5)
            constraints (list): [g1(x), g2(x), ...] where g(x) <= 0
            maximize (bool): If True, maximize; else minimize
            seed (int): Random seed for reproducibility
        """
        self.objective_func = objective_func
        self.bounds = np.array(bounds)
        self.n_dim = len(bounds)
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism = elitism
        self.constraints = constraints if constraints else []
        self.maximize = maximize
        
        np.random.seed(seed)
        
        # Initialize population
        self.population = self._initialize_population()
        
        # History tracking
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.best_solution_history = []
        
    def _initialize_population(self):
        """Random initialization within bounds"""
        return np.random.uniform(
            self.bounds[:, 0], 
            self.bounds[:, 1],
            size=(self.pop_size, self.n_dim)
        )
    
    def _evaluate_fitness(self, individual):
        """Evaluate fitness with constraint penalty"""
        # Base objective
        f = self.objective_func(individual)
        
        # Constraint penalty
        penalty = 0
        for constraint in self.constraints:
            violation = max(0, constraint(individual))
            penalty += 1000 * violation**2
        
        # Convert to minimization
        if self.maximize:
            f = -f
        
        return f + penalty
    
    def _selection_tournament(self, fitness, k=3):
        """
        Tournament selection
        
        Args:
            fitness (array): Fitness values for population
            k (int): Tournament size
            
        Returns:
            array: Selected parents
        """
        selected = []
        for _ in range(self.pop_size):
            # Randomly pick k individuals
            candidates = np.random.choice(self.pop_size, k, replace=False)
            # Select best (lowest fitness for minimization)
            winner = candidates[np.argmin(fitness[candidates])]
            selected.append(self.population[winner].copy())
        return np.array(selected)
    
    def _crossover_single_point(self, parent1, parent2):
        """
        Single-point crossover
        
        Returns:
            tuple: (child1, child2)
        """
        if np.random.rand() < self.crossover_rate:
            point = np.random.randint(1, self.n_dim)
            child1 = np.concatenate([parent1[:point], parent2[point:]])
            child2 = np.concatenate([parent2[:point], parent1[point:]])
            return child1, child2
        return parent1.copy(), parent2.copy()
    
    def _crossover_uniform(self, parent1, parent2):
        """
        Uniform crossover (each gene independently)
        """
        if np.random.rand() < self.crossover_rate:
            mask = np.random.rand(self.n_dim) < 0.5
            child1 = np.where(mask, parent1, parent2)
            child2 = np.where(mask, parent2, parent1)
            return child1, child2
        return parent1.copy(), parent2.copy()
    
    def _crossover_arithmetic(self, parent1, parent2, alpha=0.5):
        """
        Arithmetic crossover (for continuous variables)
        child1 = alpha * parent1 + (1-alpha) * parent2
        """
        if np.random.rand() < self.crossover_rate:
            child1 = alpha * parent1 + (1 - alpha) * parent2
            child2 = (1 - alpha) * parent1 + alpha * parent2
            return child1, child2
        return parent1.copy(), parent2.copy()
    
    def _mutate_gaussian(self, individual):
        """
        Gaussian mutation (for continuous variables)
        """
        for i in range(self.n_dim):
            if np.random.rand() < self.mutation_rate:
                # Add Gaussian noise (10% of range)
                sigma = (self.bounds[i, 1] - self.bounds[i, 0]) * 0.1
                individual[i] += np.random.normal(0, sigma)
                # Clip to bounds
                individual[i] = np.clip(
                    individual[i], 
                    self.bounds[i, 0], 
                    self.bounds[i, 1]
                )
        return individual
    
    def _mutate_uniform(self, individual):
        """
        Uniform mutation (replace with random value)
        """
        for i in range(self.n_dim):
            if np.random.rand() < self.mutation_rate:
                individual[i] = np.random.uniform(
                    self.bounds[i, 0], 
                    self.bounds[i, 1]
                )
        return individual
    
    def optimize(self, n_generations=100, crossover_type='single_point', 
                 mutation_type='gaussian', verbose=True):
        """
        Run genetic algorithm
        
        Args:
            n_generations (int): Number of generations
            crossover_type (str): 'single_point', 'uniform', 'arithmetic'
            mutation_type (str): 'gaussian', 'uniform'
            verbose (bool): Print progress
            
        Returns:
            dict: {
                'best_solution': array,
                'best_fitness': float,
                'fitness_history': list,
                'population': array
            }
        """
        # Select operators
        crossover_ops = {
            'single_point': self._crossover_single_point,
            'uniform': self._crossover_uniform,
            'arithmetic': self._crossover_arithmetic
        }
        mutation_ops = {
            'gaussian': self._mutate_gaussian,
            'uniform': self._mutate_uniform
        }
        
        crossover_func = crossover_ops[crossover_type]
        mutation_func = mutation_ops[mutation_type]
        
        for generation in range(n_generations):
            # Evaluate fitness
            fitness = np.array([self._evaluate_fitness(ind) for ind in self.population])
            
            # Track statistics
            best_idx = np.argmin(fitness)
            best_fitness = fitness[best_idx]
            best_solution = self.population[best_idx].copy()
            avg_fitness = np.mean(fitness)
            
            self.best_fitness_history.append(best_fitness)
            self.avg_fitness_history.append(avg_fitness)
            self.best_solution_history.append(best_solution)
            
            if verbose and generation % 10 == 0:
                print(f"Generation {generation}: Best = {best_fitness:.6f}, Avg = {avg_fitness:.6f}")
            
            # Elitism: preserve best individuals
            elite_indices = np.argsort(fitness)[:self.elitism]
            elites = self.population[elite_indices].copy()
            
            # Selection
            parents = self._selection_tournament(fitness)
            
            # Crossover
            offspring = []
            for i in range(0, self.pop_size - self.elitism, 2):
                if i + 1 < len(parents):
                    child1, child2 = crossover_func(parents[i], parents[i+1])
                    offspring.extend([child1, child2])
                else:
                    offspring.append(parents[i])
            
            # Mutation
            offspring = [mutation_func(child.copy()) for child in offspring]
            
            # New population: elites + offspring
            self.population = np.vstack([
                elites, 
                offspring[:self.pop_size - self.elitism]
            ])
        
        # Final evaluation
        fitness = np.array([self._evaluate_fitness(ind) for ind in self.population])
        best_idx = np.argmin(fitness)
        
        return {
            'best_solution': self.population[best_idx],
            'best_fitness': fitness[best_idx] if not self.maximize else -fitness[best_idx],
            'fitness_history': self.best_fitness_history,
            'avg_fitness_history': self.avg_fitness_history,
            'population': self.population
        }
    
    def plot_convergence(self, title='GA Convergence'):
        """Plot convergence curve"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(self.best_fitness_history, 'b-', linewidth=2, label='Best Fitness')
        ax.plot(self.avg_fitness_history, 'r--', linewidth=1.5, label='Average Fitness')
        
        ax.set_xlabel('Generation', fontsize=12)
        ax.set_ylabel('Fitness', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('ga_convergence.png', dpi=300)
        plt.show()

# --- Usage Example ---
if __name__ == "__main__":
    # Example: Minimize Rastrigin function
    def rastrigin(x):
        return 10 * len(x) + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))
    
    # Setup
    n_dim = 5
    bounds = [(-5.12, 5.12)] * n_dim
    
    ga = GeneticAlgorithm(
        rastrigin, 
        bounds, 
        pop_size=50,
        crossover_rate=0.8,
        mutation_rate=0.1,
        elitism=2
    )
    
    # Run
    result = ga.optimize(n_generations=100)
    
    print(f"\nBest solution: {result['best_solution']}")
    print(f"Best fitness: {result['best_fitness']:.6f}")
    
    # Plot
    ga.plot_convergence()
```

## Advanced Variants

### 1. Binary GA (for 0/1 problems)

```python
class BinaryGA(GeneticAlgorithm):
    """GA with binary encoding"""
    
    def _initialize_population(self):
        return np.random.randint(0, 2, size=(self.pop_size, self.n_dim))
    
    def _crossover_single_point(self, parent1, parent2):
        if np.random.rand() < self.crossover_rate:
            point = np.random.randint(1, self.n_dim)
            child1 = np.concatenate([parent1[:point], parent2[point:]])
            child2 = np.concatenate([parent2[:point], parent1[point:]])
            return child1, child2
        return parent1.copy(), parent2.copy()
    
    def _mutate_bit_flip(self, individual):
        for i in range(self.n_dim):
            if np.random.rand() < self.mutation_rate:
                individual[i] = 1 - individual[i]  # Flip bit
        return individual
```

### 2. Adaptive GA (self-tuning parameters)

```python
def adaptive_mutation_rate(generation, max_generations):
    """Decrease mutation rate over time"""
    return 0.1 * (1 - generation / max_generations) + 0.01
```

## Integration with Multi-Objective Optimization

### Connection to NSGA-II

**NSGA-II** (from `multi-objective-optimization`) is essentially **GA + Multi-Objective Selection**:

```python
# Single-objective GA (this skill)
from genetic_algorithm import GeneticAlgorithm
ga = GeneticAlgorithm(objective, bounds)
result = ga.optimize(n_generations=100)

# Multi-objective NSGA-II (multi-objective-optimization)
from multi_objective_optimization import NSGA2
from pymoo.optimize import minimize

problem = MultiObjectiveProblem()
algorithm = NSGA2(pop_size=100)
res = minimize(problem, algorithm, ('n_gen', 200))

# NSGA-II uses:
# 1. GA's crossover and mutation operators
# 2. Non-dominated sorting (instead of fitness-based selection)
# 3. Crowding distance (to maintain diversity)
```

## Parameter Tuning Guide

| Parameter | Typical Range | Effect | Recommendation |
|-----------|--------------|--------|----------------|
| `pop_size` | 30-100 | Larger = more exploration | 50 for most problems |
| `crossover_rate` | 0.6-0.9 | Higher = more recombination | 0.8 (standard) |
| `mutation_rate` | 0.01-0.1 | Higher = more diversity | 1/n_dim (rule of thumb) |
| `elitism` | 1-5 | Ensures best survive | 2 (good balance) |
| `n_generations` | 50-500 | More = better convergence | Until plateau |

## Common Pitfalls

1.  **Premature Convergence**: Population loses diversity too early.
    *   **Fix**: Increase mutation rate, decrease elitism.

2.  **Slow Convergence**: Takes too many generations.
    *   **Fix**: Increase population size, use adaptive parameters.

3.  **Constraint Violation**: Solutions violate constraints.
    *   **Fix**: Use repair operators or higher penalty factors.

4.  **Binary vs. Continuous**: Using wrong encoding.
    *   **Fix**: Binary GA for discrete, real-valued GA for continuous.

## Output Requirements for Paper

1.  **Algorithm Description**:
    > "We employed a Genetic Algorithm with tournament selection (k=3), single-point crossover (rate=0.8), and Gaussian mutation (rate=0.1)."

2.  **Parameter Justification**:
    > "Population size was set to 50 based on problem dimensionality (n=10). Elitism (2 individuals) ensured best solutions persisted."

3.  **Convergence Plot**: Show best and average fitness over generations.

4.  **Performance**:
    > "After 100 generations, GA converged to f(x*) = 0.0089 (Figure X). The algorithm showed stable convergence with no premature stagnation."

## Decision Guide: GA vs Other Algorithms

| Problem Type | Use GA? | Alternative |
|--------------|---------|-------------|
| Discrete/Combinatorial | ✅ Yes | None better |
| Continuous, smooth | ⚠️ Maybe | **`particle-swarm`** (faster) |
| Multi-modal | ✅ Yes | **`simulated-annealing`** (also good) |
| Multi-objective | ✅ Yes | Upgrade to NSGA-II |
| High-dimensional (>20) | ⚠️ Slow | **`particle-swarm`** |

## Summary

This **`genetic-algorithm`** skill:
1.  Provides complete GA implementation with multiple operators.
2.  Serves as foundation for **`multi-objective-optimization`** (NSGA-II).
3.  Best for discrete and combinatorial optimization.
4.  Integrates with **`sensitivity-master`** for parameter tuning.
