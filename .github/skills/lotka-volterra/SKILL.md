---
name: lotka-volterra
description: Classic ecological models for predator-prey dynamics and interspecies competition. Coupled differential equations with phase plane analysis and stability theory. Essential for ecology, population dynamics, and market competition problems in MCM/ICM.
---

# Lotka-Volterra Models

Systems of coupled differential equations describing interactions between two species.

## When to Use

- **Predator-Prey Systems**: Wolf-deer, shark-fish, parasite-host dynamics.
- **Interspecies Competition**: Two species competing for the same resource.
- **Market Competition**: Two companies competing for market share.
- **Epidemic Interactions**: Host-pathogen dynamics (related to SIR models).
- **Symbiotic Relationships**: Mutualism or commensalism modeling.

## When NOT to Use

- **Single Species**: Use **`logistic-growth`** instead.
- **Three or More Species**: Requires generalized Lotka-Volterra (more complex).
- **Spatial Effects**: Use reaction-diffusion equations or agent-based models.
- **Stochastic Fluctuations**: Use stochastic differential equations.

## Model Types

### 1. Predator-Prey Model

#### Differential Equations
$$\begin{cases}
\frac{dx}{dt} = \alpha x - \beta xy \\
\frac{dy}{dt} = \delta xy - \gamma y
\end{cases}$$

Where:
- $x(t)$: Prey population
- $y(t)$: Predator population
- $\alpha$: Prey growth rate (birth rate in absence of predators)
- $\beta$: Predation rate (impact of predators on prey)
- $\delta$: Predator efficiency (conversion of prey to predator offspring)
- $\gamma$: Predator death rate (in absence of prey)

#### Key Properties
- **Equilibria**: $(0, 0)$ (trivial, unstable) and $(\frac{\gamma}{\delta}, \frac{\alpha}{\beta})$ (non-trivial, center)
- **Behavior**: Periodic oscillations around the non-trivial equilibrium
- **Conservation**: $V(x, y) = \delta x - \gamma \ln x + \beta y - \alpha \ln y$ is conserved

### 2. Competition Model

#### Differential Equations
$$\begin{cases}
\frac{dx}{dt} = r_1 x \left(1 - \frac{x + \alpha_{12} y}{K_1}\right) \\
\frac{dy}{dt} = r_2 y \left(1 - \frac{y + \alpha_{21} x}{K_2}\right)
\end{cases}$$

Where:
- $x(t)$, $y(t)$: Populations of species 1 and 2
- $r_1$, $r_2$: Intrinsic growth rates
- $K_1$, $K_2$: Carrying capacities (in absence of competition)
- $\alpha_{12}$: Effect of species 2 on species 1
- $\alpha_{21}$: Effect of species 1 on species 2

#### Key Properties
- **Coexistence Condition**: $\alpha_{12} < \frac{K_1}{K_2}$ and $\alpha_{21} < \frac{K_2}{K_1}$
- **Competitive Exclusion**: If conditions not met, one species drives the other to extinction
- **Equilibria**: Four possible (both extinct, each alone, coexistence)

## Implementation Template

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

class LotkaVolterraBase:
    """Base class for Lotka-Volterra models"""
    
    def __init__(self):
        self.params = None
        self.fitted = False
        
    def solve(self, initial_conditions, t_span, params=None):
        """
        Solve the ODE system numerically
        
        Args:
            initial_conditions (tuple): (x0, y0)
            t_span (array): Time points
            params (dict): Model parameters (uses fitted params if None)
            
        Returns:
            tuple: (x_solution, y_solution)
        """
        if params is None:
            if not self.fitted:
                raise ValueError("Model not fitted and no parameters provided.")
            params = self.params
        
        solution = odeint(self.equations, initial_conditions, t_span, args=(params,))
        return solution[:, 0], solution[:, 1]
    
    def equations(self, state, t, params):
        """Override in subclasses"""
        raise NotImplementedError

class PredatorPrey(LotkaVolterraBase):
    """
    Predator-Prey Lotka-Volterra Model
    """
    
    def equations(self, state, t, params):
        """
        dx/dt = alpha*x - beta*x*y
        dy/dt = delta*x*y - gamma*y
        """
        x, y = state
        alpha = params['alpha']  # Prey growth rate
        beta = params['beta']    # Predation rate
        delta = params['delta']  # Predator efficiency
        gamma = params['gamma']  # Predator death rate
        
        dx_dt = alpha * x - beta * x * y
        dy_dt = delta * x * y - gamma * y
        
        return [dx_dt, dy_dt]
    
    def get_equilibria(self, params=None):
        """
        Calculate equilibrium points
        
        Returns:
            list of tuples: [(x1, y1), (x2, y2), ...]
        """
        if params is None:
            params = self.params
        
        # Trivial equilibrium
        eq1 = (0, 0)
        
        # Non-trivial equilibrium
        x_star = params['gamma'] / params['delta']
        y_star = params['alpha'] / params['beta']
        eq2 = (x_star, y_star)
        
        return [eq1, eq2]
    
    def get_nullclines(self, x_range, params=None):
        """
        Calculate nullclines for phase plane
        
        Returns:
            dict: {'x_nullcline': array, 'y_nullcline': array}
        """
        if params is None:
            params = self.params
        
        # x nullcline: dx/dt = 0 => y = alpha/beta (horizontal line)
        x_nullcline = np.full_like(x_range, params['alpha'] / params['beta'])
        
        # y nullcline: dy/dt = 0 => x = gamma/delta (vertical line)
        y_nullcline_x = params['gamma'] / params['delta']
        
        return {
            'x_nullcline_y': x_nullcline,
            'y_nullcline_x': y_nullcline_x
        }
    
    def fit(self, t_data, x_data, y_data, initial_guess=None):
        """
        Fit model parameters to data
        
        Args:
            t_data (array): Time observations
            x_data (array): Prey observations
            y_data (array): Predator observations
            initial_guess (dict): Initial parameter values
        """
        if initial_guess is None:
            initial_guess = {
                'alpha': 1.0, 'beta': 0.1, 
                'delta': 0.075, 'gamma': 1.5
            }
        
        # Pack initial guess
        p0 = [initial_guess['alpha'], initial_guess['beta'], 
              initial_guess['delta'], initial_guess['gamma']]
        
        # Define residual function
        def model_func(t, alpha, beta, delta, gamma):
            params = {'alpha': alpha, 'beta': beta, 'delta': delta, 'gamma': gamma}
            x0, y0 = x_data[0], y_data[0]
            x_pred, y_pred = self.solve((x0, y0), t, params)
            # Flatten both x and y
            return np.concatenate([x_pred, y_pred])
        
        # Combined data
        data_combined = np.concatenate([x_data, y_data])
        
        try:
            params_opt, _ = curve_fit(
                model_func, t_data, data_combined, p0=p0,
                bounds=([0, 0, 0, 0], [np.inf, np.inf, np.inf, np.inf]),
                maxfev=10000
            )
            
            self.params = {
                'alpha': params_opt[0],
                'beta': params_opt[1],
                'delta': params_opt[2],
                'gamma': params_opt[3]
            }
            self.fitted = True
            
            return self.params
            
        except Exception as e:
            print(f"Fitting failed: {e}")
            return None

class Competition(LotkaVolterraBase):
    """
    Competition Lotka-Volterra Model
    """
    
    def equations(self, state, t, params):
        """
        dx/dt = r1*x*(1 - (x + alpha12*y)/K1)
        dy/dt = r2*y*(1 - (y + alpha21*x)/K2)
        """
        x, y = state
        r1 = params['r1']
        r2 = params['r2']
        K1 = params['K1']
        K2 = params['K2']
        alpha12 = params['alpha12']
        alpha21 = params['alpha21']
        
        dx_dt = r1 * x * (1 - (x + alpha12 * y) / K1)
        dy_dt = r2 * y * (1 - (y + alpha21 * x) / K2)
        
        return [dx_dt, dy_dt]
    
    def get_equilibria(self, params=None):
        """Calculate all equilibrium points"""
        if params is None:
            params = self.params
        
        r1, r2 = params['r1'], params['r2']
        K1, K2 = params['K1'], params['K2']
        a12, a21 = params['alpha12'], params['alpha21']
        
        equilibria = []
        
        # 1. Both extinct
        equilibria.append((0, 0))
        
        # 2. Only species 1
        equilibria.append((K1, 0))
        
        # 3. Only species 2
        equilibria.append((0, K2))
        
        # 4. Coexistence (if exists)
        denom = 1 - a12 * a21
        if abs(denom) > 1e-10:
            x_coex = (K1 - a12 * K2) / denom
            y_coex = (K2 - a21 * K1) / denom
            
            if x_coex > 0 and y_coex > 0:
                equilibria.append((x_coex, y_coex))
        
        return equilibria
    
    def check_coexistence(self, params=None):
        """
        Check if coexistence is possible
        
        Returns:
            dict: Coexistence analysis
        """
        if params is None:
            params = self.params
        
        K1, K2 = params['K1'], params['K2']
        a12, a21 = params['alpha12'], params['alpha21']
        
        # Coexistence conditions
        cond1 = a12 < K1 / K2
        cond2 = a21 < K2 / K1
        
        if cond1 and cond2:
            outcome = "Stable Coexistence"
        elif not cond1 and not cond2:
            outcome = "Bistability (depends on initial conditions)"
        elif cond1 and not cond2:
            outcome = "Species 1 wins (competitive exclusion)"
        else:
            outcome = "Species 2 wins (competitive exclusion)"
        
        return {
            'condition1': cond1,
            'condition2': cond2,
            'outcome': outcome
        }

def plot_predator_prey(model, t_span, initial_conditions, title='Predator-Prey Dynamics'):
    """
    Comprehensive visualization for predator-prey model
    """
    x, y = model.solve(initial_conditions, t_span)
    equilibria = model.get_equilibria()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Time series
    ax1 = axes[0]
    ax1.plot(t_span, x, 'b-', linewidth=2, label='Prey (x)')
    ax1.plot(t_span, y, 'r-', linewidth=2, label='Predator (y)')
    ax1.set_xlabel('Time', fontsize=12)
    ax1.set_ylabel('Population', fontsize=12)
    ax1.set_title('Population Dynamics Over Time', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Phase plane
    ax2 = axes[1]
    ax2.plot(x, y, 'purple', linewidth=2, label='Trajectory')
    ax2.plot(x[0], y[0], 'go', markersize=10, label='Initial')
    
    # Plot equilibria
    for i, (x_eq, y_eq) in enumerate(equilibria):
        if x_eq > 0 and y_eq > 0:
            ax2.plot(x_eq, y_eq, 'r*', markersize=15, label=f'Equilibrium ({x_eq:.2f}, {y_eq:.2f})')
    
    # Nullclines
    x_range = np.linspace(0, max(x) * 1.2, 100)
    nullclines = model.get_nullclines(x_range)
    ax2.axhline(nullclines['x_nullcline_y'][0], color='blue', linestyle='--', 
                alpha=0.5, label='Prey nullcline')
    ax2.axvline(nullclines['y_nullcline_x'], color='red', linestyle='--', 
                alpha=0.5, label='Predator nullcline')
    
    ax2.set_xlabel('Prey Population (x)', fontsize=12)
    ax2.set_ylabel('Predator Population (y)', fontsize=12)
    ax2.set_title('Phase Plane', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('predator_prey_analysis.png', dpi=300)
    plt.show()

def plot_competition(model, t_span, initial_conditions_list, title='Competition Dynamics'):
    """
    Visualization for competition model with multiple initial conditions
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Phase plane with multiple trajectories
    ax1 = axes[0]
    
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    for i, ic in enumerate(initial_conditions_list):
        x, y = model.solve(ic, t_span)
        ax1.plot(x, y, color=colors[i % len(colors)], linewidth=2, 
                label=f'IC: ({ic[0]}, {ic[1]})')
        ax1.plot(ic[0], ic[1], 'o', color=colors[i % len(colors)], markersize=8)
    
    # Plot equilibria
    equilibria = model.get_equilibria()
    for x_eq, y_eq in equilibria:
        if x_eq >= 0 and y_eq >= 0:
            ax1.plot(x_eq, y_eq, 'k*', markersize=15)
            ax1.annotate(f'({x_eq:.1f}, {y_eq:.1f})', 
                        xy=(x_eq, y_eq), xytext=(5, 5),
                        textcoords='offset points', fontsize=9)
    
    ax1.set_xlabel('Species 1 Population', fontsize=12)
    ax1.set_ylabel('Species 2 Population', fontsize=12)
    ax1.set_title('Phase Plane (Multiple Initial Conditions)', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # 2. Time series for one trajectory
    ax2 = axes[1]
    x, y = model.solve(initial_conditions_list[0], t_span)
    ax2.plot(t_span, x, 'b-', linewidth=2, label='Species 1')
    ax2.plot(t_span, y, 'r-', linewidth=2, label='Species 2')
    ax2.set_xlabel('Time', fontsize=12)
    ax2.set_ylabel('Population', fontsize=12)
    ax2.set_title('Population Dynamics Over Time', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('competition_analysis.png', dpi=300)
    plt.show()

# --- Usage Example ---
if __name__ == "__main__":
    # ========== PREDATOR-PREY MODEL ==========
    print("=" * 60)
    print("PREDATOR-PREY MODEL")
    print("=" * 60)
    
    # Initialize model
    pp_model = PredatorPrey()
    pp_model.params = {
        'alpha': 1.0,   # Prey birth rate
        'beta': 0.1,    # Predation rate
        'delta': 0.075, # Predator efficiency
        'gamma': 1.5    # Predator death rate
    }
    pp_model.fitted = True
    
    # Equilibria
    equilibria = pp_model.get_equilibria()
    print("\nEquilibrium Points:")
    for i, (x_eq, y_eq) in enumerate(equilibria):
        print(f"  Equilibrium {i+1}: Prey={x_eq:.2f}, Predator={y_eq:.2f}")
    
    # Solve
    t_span = np.linspace(0, 50, 1000)
    initial_conditions = (10, 5)  # Initial prey and predator
    
    x, y = pp_model.solve(initial_conditions, t_span)
    
    print(f"\nPopulation ranges:")
    print(f"  Prey: {x.min():.2f} - {x.max():.2f}")
    print(f"  Predator: {y.min():.2f} - {y.max():.2f}")
    
    # Visualize
    plot_predator_prey(pp_model, t_span, initial_conditions)
    
    # ========== COMPETITION MODEL ==========
    print("\n" + "=" * 60)
    print("COMPETITION MODEL")
    print("=" * 60)
    
    comp_model = Competition()
    comp_model.params = {
        'r1': 1.0,      # Species 1 growth rate
        'r2': 1.0,      # Species 2 growth rate
        'K1': 100,      # Species 1 carrying capacity
        'K2': 80,       # Species 2 carrying capacity
        'alpha12': 0.8, # Effect of species 2 on 1
        'alpha21': 0.6  # Effect of species 1 on 2
    }
    comp_model.fitted = True
    
    # Check coexistence
    coex_analysis = comp_model.check_coexistence()
    print("\nCoexistence Analysis:")
    print(f"  Condition 1 (alpha12 < K1/K2): {coex_analysis['condition1']}")
    print(f"  Condition 2 (alpha21 < K2/K1): {coex_analysis['condition2']}")
    print(f"  Outcome: {coex_analysis['outcome']}")
    
    # Equilibria
    equilibria = comp_model.get_equilibria()
    print("\nEquilibrium Points:")
    for i, (x_eq, y_eq) in enumerate(equilibria):
        print(f"  Equilibrium {i+1}: Species1={x_eq:.2f}, Species2={y_eq:.2f}")
    
    # Solve with multiple initial conditions
    t_span = np.linspace(0, 50, 1000)
    initial_conditions_list = [
        (10, 10), (50, 20), (20, 50), (80, 5), (5, 70)
    ]
    
    # Visualize
    plot_competition(comp_model, t_span, initial_conditions_list)
```

## Extensions

### 1. Predator-Prey with Logistic Prey Growth
$$\begin{cases}
\frac{dx}{dt} = rx(1 - \frac{x}{K}) - \beta xy \\
\frac{dy}{dt} = \delta xy - \gamma y
\end{cases}$$

Removes unrealistic unbounded prey growth.

### 2. Holling Type II Functional Response
$$\frac{dx}{dt} = \alpha x - \frac{\beta xy}{1 + \beta h x}$$

Where $h$ is handling time (more realistic predation).

### 3. Three-Species Model
Add a third species (e.g., super-predator or resource).

## Common Pitfalls

1.  **Wrong Parameter Scale**: Parameters must be positive. Check units (e.g., per year vs per day).
2.  **Stiff Equations**: Use `scipy.integrate.solve_ivp` with `method='BDF'` for stiff systems.
3.  **Ignoring Nullclines**: Always plot nullclines to understand phase plane structure.
4.  **No Stability Analysis**: Report whether equilibria are stable, unstable, or centers.
5.  **Overfitting**: With 4-6 parameters, easy to overfit noisy data. Use regularization or Bayesian methods.

## Integration Workflow

- **Input**: Use **`data-cleaner`** to preprocess population time series.
- **Parameter Estimation**: Use **`automated-sweep`** for grid search if `curve_fit` fails.
- **Sensitivity**: Use **`sensitivity-master`** to identify which parameters most affect dynamics.
- **Robustness**: Use **`robustness-check`** to test stability under parameter perturbations.
- **Comparison**: Compare with **`logistic-growth`** (single species) to show interaction effects.

## Output Requirements for Paper

1.  **Model Equations**: Display the coupled ODE system.
2.  **Parameter Values**: "We estimated α=1.0, β=0.1, δ=0.075, γ=1.5 from data."
3.  **Equilibrium Analysis**: "The system has a non-trivial equilibrium at (20, 10)."
4.  **Stability**: "Eigenvalue analysis shows the equilibrium is a center (purely imaginary eigenvalues), resulting in periodic oscillations."
5.  **Phase Plane**: Show nullclines, equilibria, and trajectories.
6.  **Ecological Interpretation**: "The oscillations have a period of ~15 years, consistent with observed lynx-hare cycles."

## Decision Guide: Which Lotka-Volterra Model?

| Scenario | Model Type |
|----------|------------|
| One eats the other | Predator-Prey |
| Both compete for same resource | Competition |
| Both benefit from each other | Mutualism (modify signs) |
| One benefits, other unaffected | Commensalism (set one interaction to 0) |
| Market share dynamics | Competition (economic interpretation) |
