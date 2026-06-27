---
name: entropy-weight-method
description: Objective weighting method based on information entropy. Assigns higher weights to indicators with greater dispersion (variability), avoiding subjective bias common in AHP.
---

# Entropy Weight Method (EWM)

A purely data-driven approach to determine the importance (weight) of multiple indicators.

## When to Use

- **Evaluation Problems**: When you need to rank countries, cities, or candidates based on multiple criteria.
- **Avoiding Subjectivity**: When you don't have expert domain knowledge to assign weights manually (unlike AHP).
- **Pre-step for TOPSIS**: Often used to generate the `weights` vector required for TOPSIS analysis.
- **Data Characteristics**: When your data has significant variability that reflects "information."

## Algorithm Steps

1.  **Standardization**: Normalize data to [0, 1]. Handle positive (benefit) and negative (cost) indicators differently.
2.  **Probability Calculation**: Calculate the proportion of the $i$-th sample under the $j$-th indicator.
3.  **Entropy Calculation**: Calculate the information entropy for each indicator.
4.  **Redundancy**: Calculate the coefficient of variation ($d_j = 1 - E_j$).
5.  **Weight Normalization**: Normalize the redundancy values to get weights that sum to 1.

## Implementation Template

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def entropy_weight_method(df, negative_indicators=None):
    """
    Calculate weights using Entropy Weight Method.
    
    Args:
        df (pd.DataFrame): The numerical data (rows=samples, cols=indicators).
        negative_indicators (list): List of column names that are 'cost' type (smaller is better).
                                    Default is None (all are benefit type).
    
    Returns:
        pd.Series: Weights for each column (sums to 1).
        pd.DataFrame: Normalized data matrix.
    """
    data = df.copy().astype(float)
    negative_indicators = negative_indicators if negative_indicators else []
    
    # 1. Min-Max Normalization
    normalized_data = data.copy()
    for col in data.columns:
        min_val = data[col].min()
        max_val = data[col].max()
        
        # Avoid division by zero if max == min
        if max_val == min_val:
            normalized_data[col] = 0.0
            continue
            
        if col in negative_indicators:
            # Negative (Cost) Indicator: (max - x) / (max - min)
            normalized_data[col] = (max_val - data[col]) / (max_val - min_val)
        else:
            # Positive (Benefit) Indicator: (x - min) / (max - min)
            normalized_data[col] = (data[col] - min_val) / (max_val - min_val)
            
    # 2. Calculate Proportions (P_ij)
    # Add small epsilon to avoid log(0) later, but conceptually we normalize columns sum to 1
    # Note: Standard EWM often normalizes so sum(P_ij over i) = 1
    sum_per_col = normalized_data.sum(axis=0)
    
    # Avoid division by zero for constant columns
    epsilon = 1e-9
    P = normalized_data.div(sum_per_col + epsilon, axis=1)
    
    # 3. Calculate Entropy (E_j)
    # k = 1 / ln(n), where n is number of samples
    n = len(df)
    if n <= 1:
        # Fallback for single sample
        return pd.Series([1.0/len(df.columns)]*len(df.columns), index=df.columns), normalized_data

    k = 1.0 / np.log(n)
    
    # Compute E_j = -k * sum(p * ln(p))
    # Add epsilon inside log to avoid log(0)
    E = -k * (P * np.log(P + epsilon)).sum(axis=0)
    
    # 4. Calculate Redundancy (d_j)
    d = 1 - E
    
    # 5. Calculate Weights (W_j)
    weights = d / d.sum()
    
    return weights, normalized_data

# --- Usage Example ---
if __name__ == "__main__":
    # Mock Data: 4 Cities, 3 Indicators
    # GDP (Pos), Pollution (Neg), GreenSpace (Pos)
    data = {
        'GDP': [100, 120, 90, 150],
        'Pollution': [50, 80, 40, 60],
        'GreenSpace': [20, 15, 25, 18]
    }
    df = pd.DataFrame(data)
    
    # Calculate Weights
    weights, norm_df = entropy_weight_method(df, negative_indicators=['Pollution'])
    
    print("Calculated Weights:")
    print(weights)
    
    # Visualization
    plt.figure(figsize=(8, 5))
    weights.sort_values().plot(kind='barh', color='skyblue', edgecolor='black')
    plt.title('Indicator Weights (Entropy Method)', fontsize=14)
    plt.xlabel('Weight')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('ewm_weights.png', dpi=300)
    plt.show()
```

## Common Pitfalls

1.  **Zero/Negative Values**: The standard log method fails with zeros. This implementation uses Min-Max normalization and adds an epsilon ($1e-9$) to safely handle zeros.
2.  **Outliers**: EWM is sensitive to outliers. A single extreme value can artificially inflate the variance (and thus the weight) of an indicator. Check your data distribution first (use `data-cleaner`).
3.  **Meaningless Variation**: Sometimes data varies (high entropy) but it's just noise. EWM will assign high weight regardless. Verify weights align with common sense.

## Integration with Other Skills

- **Input**: Use **`data-cleaner`** first to handle missing values.
- **Combination**: Often combined with **`ahp-method`** (Analytic Hierarchy Process) to create "Combined Weights" ($W = \alpha W_{entropy} + \beta W_{ahp}$). This balances data objectivity with expert subjectivity.
- **Output**: Pass the resulting `weights` vector to **`topsis-scorer`** to perform the final ranking of alternatives.

## Workflow Example
1. Run `entropy-weight-method` → Get $W_e$.
2. Run `ahp-method` → Get $W_a$.
3. Average them: $W_{final} = 0.5 W_e + 0.5 W_a$.
4. Run `topsis-scorer` with $W_{final}$.
