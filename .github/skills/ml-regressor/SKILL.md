---
name: ml-regressor
description: Ensemble machine learning regression using Random Forest and XGBoost. Handles complex nonlinear relationships, provides feature importance analysis, and achieves high prediction accuracy. Essential for MCM/ICM data-driven modeling.
---

# Machine Learning Regressor (RF & XGBoost)

Advanced regression techniques using ensemble learning methods for complex, nonlinear relationships.

## When to Use

- **Nonlinear Relationships**: When linear regression assumptions are violated.
- **Complex Interactions**: Multiple variables interact in non-obvious ways.
- **Feature Importance**: Need to identify which factors drive the outcome (critical for O-Prize papers).
- **High Accuracy Required**: When prediction precision is paramount.
- **Sufficient Data**: At least 100+ samples (preferably 500+) for reliable training.

## When NOT to Use

- **Small Samples**: < 50 points → Use **`grey-forecaster`** or simple regression.
- **Time Series**: Use **`arima-forecaster`** or LSTM instead (ML methods don't capture temporal dependencies well).
- **Need Causality**: ML shows correlation, not causation. Use structural equation models if causality is critical.

## Model Comparison

| Model | Strengths | Weaknesses | Best For |
|-------|-----------|------------|----------|
| **Random Forest** | Robust, less overfitting, fast training | Lower accuracy than XGBoost | Exploratory analysis, interpretability |
| **XGBoost** | Highest accuracy, handles missing values | Slower, more hyperparameters | Final predictions, competitions |

## Algorithm Overview

### Random Forest
- Builds multiple decision trees on random subsets of data and features.
- Averages predictions to reduce variance.
- Naturally provides feature importance via mean decrease in impurity.

### XGBoost (Extreme Gradient Boosting)
- Sequentially builds trees, each correcting errors of previous ones.
- Uses gradient descent optimization.
- Includes regularization to prevent overfitting.

## Implementation Template

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

class MLRegressor:
    """
    Unified interface for Random Forest and XGBoost regression
    """
    
    def __init__(self, model_type='rf', random_state=42):
        """
        Args:
            model_type (str): 'rf' for Random Forest or 'xgb' for XGBoost
            random_state (int): Random seed for reproducibility
        """
        self.model_type = model_type
        self.random_state = random_state
        self.model = None
        self.feature_names = None
        self.best_params = None
        
    def fit(self, X, y, tune_hyperparams=True, cv_folds=5):
        """
        Train the model with optional hyperparameter tuning
        
        Args:
            X (pd.DataFrame or np.array): Features
            y (pd.Series or np.array): Target variable
            tune_hyperparams (bool): Whether to perform hyperparameter search
            cv_folds (int): Number of cross-validation folds
        """
        # Store feature names
        if isinstance(X, pd.DataFrame):
            self.feature_names = X.columns.tolist()
            X = X.values
        else:
            self.feature_names = [f'Feature_{i}' for i in range(X.shape[1])]
        
        if isinstance(y, pd.Series):
            y = y.values
        
        # Initialize model
        if self.model_type == 'rf':
            base_model = RandomForestRegressor(random_state=self.random_state)
            param_dist = {
                'n_estimators': [100, 200, 300, 500],
                'max_depth': [10, 20, 30, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'max_features': ['sqrt', 'log2', None]
            }
        else:  # xgb
            base_model = xgb.XGBRegressor(random_state=self.random_state, 
                                          objective='reg:squarederror')
            param_dist = {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 5, 7, 9],
                'learning_rate': [0.01, 0.05, 0.1, 0.2],
                'subsample': [0.6, 0.8, 1.0],
                'colsample_bytree': [0.6, 0.8, 1.0],
                'min_child_weight': [1, 3, 5]
            }
        
        # Hyperparameter tuning
        if tune_hyperparams:
            print(f"🔍 Tuning hyperparameters for {self.model_type.upper()}...")
            search = RandomizedSearchCV(
                base_model, 
                param_distributions=param_dist,
                n_iter=20,  # Try 20 random combinations
                cv=cv_folds,
                scoring='r2',
                random_state=self.random_state,
                n_jobs=-1,
                verbose=1
            )
            search.fit(X, y)
            self.model = search.best_estimator_
            self.best_params = search.best_params_
            print(f"✅ Best parameters: {self.best_params}")
        else:
            # Use default parameters
            self.model = base_model
            self.model.fit(X, y)
        
        return self
    
    def predict(self, X):
        """Make predictions"""
        if isinstance(X, pd.DataFrame):
            X = X.values
        return self.model.predict(X)
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance
        
        Returns:
            dict: Metrics including R², RMSE, MAE
        """
        y_pred = self.predict(X_test)
        
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        
        return {
            'r2': r2,
            'rmse': rmse,
            'mae': mae,
            'predictions': y_pred
        }
    
    def cross_validate(self, X, y, cv_folds=5):
        """
        Perform cross-validation
        
        Returns:
            dict: Mean and std of R² scores
        """
        if isinstance(X, pd.DataFrame):
            X = X.values
        if isinstance(y, pd.Series):
            y = y.values
            
        scores = cross_val_score(self.model, X, y, cv=cv_folds, 
                                 scoring='r2', n_jobs=-1)
        
        return {
            'mean_r2': scores.mean(),
            'std_r2': scores.std(),
            'all_scores': scores
        }
    
    def get_feature_importance(self):
        """
        Extract feature importance
        
        Returns:
            pd.DataFrame: Features ranked by importance
        """
        if self.model_type == 'rf':
            importance = self.model.feature_importances_
        else:  # xgb
            importance = self.model.feature_importances_
        
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return importance_df

def plot_feature_importance(importance_df, top_n=10, title='Feature Importance'):
    """Visualize top N most important features"""
    plt.figure(figsize=(10, 6))
    
    top_features = importance_df.head(top_n)
    
    plt.barh(range(len(top_features)), top_features['importance'], 
             color='steelblue', alpha=0.8)
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('Importance Score', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300)
    plt.show()

def plot_predictions(y_true, y_pred, title='Actual vs Predicted'):
    """Scatter plot of predictions vs actual values"""
    plt.figure(figsize=(8, 8))
    
    plt.scatter(y_true, y_pred, alpha=0.6, edgecolors='k', s=50)
    
    # Perfect prediction line
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
    
    plt.xlabel('Actual Values', fontsize=12)
    plt.ylabel('Predicted Values', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('prediction_scatter.png', dpi=300)
    plt.show()

# --- Usage Example ---
if __name__ == "__main__":
    # Mock Data: Housing prices prediction
    from sklearn.datasets import fetch_california_housing
    
    data = fetch_california_housing()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name='Price')
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print("=" * 60)
    print("RANDOM FOREST REGRESSION")
    print("=" * 60)
    
    # Train Random Forest
    rf_model = MLRegressor(model_type='rf')
    rf_model.fit(X_train, y_train, tune_hyperparams=True)
    
    # Evaluate
    rf_results = rf_model.evaluate(X_test, y_test)
    print(f"\nTest Set Performance:")
    print(f"  R² Score: {rf_results['r2']:.4f}")
    print(f"  RMSE: {rf_results['rmse']:.4f}")
    print(f"  MAE: {rf_results['mae']:.4f}")
    
    # Cross-validation
    cv_results = rf_model.cross_validate(X_train, y_train)
    print(f"\nCross-Validation (5-fold):")
    print(f"  Mean R²: {cv_results['mean_r2']:.4f} ± {cv_results['std_r2']:.4f}")
    
    # Feature importance
    importance = rf_model.get_feature_importance()
    print("\nTop 5 Most Important Features:")
    print(importance.head())
    
    # Visualizations
    plot_feature_importance(importance, top_n=8, title='Random Forest Feature Importance')
    plot_predictions(y_test, rf_results['predictions'], title='RF: Actual vs Predicted')
    
    # ========== XGBoost ==========
    print("\n" + "=" * 60)
    print("XGBOOST REGRESSION")
    print("=" * 60)
    
    xgb_model = MLRegressor(model_type='xgb')
    xgb_model.fit(X_train, y_train, tune_hyperparams=True)
    
    xgb_results = xgb_model.evaluate(X_test, y_test)
    print(f"\nTest Set Performance:")
    print(f"  R² Score: {xgb_results['r2']:.4f}")
    print(f"  RMSE: {xgb_results['rmse']:.4f}")
    print(f"  MAE: {xgb_results['mae']:.4f}")
    
    # Feature importance
    xgb_importance = xgb_model.get_feature_importance()
    plot_feature_importance(xgb_importance, top_n=8, title='XGBoost Feature Importance')
```

## Hyperparameter Tuning Guide

### Random Forest Key Parameters
- **n_estimators**: Number of trees (100-500). More is better but slower.
- **max_depth**: Tree depth. Too deep = overfitting. Start with 20-30.
- **min_samples_split**: Minimum samples to split a node. Higher = less overfitting.
- **max_features**: Features per split. 'sqrt' is a good default.

### XGBoost Key Parameters
- **learning_rate**: Step size (0.01-0.3). Lower = more trees needed but better accuracy.
- **max_depth**: Tree depth (3-9). Lower = less overfitting.
- **n_estimators**: Number of boosting rounds (100-1000).
- **subsample**: Fraction of samples per tree (0.6-1.0).
- **colsample_bytree**: Fraction of features per tree (0.6-1.0).

## Common Pitfalls

1.  **Data Leakage**: Never include the target variable or its derivatives in features.
2.  **Not Scaling**: While tree-based models don't require scaling, it helps with interpretation.
3.  **Ignoring Feature Importance**: This is your paper's goldmine. Always visualize and discuss it.
4.  **Overfitting**: Always report cross-validation scores, not just test set scores.
5.  **Small Test Set**: Use at least 20% of data for testing (or k-fold CV if data is limited).

## Integration Workflow

- **Input**: Use **`data-cleaner`** first to handle missing values and outliers.
- **Feature Engineering**: Use **`pca-analyzer`** if you have too many correlated features.
- **Validation**: Use **`robustness-check`** to test model stability with perturbed data.
- **Sensitivity**: Use **`sensitivity-master`** to analyze how predictions change with input variations.
- **Visualization**: Use **`visual-engineer`** for publication-quality plots.

## Output Requirements for Paper

1.  **Model Specification**: "We trained a Random Forest with 300 trees and max_depth=20."
2.  **Performance Metrics**: "The model achieved R²=0.87, RMSE=2.34 on the test set."
3.  **Cross-Validation**: "5-fold CV yielded mean R²=0.85±0.03, demonstrating robust generalization."
4.  **Feature Importance Plot**: Bar chart showing top 10 features (MUST include).
5.  **Prediction Scatter Plot**: Actual vs Predicted with perfect prediction line.
6.  **Interpretation**: "GDP per capita was the most influential factor, accounting for 35% of model importance."

## Advanced: Partial Dependence Plot (Optional)

For deeper interpretability, show how predictions change with one feature while holding others constant:

```python
from sklearn.inspection import PartialDependenceDisplay

fig, ax = plt.subplots(figsize=(10, 6))
PartialDependenceDisplay.from_estimator(
    model.model, X_train, features=[0, 1], ax=ax
)
plt.tight_layout()
plt.savefig('partial_dependence.png', dpi=300)
```

This is O-Prize level analysis showing causal-like relationships.

## References & Tutorials

### Integrated Course Materials

This skill now includes comprehensive regression tutorials from 数模加油站:

#### `references/` Folder:
- **17-回归分析概述.pdf**: Overview of regression analysis theory
- **18-一元线性回归模型.pdf**: Simple linear regression (single variable)
- **19-多元线性回归模型.pdf**: Multiple linear regression
- **20-非线性回归模型.pdf**: Nonlinear regression methods

#### `examples/` Folder:
- **Regress.py / Regress.m**: Simple linear regression implementation (第18课)
- **MultipleLinearRegression.ipynb / .mlx**: Multiple regression examples (第19课)
- **code1.m, code2.py, code3.py, etc.**: Nonlinear regression examples (第20课)
- **coe1.py, volum.m**: Additional regression utilities

### Learning Path

1. **Beginners**: Start with 第17课 (overview) → 第18课 (simple regression)
2. **Intermediate**: 第19课 (multiple regression) → Run `MultipleLinearRegression.ipynb`
3. **Advanced**: 第20课 (nonlinear) → Use Random Forest/XGBoost (this skill)

### When to Use Traditional Regression vs ML

| Scenario | Method | Reason |
|----------|--------|--------|
| Need interpretable coefficients | Linear regression (第18-19课) | Clear β values |
| Small sample (< 50) | Simple regression (第18课) | Avoid overfitting |
| Complex nonlinear | Random Forest / XGBoost (this skill) | Higher accuracy |
| Feature selection critical | This skill | Feature importance built-in |

## Time Budget

- **Data preparation**: 30-60 min (use `data-cleaner`)
- **Model training**: 20-40 min (with hyperparameter tuning)
- **Feature importance analysis**: 15-30 min
- **Validation & plots**: 30-45 min
- **Total**: 1.5-3 hours

## Related Skills

- `data-cleaner`: Preprocessing before regression
- `pca-analyzer`: Dimensionality reduction for many features
- `sensitivity-master`: Analyze prediction sensitivity
- `visual-engineer`: Publication-quality plots

