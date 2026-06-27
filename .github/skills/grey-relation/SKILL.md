---
name: grey-relation
description: Grey Relational Analysis for MCM/ICM competitions. Use for small-sample correlation analysis and factor importance ranking. Does not require large samples, normal distribution, or linear relationships. Ideal for analyzing which factors most influence outcomes when data is limited.
---

# Grey Relational Analysis (GRA)

Analyze correlation between factors and outcomes using grey relational grade, especially for small samples.

## When to Use

- **Small sample size**: 4-20 data points (unlike correlation which needs >30)
- **Factor analysis**: Which factors most influence the outcome?
- **Non-linear relationships**: No assumption of linearity
- **Multi-factor ranking**: Rank importance of multiple influencing factors
- **Incomplete information**: "Grey" = between black (unknown) and white (known)

**Key difference from correlation coefficient**:
- No requirement for large samples
- No assumption of linear relationship
- No requirement for normal distribution

**This is NOT forecasting**: Use `grey-forecaster` for prediction, use `grey-relation` for correlation analysis.

## Quick Start

### Core Concepts

1. **Reference sequence** (母序列) $X_0$: The outcome/target variable
   - Example: Student test scores

2. **Comparison sequences** (子序列) $X_i$: The influencing factors
   - Example: Study hours, sleep hours, exercise hours

3. **Grey relational coefficient** $\xi_i(k)$: Similarity at each data point
   $$\xi_i(k) = \frac{\min_i \min_k |x_0(k) - x_i(k)| + \rho \max_i \max_k |x_0(k) - x_i(k)|}{|x_0(k) - x_i(k)| + \rho \max_i \max_k |x_0(k) - x_i(k)|}$$
   where $\rho = 0.5$ (resolution coefficient, usually 0.5)

4. **Grey relational grade** $\gamma_i$: Overall correlation (average of coefficients)
   $$\gamma_i = \frac{1}{n} \sum_{k=1}^n \xi_i(k)$$

5. **Ranking**: Higher $\gamma_i$ means stronger correlation

### Python Implementation

```python
import numpy as np

# Example: Which factor most affects test scores?
# Columns: [Test Score, Study Hours, Sleep Hours, Exercise Hours]
data = np.array([
    [55, 24, 10, 5],
    [65, 38, 22, 8],
    [75, 40, 18, 6],
    [100, 50, 20, 10]
])

# Step 1: Normalization (dimensionless)
mean = np.mean(data, axis=0)
data_norm = data / mean

# Step 2: Reference sequence (outcome)
Y = data_norm[:, 0]  # Test scores

# Step 3: Comparison sequences (factors)
X = data_norm[:, 1:]  # Study, Sleep, Exercise

# Step 4: Calculate absolute differences |X0 - Xi|
abs_diff = np.abs(X - Y.reshape(-1, 1))

# Step 5: Find min and max differences
a = np.min(abs_diff)  # Two-level minimum
b = np.max(abs_diff)  # Two-level maximum

# Step 6: Resolution coefficient
rho = 0.5

# Step 7: Grey relational coefficient
gamma_matrix = (a + rho * b) / (abs_diff + rho * b)

# Step 8: Grey relational grade (average)
gamma = np.mean(gamma_matrix, axis=0)

# Step 9: Rank factors
factors = ['Study Hours', 'Sleep Hours', 'Exercise Hours']
ranking = sorted(zip(factors, gamma), key=lambda x: x[1], reverse=True)

print("Grey Relational Grade:")
for factor, grade in ranking:
    print(f"{factor}: {grade:.4f}")

print(f"\nMost important factor: {ranking[0][0]}")
```

### MATLAB Implementation

```matlab
% Data: [Test Score, Study Hours, Sleep Hours, Exercise Hours]
A = [55, 24, 10, 5;
     65, 38, 22, 8;
     75, 40, 18, 6;
     100, 50, 20, 10];

% Step 1: Normalization
Mean = mean(A, 1);
A_norm = A ./ Mean;

% Step 2: Reference sequence
Y = A_norm(:, 1);

% Step 3: Comparison sequences
X = A_norm(:, 2:end);

% Step 4: Absolute differences
absX0_Xi = abs(X - repmat(Y, 1, size(X, 2)));

% Step 5: Min and max
a = min(absX0_Xi(:));
b = max(absX0_Xi(:));

% Step 6: Resolution coefficient
rho = 0.5;

% Step 7: Grey relational coefficient
gamma_matrix = (a + rho * b) ./ (absX0_Xi + rho * b);

% Step 8: Grey relational grade
gamma = mean(gamma_matrix, 1);

% Step 9: Display results
factors = {'Study Hours', 'Sleep Hours', 'Exercise Hours'};
fprintf('Grey Relational Grade:\n');
for i = 1:length(factors)
    fprintf('%s: %.4f\n', factors{i}, gamma(i));
end

[~, idx] = max(gamma);
fprintf('\nMost important factor: %s\n', factors{idx});
```

## Standard Procedure

### Step 1: Data Preparation

Organize data into matrix:
- Rows: Samples (observations)
- Columns: [Outcome, Factor1, Factor2, ..., FactorN]

### Step 2: Normalization (Dimensionless)

Three common methods:

**1. Mean normalization** (most common):
$$x_i'(k) = \frac{x_i(k)}{\bar{x_i}}$$

**2. Min-max normalization**:
$$x_i'(k) = \frac{x_i(k) - \min x_i}{\max x_i - \min x_i}$$

**3. Initial value normalization**:
$$x_i'(k) = \frac{x_i(k)}{x_i(1)}$$

### Step 3: Separate Reference and Comparison

- Reference sequence $X_0$: The outcome variable
- Comparison sequences $X_1, X_2, ..., X_m$: The factors

### Step 4: Calculate Differences

$$\Delta_i(k) = |x_0(k) - x_i(k)|$$

### Step 5: Find Two-Level Extrema

$$a = \min_i \min_k \Delta_i(k)$$
$$b = \max_i \max_k \Delta_i(k)$$

### Step 6: Calculate Grey Relational Coefficient

$$\xi_i(k) = \frac{a + \rho b}{\Delta_i(k) + \rho b}$$

where $\rho \in [0, 1]$ is resolution coefficient (usually 0.5)

### Step 7: Calculate Grey Relational Grade

$$\gamma_i = \frac{1}{n} \sum_{k=1}^n \xi_i(k)$$

### Step 8: Rank Factors

Sort factors by $\gamma_i$ in descending order.

## Examples in Skill

See `examples/` folder:

- **`code1.py` / `code1.m`**: Basic grey relational analysis with normalization
- **`code2.py` / `code2.m`**: Alternative implementation
- **`Inter2Max.m`, `Mid2Max.m`, `Min2Max.m`**: Data preprocessing functions (convert to "larger is better")
- **`Positivization.m`**: Positive transformation for indicators

## Competition Tips

### Problem Recognition (Day 1)

**Grey relational analysis indicators**:
- "Which factors most influence..."
- "Rank importance of factors"
- **Small sample size** (< 30 observations)
- No clear linear relationship
- Multiple factors, need to find key drivers

**Use GRA when**:
- Sample size is small (4-20 points)
- Don't know if relationship is linear
- Want to rank factor importance
- Data doesn't meet assumptions for regression/correlation

### Formulation Steps (Day 1-2)

1. **Define outcome variable**: What are you trying to explain?
2. **Identify factors**: What might influence the outcome?
3. **Collect data**: Organize into matrix
4. **Normalize**: Make data dimensionless
5. **Compute GRA**: Follow 8-step procedure
6. **Interpret**: Rank factors by grey relational grade

### Implementation Template

```python
import numpy as np

# 1. Prepare data (rows=samples, cols=[outcome, factor1, factor2, ...])
data = np.array([
    [y1, x1_1, x1_2, ...],
    [y2, x2_1, x2_2, ...],
    # ...
])

# 2. Normalize
mean = np.mean(data, axis=0)
data_norm = data / mean

# 3. Separate reference and comparison
Y = data_norm[:, 0]
X = data_norm[:, 1:]

# 4. Calculate differences
abs_diff = np.abs(X - Y.reshape(-1, 1))

# 5. Two-level extrema
a = np.min(abs_diff)
b = np.max(abs_diff)

# 6. Grey relational coefficient
rho = 0.5
gamma_matrix = (a + rho * b) / (abs_diff + rho * b)

# 7. Grey relational grade
gamma = np.mean(gamma_matrix, axis=0)

# 8. Rank and display
factors = ['Factor1', 'Factor2', 'Factor3']
for factor, grade in sorted(zip(factors, gamma), 
                            key=lambda x: x[1], reverse=True):
    print(f"{factor}: {grade:.4f}")
```

### Validation (Day 3)

- **Check normalization**: All sequences should be dimensionless
- **Verify ranking**: Does it match intuition/domain knowledge?
- **Sensitivity to $\rho$**: Try $\rho = 0.3, 0.5, 0.7$ - ranking should be stable
- **Compare with correlation**: For validation, compute Pearson correlation

### Common Pitfalls

1. **Confusing with grey forecasting**: GRA is for correlation, not prediction
   - **Fix**: Use `grey-forecaster` for time series prediction

2. **Too large sample**: If n > 50, use standard correlation/regression
   - GRA advantage is for small samples

3. **Forgot normalization**: Different units make comparison meaningless
   - **Fix**: Always normalize first

4. **Wrong reference sequence**: Used factor as reference instead of outcome
   - **Fix**: Reference = outcome variable, comparison = factors

5. **Over-interpreting**: High $\gamma$ doesn't mean causation
   - GRA shows correlation, not causation

## Advanced: Data Preprocessing

### Indicator Direction Transformation

Convert all indicators to "larger is better":

**1. Cost-type (smaller is better) → Benefit-type**:
$$x_i'(k) = \max x_i - x_i(k)$$

**2. Interval-type (optimal range [a, b])**:
$$x_i'(k) = \begin{cases}
1 - \frac{a - x_i(k)}{M}, & x_i(k) < a \\
1, & a \leq x_i(k) \leq b \\
1 - \frac{x_i(k) - b}{M}, & x_i(k) > b
\end{cases}$$

where $M = \max\{a - \min x_i, \max x_i - b\}$

## Comparison with Other Methods

| Method | Sample Size | Assumptions | When to Use |
|--------|-------------|-------------|-------------|
| **Grey Relational Analysis** | Small (4-20) | None | Small sample, non-linear |
| **Pearson Correlation** | Large (>30) | Linear, normal | Large sample, linear |
| **Spearman Correlation** | Medium (>10) | Monotonic | Non-linear but monotonic |
| **Regression** | Large (>30) | Linear, normal | Prediction, causation |

## References

- `references/5-灰色关联分析【微信公众号丨B站：数模加油站】.pdf`: Complete tutorial
- Deng, J. (1982) "Control problems of grey systems"

## Time Budget

- **Data preparation**: 15-30 min
- **Normalization**: 10-15 min
- **Implementation**: 15-25 min
- **Validation**: 20-30 min
- **Total**: 1-1.5 hours

## Related Skills

- `grey-forecaster`: Grey prediction (GM(1,1)) for time series
- `pca-analyzer`: Alternative for factor analysis (large samples)
- `entropy-weight-method`: Objective weighting based on data variation
- `fuzzy-evaluation`: For qualitative factor evaluation
