---
name: topsis-scorer
description: Comprehensive evaluation method that ranks alternatives based on their geometric distance to the 'Positive Ideal Solution' and 'Negative Ideal Solution'.
---

# TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)

Calculates a score (0 to 1) for each option. The best option is closest to the ideal best and farthest from the ideal worst.

## When to Use

- **Ranking**: When you have multiple candidates/plans and need to pick the "best" one.
- **Multi-Criteria Decision Making (MCDM)**: The standard solver for Problem E/F.
- **Post-Weighting**: Use this **AFTER** obtaining weights from AHP or Entropy Method.

## Algorithm Steps

1.  **Vector Normalization**: $z_{ij} = x_{ij} / \sqrt{\sum x_{ij}^2}$.
2.  **Apply Weights**: Multiply normalized columns by input weights.
3.  **Determine Ideal Solutions**:
    - $Z^+$ (Best): Max value for benefit criteria, Min value for cost criteria.
    - $Z^-$ (Worst): Min value for benefit criteria, Max value for cost criteria.
4.  **Calculate Distances**: Euclidean distance to $Z^+$ ($D^+$) and $Z^-$ ($D^-$).
5.  **Calculate Score**: $C_i = D^-_i / (D^+_i + D^-_i)$.
6.  **Rank**: Higher score is better.

## Implementation Template

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def topsis_scorer(df, weights, negative_indicators=None):
    """
    Perform TOPSIS analysis.
    
    Args:
        df (pd.DataFrame): Raw numerical data (Alternatives x Criteria).
        weights (list or pd.Series): Weights corresponding to columns. Must sum to 1.
        negative_indicators (list): List of column names where 'smaller is better'.
        
    Returns:
        pd.DataFrame: Result dataframe with 'Distance_Pos', 'Distance_Neg', 'Score', 'Rank'.
    """
    data = df.copy().astype(float)
    weights = np.array(weights)
    negative_indicators = negative_indicators if negative_indicators else []
    
    # Verify dimensions
    if len(weights) != data.shape[1]:
        raise ValueError(f"Length of weights ({len(weights)}) matches columns ({data.shape[1]})")
        
    # 1. Vector Normalization
    # denom = sqrt(sum(x^2))
    norm_data = data / np.sqrt((data**2).sum(axis=0))
    
    # 2. Apply Weights
    weighted_data = norm_data * weights
    
    # 3. Determine Ideal Solutions
    ideal_best = []
    ideal_worst = []
    
    for col in data.columns:
        if col in negative_indicators:
            # Cost criteria: Best is Min, Worst is Max
            ideal_best.append(weighted_data[col].min())
            ideal_worst.append(weighted_data[col].max())
        else:
            # Benefit criteria: Best is Max, Worst is Min
            ideal_best.append(weighted_data[col].max())
            ideal_worst.append(weighted_data[col].min())
            
    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)
    
    # 4. Calculate Euclidean Distances
    # shape: (n_samples, n_features) - (n_features,)
    d_pos = np.sqrt(((weighted_data - ideal_best)**2).sum(axis=1))
    d_neg = np.sqrt(((weighted_data - ideal_worst)**2).sum(axis=1))
    
    # 5. Calculate Score
    # Score = D_neg / (D_pos + D_neg)
    scores = d_neg / (d_pos + d_neg)
    
    # Pack results
    results = df.copy()
    results['TOPSIS_Score'] = scores
    results['Rank'] = scores.rank(ascending=False).astype(int)
    
    return results.sort_values('Rank')

# --- Usage Example ---
if __name__ == "__main__":
    # Mock Data
    data = pd.DataFrame({
        'GDP': [100, 120, 90, 150],       # Weight 0.4
        'Pollution': [50, 80, 40, 60],    # Weight 0.4 (Neg)
        'GreenSpace': [20, 15, 25, 18]    # Weight 0.2
    })
    
    # Weights usually come from Entropy or AHP
    weights = [0.4, 0.4, 0.2] 
    
    results = topsis_scorer(data, weights, negative_indicators=['Pollution'])
    
    print(results[['TOPSIS_Score', 'Rank']])
    
    # Visualization
    plt.figure(figsize=(8, 5))
    results['TOPSIS_Score'].plot(kind='bar', color='coral', alpha=0.8)
    plt.title('TOPSIS Rankings', fontsize=14)
    plt.ylabel('Score')
    plt.tight_layout()
    plt.savefig('topsis_results.png', dpi=300)
    plt.show()
```

## Integration Workflow

This is the final step in the evaluation pipeline:
- **Pre-requisite 1**: Clean data using `data-cleaner`.
- **Pre-requisite 2**: Get weights from **`entropy-weight-method`** (objective) OR **`ahp-method`** (subjective).
- **Action**: Run `topsis-scorer` with the data and weights.
