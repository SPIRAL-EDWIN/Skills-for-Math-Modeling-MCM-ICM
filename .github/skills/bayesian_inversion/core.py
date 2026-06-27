"""
Core Bayesian inversion framework
"""

import numpy as np
from typing import Callable, Dict, Optional, Union
from dataclasses import dataclass, field
import warnings

from .priors import Prior, MultivariatePrior
from .optimizers import PSO
from .samplers import MetropolisHastingsSampler


@dataclass
class InversionResult:
    """
    Results from Bayesian parameter inversion
    
    Attributes:
        theta_map: Maximum a posteriori (MAP) estimate
        posterior_samples: MCMC samples from posterior (if available)
        credible_intervals: 95% credible intervals for each parameter
        log_posterior: Log posterior values at MAP
        convergence: Convergence diagnostics (R-hat, ESS, etc.)
        method: Method used ('pso_mcmc' or 'map_grid')
    """
    theta_map: Dict[str, float]
    posterior_samples: Optional[Dict[str, np.ndarray]] = None
    credible_intervals: Dict[str, tuple] = field(default_factory=dict)
    log_posterior: float = -np.inf
    convergence: Dict[str, float] = field(default_factory=dict)
    method: str = "unknown"
    
    def summary(self) -> str:
        """Print summary of inversion results"""
        lines = [f"Bayesian Inversion Results ({self.method})"]
        lines.append("=" * 50)
        
        for param, value in self.theta_map.items():
            ci = self.credible_intervals.get(param, (None, None))
            if ci[0] is not None:
                lines.append(f"{param:>10}: {value:.6e}  [{ci[0]:.6e}, {ci[1]:.6e}]")
            else:
                lines.append(f"{param:>10}: {value:.6e}")
        
        lines.append(f"\nLog posterior: {self.log_posterior:.2f}")
        
        if self.convergence:
            lines.append("\nConvergence diagnostics:")
            for key, val in self.convergence.items():
                lines.append(f"  {key}: {val:.4f}")
        
        return "\n".join(lines)


class BayesianInverter:
    """
    Bayesian parameter inversion framework
    
    Implements two approaches:
    1. PSO + MCMC: Global optimization + local uncertainty quantification
    2. MAP grid search: Fast point estimation
    
    Example:
        >>> def forward_model(x, y, theta):
        ...     return theta['alpha'] * theta['N'] * theta['T']
        >>> 
        >>> priors = {
        ...     'alpha': LogUniformPrior(1e-10, 1e-8),
        ...     'N': UniformPrior(100, 1000),
        ...     'T': UniformPrior(50, 200)
        ... }
        >>> 
        >>> inverter = BayesianInverter(forward_model, priors, method='pso_mcmc')
        >>> result = inverter.invert(observed_data, observation_points)
        >>> print(result.summary())
    """
    
    def __init__(
        self,
        forward_model: Callable,
        params: Dict[str, Prior],
        method: str = 'pso_mcmc'
    ):
        """
        Initialize Bayesian inverter
        
        Args:
            forward_model: Function that computes h_sim(x, y; θ)
                          Signature: forward_model(x, y, theta_dict) -> h_sim
            params: Dictionary of parameter priors
            method: 'pso_mcmc' or 'map_grid'
        """
        self.forward_model = forward_model
        self.priors = MultivariatePrior(params)
        self.method = method
        
        # Validate method
        valid_methods = ['pso_mcmc', 'map_grid']
        if method not in valid_methods:
            raise ValueError(f"method must be one of {valid_methods}, got '{method}'")
    
    def invert(
        self,
        observed_data: np.ndarray,
        observation_points: Optional[np.ndarray] = None,
        sigma: float = 0.01,
        smooth_lambda: float = 0.0,
        pso_config: Optional[dict] = None,
        mcmc_config: Optional[dict] = None
    ) -> InversionResult:
        """
        Perform Bayesian parameter inversion
        
        Args:
            observed_data: Observed values h_obs
                          Shape: (n_obs,) for point observations
                                 (ny, nx) for gridded data
            observation_points: Coordinates (x, y) where data observed
                               Shape: (n_obs, 2) or None for gridded data
            sigma: Observation noise standard deviation
            smooth_lambda: Smoothness regularization weight (λ)
            pso_config: PSO hyperparameters (for 'pso_mcmc' method)
            mcmc_config: MCMC hyperparameters (for 'pso_mcmc' method)
            
        Returns:
            InversionResult object
        """
        # Flatten observed data if gridded
        if observed_data.ndim == 2:
            ny, nx = observed_data.shape
            observed_data_flat = observed_data.flatten()
            
            if observation_points is None:
                # Create grid points
                x = np.linspace(0, 1, nx)
                y = np.linspace(0, 1, ny)
                X, Y = np.meshgrid(x, y)
                observation_points = np.column_stack([X.flatten(), Y.flatten()])
        else:
            observed_data_flat = observed_data
            
        # Validate observation points
        if observation_points is None:
            raise ValueError("observation_points required for 1D observed_data")
        
        # Build energy function
        def energy_function(theta_dict: dict) -> float:
            """
            E(θ) = (1/2σ²) Σ(h_sim - h_obs)² + λ·E_smooth - ln p(θ)
            """
            # Prior term: -ln p(θ)
            log_prior = self.priors.log_prob(theta_dict)
            if not np.isfinite(log_prior):
                return np.inf  # Outside prior bounds
            
            # Simulate forward model
            try:
                x_coords = observation_points[:, 0]
                y_coords = observation_points[:, 1]
                h_sim = self.forward_model(x_coords, y_coords, theta_dict)
            except Exception as e:
                warnings.warn(f"Forward model failed: {e}")
                return np.inf
            
            # Data misfit term
            residuals = h_sim - observed_data_flat
            data_misfit = np.sum(residuals**2) / (2 * sigma**2)
            
            # Smoothness regularization (if λ > 0)
            smooth_penalty = 0.0
            if smooth_lambda > 0 and observed_data.ndim == 2:
                # Compute discrete Laplacian
                h_sim_2d = h_sim.reshape(observed_data.shape)
                laplacian = self._compute_laplacian(h_sim_2d)
                smooth_penalty = smooth_lambda * np.sum(laplacian**2)
            
            # Total energy
            return data_misfit + smooth_penalty - log_prior
        
        # Run inversion based on method
        if self.method == 'pso_mcmc':
            return self._invert_pso_mcmc(
                energy_function,
                pso_config or {},
                mcmc_config or {}
            )
        elif self.method == 'map_grid':
            return self._invert_map_grid(energy_function)
        else:
            raise ValueError(f"Unknown method: {self.method}")
    
    def _invert_pso_mcmc(
        self,
        energy_fn: Callable,
        pso_config: dict,
        mcmc_config: dict
    ) -> InversionResult:
        """
        PSO + MCMC inversion
        
        Step 1: PSO finds global optimum θ*
        Step 2: MCMC samples posterior around θ*
        """
        # Default PSO configuration
        pso_defaults = {
            'n_particles': 30,
            'max_iter': 100,
            'w': 0.7,  # Inertia weight
            'c1': 1.5,  # Cognitive parameter
            'c2': 1.5,  # Social parameter
        }
        pso_defaults.update(pso_config)
        
        # Step 1: PSO global optimization
        print("Running PSO global optimization...")
        pso = PSO(
            objective_fn=energy_fn,
            bounds=self.priors.bounds(),
            **pso_defaults
        )
        theta_star, energy_star = pso.optimize()
        
        print(f"PSO converged: E(θ*) = {energy_star:.4f}")
        
        # Step 2: MCMC local sampling
        print("Running MCMC posterior sampling...")
        
        # Default MCMC configuration
        mcmc_defaults = {
            'n_samples': 5000,
            'n_burnin': 1000,
            'step_size': 0.01,
            'n_chains': 1,
        }
        mcmc_defaults.update(mcmc_config)
        
        sampler = MetropolisHastingsSampler(
            log_posterior_fn=lambda theta: -energy_fn(theta),  # Convert energy to log-posterior
            priors=self.priors,
            initial_state=theta_star
        )
        
        samples, diagnostics = sampler.sample(**mcmc_defaults)
        
        # Compute MAP estimate (mean of posterior samples)
        theta_map = {
            param: np.mean(samples[param])
            for param in self.priors.param_names
        }
        
        # Compute 95% credible intervals
        credible_intervals = {
            param: (
                np.percentile(samples[param], 2.5),
                np.percentile(samples[param], 97.5)
            )
            for param in self.priors.param_names
        }
        
        return InversionResult(
            theta_map=theta_map,
            posterior_samples=samples,
            credible_intervals=credible_intervals,
            log_posterior=-energy_fn(theta_map),
            convergence=diagnostics,
            method='pso_mcmc'
        )
    
    def _invert_map_grid(self, energy_fn: Callable) -> InversionResult:
        """
        MAP estimation via grid search
        
        Works well for 1-2 parameters, becomes expensive for higher dimensions
        """
        print("Running MAP grid search...")
        
        # Get parameter bounds
        bounds = self.priors.bounds()
        param_names = self.priors.param_names
        
        if len(param_names) > 2:
            warnings.warn(
                f"Grid search with {len(param_names)} parameters may be slow. "
                "Consider using method='pso_mcmc' instead."
            )
        
        # Create grid (100 points per dimension, adjust if needed)
        n_grid = 100 if len(param_names) == 1 else 50
        
        grids = {
            param: np.linspace(bounds[param][0], bounds[param][1], n_grid)
            for param in param_names
        }
        
        # Evaluate energy on grid
        best_energy = np.inf
        best_theta = None
        
        # Generate all combinations
        if len(param_names) == 1:
            param = param_names[0]
            for val in grids[param]:
                theta = {param: val}
                energy = energy_fn(theta)
                if energy < best_energy:
                    best_energy = energy
                    best_theta = theta
                    
        elif len(param_names) == 2:
            p1, p2 = param_names
            for val1 in grids[p1]:
                for val2 in grids[p2]:
                    theta = {p1: val1, p2: val2}
                    energy = energy_fn(theta)
                    if energy < best_energy:
                        best_energy = energy
                        best_theta = theta
        else:
            # For >2 parameters, use meshgrid (memory intensive!)
            grid_arrays = np.meshgrid(*[grids[p] for p in param_names], indexing='ij')
            flat_grids = [g.flatten() for g in grid_arrays]
            
            for i in range(len(flat_grids[0])):
                theta = {
                    param: flat_grids[j][i]
                    for j, param in enumerate(param_names)
                }
                energy = energy_fn(theta)
                if energy < best_energy:
                    best_energy = energy
                    best_theta = theta
        
        print(f"Grid search converged: E(θ_MAP) = {best_energy:.4f}")
        
        return InversionResult(
            theta_map=best_theta,
            posterior_samples=None,
            credible_intervals={},  # No uncertainty quantification in MAP
            log_posterior=-best_energy,
            convergence={},
            method='map_grid'
        )
    
    @staticmethod
    def _compute_laplacian(h: np.ndarray) -> np.ndarray:
        """
        Compute discrete 2D Laplacian: ∇²h ≈ (h[i+1,j] + h[i-1,j] + h[i,j+1] + h[i,j-1] - 4*h[i,j])
        
        Args:
            h: 2D array, shape (ny, nx)
            
        Returns:
            Laplacian, shape (ny-2, nx-2) (interior points only)
        """
        laplacian = (
            h[2:, 1:-1] + h[:-2, 1:-1] +  # Vertical neighbors
            h[1:-1, 2:] + h[1:-1, :-2] -  # Horizontal neighbors
            4 * h[1:-1, 1:-1]              # Center
        )
        return laplacian
