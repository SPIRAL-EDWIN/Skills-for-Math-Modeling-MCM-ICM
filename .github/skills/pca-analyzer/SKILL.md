---
name: pca-analyzer
description: Dimensionality reduction technique using Principal Component Analysis. Extracts key features, removes multicollinearity, and visualizes high-dimensional data.
---

# Principal Component Analysis (PCA)

Transforms a large set of variables into a smaller one that still contains most of the information in the large set.

## When to Use

- **Dimensionality Reduction**: When you have too many variables (e.g., > 10) relative to your sample size.
- **Multicollinearity**: When independent variables are highly correlated (which breaks regression models).
- **Feature Extraction**: To create new, uncorrelated indices (Principal Components) for ranking or clustering.
- **Visualization**: To plot high-dimensional data in 2D or 3D.

## Algorithm Steps

1.  **Standardization**: Scale data to have mean=0 and variance=1 (Critical step, as PCA is sensitive to scale).
2.  **Covariance Matrix**: Compute the relationship between variables.
3.  **Eigendecomposition**: Calculate eigenvalues and eigenvectors of the covariance matrix.
4.  **Selection**: Sort eigenvalues and keep the top $k$ components that explain sufficient variance (e.g., > 85%).
5.  **Projection**: Transform the original data onto the new principal component axes.

## Implementation Template

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def pca_analyzer(df, n_components=None, variance_threshold=0.85):
    """
    Perform PCA analysis.
    
    Args:
        df (pd.DataFrame): Numerical data features.
        n_components (int): Number of components to keep. If None, uses variance_threshold.
        variance_threshold (float): Keep components until cumulative variance > threshold.
        
    Returns:
        dict: {
            'pca_model': sklearn PCA object,
            'transformed_data': pd.DataFrame (the principal components),
            'loadings': pd.DataFrame (correlations between vars and PCs),
            'explained_variance': np.array
        }
    """
    # 1. Standardization (Z-score normalization)
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(df)
    
    # 2. Fit PCA
    # If n_components is None, fit all first to check variance
    pca_full = PCA()
    pca_full.fit(data_scaled)
    
    # Determine n_components based on threshold if not specified
    if n_components is None:
        cumsum = np.cumsum(pca_full.explained_variance_ratio_)
        # +1 because index starts at 0
        n_components = np.argmax(cumsum >= variance_threshold) + 1
        print(f"Selected {n_components} components to explain {variance_threshold*100}% variance.")
    
    # Refit with chosen n_components
    pca = PCA(n_components=n_components)
    data_pca = pca.fit_transform(data_scaled)
    
    # 3. Create Result DataFrame
    pc_columns = [f'PC{i+1}' for i in range(n_components)]
    df_pca = pd.DataFrame(data_pca, columns=pc_columns, index=df.index)
    
    # 4. Calculate Loadings (Eigenvectors * sqrt(Eigenvalues))
    # Loadings represent the correlation between original variables and PCs
    loadings = pd.DataFrame(
        pca.components_.T * np.sqrt(pca.explained_variance_), 
        columns=pc_columns, 
        index=df.columns
    )
    
    return {
        'model': pca,
        'transformed_data': df_pca,
        'loadings': loadings,
        'explained_variance_ratio': pca.explained_variance_ratio_
    }

def plot_pca_results(pca_result):
    """Visualize Scree Plot and Loadings Heatmap"""
    pca = pca_result['model']
    loadings = pca_result['loadings']
    
    # A. Scree Plot (Pareto Chart style)
    var_ratio = pca.explained_variance_ratio_
    cum_var_ratio = np.cumsum(var_ratio)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Scree Plot
    x = range(1, len(var_ratio) + 1)
    ax1.bar(x, var_ratio, alpha=0.6, align='center', label='Individual explained variance')
    ax1.step(x, cum_var_ratio, where='mid', label='Cumulative explained variance')
    ax1.set_ylabel('Explained variance ratio')
    ax1.set_xlabel('Principal components')
    ax1.set_title('Scree Plot')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # B. Loadings Heatmap
    sns.heatmap(loadings, annot=True, cmap='coolwarm', center=0, ax=ax2)
    ax2.set_title('Factor Loadings (Correlations)')
    
    plt.tight_layout()
    plt.savefig('pca_analysis.png', dpi=300)
    plt.show()

# --- Usage Example ---
if __name__ == "__main__":
    # Mock Data: 5 correlated variables
    np.random.seed(42)
    n_samples = 100
    # X1, X2 highly correlated; X3, X4 highly correlated
    X = np.random.rand(n_samples, 5)
    X[:, 1] = X[:, 0] * 0.8 + np.random.normal(0, 0.1, n_samples) 
    
    df = pd.DataFrame(X, columns=['VarA', 'VarB', 'VarC', 'VarD', 'VarE'])
    
    # Run PCA
    result = pca_analyzer(df, variance_threshold=0.90)
    
    print("Transformed Data Head:")
    print(result['transformed_data'].head())
    
    print("\nLoadings (Interpretation):")
    print(result['loadings'])
    
    # Visualize
    plot_pca_results(result)
```

## Output Interpretation

- **Scree Plot**: The "elbow" point indicates the optimal number of components.
- **Loadings**:
    - High absolute value (>0.5) = Strong relationship.
    - Positive/Negative sign = Direction of correlation.
    - Use these to **name** your components (e.g., if PC1 correlates with GDP and Income, call it "Economic Factor").
- **Transformed Data**: Use these new `PC1`, `PC2` columns as inputs for regression or clustering (K-Means).

## Integration Workflow

- **Input**: Use **`data-cleaner`** first. PCA hates missing values.
- **Downstream**:
    - **Clustering**: Feed `transformed_data` into K-Means or Hierarchical Clustering.
    - **Regression**: Use PCs as independent variables to avoid multicollinearity (Principal Component Regression).
    - **Evaluation**: Sometimes PC1 score is used as a comprehensive evaluation index itself.
