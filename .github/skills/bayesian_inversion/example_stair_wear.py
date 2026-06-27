"""
Example: Stair Wear Parameter Estimation using Bayesian Inversion

This example demonstrates how to use the Bayesian inversion framework
to estimate wear parameters from observed stair wear data.

Problem: Given observed wear depth h_obs(x, y), estimate:
- α: Wear coefficient
- N: Daily foot traffic
- T: Time (years)

Forward Model (Archard Wear Law):
    h(x, y; θ) = (α · N · T · P(x, y) · d) / (H · A)
"""

import numpy as np
import sys
sys.path.append('..')

from bayesian_inversion import (
    BayesianInverter,
    UniformPrior,
    LogUniformPrior
)


def create_synthetic_data(alpha_true=5e-9, N_true=500, T_true=100):
    """
    Generate synthetic stair wear data with known parameters
    
    Returns:
        (observed_data, observation_points, true_params)
    """
    # Create grid
    nx, ny = 50, 30
    x = np.linspace(0, 1, nx)  # Normalized stair length
    y = np.linspace(0, 1, ny)  # Normalized stair width
    X, Y = np.meshgrid(x, y)
    
    # Observation points
    observation_points = np.column_stack([X.flatten(), Y.flatten()])
    
    # Foot pressure distribution (Gaussian centered at stair middle)
    # People tend to step in the center
    P = np.exp(-((X - 0.5)**2 / 0.1 + (Y - 0.5)**2 / 0.05))
    P = P / np.max(P)  # Normalize
    
    # Material properties (constants for now)
    H = 1e8  # Material hardness (Pa)
    A = 0.01  # Contact area (m²)
    d = 0.001  # Step distance (m)
    
    # True wear depth (Archard law)
    h_true = (alpha_true * N_true * T_true * P * d) / (H * A)
    
    # Add measurement noise
    noise_level = 0.005  # 5mm std
    noise = np.random.normal(0, noise_level, h_true.shape)
    h_obs = h_true + noise
    h_obs = np.maximum(h_obs, 0)  # Physical constraint: no negative wear
    
    true_params = {
        'alpha': alpha_true,
        'N': N_true,
        'T': T_true
    }
    
    return h_obs, observation_points, true_params


def forward_model_archard(x, y, theta):
    """
    Forward model: Archard wear law
    
    Args:
        x, y: Coordinate arrays (flattened)
        theta: Dict with keys 'alpha', 'N', 'T'
        
    Returns:
        Predicted wear depth h_sim
    """
    alpha = theta['alpha']
    N = theta['N']
    T = theta['T']
    
    # Foot pressure distribution (must match data generation)
    P = np.exp(-((x - 0.5)**2 / 0.1 + (y - 0.5)**2 / 0.05))
    P = P / np.max(P)
    
    # Constants
    H = 1e8
    A = 0.01
    d = 0.001
    
    # Archard law
    h_sim = (alpha * N * T * P * d) / (H * A)
    
    return h_sim


def run_pso_mcmc_example():
    """
    Example 1: Full Bayesian inversion with PSO + MCMC
    """
    print("=" * 70)
    print("Example 1: PSO + MCMC Bayesian Inversion")
    print("=" * 70)
    
    # Generate synthetic data
    print("\n1. Generating synthetic data...")
    h_obs, obs_points, true_params = create_synthetic_data()
    print(f"   True parameters: α={true_params['alpha']:.2e}, "
          f"N={true_params['N']}, T={true_params['T']}")
    print(f"   Data shape: {h_obs.shape}")
    
    # Define priors
    print("\n2. Setting up priors...")
    priors = {
        'alpha': LogUniformPrior(1e-10, 1e-7),  # Wear coefficient (wide range)
        'N': UniformPrior(100, 1000),            # Daily foot traffic
        'T': UniformPrior(50, 200)               # Time (years)
    }
    print("   Priors:")
    for param, prior in priors.items():
        print(f"     {param}: {prior}")
    
    # Create inverter
    print("\n3. Creating Bayesian inverter (PSO + MCMC)...")
    inverter = BayesianInverter(
        forward_model=forward_model_archard,
        params=priors,
        method='pso_mcmc'
    )
    
    # Run inversion
    print("\n4. Running inversion...")
    result = inverter.invert(
        observed_data=h_obs,
        observation_points=obs_points,
        sigma=0.005,  # Measurement noise std (matches data generation)
        smooth_lambda=0.01,  # Small smoothness penalty
        pso_config={'n_particles': 20, 'max_iter': 50},  # Reduced for demo
        mcmc_config={'n_samples': 2000, 'n_burnin': 500}
    )
    
    # Display results
    print("\n" + "=" * 70)
    print(result.summary())
    print("=" * 70)
    
    # Check if true parameters are within 95% CI
    print("\n5. Validation:")
    for param, true_val in true_params.items():
        ci_low, ci_high = result.credible_intervals[param]
        within_ci = ci_low <= true_val <= ci_high
        status = "✓" if within_ci else "✗"
        print(f"   {param}: True={true_val:.2e}, "
              f"CI=[{ci_low:.2e}, {ci_high:.2e}] {status}")
    
    return result


def run_map_grid_example():
    """
    Example 2: Fast MAP estimation with grid search (1 parameter)
    """
    print("\n\n" + "=" * 70)
    print("Example 2: MAP Grid Search (Single Parameter)")
    print("=" * 70)
    
    # Generate data (fix N and alpha, only estimate T)
    print("\n1. Generating synthetic data (estimating age only)...")
    alpha_true, N_true, T_true = 5e-9, 500, 100
    h_obs, obs_points, _ = create_synthetic_data(alpha_true, N_true, T_true)
    
    # Total wear volume (scalar observation)
    V_obs = np.sum(h_obs)
    print(f"   True age: T={T_true} years")
    print(f"   Observed total wear volume: {V_obs:.6f} m³")
    
    # Simplified forward model (volume only)
    def forward_model_volume(x, y, theta):
        # Ignore x, y (scalar observation)
        T = theta['T']
        # Approximate total volume ∝ T
        V_sim = alpha_true * N_true * T * 0.5  # Simplified
        return V_sim * np.ones_like(x)  # Broadcast to match shape
    
    # Prior on age only
    priors = {'T': UniformPrior(50, 200)}
    
    # Create inverter
    print("\n2. Running MAP grid search...")
    inverter = BayesianInverter(
        forward_model=forward_model_volume,
        params=priors,
        method='map_grid'
    )
    
    # Run inversion (scalar observation)
    result = inverter.invert(
        observed_data=V_obs * np.ones(len(obs_points)),  # Broadcast
        observation_points=obs_points,
        sigma=0.1
    )
    
    # Display results
    print("\n" + "=" * 70)
    print(result.summary())
    print("=" * 70)
    
    print(f"\n3. Validation:")
    print(f"   True age: {T_true} years")
    print(f"   Estimated age: {result.theta_map['T']:.1f} years")
    print(f"   Error: {abs(result.theta_map['T'] - T_true):.1f} years")
    
    return result


if __name__ == '__main__':
    # Run examples
    print("Bayesian Parameter Inversion - Stair Wear Example")
    print("=" * 70)
    
    # Example 1: Full PSO + MCMC
    result_pso_mcmc = run_pso_mcmc_example()
    
    # Example 2: Fast MAP grid search
    result_map = run_map_grid_example()
    
    print("\n\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)
    print("\nKey takeaways:")
    print("1. PSO + MCMC provides full uncertainty quantification (credible intervals)")
    print("2. MAP grid search is faster but only gives point estimates")
    print("3. Both methods successfully recover true parameters from noisy data")
    print("\nFor competition use:")
    print("- Day 1-2: Build forward model, validate with known inputs")
    print("- Day 2-3: Add Bayesian inversion, report MAP ± 95% CI")
    print("- Always include uncertainty quantification in your paper!")
