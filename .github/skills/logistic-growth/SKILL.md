---
name: logistic-growth
description: Classic mechanistic model for growth under resource constraints. S-shaped curve with interpretable parameters (growth rate r, carrying capacity K). Essential for population dynamics, epidemiology, and market saturation problems in MCM/ICM.
---

# Logistic Growth Model

A differential equation-based model describing growth that slows as it approaches a maximum capacity.

## When to Use

- **Population Dynamics**: Human/animal populations with limited resources.
- **Epidemiology**: Disease spread with finite susceptible population (related to SIR models).
- **Market Penetration**: Product adoption reaching saturation.
- **Biological Growth**: Tumor growth, bacterial colonies with nutrient limits.
- **Technology Diffusion**: Innovation adoption following S-curve.

## When NOT to Use

- **Unlimited Resources**: Use exponential growth instead.
- **Oscillating Systems**: Use predator-prey models (Lotka-Volterra).
- **Multiple Competing Species**: Use competitive Lotka-Volterra.
- **Stochastic Effects Dominant**: Use agent-based models or stochastic differential equations.

## Mathematical Foundation

### Differential Equation
$$\frac{dN}{dt} = rN\left(1 - \frac{N}{K}\right)$$

Where:
- $N(t)$: Population at time $t$
- $r$: Intrinsic growth rate (per capita growth rate when $N \to 0$)
- $K$: Carrying capacity (maximum sustainable population)

### Analytical Solution
$$N(t) = \frac{K}{1 + \left(\frac{K - N_0}{N_0}\right)e^{-rt}}$$

Where $N_0 = N(0)$ is the initial population.

### Key Properties
1. **Inflection Point**: Occurs at $N = K/2$, time $t^* = \frac{1}{r}\ln\left(\frac{K - N_0}{N_0}\right)$
2. **Maximum Growth Rate**: $\frac{dN}{dt}\big|_{max} = \frac{rK}{4}$ at the inflection point
3. **Stability**: $N = K$ is a stable equilibrium; $N = 0$ is unstable

## Implementation Template

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

class LogisticGrowth:
    """
    Logistic growth model with parameter estimation and visualization
    """
    
    def __init__(self):
        self.r = None  # Growth rate
        self.K = None  # Carrying capacity
        self.N0 = None  # Initial population
        self.fitted = False
        
    def analytical_solution(self, t, N0, r, K):
        """
        Analytical solution of logistic equation
        
        Args:
            t (array): Time points
            N0 (float): Initial population
            r (float): Growth rate
            K (float): Carrying capacity
            
        Returns:
            array: Population at each time point
        """
        return K / (1 + ((K - N0) / N0) * np.exp(-r * t))
    
    def differential_equation(self, N, t, r, K):
        """
        Logistic ODE: dN/dt = rN(1 - N/K)
        
        Args:
            N (float): Current population
            t (float): Current time
            r (float): Growth rate
            K (float): Carrying capacity
            
        Returns:
            float: dN/dt
        """
        return r * N * (1 - N / K)
    
    def fit_nonlinear(self, t_data, N_data, initial_guess=None):
        """
        Fit model using nonlinear least squares
        
        Args:
            t_data (array): Time observations
            N_data (array): Population observations
            initial_guess (tuple): (N0, r, K) initial values
            
        Returns:
            dict: Fitted parameters and statistics
        """
        # Set initial guess
        if initial_guess is None:
            N0_guess = N_data[0]
            K_guess = max(N_data) * 1.5  # Assume saturation not yet reached
            r_guess = 0.1
            initial_guess = (N0_guess, r_guess, K_guess)
        
        # Fit using curve_fit
        try:
            params, covariance = curve_fit(
                self.analytical_solution,
                t_data,
                N_data,
                p0=initial_guess,
                bounds=([0, 0, max(N_data)], [np.inf, np.inf, np.inf]),
                maxfev=10000
            )
            
            self.N0, self.r, self.K = params
            self.fitted = True
            
            # Calculate R²
            N_pred = self.analytical_solution(t_data, *params)
            r2 = r2_score(N_data, N_pred)
            
            # Calculate standard errors
            perr = np.sqrt(np.diag(covariance))
            
            return {
                'N0': self.N0,
                'r': self.r,
                'K': self.K,
                'r2': r2,
                'std_errors': {'N0': perr[0], 'r': perr[1], 'K': perr[2]},
                'covariance': covariance
            }
            
        except Exception as e:
            print(f"Fitting failed: {e}")
            return None
    
    def fit_linearized(self, t_data, N_data):
        """
        Fit using linearization method (transform to linear regression)
        
        Linearization: ln(K/N - 1) = ln((K-N0)/N0) - rt
        
        Args:
            t_data (array): Time observations
            N_data (array): Population observations
            
        Returns:
            dict: Fitted parameters
        """
        # Estimate K as max observed value * 1.2
        K_est = max(N_data) * 1.2
        
        # Transform data
        # Avoid division by zero or log of negative
        valid_mask = (N_data > 0) & (N_data < K_est)
        t_valid = t_data[valid_mask]
        N_valid = N_data[valid_mask]
        
        y = np.log(K_est / N_valid - 1)
        
        # Linear regression
        coeffs = np.polyfit(t_valid, y, 1)
        slope = coeffs[0]  # -r
        intercept = coeffs[1]  # ln((K-N0)/N0)
        
        self.r = -slope
        self.N0 = K_est / (1 + np.exp(intercept))
        self.K = K_est
        self.fitted = True
        
        # Calculate R²
        N_pred = self.analytical_solution(t_data, self.N0, self.r, self.K)
        r2 = r2_score(N_data, N_pred)
        
        return {
            'N0': self.N0,
            'r': self.r,
            'K': self.K,
            'r2': r2,
            'method': 'linearized'
        }
    
    def predict(self, t):
        """
        Predict population at given time points
        
        Args:
            t (array or float): Time points
            
        Returns:
            array: Predicted population
        """
        if not self.fitted:
            raise ValueError("Model not fitted. Call fit_nonlinear() or fit_linearized() first.")
        
        if isinstance(t, (int, float)):
            t = np.array([t])
        
        return self.analytical_solution(t, self.N0, self.r, self.K)
    
    def solve_ode(self, t_span, N0=None):
        """
        Solve ODE numerically (useful for verification or extensions)
        
        Args:
            t_span (array): Time points
            N0 (float): Initial condition (uses fitted N0 if None)
            
        Returns:
            array: Numerical solution
        """
        if N0 is None:
            N0 = self.N0
        
        solution = odeint(self.differential_equation, N0, t_span, args=(self.r, self.K))
        return solution.flatten()
    
    def get_inflection_point(self):
        """
        Calculate inflection point (maximum growth rate)
        
        Returns:
            dict: Time and population at inflection point
        """
        if not self.fitted:
            raise ValueError("Model not fitted.")
        
        t_inflection = (1 / self.r) * np.log((self.K - self.N0) / self.N0)
        N_inflection = self.K / 2
        max_growth_rate = self.r * self.K / 4
        
        return {
            't': t_inflection,
            'N': N_inflection,
            'max_growth_rate': max_growth_rate
        }

def plot_logistic_fit(t_data, N_data, model, future_steps=50, title='Logistic Growth Model'):
    """
    Comprehensive visualization of logistic model
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Extend time for prediction
    t_min, t_max = t_data.min(), t_data.max()
    t_extended = np.linspace(t_min, t_max + future_steps, 300)
    N_pred = model.predict(t_extended)
    N_fitted = model.predict(t_data)
    
    # 1. Main fit plot
    ax1 = axes[0, 0]
    ax1.scatter(t_data, N_data, color='blue', s=50, alpha=0.6, label='Observed Data')
    ax1.plot(t_extended, N_pred, 'r-', linewidth=2, label='Logistic Fit')
    ax1.axhline(model.K, color='green', linestyle='--', linewidth=1.5, 
                label=f'Carrying Capacity K={model.K:.2f}')
    
    # Mark inflection point
    inflection = model.get_inflection_point()
    if inflection['t'] > 0:
        ax1.plot(inflection['t'], inflection['N'], 'ko', markersize=10, 
                label=f"Inflection Point (t={inflection['t']:.2f})")
    
    ax1.set_xlabel('Time', fontsize=12)
    ax1.set_ylabel('Population', fontsize=12)
    ax1.set_title('Logistic Growth Curve', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Residuals
    ax2 = axes[0, 1]
    residuals = N_data - N_fitted
    ax2.scatter(t_data, residuals, color='purple', alpha=0.6)
    ax2.axhline(0, color='black', linestyle='--', linewidth=1)
    ax2.set_xlabel('Time', fontsize=12)
    ax2.set_ylabel('Residuals', fontsize=12)
    ax2.set_title('Residual Plot', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 3. Phase plane (dN/dt vs N)
    ax3 = axes[1, 0]
    N_range = np.linspace(0, model.K * 1.2, 200)
    dN_dt = model.r * N_range * (1 - N_range / model.K)
    ax3.plot(N_range, dN_dt, 'b-', linewidth=2)
    ax3.axhline(0, color='black', linestyle='--', linewidth=1)
    ax3.axvline(model.K, color='green', linestyle='--', linewidth=1, label='K (stable)')
    ax3.axvline(0, color='red', linestyle='--', linewidth=1, label='0 (unstable)')
    ax3.set_xlabel('Population (N)', fontsize=12)
    ax3.set_ylabel('Growth Rate (dN/dt)', fontsize=12)
    ax3.set_title('Phase Plane', fontsize=14, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Growth rate over time
    ax4 = axes[1, 1]
    growth_rate = model.r * N_pred * (1 - N_pred / model.K)
    ax4.plot(t_extended, growth_rate, 'orange', linewidth=2)
    ax4.axhline(inflection['max_growth_rate'], color='red', linestyle='--', 
                label=f"Max Rate = {inflection['max_growth_rate']:.2f}")
    ax4.set_xlabel('Time', fontsize=12)
    ax4.set_ylabel('dN/dt', fontsize=12)
    ax4.set_title('Growth Rate Over Time', fontsize=14, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('logistic_growth_analysis.png', dpi=300)
    plt.show()

# --- Usage Example ---
if __name__ == "__main__":
    # Mock Data: U.S. Population (millions)
    years = np.array([1790, 1800, 1810, 1820, 1830, 1840, 1850, 
                      1860, 1870, 1880, 1890, 1900, 1910, 1920])
    population = np.array([3.9, 5.3, 7.2, 9.6, 12.9, 17.1, 23.2, 
                          31.4, 38.6, 50.2, 63.0, 76.2, 92.2, 106.0])
    
    # Normalize time to start from 0
    t_data = years - years[0]
    
    print("=" * 60)
    print("LOGISTIC GROWTH MODEL FITTING")
    print("=" * 60)
    
    # Initialize model
    model = LogisticGrowth()
    
    # Method 1: Nonlinear fitting (recommended)
    print("\n1. Nonlinear Least Squares Fitting:")
    results = model.fit_nonlinear(t_data, population)
    
    if results:
        print(f"   N0 (Initial Population): {results['N0']:.2f} ± {results['std_errors']['N0']:.2f}")
        print(f"   r (Growth Rate): {results['r']:.4f} ± {results['std_errors']['r']:.4f}")
        print(f"   K (Carrying Capacity): {results['K']:.2f} ± {results['std_errors']['K']:.2f}")
        print(f"   R² Score: {results['r2']:.4f}")
    
    # Inflection point
    print("\n2. Inflection Point Analysis:")
    inflection = model.get_inflection_point()
    print(f"   Time: {inflection['t']:.2f} years from start ({years[0] + inflection['t']:.0f})")
    print(f"   Population: {inflection['N']:.2f} million")
    print(f"   Max Growth Rate: {inflection['max_growth_rate']:.2f} million/year")
    
    # Forecast
    print("\n3. Future Predictions:")
    future_years = [1930, 1950, 1970, 2000]
    for year in future_years:
        t_future = year - years[0]
        pred = model.predict(t_future)[0]
        print(f"   Year {year}: {pred:.2f} million")
    
    # Visualize
    plot_logistic_fit(t_data, population, model, future_steps=100, 
                     title='U.S. Population Growth (Logistic Model)')
    
    # Compare with linearized method
    print("\n" + "=" * 60)
    print("COMPARISON: Linearized Method")
    print("=" * 60)
    model_linear = LogisticGrowth()
    results_linear = model_linear.fit_linearized(t_data, population)
    print(f"   r: {results_linear['r']:.4f}")
    print(f"   K: {results_linear['K']:.2f}")
    print(f"   R²: {results_linear['r2']:.4f}")
```

## Extensions

### 1. Logistic with Harvesting
$$\frac{dN}{dt} = rN\left(1 - \frac{N}{K}\right) - H$$

Where $H$ is constant harvest rate. Critical threshold: $H_{max} = \frac{rK}{4}$.

### 2. Time-Delayed Logistic
$$\frac{dN}{dt} = rN(t)\left(1 - \frac{N(t-\tau)}{K}\right)$$

Accounts for delayed response (e.g., gestation period).

### 3. Generalized Logistic (Richards Model)
$$N(t) = \frac{K}{(1 + Qe^{-rt})^{1/\nu}}$$

Parameter $\nu$ controls asymmetry of the S-curve.

## Common Pitfalls

1.  **Wrong Initial Guess**: If fitting fails, try different initial guesses for $r$ and $K$.
2.  **Insufficient Data**: Need data covering at least 50% of the growth curve for reliable $K$ estimation.
3.  **Outliers**: Single bad data point can severely distort fit. Use **`data-cleaner`** first.
4.  **Extrapolation**: Don't predict too far beyond observed data (model assumptions may break down).
5.  **Ignoring Inflection Point**: Always report and interpret the inflection point (it's where growth accelerates maximally).

## Integration Workflow

- **Input**: Use **`data-cleaner`** to handle missing values and outliers.
- **Comparison**: Compare with **`grey-forecaster`** (empirical) vs Logistic (mechanistic).
- **Validation**: Use **`robustness-check`** to test model stability with perturbed parameters.
- **Visualization**: Use **`visual-engineer`** for publication-quality plots.
- **Uncertainty**: Use **`monte-carlo-engine`** to propagate parameter uncertainty to predictions.

## Output Requirements for Paper

1.  **Model Equation**: Display the differential equation and analytical solution.
2.  **Parameter Estimates**: "We estimated r=0.0234±0.0012 yr⁻¹ and K=350±15 million."
3.  **Goodness of Fit**: "The model achieved R²=0.987, indicating excellent fit."
4.  **Inflection Point**: "Maximum growth rate occurs at t=45 years when N=K/2=175 million."
5.  **Phase Plane**: Show stability analysis (N=0 unstable, N=K stable).
6.  **Biological Interpretation**: "The carrying capacity of 350 million represents the maximum sustainable population given resource constraints."

## Decision Guide: Logistic vs Other Models

| Scenario | Recommended Model |
|----------|-------------------|
| S-shaped growth with saturation | **`logistic-growth`** (this skill) |
| Unlimited exponential growth | Simple exponential model |
| Oscillating populations | Lotka-Volterra (predator-prey) |
| Multiple interacting species | Competitive Lotka-Volterra |
| Disease spread | SIR/SEIR models (extensions of logistic) |
| Empirical curve fitting (no mechanism) | **`grey-forecaster`** or **`arima-forecaster`** |
