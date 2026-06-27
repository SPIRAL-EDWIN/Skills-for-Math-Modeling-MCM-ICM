---
name: lstm-forecaster
description: Deep learning time series forecasting using LSTM and GRU networks. Captures long-term dependencies and nonlinear patterns in sequential data. Essential for complex temporal prediction in MCM/ICM.
---

# LSTM/GRU Forecaster

Recurrent Neural Networks (RNN) specialized for time series prediction with memory mechanisms.

## When to Use

- **Long Sequences**: Data with 100+ time steps (e.g., daily data over months/years).
- **Nonlinear Dynamics**: Complex patterns that ARIMA cannot capture.
- **Multivariate Time Series**: Multiple related variables evolving together (e.g., weather + energy consumption).
- **Long-Term Dependencies**: Current value depends on events far in the past.
- **Sufficient Data**: At least 500+ samples for reliable training (preferably 1000+).

## When NOT to Use

- **Small Samples**: < 100 points → Use **`arima-forecaster`** or **`grey-forecaster`**.
- **Simple Trends**: Linear or exponential growth → Classical methods are faster and more interpretable.
- **Need Interpretability**: LSTM is a black box. Use **`ml-regressor`** with feature importance if explanation is critical.
- **Short Sequences**: < 20 time steps → Use simpler models.

## Model Comparison

| Model | Strengths | Weaknesses | Best For |
|-------|-----------|------------|----------|
| **LSTM** | Captures long-term memory, handles vanishing gradients | Slower training, more parameters | Complex sequences, long dependencies |
| **GRU** | Faster than LSTM, fewer parameters | Slightly less powerful | When speed matters, shorter sequences |
| **Simple RNN** | Fast, simple | Vanishing gradient problem | Baseline comparison only |

## Architecture Overview

### LSTM (Long Short-Term Memory)
- **Cell State**: Long-term memory highway.
- **Gates**: Forget gate (discard info), Input gate (add info), Output gate (read info).
- **Use Case**: Default choice for most time series tasks.

### GRU (Gated Recurrent Unit)
- Simplified LSTM with 2 gates (reset, update) instead of 3.
- 25% fewer parameters → Faster training.
- **Use Case**: When computational budget is tight or data is limited.

## Implementation Template

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, GRU, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import warnings
warnings.filterwarnings('ignore')

class LSTMForecaster:
    """
    LSTM/GRU time series forecaster with automatic preprocessing
    """
    
    def __init__(self, model_type='lstm', lookback=20, units=50, 
                 layers=2, dropout=0.2, random_state=42):
        """
        Args:
            model_type (str): 'lstm' or 'gru'
            lookback (int): Number of past time steps to use as input
            units (int): Number of units per RNN layer
            layers (int): Number of stacked RNN layers
            dropout (float): Dropout rate for regularization
            random_state (int): Random seed
        """
        self.model_type = model_type
        self.lookback = lookback
        self.units = units
        self.layers = layers
        self.dropout = dropout
        self.random_state = random_state
        
        self.model = None
        self.scaler = MinMaxScaler()
        self.history = None
        
        # Set random seeds
        np.random.seed(random_state)
        tf.random.set_seed(random_state)
    
    def create_sequences(self, data, lookback):
        """
        Transform time series into supervised learning format
        
        Args:
            data (np.array): Time series data (n_samples, n_features)
            lookback (int): Number of past steps to use
            
        Returns:
            X (np.array): Input sequences (n_samples, lookback, n_features)
            y (np.array): Target values (n_samples,)
        """
        X, y = [], []
        for i in range(len(data) - lookback):
            X.append(data[i:i+lookback])
            y.append(data[i+lookback, 0])  # Predict first feature
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape):
        """
        Build LSTM or GRU model
        
        Args:
            input_shape (tuple): (lookback, n_features)
        """
        model = Sequential()
        
        # Choose RNN type
        RNN_Layer = LSTM if self.model_type == 'lstm' else GRU
        
        # Stacked RNN layers
        for i in range(self.layers):
            return_sequences = (i < self.layers - 1)  # All but last layer
            
            model.add(RNN_Layer(
                units=self.units,
                return_sequences=return_sequences,
                input_shape=input_shape if i == 0 else None
            ))
            model.add(Dropout(self.dropout))
        
        # Output layer
        model.add(Dense(1))
        
        # Compile
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        self.model = model
        return model
    
    def fit(self, data, validation_split=0.2, epochs=100, batch_size=32, 
            verbose=1, early_stop_patience=10):
        """
        Train the model
        
        Args:
            data (pd.Series or np.array): Time series data
            validation_split (float): Fraction for validation
            epochs (int): Maximum training epochs
            batch_size (int): Batch size
            verbose (int): Verbosity level
            early_stop_patience (int): Epochs to wait before early stopping
        """
        # Convert to numpy
        if isinstance(data, pd.Series):
            data = data.values
        
        # Reshape if 1D
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
        
        # Normalize
        data_scaled = self.scaler.fit_transform(data)
        
        # Create sequences
        X, y = self.create_sequences(data_scaled, self.lookback)
        
        print(f"Training data shape: X={X.shape}, y={y.shape}")
        
        # Build model
        self.build_model(input_shape=(self.lookback, data.shape[1]))
        
        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=early_stop_patience,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-6,
                verbose=1
            )
        ]
        
        # Train
        self.history = self.model.fit(
            X, y,
            validation_split=validation_split,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=verbose
        )
        
        return self
    
    def predict(self, data, steps=1):
        """
        Multi-step ahead prediction
        
        Args:
            data (np.array): Recent data (at least lookback points)
            steps (int): Number of future steps to predict
            
        Returns:
            np.array: Predictions (original scale)
        """
        # Prepare input
        if isinstance(data, pd.Series):
            data = data.values
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
        
        # Normalize
        data_scaled = self.scaler.transform(data)
        
        # Use last lookback points as initial input
        current_sequence = data_scaled[-self.lookback:].reshape(1, self.lookback, -1)
        
        predictions = []
        
        # Recursive prediction
        for _ in range(steps):
            # Predict next step
            next_pred = self.model.predict(current_sequence, verbose=0)
            predictions.append(next_pred[0, 0])
            
            # Update sequence (shift left, append prediction)
            next_pred_full = np.zeros((1, 1, data_scaled.shape[1]))
            next_pred_full[0, 0, 0] = next_pred[0, 0]
            
            current_sequence = np.concatenate([
                current_sequence[:, 1:, :],
                next_pred_full
            ], axis=1)
        
        # Inverse transform
        predictions = np.array(predictions).reshape(-1, 1)
        predictions_original = self.scaler.inverse_transform(
            np.concatenate([predictions, 
                           np.zeros((len(predictions), data_scaled.shape[1]-1))], 
                          axis=1)
        )[:, 0]
        
        return predictions_original
    
    def evaluate(self, data):
        """
        Evaluate on test data
        
        Returns:
            dict: RMSE and MAE
        """
        if isinstance(data, pd.Series):
            data = data.values
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
        
        data_scaled = self.scaler.transform(data)
        X, y = self.create_sequences(data_scaled, self.lookback)
        
        # Predict
        y_pred_scaled = self.model.predict(X, verbose=0)
        
        # Inverse transform
        y_pred = self.scaler.inverse_transform(
            np.concatenate([y_pred_scaled, 
                           np.zeros((len(y_pred_scaled), data.shape[1]-1))], 
                          axis=1)
        )[:, 0]
        
        y_true = self.scaler.inverse_transform(
            np.concatenate([y.reshape(-1, 1), 
                           np.zeros((len(y), data.shape[1]-1))], 
                          axis=1)
        )[:, 0]
        
        rmse = np.sqrt(np.mean((y_true - y_pred)**2))
        mae = np.mean(np.abs(y_true - y_pred))
        
        return {
            'rmse': rmse,
            'mae': mae,
            'predictions': y_pred,
            'actual': y_true
        }

def plot_training_history(history, title='Training History'):
    """Plot loss curves"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Loss
    ax1.plot(history.history['loss'], label='Training Loss')
    ax1.plot(history.history['val_loss'], label='Validation Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss (MSE)')
    ax1.set_title('Loss Curve')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # MAE
    ax2.plot(history.history['mae'], label='Training MAE')
    ax2.plot(history.history['val_mae'], label='Validation MAE')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('MAE')
    ax2.set_title('MAE Curve')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('training_history.png', dpi=300)
    plt.show()

def plot_forecast(historical_data, forecast_values, title='LSTM Forecast'):
    """Visualize forecast"""
    n_hist = len(historical_data)
    n_fore = len(forecast_values)
    
    plt.figure(figsize=(12, 6))
    
    # Historical
    plt.plot(range(n_hist), historical_data, 'o-', 
             label='Historical', color='blue', linewidth=2)
    
    # Forecast
    plt.plot(range(n_hist, n_hist + n_fore), forecast_values, '^-', 
             label='Forecast', color='red', linewidth=2)
    
    # Connection line
    plt.plot([n_hist-1, n_hist], 
             [historical_data[-1], forecast_values[0]], 
             'k--', alpha=0.3)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Time Step')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('lstm_forecast.png', dpi=300)
    plt.show()

# --- Usage Example ---
if __name__ == "__main__":
    # Mock Data: Sinusoidal with trend and noise
    np.random.seed(42)
    t = np.linspace(0, 100, 500)
    trend = 0.05 * t
    seasonal = 10 * np.sin(0.5 * t)
    noise = np.random.normal(0, 1, len(t))
    data = trend + seasonal + noise
    
    # Split data
    train_size = int(0.8 * len(data))
    train_data = data[:train_size]
    test_data = data[train_size:]
    
    print("=" * 60)
    print("LSTM FORECASTING")
    print("=" * 60)
    
    # Initialize model
    model = LSTMForecaster(
        model_type='lstm',
        lookback=30,
        units=64,
        layers=2,
        dropout=0.2
    )
    
    # Train
    model.fit(train_data, epochs=50, batch_size=16, verbose=1)
    
    # Plot training history
    plot_training_history(model.history)
    
    # Evaluate on test set
    results = model.evaluate(test_data)
    print(f"\nTest Set Performance:")
    print(f"  RMSE: {results['rmse']:.4f}")
    print(f"  MAE: {results['mae']:.4f}")
    
    # Forecast future
    forecast = model.predict(data, steps=50)
    print(f"\nForecast next 50 steps:")
    print(forecast[:10])  # Show first 10
    
    # Visualize
    plot_forecast(data, forecast, title='LSTM Time Series Forecast')
    
    # Compare LSTM vs GRU
    print("\n" + "=" * 60)
    print("GRU FORECASTING (for comparison)")
    print("=" * 60)
    
    gru_model = LSTMForecaster(model_type='gru', lookback=30, units=64)
    gru_model.fit(train_data, epochs=50, batch_size=16, verbose=0)
    gru_results = gru_model.evaluate(test_data)
    
    print(f"\nGRU Test Performance:")
    print(f"  RMSE: {gru_results['rmse']:.4f}")
    print(f"  MAE: {gru_results['mae']:.4f}")
```

## Hyperparameter Tuning Guide

### Architecture Parameters
- **lookback**: Input sequence length (10-60). Longer = more context but slower.
- **units**: Hidden units per layer (32-128). More = more capacity but risk overfitting.
- **layers**: Number of stacked RNN layers (1-3). More = deeper but harder to train.
- **dropout**: Regularization (0.1-0.3). Higher = less overfitting but may underfit.

### Training Parameters
- **batch_size**: 16-64 for small datasets, 128-256 for large.
- **learning_rate**: 0.001 is a good default. Use ReduceLROnPlateau to adapt.
- **epochs**: 50-200. Use EarlyStopping to prevent overfitting.

## Common Pitfalls

1.  **Not Scaling Data**: Neural networks require normalized inputs (0-1 or standardized).
2.  **Too Few Samples**: LSTM needs 500+ samples. Use classical methods for small data.
3.  **Overfitting**: Always use dropout and early stopping. Monitor val_loss.
4.  **Wrong Lookback**: Too short = misses patterns. Too long = overfits noise.
5.  **Ignoring Validation Loss**: If val_loss >> train_loss, you're overfitting.

## Integration Workflow

- **Input**: Use **`data-cleaner`** to handle missing values and outliers.
- **Feature Engineering**: For multivariate, use **`pca-analyzer`** to reduce feature dimensions.
- **Comparison**: Compare with **`arima-forecaster`** to show LSTM's superiority on nonlinear data.
- **Uncertainty**: Use Monte Carlo Dropout (predict multiple times with dropout enabled) for confidence intervals.
- **Visualization**: Use **`visual-engineer`** for publication-quality plots.

## Output Requirements for Paper

1.  **Model Architecture**: "We used a 2-layer LSTM with 64 units per layer and 0.2 dropout."
2.  **Training Details**: "Trained for 87 epochs with early stopping (patience=10) on 80/20 train/val split."
3.  **Performance Metrics**: "Test RMSE=2.34, MAE=1.87, outperforming ARIMA (RMSE=3.45)."
4.  **Learning Curves**: Show training and validation loss over epochs.
5.  **Forecast Plot**: Historical data + multi-step forecast.
6.  **Comparison Table**: LSTM vs GRU vs ARIMA performance side-by-side.

## Advanced: Attention Mechanism (Optional)

For O-Prize level analysis, add attention to visualize which past time steps the model focuses on:

```python
from tensorflow.keras.layers import Attention, Concatenate

# After LSTM layer
lstm_output = LSTM(units, return_sequences=True)(input_layer)
attention_output = Attention()([lstm_output, lstm_output])
# Continue with Dense layers...
```

This provides interpretability by showing "the model pays most attention to events 20 days ago."

## Decision Guide: LSTM vs Other Methods

| Scenario | Recommended Method |
|----------|-------------------|
| < 100 samples | **`grey-forecaster`** or **`arima-forecaster`** |
| Linear trend, stationary | **`arima-forecaster`** |
| Nonlinear, 500+ samples | **`lstm-forecaster`** (this skill) |
| Multivariate time series | **`lstm-forecaster`** with multiple input features |
| Need interpretability | **`arima-forecaster`** or **`ml-regressor`** |
| Highest accuracy at any cost | **`lstm-forecaster`** with hyperparameter tuning |
