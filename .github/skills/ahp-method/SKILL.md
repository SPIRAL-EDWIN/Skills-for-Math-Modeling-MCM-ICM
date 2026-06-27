---
name: ahp-method
description: Subjective weighting method based on pairwise comparison matrices. Calculates weights using Eigenvalue method and performs Consistency Check (CR).
---

# Analytic Hierarchy Process (AHP)

A structured technique for organizing and analyzing complex decisions, based on mathematics and psychology.

## When to Use

- **Subjective Criteria**: When importance depends on expert judgment (e.g., "Safety is 3x more important than Cost").
- **Small Sample Size**: Can be used even with no data, just logical relations.
- **Combined Weighting**: Use alongside **`entropy-weight-method`** to balance subjective and objective views.

## Algorithm Steps

1.  **Construct Matrix**: Create a pairwise comparison matrix ($A$) where $a_{ij}$ represents how much more important $i$ is than $j$.
2.  **Eigenvector Calculation**: Find the max eigenvalue ($\lambda_{max}$) and corresponding eigenvector.
3.  **Normalization**: Normalize the eigenvector to sum to 1. These are the weights.
4.  **Consistency Check**:
    - Calculate Consistency Index: $CI = (\lambda_{max} - n) / (n - 1)$
    - Look up Random Index ($RI$) table.
    - Calculate Consistency Ratio: $CR = CI / RI$.
    - **Rule**: If $CR < 0.1$, matrix is consistent. Else, adjust judgments.

## Implementation Template

```python
import numpy as np
import pandas as pd

def ahp_method(comparison_matrix):
    """
    Calculate weights and consistency ratio using AHP.
    
    Args:
        comparison_matrix (np.array or list of lists): n x n pairwise comparison matrix.
        
    Returns:
        dict: {'weights': pd.Series, 'cr': float, 'consistent': bool}
    """
    A = np.array(comparison_matrix)
    n = A.shape[0]
    
    # 1. Calculate Eigenvalues and Eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(A)
    
    # 2. Find max eigenvalue and corresponding eigenvector
    max_index = np.argmax(np.real(eigenvalues))
    max_eigenvalue = np.real(eigenvalues[max_index])
    corresponding_eigenvector = np.real(eigenvectors[:, max_index])
    
    # 3. Normalize eigenvector to get weights
    weights = corresponding_eigenvector / corresponding_eigenvector.sum()
    
    # 4. Consistency Check
    RI_dict = {
        1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 
        6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49,
        11: 1.51, 12: 1.48, 13: 1.56, 14: 1.57, 15: 1.59
    }
    
    CI = (max_eigenvalue - n) / (n - 1)
    RI = RI_dict.get(n, 1.49) # Default to reasonable value if n > 15
    
    if RI == 0:
        CR = 0.0
    else:
        CR = CI / RI
        
    return {
        'weights': pd.Series(weights),
        'cr': CR,
        'consistent': CR < 0.10
    }

# --- Usage Example ---
if __name__ == "__main__":
    # Example: Choosing a Leader (Experience, Education, Charisma)
    # Experience is 3x Education, 5x Charisma
    # Education is 2x Charisma
    matrix = [
        [1,   3,   5],
        [1/3, 1,   2],
        [1/5, 1/2, 1]
    ]
    
    result = ahp_method(matrix)
    
    print("Weights:", result['weights'].values)
    print(f"CR: {result['cr']:.4f}")
    
    if result['consistent']:
        print("✅ Matrix is consistent. You can use these weights for `topsis-scorer`.")
    else:
        print("❌ Inconsistent! Adjust the comparison matrix.")
```

## Integration Workflow

1.  **Step 1**: Run **`ahp-method`** to get subjective weights ($W_s$).
2.  **Step 2**: Run **`entropy-weight-method`** to get objective weights ($W_o$).
3.  **Step 3**: Combine them (e.g., $W = 0.5 W_s + 0.5 W_o$).
4.  **Step 4**: Pass final weights to **`topsis-scorer`**.
