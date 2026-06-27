"""
Particle Swarm Optimization (PSO) for global parameter search
"""

import numpy as np
from typing import Callable, Dict, Tuple


class PSO:
    """
    Particle Swarm Optimization
    
    Finds global minimum of objective function f(θ) in bounded parameter space.
    Based on Paper 2504218 implementation.
    
    Algorithm:
        1. Initialize particle swarm with random positions and velocities
        2. Iterate:
            - Evaluate fitness f(θ) for each particle
            - Update personal best and global best
            - Update velocities: v = w*v + c1*r1*(pbest - θ) + c2*r2*(gbest - θ)
            - Update positions: θ = θ + v
        3. Return global best θ*
    
    Example:
        >>> def rosenbrock(theta):
        ...     x, y = theta['x'], theta['y']
        ...     return (1 - x)**2 + 100*(y - x**2)**2
        >>> 
        >>> pso = PSO(rosenbrock, {'x': (-5, 5), 'y': (-5, 5)}, n_particles=30)
        >>> theta_star, f_star = pso.optimize()
        >>> # Should find x ≈ 1, y ≈ 1
    """
    
    def __init__(
        self,
        objective_fn: Callable[[Dict[str, float]], float],
        bounds: Dict[str, Tuple[float, float]],
        n_particles: int = 30,
        max_iter: int = 100,
        w: float = 0.7,
        c1: float = 1.5,
        c2: float = 1.5,
        tol: float = 1e-6,
        patience: int = 10
    ):
        """
        Initialize PSO optimizer
        
        Args:
            objective_fn: Function to minimize, f(θ_dict) -> scalar
            bounds: Parameter bounds, {param: (low, high)}
            n_particles: Swarm size
            max_iter: Maximum iterations
            w: Inertia weight (momentum)
            c1: Cognitive parameter (personal best attraction)
            c2: Social parameter (global best attraction)
            tol: Convergence tolerance
            patience: Stop if no improvement for this many iterations
        """
        self.objective_fn = objective_fn
        self.bounds = bounds
        self.param_names = list(bounds.keys())
        self.n_params = len(self.param_names)
        
        self.n_particles = n_particles
        self.max_iter = max_iter
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.tol = tol
        self.patience = patience
        
        # Initialize swarm
        self.positions = self._initialize_positions()
        self.velocities = self._initialize_velocities()
        
        # Track best positions
        self.personal_best_positions = self.positions.copy()
        self.personal_best_scores = np.full(n_particles, np.inf)
        
        self.global_best_position = None
        self.global_best_score = np.inf
        
        # Convergence tracking
        self.history = {
            'global_best_scores': [],
            'mean_scores': []
        }
    
    def _initialize_positions(self) -> np.ndarray:
        """
        Initialize particle positions uniformly in bounds
        
        Returns:
            Array shape (n_particles, n_params)
        """
        positions = np.zeros((self.n_particles, self.n_params))
        
        for i, param in enumerate(self.param_names):
            low, high = self.bounds[param]
            positions[:, i] = np.random.uniform(low, high, self.n_particles)
        
        return positions
    
    def _initialize_velocities(self) -> np.ndarray:
        """
        Initialize velocities as small random values
        
        Returns:
            Array shape (n_particles, n_params)
        """
        velocities = np.zeros((self.n_particles, self.n_params))
        
        for i, param in enumerate(self.param_names):
            low, high = self.bounds[param]
            v_max = 0.1 * (high - low)  # 10% of range
            velocities[:, i] = np.random.uniform(-v_max, v_max, self.n_particles)
        
        return velocities
    
    def _array_to_dict(self, position: np.ndarray) -> Dict[str, float]:
        """Convert position array to parameter dictionary"""
        return {
            param: position[i]
            for i, param in enumerate(self.param_names)
        }
    
    def _clip_to_bounds(self, positions: np.ndarray) -> np.ndarray:
        """Clip positions to stay within bounds"""
        clipped = positions.copy()
        
        for i, param in enumerate(self.param_names):
            low, high = self.bounds[param]
            clipped[:, i] = np.clip(clipped[:, i], low, high)
        
        return clipped
    
    def optimize(self, verbose: bool = True) -> Tuple[Dict[str, float], float]:
        """
        Run PSO optimization
        
        Args:
            verbose: Print progress
            
        Returns:
            (theta_star, f_star): Best parameters and objective value
        """
        no_improve_count = 0
        
        for iteration in range(self.max_iter):
            # Evaluate fitness for all particles
            scores = np.array([
                self.objective_fn(self._array_to_dict(pos))
                for pos in self.positions
            ])
            
            # Update personal bests
            improved = scores < self.personal_best_scores
            self.personal_best_positions[improved] = self.positions[improved]
            self.personal_best_scores[improved] = scores[improved]
            
            # Update global best
            min_idx = np.argmin(self.personal_best_scores)
            if self.personal_best_scores[min_idx] < self.global_best_score:
                improvement = self.global_best_score - self.personal_best_scores[min_idx]
                self.global_best_score = self.personal_best_scores[min_idx]
                self.global_best_position = self.personal_best_positions[min_idx].copy()
                
                if improvement < self.tol:
                    no_improve_count += 1
                else:
                    no_improve_count = 0
            else:
                no_improve_count += 1
            
            # Store history
            self.history['global_best_scores'].append(self.global_best_score)
            self.history['mean_scores'].append(np.mean(scores))
            
            if verbose and iteration % 10 == 0:
                print(f"Iter {iteration:3d}: Best = {self.global_best_score:.6f}, "
                      f"Mean = {np.mean(scores):.6f}")
            
            # Check convergence
            if no_improve_count >= self.patience:
                if verbose:
                    print(f"Converged at iteration {iteration} (no improvement for {self.patience} iters)")
                break
            
            # Update velocities and positions
            r1 = np.random.rand(self.n_particles, self.n_params)
            r2 = np.random.rand(self.n_particles, self.n_params)
            
            cognitive = self.c1 * r1 * (self.personal_best_positions - self.positions)
            social = self.c2 * r2 * (self.global_best_position - self.positions)
            
            self.velocities = self.w * self.velocities + cognitive + social
            
            # Update positions
            self.positions = self.positions + self.velocities
            
            # Enforce bounds
            self.positions = self._clip_to_bounds(self.positions)
        
        # Return best solution
        theta_star = self._array_to_dict(self.global_best_position)
        return theta_star, self.global_best_score
    
    def plot_convergence(self):
        """Plot convergence history"""
        try:
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(self.history['global_best_scores'], label='Global Best', linewidth=2)
            ax.plot(self.history['mean_scores'], label='Swarm Mean', alpha=0.7)
            ax.set_xlabel('Iteration')
            ax.set_ylabel('Objective Value')
            ax.set_title('PSO Convergence')
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            return fig
        except ImportError:
            print("matplotlib not available for plotting")
            return None
