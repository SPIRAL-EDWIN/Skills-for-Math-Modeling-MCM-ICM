---
name: data-cleaner
description: Automated data cleaning and preprocessing for MCM/ICM competitions. Use when loading raw CSV/Excel data that needs missing value handling, outlier detection, normalization, and quality reporting. Produces clean datasets and statistical summaries ready for modeling.
---

# Data-Cleaner

Systematically clean and preprocess raw data to ensure quality inputs for mathematical models.

## When to Use

- After downloading or web scraping raw data
- Before any modeling or analysis
- When data has missing values, outliers, or inconsistent formats
- Need to document data quality for paper

## Standard Cleaning Pipeline

### Step 1: Load and Inspect

```python
import pandas as pd
import numpy as np

def load_data(filepath):
    """Load data with automatic format detection"""
    
    # Detect file type
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(filepath)
    elif filepath.endswith('.json'):
        df = pd.read_json(filepath)
    else:
        raise ValueError(f"Unsupported file format: {filepath}")
    
    # Initial inspection
    print(f"Data shape: {df.shape}")
    print(f"\nColumn types:\n{df.dtypes}")
    print(f"\nFirst few rows:\n{df.head()}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nBasic statistics:\n{df.describe()}")
    
    return df
```

### Step 2: Handle Missing Values

```python
def handle_missing_values(df, strategy='auto', threshold=0.5):
    """
    Handle missing data with appropriate strategy
    
    Parameters:
    - strategy: 'auto', 'drop', 'mean', 'median', 'forward_fill', 'interpolate'
    - threshold: Drop columns if missing > threshold fraction
    """
    
    # Record initial state
    initial_shape = df.shape
    missing_report = df.isnull().sum()
    
    # Drop columns with too many missing values
    missing_fraction = df.isnull().sum() / len(df)
    cols_to_drop = missing_fraction[missing_fraction > threshold].index
    
    if len(cols_to_drop) > 0:
        print(f"Dropping columns with >{threshold*100}% missing: {list(cols_to_drop)}")
        df = df.drop(columns=cols_to_drop)
    
    # Handle remaining missing values
    for col in df.columns:
        if df[col].isnull().any():
            
            if strategy == 'auto':
                # Auto-select strategy based on data type and distribution
                if df[col].dtype in ['int64', 'float64']:
                    # Numeric: use median (robust to outliers)
                    fill_value = df[col].median()
                    df[col].fillna(fill_value, inplace=True)
                    print(f"  {col}: filled {missing_report[col]} values with median ({fill_value:.2f})")
                else:
                    # Categorical: use mode
                    fill_value = df[col].mode()[0]
                    df[col].fillna(fill_value, inplace=True)
                    print(f"  {col}: filled {missing_report[col]} values with mode ('{fill_value}')")
            
            elif strategy == 'mean':
                df[col].fillna(df[col].mean(), inplace=True)
            
            elif strategy == 'median':
                df[col].fillna(df[col].median(), inplace=True)
            
            elif strategy == 'forward_fill':
                df[col].fillna(method='ffill', inplace=True)
            
            elif strategy == 'interpolate':
                df[col].interpolate(method='linear', inplace=True)
            
            elif strategy == 'drop':
                df = df.dropna(subset=[col])
    
    print(f"\nShape after missing value handling: {initial_shape} → {df.shape}")
    
    return df
```

### Step 3: Detect and Handle Outliers

```python
def detect_outliers(df, method='iqr', threshold=3):
    """
    Detect outliers using IQR or Z-score method
    
    Parameters:
    - method: 'iqr' (Interquartile Range) or 'zscore'
    - threshold: 3 for z-score, 1.5 for IQR (standard values)
    """
    
    outlier_report = {}
    
    for col in df.select_dtypes(include=[np.number]).columns:
        
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            
        elif method == 'zscore':
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            outliers = df[z_scores > threshold]
        
        if len(outliers) > 0:
            outlier_report[col] = {
                'count': len(outliers),
                'percentage': len(outliers) / len(df) * 100,
                'values': outliers[col].tolist()
            }
            print(f"  {col}: {len(outliers)} outliers ({len(outliers)/len(df)*100:.1f}%)")
    
    return outlier_report

def handle_outliers(df, method='cap', outlier_report=None):
    """
    Handle detected outliers
    
    Parameters:
    - method: 'cap' (winsorize), 'remove', or 'keep'
    """
    
    if method == 'cap':
        # Cap at 1st and 99th percentiles
        for col in df.select_dtypes(include=[np.number]).columns:
            lower = df[col].quantile(0.01)
            upper = df[col].quantile(0.99)
            df[col] = df[col].clip(lower, upper)
        print("Outliers capped at 1st/99th percentiles")
    
    elif method == 'remove':
        # Remove rows with any outliers (use cautiously!)
        initial_len = len(df)
        for col in df.select_dtypes(include=[np.number]).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df = df[(df[col] >= Q1 - 1.5*IQR) & (df[col] <= Q3 + 1.5*IQR)]
        print(f"Removed {initial_len - len(df)} rows with outliers")
    
    elif method == 'keep':
        print("Outliers kept (no action taken)")
    
    return df
```

### Step 4: Normalize and Standardize

```python
def normalize_data(df, method='standard', columns=None):
    """
    Normalize numeric columns
    
    Parameters:
    - method: 'standard' (z-score), 'minmax' (0-1), or 'robust'
    - columns: List of columns to normalize (None = all numeric)
    """
    
    from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
    
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns
    
    if method == 'standard':
        scaler = StandardScaler()
    elif method == 'minmax':
        scaler = MinMaxScaler()
    elif method == 'robust':
        scaler = RobustScaler()  # Robust to outliers
    
    df[columns] = scaler.fit_transform(df[columns])
    
    print(f"Normalized {len(columns)} columns using {method} scaling")
    
    return df, scaler
```

### Step 5: Data Type Conversion

```python
def fix_data_types(df):
    """Convert columns to appropriate data types"""
    
    for col in df.columns:
        
        # Try to convert string dates to datetime
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col])
                print(f"  {col}: converted to datetime")
            except:
                pass
        
        # Convert object columns with few unique values to category
        if df[col].dtype == 'object':
            n_unique = df[col].nunique()
            if n_unique < 50:  # Heuristic threshold
                df[col] = df[col].astype('category')
                print(f"  {col}: converted to category ({n_unique} levels)")
    
    return df
```

## Complete Cleaning Function

```python
def clean_data(filepath, output_path='data/processed.csv', 
               missing_strategy='auto', outlier_method='cap',
               normalize=False):
    """
    Complete data cleaning pipeline
    
    Returns: cleaned DataFrame and cleaning report
    """
    
    print("="*60)
    print("DATA CLEANING PIPELINE")
    print("="*60)
    
    # Load
    print("\n[1/6] Loading data...")
    df = load_data(filepath)
    
    # Missing values
    print("\n[2/6] Handling missing values...")
    df = handle_missing_values(df, strategy=missing_strategy)
    
    # Data types
    print("\n[3/6] Fixing data types...")
    df = fix_data_types(df)
    
    # Outliers
    print("\n[4/6] Detecting outliers...")
    outlier_report = detect_outliers(df, method='iqr')
    
    print("\n[5/6] Handling outliers...")
    df = handle_outliers(df, method=outlier_method)
    
    # Normalize (optional)
    if normalize:
        print("\n[6/6] Normalizing data...")
        df, scaler = normalize_data(df, method='standard')
    else:
        print("\n[6/6] Skipping normalization")
        scaler = None
    
    # Save
    df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to: {output_path}")
    
    # Generate report
    report = {
        'original_shape': df.shape,
        'final_shape': df.shape,
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'outliers': outlier_report,
        'summary_stats': df.describe().to_dict()
    }
    
    # Save report
    import json
    with open(output_path.replace('.csv', '_report.json'), 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print("\nCleaning complete!")
    print("="*60)
    
    return df, report
```

## Usage Example

```python
# Clean data with default settings
df_clean, report = clean_data(
    filepath='data/raw_data.csv',
    output_path='data/processed.csv',
    missing_strategy='auto',
    outlier_method='cap',
    normalize=False
)

# Access cleaned data
print(df_clean.head())
print(df_clean.info())
```

## Output Files

Save to `data/`:
- `processed.csv` - Cleaned dataset
- `processed_report.json` - Cleaning statistics and decisions
- `raw_data.csv` - Original data (never modify!)

## Quality Checklist

Before using cleaned data:
- [ ] No missing values remain (or documented why kept)
- [ ] Outliers handled appropriately (not just deleted blindly)
- [ ] Data types are correct (dates as datetime, categories as category)
- [ ] Column names are clean (no spaces, lowercase)
- [ ] Duplicates checked and removed if appropriate
- [ ] Ranges are reasonable (no negative ages, etc.)

## Common Pitfalls

- **Deleting too much**: Removing outliers can lose real information
- **Wrong imputation**: Using mean for skewed data (use median)
- **No documentation**: Must record what cleaning was done
- **Normalizing too early**: Clean first, normalize last
- **Ignoring domain knowledge**: Some "outliers" are real (billionaires exist!)
