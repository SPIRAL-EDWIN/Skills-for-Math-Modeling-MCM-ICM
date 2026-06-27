---
name: grey-forecaster
description: Grey prediction model (GM(1,1)) for small-sample forecasting. Solves "poor information" problems with as few as 4 data points. O-Prize paper staple for annual/limited data scenarios.
---

# Grey Forecast (GM(1,1))

A forecasting method specifically designed for small samples and incomplete information systems.

## When to Use

- **Small Sample Size**: Only 4-10 data points available (e.g., annual data over a few years).
- **Limited Historical Data**: New phenomena, emerging markets, or rare events.
- **Short-Term Prediction**: Forecasting 1-5 periods ahead (not suitable for long-term).
- **Exponential Growth**: Data shows roughly exponential trend (not oscillating or chaotic).

## When NOT to Use

- **Large Samples**: If you have > 50 points, use **`arima-forecaster`** instead.
- **Seasonal Patterns**: Grey models don't capture seasonality well.
- **Oscillating Data**: Grey assumes monotonic trends (always increasing or decreasing).

## Algorithm Steps (GM(1,1))

1.  **Level Ratio Test**: Check if data is suitable for GM(1,1).
    - Calculate level ratios: $\lambda(k) = X^{(0)}(k-1) / X^{(0)}(k)$
    - Must satisfy: $\lambda(k) \in (e^{-2/(n+1)}, e^{2/(n+1)})$
    - If violated, apply translation transformation.

2.  **1-AGO (Accumulated Generating Operation)**:
    - $X^{(1)}(k) = \sum_{i=1}^{k} X^{(0)}(i)$

3.  **Construct Mean Sequence**:
    - $Z^{(1)}(k) = 0.5 \times (X^{(1)}(k) + X^{(1)}(k-1))$

4.  **Parameter Estimation**:
    - Build matrix $B$ and vector $Y$
    - Solve $\hat{a} = [a, u]^T = (B^T B)^{-1} B^T Y$ using least squares

5.  **Build Differential Equation**:
    - $\frac{dX^{(1)}}{dt} + a X^{(1)} = u$
    - Solution: $\hat{X}^{(1)}(k+1) = (X^{(0)}(1) - \frac{u}{a}) e^{-ak} + \frac{u}{a}$

6.  **Inverse AGO (IAGO)**:
    - $\hat{X}^{(0)}(k+1) = \hat{X}^{(1)}(k+1) - \hat{X}^{(1)}(k)$

7.  **Accuracy Test**:
    - Posterior variance ratio: $C = S_2 / S_1$ (should be < 0.35 for "good")
    - Small error probability: $P = P(|\epsilon(k) - \bar{\epsilon}| < 0.6745 S_1)$ (should be > 0.95)

## Implementation Template

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class GreyForecaster:
    """
    GM(1,1) Grey Prediction Model
    """
    
    def __init__(self, data):
        """
        Args:
            data (array-like): Original time series (at least 4 points)
        """
        self.X0 = np.array(data).flatten()
        self.n = len(self.X0)
        
        if self.n < 4:
            raise ValueError("Grey model requires at least 4 data points")
        
        self.a = None
        self.u = None
        self.X1 = None
        self.fitted_values = None
        
    def level_ratio_test(self):
        """
        Check if data is suitable for GM(1,1)
        
        Returns:
            dict: {'passed': bool, 'ratios': array, 'bounds': tuple}
        """
        # Calculate level ratios
        ratios = self.X0[:-1] / self.X0[1:]
        
        # Calculate bounds
        lower_bound = np.exp(-2 / (self.n + 1))
        upper_bound = np.exp(2 / (self.n + 1))
        
        # Check if all ratios are within bounds
        passed = np.all((ratios > lower_bound) & (ratios < upper_bound))
        
        return {
            'passed': passed,
            'ratios': ratios,
            'bounds': (lower_bound, upper_bound),
            'recommendation': 'Data is suitable for GM(1,1)' if passed 
                            else 'Consider translation transformation (add constant to data)'
        }
    
    def fit(self):
        """
        Fit the GM(1,1) model
        """
        # 1. 1-AGO (Accumulated Generating Operation)
        self.X1 = np.cumsum(self.X0)
        
        # 2. Generate mean sequence Z
        Z = 0.5 * (self.X1[:-1] + self.X1[1:])
        
        # 3. Construct matrix B and vector Y
        B = np.column_stack([-Z, np.ones(self.n - 1)])
        Y = self.X0[1:]
        
        # 4. Least squares estimation
        params = np.linalg.inv(B.T @ B) @ B.T @ Y
        self.a = params[0]
        self.u = params[1]
        
        # 5. Calculate fitted values
        self.fitted_values = self._predict_accumulated(self.n)
        
        return self
    
    def _predict_accumulated(self, steps):
        """
        Predict accumulated values X^(1)
        """
        k = np.arange(0, steps)
        X1_pred = (self.X0[0] - self.u / self.a) * np.exp(-self.a * k) + self.u / self.a
        return X1_pred
    
    def predict(self, steps=5):
        """
        Forecast future values
        
        Args:
            steps (int): Number of periods to forecast
            
        Returns:
            np.array: Predicted values
        """
        if self.a is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        # Predict accumulated values
        total_steps = self.n + steps
        X1_pred = self._predict_accumulated(total_steps)
        
        # IAGO (Inverse Accumulated Generating Operation)
        X0_pred = np.diff(X1_pred, prepend=0)
        
        return X0_pred[-steps:]
    
    def get_fitted_values(self):
        """
        Get fitted values for original data
        """
        X0_fitted = np.diff(self.fitted_values, prepend=0)
        return X0_fitted
    
    def accuracy_test(self):
        """
        Perform posterior variance test
        
        Returns:
            dict: {'C': float, 'P': float, 'grade': str, 'mape': float}
        """
        X0_fitted = self.get_fitted_values()
        residuals = self.X0 - X0_fitted
        
        # Mean and std of original data
        S1 = np.std(self.X0, ddof=1)
        
        # Mean and std of residuals
        mean_residual = np.mean(residuals)
        S2 = np.std(residuals, ddof=1)
        
        # Posterior variance ratio
        C = S2 / S1
        
        # Small error probability
        threshold = 0.6745 * S1
        P = np.sum(np.abs(residuals - mean_residual) < threshold) / self.n
        
        # Determine grade
        if C < 0.35 and P > 0.95:
            grade = "Excellent (一级)"
        elif C < 0.50 and P > 0.80:
            grade = "Good (二级)"
        elif C < 0.65 and P > 0.70:
            grade = "Acceptable (三级)"
        else:
            grade = "Poor (四级) - Consider other methods"
        
        # MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs(residuals / self.X0)) * 100
        
        return {
            'C': C,
            'P': P,
            'grade': grade,
            'mape': mape,
            'residuals': residuals
        }

def plot_grey_forecast(original_data, fitted_values, forecast_values, 
                       title='Grey Forecast (GM(1,1))'):
    """
    Visualize Grey model results
    """
    n = len(original_data)
    n_forecast = len(forecast_values)
    
    # Time indices
    time_original = np.arange(1, n + 1)
    time_fitted = np.arange(1, n + 1)
    time_forecast = np.arange(n + 1, n + n_forecast + 1)
    
    plt.figure(figsize=(12, 6))
    
    # Original data
    plt.plot(time_original, original_data, 'o-', label='Original Data', 
             color='blue', linewidth=2, markersize=8)
    
    # Fitted values
    plt.plot(time_fitted, fitted_values, 's--', label='Fitted Values', 
             color='green', linewidth=2, markersize=6, alpha=0.7)
    
    # Forecast
    plt.plot(time_forecast, forecast_values, '^-', label='Forecast', 
             color='red', linewidth=2, markersize=8)
    
    # Connect fitted and forecast
    plt.plot([time_fitted[-1], time_forecast[0]], 
             [fitted_values[-1], forecast_values[0]], 
             'k--', alpha=0.3)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Time Period', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('grey_forecast.png', dpi=300)
    plt.show()

# --- Usage Example ---
if __name__ == "__main__":
    # Example: Annual GDP data (only 7 points)
    gdp_data = [3.5, 4.2, 5.1, 6.3, 7.8, 9.5, 11.8]
    
    # Initialize model
    model = GreyForecaster(gdp_data)
    
    # Level ratio test
    print("=" * 50)
    print("LEVEL RATIO TEST")
    print("=" * 50)
    test_result = model.level_ratio_test()
    print(f"Passed: {test_result['passed']}")
    print(f"Recommendation: {test_result['recommendation']}")
    
    # Fit model
    print("\n" + "=" * 50)
    print("MODEL FITTING")
    print("=" * 50)
    model.fit()
    print(f"Parameter a (development coefficient): {model.a:.4f}")
    print(f"Parameter u (grey input): {model.u:.4f}")
    
    # Accuracy test
    print("\n" + "=" * 50)
    print("ACCURACY TEST")
    print("=" * 50)
    accuracy = model.accuracy_test()
    print(f"Posterior Variance Ratio (C): {accuracy['C']:.4f}")
    print(f"Small Error Probability (P): {accuracy['P']:.4f}")
    print(f"Grade: {accuracy['grade']}")
    print(f"MAPE: {accuracy['mape']:.2f}%")
    
    # Forecast
    print("\n" + "=" * 50)
    print("FORECAST")
    print("=" * 50)
    forecast = model.predict(steps=5)
    print("Next 5 periods forecast:")
    print(forecast)
    
    # Visualize
    fitted = model.get_fitted_values()
    plot_grey_forecast(gdp_data, fitted, forecast)
```

## Decision Guide: Grey vs ARIMA

| Criterion | Use Grey | Use ARIMA |
|-----------|----------|-----------|
| Sample Size | < 10 points | > 50 points |
| Data Pattern | Exponential trend | Trend + Seasonality |
| Forecast Horizon | 1-5 periods | 5-50 periods |
| Computational Cost | Very low | Medium to high |
| Interpretability | High (simple equation) | Medium (complex coefficients) |

## Common Pitfalls

1.  **Ignoring Level Ratio Test**: Always run the test first. If it fails, add a constant to all data points (e.g., +100).
2.  **Using for Long-Term**: Grey models degrade quickly after 3-5 periods. Don't forecast 10+ periods ahead.
3.  **Oscillating Data**: If data goes up and down frequently, Grey will fail. Use ARIMA or smoothing methods.
4.  **Not Checking Accuracy**: Always report C and P values in your paper. If grade is "Poor", acknowledge limitations.

## Integration Workflow

- **Input**: Use **`data-cleaner`** to ensure no missing values.
- **Comparison**: Often used alongside **`arima-forecaster`** to compare small-sample vs large-sample methods.
- **Visualization**: Use **`visual-engineer`** to create publication-quality plots.
- **Uncertainty**: Combine with **`monte-carlo-engine`** for confidence intervals (Grey doesn't provide them natively).

## Output Requirements for Paper

1.  **Model Specification**: "We built a GM(1,1) model with parameters a=-0.234, u=4.567."
2.  **Level Ratio Test**: "All level ratios fell within the acceptable range [0.85, 1.18]."
3.  **Accuracy Metrics**: "The model achieved C=0.28 and P=0.98, indicating excellent fit (Grade I)."
4.  **Forecast Table**: Show predicted values for next 3-5 periods.
5.  **Limitations**: "Due to the small sample size, we recommend updating the model as new data becomes available."
