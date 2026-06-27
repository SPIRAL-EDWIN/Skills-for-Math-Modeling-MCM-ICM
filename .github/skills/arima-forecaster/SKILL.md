---
name: arima-forecaster
description: Classical time series forecasting using ARIMA/SARIMA models. Captures trends, seasonality, and provides confidence intervals. Essential for temporal prediction problems in MCM/ICM.
---

# ARIMA/SARIMA Forecaster

Autoregressive Integrated Moving Average (ARIMA) and its seasonal extension (SARIMA) for time series prediction.

## When to Use

- **Temporal Data**: When data points are ordered in time (monthly sales, annual population, daily temperature).
- **Trend & Seasonality**: Data shows clear upward/downward trend or repeating patterns.
- **Need Confidence Intervals**: Unlike neural networks, ARIMA provides statistical uncertainty bounds.
- **Interpretability**: Coefficients have clear mathematical meaning (important for O-Prize papers).

## Model Components

### ARIMA(p, d, q)
- **p** (AutoRegressive): How many past values influence the current value.
- **d** (Integrated): How many times to difference the data to make it stationary.
- **q** (Moving Average): How many past forecast errors influence the current value.

### SARIMA(p, d, q)(P, D, Q, s)
- **(P, D, Q)**: Seasonal versions of p, d, q.
- **s**: Seasonal period (e.g., 12 for monthly data with yearly cycles, 4 for quarterly).

## Algorithm Steps

1.  **Stationarity Check**: Use Augmented Dickey-Fuller (ADF) test. If p-value > 0.05, data is non-stationary → need differencing.
2.  **Differencing**: Apply $d$ or $D$ times until stationary.
3.  **Parameter Selection**:
    - Manual: Plot ACF/PACF to guess $p$ and $q$.
    - Automatic: Use `auto_arima` with AIC/BIC criterion.
4.  **Model Fitting**: Estimate coefficients using Maximum Likelihood Estimation (MLE).
5.  **Diagnostics**: Check residuals are white noise (Ljung-Box test).
6.  **Forecasting**: Predict future values with confidence intervals.

## Implementation Template

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
import warnings
warnings.filterwarnings('ignore')

def check_stationarity(series, alpha=0.05):
    """
    Perform Augmented Dickey-Fuller test.
    
    Returns:
        dict: {'stationary': bool, 'p_value': float, 'critical_values': dict}
    """
    result = adfuller(series.dropna())
    
    return {
        'stationary': result[1] < alpha,
        'p_value': result[1],
        'adf_statistic': result[0],
        'critical_values': result[4]
    }

def arima_forecaster(series, seasonal=False, m=12, forecast_steps=12, auto_select=True):
    """
    Fit ARIMA or SARIMA model and generate forecasts.
    
    Args:
        series (pd.Series): Time series data with datetime index.
        seasonal (bool): Whether to use SARIMA (default False).
        m (int): Seasonal period (e.g., 12 for monthly, 4 for quarterly).
        forecast_steps (int): Number of periods to forecast.
        auto_select (bool): Use auto_arima to find optimal parameters.
        
    Returns:
        dict: {
            'model': fitted model object,
            'forecast': pd.Series with predictions,
            'conf_int': pd.DataFrame with confidence intervals,
            'diagnostics': residual statistics
        }
    """
    # 1. Stationarity Check
    stationarity = check_stationarity(series)
    print(f"ADF Test p-value: {stationarity['p_value']:.4f}")
    
    if stationarity['stationary']:
        print("✅ Series is stationary.")
    else:
        print("⚠️ Series is non-stationary. Model will apply differencing.")
    
    # 2. Automatic Parameter Selection
    if auto_select:
        print("\n🔍 Running auto_arima to find optimal parameters...")
        
        model = auto_arima(
            series,
            seasonal=seasonal,
            m=m if seasonal else 1,
            start_p=0, start_q=0,
            max_p=5, max_q=5,
            d=None,  # Let it determine d automatically
            D=None,  # Let it determine D automatically
            trace=True,
            error_action='ignore',
            suppress_warnings=True,
            stepwise=True,
            information_criterion='aic'
        )
        
        print(f"\n✅ Best model: {model.order}")
        if seasonal:
            print(f"   Seasonal order: {model.seasonal_order}")
    else:
        # Manual mode: use default ARIMA(1,1,1)
        print("Using default ARIMA(1,1,1)")
        model = SARIMAX(series, order=(1, 1, 1), seasonal_order=(0, 0, 0, 0))
        model = model.fit(disp=False)
    
    # 3. Generate Forecast
    forecast_result = model.predict(n_periods=forecast_steps, return_conf_int=True)
    
    # Extract forecast and confidence intervals
    if isinstance(forecast_result, tuple):
        forecast_values, conf_int = forecast_result
    else:
        forecast_values = forecast_result
        conf_int = None
    
    # Create future dates
    last_date = series.index[-1]
    if isinstance(last_date, pd.Timestamp):
        freq = pd.infer_freq(series.index) or 'M'
        future_dates = pd.date_range(start=last_date, periods=forecast_steps+1, freq=freq)[1:]
    else:
        future_dates = range(len(series), len(series) + forecast_steps)
    
    forecast_series = pd.Series(forecast_values, index=future_dates, name='Forecast')
    
    if conf_int is not None:
        conf_df = pd.DataFrame(conf_int, index=future_dates, columns=['Lower', 'Upper'])
    else:
        conf_df = None
    
    # 4. Residual Diagnostics
    residuals = model.resid() if hasattr(model, 'resid') else None
    
    return {
        'model': model,
        'forecast': forecast_series,
        'conf_int': conf_df,
        'residuals': residuals
    }

def plot_forecast(series, forecast_result, title='ARIMA Forecast'):
    """Visualize historical data and forecast with confidence intervals."""
    
    forecast = forecast_result['forecast']
    conf_int = forecast_result['conf_int']
    
    plt.figure(figsize=(12, 6))
    
    # Historical data
    plt.plot(series.index, series.values, label='Historical', color='blue', linewidth=2)
    
    # Forecast
    plt.plot(forecast.index, forecast.values, label='Forecast', color='red', 
             linewidth=2, linestyle='--')
    
    # Confidence interval
    if conf_int is not None:
        plt.fill_between(conf_int.index, conf_int['Lower'], conf_int['Upper'], 
                         color='pink', alpha=0.3, label='95% Confidence Interval')
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('arima_forecast.png', dpi=300)
    plt.show()

def plot_diagnostics(series):
    """Plot ACF and PACF for manual parameter selection."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    plot_acf(series.dropna(), lags=40, ax=axes[0])
    axes[0].set_title('Autocorrelation Function (ACF)')
    
    plot_pacf(series.dropna(), lags=40, ax=axes[1])
    axes[1].set_title('Partial Autocorrelation Function (PACF)')
    
    plt.tight_layout()
    plt.savefig('acf_pacf_plots.png', dpi=300)
    plt.show()

# --- Usage Example ---
if __name__ == "__main__":
    # Mock Data: Monthly sales with trend and seasonality
    np.random.seed(42)
    dates = pd.date_range('2020-01', periods=60, freq='M')
    trend = np.linspace(100, 200, 60)
    seasonal = 20 * np.sin(np.linspace(0, 10*np.pi, 60))
    noise = np.random.normal(0, 5, 60)
    
    sales = trend + seasonal + noise
    series = pd.Series(sales, index=dates, name='Sales')
    
    # Check stationarity
    print("=" * 50)
    print("STATIONARITY CHECK")
    print("=" * 50)
    stationarity = check_stationarity(series)
    
    # Plot diagnostics (optional)
    # plot_diagnostics(series)
    
    # Fit SARIMA model
    print("\n" + "=" * 50)
    print("FITTING SARIMA MODEL")
    print("=" * 50)
    result = arima_forecaster(series, seasonal=True, m=12, forecast_steps=12)
    
    print("\nForecast Values:")
    print(result['forecast'])
    
    # Visualize
    plot_forecast(series, result, title='Sales Forecast (SARIMA)')
```

## Decision Guide: ARIMA vs SARIMA

| Data Characteristics | Recommended Model |
|---------------------|-------------------|
| No obvious seasonality | ARIMA(p, d, q) |
| Clear seasonal pattern (monthly/quarterly) | SARIMA(p, d, q)(P, D, Q, s) |
| Very short series (< 50 points) | Simple ARIMA with low orders |
| Long series with complex patterns | SARIMA with auto_arima |

## Common Pitfalls

1.  **Non-stationary Data**: Always check ADF test first. If p-value > 0.05, increase $d$ or apply log transformation.
2.  **Overfitting**: Don't use too high $p$ or $q$ (usually ≤ 3 is sufficient). Check AIC/BIC.
3.  **Ignoring Residuals**: After fitting, plot residuals. They should look like white noise (no patterns).
4.  **Wrong Seasonal Period**: For monthly data with yearly cycles, use $s=12$, not $s=365$.

## Integration Workflow

- **Input**: Use **`data-cleaner`** to handle missing values (ARIMA cannot handle gaps).
- **Pre-processing**: Consider log transformation if variance increases over time.
- **Post-processing**: Use **`visual-engineer`** to create publication-quality forecast plots.
- **Comparison**: Often combined with **`monte-carlo-engine`** to show uncertainty from different angles.

## Output Requirements for Paper

1.  **Model Specification**: "We fitted a SARIMA(1,1,1)(1,1,1,12) model with AIC=234.5."
2.  **Diagnostics**: "Ljung-Box test (p=0.45) confirms residuals are white noise."
3.  **Forecast Plot**: Show historical data + forecast + 95% confidence interval.
4.  **Interpretation**: "The model predicts sales will reach X units by December 2025 (95% CI: [Y, Z])."
