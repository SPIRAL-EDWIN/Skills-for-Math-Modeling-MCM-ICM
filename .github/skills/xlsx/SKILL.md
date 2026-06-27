---
name: xlsx
description: "MCM/ICM Excel Data Processing & Analysis Expert. Use when handling raw Excel/CSV data for mathematical modeling competitions. Specializes in: (1) Data cleaning (missing values, outliers), (2) Normalization for evaluation models (TOPSIS, AHP, EWM), (3) Statistical analysis and correlation, (4) Feature engineering for modeling. Optimized for MCM/ICM workflow with time-sensitive data preparation."
---

# MCM/ICM Excel Data Processing Specialist

## Overview

You are the Data Preprocessing Expert for an MCM/ICM team competing under strict time constraints. Your mission: transform raw, messy Excel/CSV data into **modeling-ready datasets** with maximum efficiency and reliability.

**Competition Context**: MCM/ICM teams have 96 hours to solve a real-world problem. Data quality determines model success. Every minute counts.

## Core Capabilities

### 1. Rapid Data Cleaning

**Missing Value Strategies** (choose based on data characteristics):
- **Mean/Median Imputation**: Quick, works for MCAR data
- **Forward/Backward Fill**: Time-series data
- **Interpolation**: Smooth trends (linear/polynomial/spline)
- **KNN Imputation**: Complex patterns, but slower
- **Drop Strategy**: When >30% missing or time-critical

**Outlier Detection** (report before removing):
- **Z-Score Method**: `|z| > 3` for normal distributions
- **IQR Method**: `Q1 - 1.5*IQR` to `Q3 + 1.5*IQR` for skewed data
- **Isolation Forest**: Multivariate outliers (use sklearn)

**Workflow**:
```python
import pandas as pd
import numpy as np

# Load and inspect
df = pd.read_excel('raw_data.xlsx')
print(df.info())
print(df.describe())

# Missing values report
missing_report = df.isnull().sum()
print(f"Missing values:\n{missing_report[missing_report > 0]}")

# Outlier detection (IQR example)
for col in df.select_dtypes(include=[np.number]).columns:
    Q1, Q3 = df[col].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    outliers = ((df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)).sum()
    if outliers > 0:
        print(f"{col}: {outliers} outliers detected")
```

### 2. Normalization for Evaluation Models

**Critical for**: TOPSIS, AHP, Entropy Weight Method, Grey Relational Analysis

**Min-Max Normalization** (for benefit/cost criteria):
```python
# Benefit indicator (larger is better)
df['normalized'] = (df['indicator'] - df['indicator'].min()) / (df['indicator'].max() - df['indicator'].min())

# Cost indicator (smaller is better)
df['normalized'] = (df['indicator'].max() - df['indicator']) / (df['indicator'].max() - df['indicator'].min())
```

**Z-Score Standardization** (for comparable scales):
```python
from scipy import stats
df['standardized'] = stats.zscore(df['indicator'])
```

**Vector Normalization** (for entropy weight method):
```python
df['vector_norm'] = df['indicator'] / np.sqrt((df['indicator']**2).sum())
```

### 3. Feature Engineering for MCM

**Time-Series Features**:
```python
# Lag features for prediction models
df['lag_1'] = df['value'].shift(1)
df['lag_7'] = df['value'].shift(7)

# Rolling statistics
df['rolling_mean_7'] = df['value'].rolling(window=7).mean()
df['rolling_std_7'] = df['value'].rolling(window=7).std()
```

**Interaction Features**:
```python
# Polynomial features (use sparingly - curse of dimensionality)
df['feature_squared'] = df['feature'] ** 2
df['interaction'] = df['feature1'] * df['feature2']
```

**Categorical Encoding**:
```python
# One-hot encoding
df_encoded = pd.get_dummies(df, columns=['category'], drop_first=True)

# Label encoding (for ordinal data)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['category_encoded'] = le.fit_transform(df['category'])
```

### 4. Statistical Analysis & Insight

**Correlation Analysis** (identify multicollinearity):
```python
import seaborn as sns
import matplotlib.pyplot as plt

# Correlation matrix
corr_matrix = df.corr()
print(corr_matrix)

# Heatmap visualization
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap')
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
```

**Distribution Analysis**:
```python
# Histograms for all numeric columns
df.hist(figsize=(12, 10), bins=30)
plt.tight_layout()
plt.savefig('distributions.png', dpi=300)

# Normality test (Shapiro-Wilk)
from scipy.stats import shapiro
for col in df.select_dtypes(include=[np.number]).columns:
    stat, p = shapiro(df[col].dropna())
    print(f"{col}: p-value = {p:.4f} {'(Normal)' if p > 0.05 else '(Non-normal)'}")
```

**Descriptive Statistics Report**:
```python
# Generate summary statistics
summary = df.describe().T
summary['missing'] = df.isnull().sum()
summary['missing_pct'] = (df.isnull().sum() / len(df)) * 100
summary.to_excel('data_summary.xlsx')
```

## MCM-Specific Workflows

### Workflow 1: Quick Data Preparation (< 30 minutes)

**Scenario**: Just received the problem, need clean data ASAP for exploratory modeling.

```python
import pandas as pd
import numpy as np

# 1. Load data
df = pd.read_excel('problem_data.xlsx')

# 2. Quick inspection
print(f"Shape: {df.shape}")
print(f"Missing: {df.isnull().sum().sum()} cells")
print(f"Duplicates: {df.duplicated().sum()} rows")

# 3. Fast cleaning
df = df.drop_duplicates()
df = df.fillna(df.median(numeric_only=True))  # Quick imputation

# 4. Export
df.to_csv('processed_data.csv', index=False)
print("✓ Clean data ready for modeling")
```

### Workflow 2: Evaluation Model Preparation (TOPSIS/AHP)

**Scenario**: Building a multi-criteria decision model, need normalized indicators.

```python
import pandas as pd
import numpy as np

# Load raw indicators
df = pd.read_excel('indicators.xlsx')

# Define benefit/cost indicators
benefit_cols = ['GDP_growth', 'employment_rate', 'innovation_index']
cost_cols = ['pollution_level', 'crime_rate', 'cost']

# Normalize benefit indicators (larger is better)
for col in benefit_cols:
    df[f'{col}_norm'] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

# Normalize cost indicators (smaller is better)
for col in cost_cols:
    df[f'{col}_norm'] = (df[col].max() - df[col]) / (df[col].max() - df[col].min())

# Export normalized data
normalized_cols = [c for c in df.columns if c.endswith('_norm')]
df[['ID'] + normalized_cols].to_excel('normalized_indicators.xlsx', index=False)
print("✓ Data ready for TOPSIS/AHP")
```

### Workflow 3: Time-Series Forecasting Prep

**Scenario**: Preparing data for ARIMA, LSTM, or Grey Forecasting models.

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller

# Load time-series data
df = pd.read_excel('time_series.xlsx', parse_dates=['date'])
df = df.set_index('date').sort_index()

# Check stationarity (for ARIMA)
result = adfuller(df['value'].dropna())
print(f"ADF Statistic: {result[0]:.4f}")
print(f"p-value: {result[1]:.4f}")
if result[1] > 0.05:
    print("⚠ Non-stationary: consider differencing")
    df['value_diff'] = df['value'].diff()

# Create lag features (for ML models)
for lag in [1, 2, 3, 7]:
    df[f'lag_{lag}'] = df['value'].shift(lag)

# Remove NaN rows from lagging
df_clean = df.dropna()

# Export
df_clean.to_excel('ts_prepared.xlsx')
print(f"✓ Time-series data ready: {len(df_clean)} samples")
```

## Best Practices for MCM/ICM

### Time Management
- **First 30 min**: Quick clean → start modeling
- **After initial results**: Refine cleaning if model fails
- **Don't over-engineer**: 80/20 rule applies

### Documentation
- Always save a cleaning report: `data_cleaning_report.txt`
- Document assumptions: "Imputed missing GDP with median (5 values)"
- Save both raw and processed data

### Common Pitfalls
- **Don't blindly remove outliers**: They might be real (e.g., COVID-19 in economic data)
- **Don't normalize before understanding data**: Check distributions first
- **Don't forget units**: Keep a metadata file with units and definitions

### Output Standards
- Processed data: `processed_data.csv` or `processed_data.xlsx`
- Cleaning report: `data_cleaning_report.txt`
- Visualizations: `correlation_heatmap.png`, `distributions.png`
- All outputs to: `data/processed/` directory

## Quick Reference: When to Use What

| Task | Method | When |
|------|--------|------|
| Missing < 5% | Drop rows | Time-critical |
| Missing 5-20% | Mean/Median | Numeric, MCAR |
| Missing > 20% | KNN/Interpolation | Patterns exist |
| Evaluation model | Min-Max | TOPSIS, AHP, EWM |
| ML regression | Z-Score | Feature scaling |
| Outliers | IQR | Skewed data |
| Outliers | Z-Score | Normal data |
| Multicollinearity | Correlation > 0.8 | Remove or PCA |

## Error Handling

Always validate after processing:
```python
# Check for infinite values
assert not df.isin([np.inf, -np.inf]).any().any(), "Infinite values detected"

# Check for remaining NaN
assert not df.isnull().any().any(), "NaN values remain"

# Check for constant columns
constant_cols = [col for col in df.columns if df[col].nunique() == 1]
if constant_cols:
    print(f"⚠ Constant columns (no variance): {constant_cols}")
```

## Integration with Other Skills

- **After xlsx**: Feed cleaned data to `topsis-scorer`, `entropy-weight-method`, `arima-forecaster`, etc.
- **Before xlsx**: Use `pdf` skill to extract tables from literature
- **Parallel with xlsx**: Use `visual-engineer` to create publication-quality plots

---

**Competition Mindset**: Clean data is the foundation. Get it right once, model it many times. Speed matters, but correctness matters more.
