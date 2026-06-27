---
name: differential-equations
description: Unified framework for mechanistic modeling using ODEs and PDEs. Provides model library, parameter estimation, stability analysis, phase plane visualization, and bifurcation analysis. Integrates logistic-growth, lotka-volterra, and reaction-diffusion models into a cohesive workflow.
---

# Differential Equations Framework

A comprehensive toolkit for building, analyzing, and solving differential equation models in MCM/ICM competitions.

## When to Use

- **Mechanistic Modeling**: When you understand the underlying mechanisms (not just fitting data).
- **State Evolution**: Describing how quantities change over time based on their current state.
- **Physical Laws**: Conservation laws, reaction kinetics, population dynamics.
- **Interpretability Required**: Need to explain why the model works (not just black-box prediction).

## Model Hierarchy

```
Differential Equations (this skill)
├── ODE Models (time only)
│   ├── Single Species
│   │   └── Logistic Growth (logistic-growth skill)
│   ├── Multi-Species
│   │   ├── Predator-Prey (lotka-volterra skill)
│   │   └── Competition (lotka-volterra skill)
│   └── Epidemiology
│       ├── SIR
│       └── SEIR
└── PDE Models (time + space)
    ├── Reaction-Diffusion (reaction-diffusion skill)
    │   ├── Fisher-KPP
    │   ├── Gray-Scott
    │   └── SIR Spatial
    └── Advection-Diffusion
```

## Workflow Overview

```
1. Problem Analysis
   ├── Identify state variables
   ├── Identify parameters
   └── Determine spatial structure

2. Model Selection
   ├── Use model library (Logistic, Lotka-Volterra, etc.)
   └── Or define custom equations

3. Parameter Estimation
   ├── Fit to data (curve_fit, least squares)
   └── Or use literature values

4. Model Analysis
   ├── Equilibrium points
   ├── Stability analysis (Jacobian, eigenvalues)
   ├── Phase plane visualization
   └── Bifurcation analysis

5. Validation & Prediction
   ├── Compare with data (R², RMSE)
   ├── Sensitivity analysis (sensitivity-master)
   ├── Robustness check (robustness-check)
   └── Generate forecasts

6. Documentation
   ├── Write equations in LaTeX (latex-transformer)
   └── Create publication figures (visual-engineer)
```

## Implementation Template

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, solve_ivp
from scipy.optimize import curve_fit, fsolve
from scipy.linalg import eig
import warnings
warnings.filterwarnings('ignore')

# ========== CORE FRAMEWORK ==========

class ODEModel:
    """
    Base class for ODE models
    """
    
    def __init__(self, name="Custom ODE"):
        self.name = name
        self.params = {}
        self.state_vars = []
        self.param_names = []
        
    def equations(self, state, t, params):
        """
        Override this method to define your ODE system
        
        Args:
            state (array): Current state [x1, x2, ...]
            t (float): Current time
            params (dict): Model parameters
            
        Returns:
            array: Derivatives [dx1/dt, dx2/dt, ...]
        """
        raise NotImplementedError("Must implement equations() method")
    
    def solve(self, initial_state, t_span, params=None):
        """
        Solve the ODE system
        
        Args:
            initial_state (array): Initial conditions
            t_span (array): Time points
            params (dict): Parameters (uses self.params if None)
            
        Returns:
            array: Solution [time_points, state_variables]
        """
        if params is None:
            params = self.params
        
        solution = odeint(self.equations, initial_state, t_span, args=(params,))
        return solution
    
    def find_equilibria(self, search_ranges, params=None):
        """
        Find equilibrium points numerically
        
        Args:
            search_ranges (list of tuples): [(x1_min, x1_max), (x2_min, x2_max), ...]
            params (dict): Model parameters
            
        Returns:
            list: Equilibrium points
        """
        if params is None:
            params = self.params
        
        def equilibrium_condition(state):
            return self.equations(state, 0, params)
        
        equilibria = []
        
        # Grid search for initial guesses
        n_dim = len(search_ranges)
        n_points = 10
        
        grids = [np.linspace(r[0], r[1], n_points) for r in search_ranges]
        
        if n_dim == 1:
            initial_guesses = [[x] for x in grids[0]]
        elif n_dim == 2:
            X, Y = np.meshgrid(grids[0], grids[1])
            initial_guesses = np.column_stack([X.ravel(), Y.ravel()])
        else:
            # For higher dimensions, use random sampling
            initial_guesses = [
                [np.random.uniform(r[0], r[1]) for r in search_ranges]
                for _ in range(50)
            ]
        
        for guess in initial_guesses:
            try:
                eq = fsolve(equilibrium_condition, guess, full_output=True)
                if eq[2] == 1:  # Solution found
                    point = eq[0]
                    # Check if already found (avoid duplicates)
                    is_new = True
                    for existing in equilibria:
                        if np.allclose(point, existing, atol=1e-3):
                            is_new = False
                            break
                    if is_new and all(search_ranges[i][0] <= point[i] <= search_ranges[i][1] 
                                     for i in range(len(point))):
                        equilibria.append(point)
            except:
                pass
        
        return equilibria
    
    def jacobian(self, state, params=None):
        """
        Compute Jacobian matrix numerically
        
        Returns:
            array: Jacobian matrix
        """
        if params is None:
            params = self.params
        
        eps = 1e-8
        n = len(state)
        jac = np.zeros((n, n))
        
        f0 = self.equations(state, 0, params)
        
        for i in range(n):
            state_perturbed = state.copy()
            state_perturbed[i] += eps
            f_perturbed = self.equations(state_perturbed, 0, params)
            jac[:, i] = (f_perturbed - f0) / eps
        
        return jac
    
    def stability_analysis(self, equilibrium, params=None):
        """
        Analyze stability of an equilibrium point
        
        Returns:
            dict: Eigenvalues, eigenvectors, and stability classification
        """
        if params is None:
            params = self.params
        
        J = self.jacobian(equilibrium, params)
        eigenvalues, eigenvectors = eig(J)
        
        # Classify stability
        real_parts = np.real(eigenvalues)
        imag_parts = np.imag(eigenvalues)
        
        if all(real_parts < 0):
            stability = "Stable (Sink)"
        elif all(real_parts > 0):
            stability = "Unstable (Source)"
        elif any(real_parts == 0) and all(real_parts <= 0):
            if any(imag_parts != 0):
                stability = "Center (Periodic)"
            else:
                stability = "Marginally Stable"
        else:
            stability = "Saddle Point"
        
        return {
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'stability': stability,
            'jacobian': J
        }
    
    def fit(self, t_data, state_data, initial_guess):
        """
        Fit model parameters to data
        
        Args:
            t_data (array): Time observations
            state_data (array): State observations [time_points, state_variables]
            initial_guess (dict): Initial parameter values
            
        Returns:
            dict: Fitted parameters
        """
        # Flatten state data
        data_flat = state_data.flatten()
        
        # Parameter names and initial values
        param_names = list(initial_guess.keys())
        p0 = [initial_guess[name] for name in param_names]
        
        # Define model function for curve_fit
        def model_func(t, *params):
            param_dict = dict(zip(param_names, params))
            initial_state = state_data[0]
            solution = self.solve(initial_state, t, param_dict)
            return solution.flatten()
        
        try:
            params_opt, _ = curve_fit(
                model_func, t_data, data_flat, p0=p0,
                bounds=([0]*len(p0), [np.inf]*len(p0)),
                maxfev=10000
            )
            
            self.params = dict(zip(param_names, params_opt))
            return self.params
            
        except Exception as e:
            print(f"Fitting failed: {e}")
            return None

# ========== MODEL LIBRARY ==========

class LogisticModel(ODEModel):
    """Logistic growth model (wraps logistic-growth skill)"""
    
    def __init__(self):
        super().__init__("Logistic Growth")
        self.state_vars = ['N']
        self.param_names = ['r', 'K']
        
    def equations(self, state, t, params):
        N = state[0]
        r = params['r']
        K = params['K']
        
        dN_dt = r * N * (1 - N / K)
        return [dN_dt]

class PredatorPreyModel(ODEModel):
    """Predator-Prey model (wraps lotka-volterra skill)"""
    
    def __init__(self):
        super().__init__("Predator-Prey (Lotka-Volterra)")
        self.state_vars = ['prey', 'predator']
        self.param_names = ['alpha', 'beta', 'delta', 'gamma']
        
    def equations(self, state, t, params):
        x, y = state
        alpha = params['alpha']
        beta = params['beta']
        delta = params['delta']
        gamma = params['gamma']
        
        dx_dt = alpha * x - beta * x * y
        dy_dt = delta * x * y - gamma * y
        
        return [dx_dt, dy_dt]

class CompetitionModel(ODEModel):
    """Competition model (wraps lotka-volterra skill)"""
    
    def __init__(self):
        super().__init__("Competition (Lotka-Volterra)")
        self.state_vars = ['species1', 'species2']
        self.param_names = ['r1', 'r2', 'K1', 'K2', 'alpha12', 'alpha21']
        
    def equations(self, state, t, params):
        x, y = state
        r1 = params['r1']
        r2 = params['r2']
        K1 = params['K1']
        K2 = params['K2']
        a12 = params['alpha12']
        a21 = params['alpha21']
        
        dx_dt = r1 * x * (1 - (x + a12 * y) / K1)
        dy_dt = r2 * y * (1 - (y + a21 * x) / K2)
        
        return [dx_dt, dy_dt]

class SIRModel(ODEModel):
    """SIR epidemic model"""
    
    def __init__(self):
        super().__init__("SIR Epidemic Model")
        self.state_vars = ['S', 'I', 'R']
        self.param_names = ['beta', 'gamma', 'N']
        
    def equations(self, state, t, params):
        S, I, R = state
        beta = params['beta']  # Transmission rate
        gamma = params['gamma']  # Recovery rate
        N = params['N']  # Total population
        
        dS_dt = -beta * S * I / N
        dI_dt = beta * S * I / N - gamma * I
        dR_dt = gamma * I
        
        return [dS_dt, dI_dt, dR_dt]
    
    def basic_reproduction_number(self):
        """Calculate R0 = beta / gamma"""
        return self.params['beta'] / self.params['gamma']

# ========== VISUALIZATION TOOLS ==========

def plot_phase_plane_2d(model, state_ranges, params=None, n_trajectories=5):
    """
    Plot 2D phase plane with nullclines and trajectories
    
    Args:
        model (ODEModel): 2D ODE model
        state_ranges (list): [(x_min, x_max), (y_min, y_max)]
        params (dict): Model parameters
        n_trajectories (int): Number of trajectories to plot
    """
    if params is None:
        params = model.params
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create grid
    x_range = np.linspace(state_ranges[0][0], state_ranges[0][1], 20)
    y_range = np.linspace(state_ranges[1][0], state_ranges[1][1], 20)
    X, Y = np.meshgrid(x_range, y_range)
    
    # Compute vector field
    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            derivatives = model.equations([X[i, j], Y[i, j]], 0, params)
            U[i, j] = derivatives[0]
            V[i, j] = derivatives[1]
    
    # Normalize for better visualization
    M = np.sqrt(U**2 + V**2)
    M[M == 0] = 1
    U_norm = U / M
    V_norm = V / M
    
    # Plot vector field
    ax.quiver(X, Y, U_norm, V_norm, M, cmap='coolwarm', alpha=0.6)
    
    # Find and plot equilibria
    equilibria = model.find_equilibria(state_ranges, params)
    for eq in equilibria:
        stability_info = model.stability_analysis(eq, params)
        color = 'green' if 'Stable' in stability_info['stability'] else 'red'
        ax.plot(eq[0], eq[1], 'o', color=color, markersize=12, 
               label=f"Equilibrium: {stability_info['stability']}")
    
    # Plot sample trajectories
    t_span = np.linspace(0, 20, 500)
    for _ in range(n_trajectories):
        x0 = np.random.uniform(state_ranges[0][0], state_ranges[0][1])
        y0 = np.random.uniform(state_ranges[1][0], state_ranges[1][1])
        
        solution = model.solve([x0, y0], t_span, params)
        ax.plot(solution[:, 0], solution[:, 1], 'b-', alpha=0.5, linewidth=1.5)
        ax.plot(x0, y0, 'ko', markersize=5)
    
    ax.set_xlabel(model.state_vars[0], fontsize=12)
    ax.set_ylabel(model.state_vars[1], fontsize=12)
    ax.set_title(f'Phase Plane: {model.name}', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('phase_plane_analysis.png', dpi=300)
    plt.show()

def plot_bifurcation_diagram(model, param_name, param_range, initial_state, 
                             state_index=0, transient=100):
    """
    Create bifurcation diagram showing how equilibria change with parameter
    
    Args:
        model (ODEModel): ODE model
        param_name (str): Parameter to vary
        param_range (array): Range of parameter values
        initial_state (array): Initial condition
        state_index (int): Which state variable to plot
        transient (int): Time steps to skip (transient behavior)
    """
    equilibria_values = []
    
    for param_value in param_range:
        # Update parameter
        params = model.params.copy()
        params[param_name] = param_value
        
        # Solve for long time
        t_span = np.linspace(0, 200, 2000)
        solution = model.solve(initial_state, t_span, params)
        
        # Extract values after transient
        final_values = solution[transient:, state_index]
        
        # Store unique values (for periodic or chaotic behavior)
        unique_vals = np.unique(np.round(final_values, 3))
        equilibria_values.append((param_value, unique_vals))
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for param_val, eq_vals in equilibria_values:
        ax.plot([param_val] * len(eq_vals), eq_vals, 'b.', markersize=1)
    
    ax.set_xlabel(f'Parameter: {param_name}', fontsize=12)
    ax.set_ylabel(f'Equilibrium {model.state_vars[state_index]}', fontsize=12)
    ax.set_title('Bifurcation Diagram', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('bifurcation_diagram.png', dpi=300)
    plt.show()

# ========== USAGE EXAMPLES ==========

def example_logistic():
    """Example: Logistic growth"""
    print("=" * 60)
    print("EXAMPLE 1: LOGISTIC GROWTH")
    print("=" * 60)
    
    model = LogisticModel()
    model.params = {'r': 0.5, 'K': 100}
    
    # Solve
    t_span = np.linspace(0, 20, 200)
    solution = model.solve([10], t_span)
    
    # Find equilibria
    equilibria = model.find_equilibria([(0, 150)], model.params)
    print(f"\nEquilibrium points: {equilibria}")
    
    # Stability analysis
    for eq in equilibria:
        if eq[0] > 0:
            stability = model.stability_analysis(eq)
            print(f"\nEquilibrium N={eq[0]:.2f}:")
            print(f"  Eigenvalues: {stability['eigenvalues']}")
            print(f"  Stability: {stability['stability']}")
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(t_span, solution[:, 0], 'b-', linewidth=2, label='Population')
    plt.axhline(model.params['K'], color='r', linestyle='--', label='Carrying Capacity K')
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Population (N)', fontsize=12)
    plt.title('Logistic Growth Model', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('logistic_example.png', dpi=300)
    plt.show()

def example_predator_prey():
    """Example: Predator-Prey with phase plane"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: PREDATOR-PREY (PHASE PLANE)")
    print("=" * 60)
    
    model = PredatorPreyModel()
    model.params = {
        'alpha': 1.0,
        'beta': 0.1,
        'delta': 0.075,
        'gamma': 1.5
    }
    
    # Phase plane analysis
    state_ranges = [(0, 30), (0, 15)]
    plot_phase_plane_2d(model, state_ranges, n_trajectories=8)

def example_sir():
    """Example: SIR epidemic model"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: SIR EPIDEMIC MODEL")
    print("=" * 60)
    
    model = SIRModel()
    model.params = {
        'beta': 0.5,   # Transmission rate
        'gamma': 0.1,  # Recovery rate
        'N': 1000      # Total population
    }
    
    # Calculate R0
    R0 = model.basic_reproduction_number()
    print(f"\nBasic Reproduction Number R0 = {R0:.2f}")
    
    if R0 > 1:
        print("⚠️  Epidemic will spread (R0 > 1)")
    else:
        print("✅ Epidemic will die out (R0 < 1)")
    
    # Solve
    initial_state = [990, 10, 0]  # S, I, R
    t_span = np.linspace(0, 100, 1000)
    solution = model.solve(initial_state, t_span)
    
    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Time series
    ax1 = axes[0]
    ax1.plot(t_span, solution[:, 0], 'b-', label='Susceptible', linewidth=2)
    ax1.plot(t_span, solution[:, 1], 'r-', label='Infected', linewidth=2)
    ax1.plot(t_span, solution[:, 2], 'g-', label='Recovered', linewidth=2)
    ax1.set_xlabel('Time (days)', fontsize=12)
    ax1.set_ylabel('Population', fontsize=12)
    ax1.set_title(f'SIR Model (R0={R0:.2f})', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Phase plane (S vs I)
    ax2 = axes[1]
    ax2.plot(solution[:, 0], solution[:, 1], 'purple', linewidth=2)
    ax2.plot(solution[0, 0], solution[0, 1], 'go', markersize=10, label='Start')
    ax2.plot(solution[-1, 0], solution[-1, 1], 'ro', markersize=10, label='End')
    ax2.set_xlabel('Susceptible (S)', fontsize=12)
    ax2.set_ylabel('Infected (I)', fontsize=12)
    ax2.set_title('Phase Plane (S vs I)', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('sir_example.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    # Run examples
    example_logistic()
    example_predator_prey()
    example_sir()
    
    print("\n" + "=" * 60)
    print("DIFFERENTIAL EQUATIONS FRAMEWORK DEMO COMPLETE")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - logistic_example.png")
    print("  - phase_plane_analysis.png")
    print("  - sir_example.png")
```

## Integration with Existing Skills

### Workflow: From Simple to Complex

```python
# Step 1: Start with simple ODE (logistic-growth)
from logistic_growth import LogisticGrowth
simple_model = LogisticGrowth()
simple_model.fit_nonlinear(t_data, N_data)

# Step 2: Upgrade to multi-species (lotka-volterra)
from lotka_volterra import PredatorPrey
complex_model = PredatorPrey()
complex_model.fit(t_data, prey_data, predator_data)

# Step 3: Add spatial dimension (reaction-diffusion)
from reaction_diffusion import ReactionDiffusion1D
spatial_model = ReactionDiffusion1D(L=100, N=200, D=0.1, reaction_func=logistic_reaction)
spatial_model.solve(u0, T=50)

# Step 4: Use unified framework for analysis
from differential_equations import ODEModel
unified_model = PredatorPreyModel()
unified_model.params = complex_model.params
equilibria = unified_model.find_equilibria([(0, 50), (0, 20)])
stability = unified_model.stability_analysis(equilibria[1])
```

## Model Selection Guide

| Problem Characteristics | Recommended Model | Skill to Use |
|------------------------|-------------------|--------------|
| Single species, no space | Logistic | **`logistic-growth`** |
| Two species interact, no space | Lotka-Volterra | **`lotka-volterra`** |
| Single species, spatial spread | Fisher-KPP | **`reaction-diffusion`** |
| Disease spread, no space | SIR/SEIR | **`differential-equations`** (SIR) |
| Disease spread, spatial | SIR-PDE | **`reaction-diffusion`** (SIR spatial) |
| Pattern formation | Gray-Scott | **`reaction-diffusion`** (Gray-Scott) |
| Custom mechanism | Define equations | **`differential-equations`** (ODEModel) |

## Common Analysis Workflow

### 1. Model Building
```python
# Option A: Use pre-defined model
model = PredatorPreyModel()

# Option B: Define custom model
class CustomModel(ODEModel):
    def equations(self, state, t, params):
        # Your equations here
        return derivatives
```

### 2. Parameter Estimation
```python
# Fit to data
initial_guess = {'r': 0.5, 'K': 100}
model.fit(t_data, state_data, initial_guess)
```

### 3. Equilibrium Analysis
```python
# Find equilibria
equilibria = model.find_equilibria(search_ranges)

# Analyze stability
for eq in equilibria:
    stability = model.stability_analysis(eq)
    print(f"Equilibrium: {eq}, Stability: {stability['stability']}")
```

### 4. Visualization
```python
# Phase plane (2D models)
plot_phase_plane_2d(model, state_ranges)

# Bifurcation diagram
plot_bifurcation_diagram(model, 'r', np.linspace(0.1, 2.0, 100), initial_state)
```

### 5. Sensitivity Analysis
```python
# Use sensitivity-master skill
from sensitivity_master import sobol_analyze
# Analyze how parameters affect equilibria or dynamics
```

## Common Pitfalls

1.  **Stiff Equations**: Use `solve_ivp` with `method='BDF'` instead of `odeint`.
2.  **Multiple Equilibria**: Always search entire state space, not just near origin.
3.  **Numerical Jacobian**: May be inaccurate near discontinuities. Use analytical if possible.
4.  **Overfitting**: With many parameters, easy to overfit. Use cross-validation or AIC/BIC.
5.  **Ignoring Units**: Always check dimensional consistency (e.g., $[r] = \text{time}^{-1}$).

## Output Requirements for Paper

1.  **Model Equations**: Display full ODE/PDE system with parameter definitions.
2.  **Parameter Table**: List all parameters with values, units, and sources.
3.  **Equilibrium Analysis**: State all equilibria and their stability.
4.  **Phase Plane**: For 2D systems, show nullclines, equilibria, and trajectories.
5.  **Validation**: Compare model predictions with data (R², RMSE).
6.  **Sensitivity**: Show which parameters most affect model behavior.

## Advanced Topics

### 1. Stochastic Differential Equations (SDEs)
Add noise to model uncertainty:
$$dX = f(X, t)dt + g(X, t)dW$$

### 2. Delay Differential Equations (DDEs)
Account for time lags:
$$\frac{dN}{dt} = rN(t)(1 - \frac{N(t-\tau)}{K})$$

### 3. Hybrid Models
Combine discrete events with continuous dynamics (e.g., vaccination campaigns in SIR).

## Decision Tree: Which Framework?

```
Start
├── Spatial structure important?
│   ├── Yes → reaction-diffusion skill
│   └── No → Continue
├── Number of species/compartments?
│   ├── 1 → logistic-growth skill
│   ├── 2 → lotka-volterra skill
│   └── 3+ or custom → differential-equations skill (define custom)
└── Need advanced analysis? (bifurcation, Lyapunov)
    └── Yes → differential-equations skill (full framework)
```

## Summary: Skill Integration

This **`differential-equations`** skill serves as:
1.  **Unified Interface**: Common API for all ODE models.
2.  **Model Library**: Pre-built Logistic, Lotka-Volterra, SIR models.
3.  **Analysis Toolkit**: Equilibrium, stability, phase plane, bifurcation.
4.  **Bridge**: Connects specialized skills (logistic-growth, lotka-volterra, reaction-diffusion) into cohesive workflow.

**When to use each skill:**
- **Quick prototyping**: Use specialized skills directly (logistic-growth, etc.)
- **Advanced analysis**: Use differential-equations framework
- **Spatial problems**: Use reaction-diffusion skill
- **Custom models**: Extend differential-equations ODEModel class
