---
name: fuzzy-evaluation
description: Fuzzy Comprehensive Evaluation for MCM/ICM competitions. Use for qualitative indicators that cannot be precisely quantified (environmental quality, teaching quality, risk assessment). Handles linguistic terms (good/fair/poor) and subjective judgments through membership functions.
---

# Fuzzy Comprehensive Evaluation

Evaluate objects with qualitative/fuzzy indicators using membership functions and fuzzy operations.

## When to Use

- **Qualitative indicators**: "Good", "Fair", "Poor" instead of precise numbers
- **Subjective judgments**: Expert opinions, satisfaction surveys
- **Environmental quality**: Air quality (clean/moderate/polluted)
- **Teaching quality**: Student evaluations (excellent/good/average/poor)
- **Risk assessment**: Low/medium/high risk levels
- **Performance appraisal**: Employee evaluations with vague criteria

**Key difference from AHP/TOPSIS**: Handles **fuzzy** (imprecise) data, not just crisp numerical values.

## Quick Start

### Core Concepts

1. **Factor Set** $U$: Evaluation factors (criteria)
   - Example: $U = \{u_1, u_2, u_3\}$ = {Product Quality, Service, Price}

2. **Evaluation Set** $V$: Evaluation grades (outcomes)
   - Example: $V = \{v_1, v_2, v_3, v_4\}$ = {Excellent, Good, Fair, Poor}

3. **Membership Matrix** $R$: Degree of membership to each grade
   - $r_{ij}$ = membership degree of factor $i$ to grade $j$
   - Each row sums to 1 (or approximately 1)

4. **Weight Vector** $A$: Importance of each factor
   - $A = (a_1, a_2, ..., a_n)$ where $\sum a_i = 1$

5. **Fuzzy Operation**: Combine weights and memberships
   - **Weighted average**: $B = A \cdot R$ (matrix multiplication)
   - **Max-min**: $b_j = \max_i \min(a_i, r_{ij})$

### Python Implementation

```python
import numpy as np

# Example: Restaurant evaluation
# Factors: Food Quality, Service, Environment, Price
# Grades: Excellent, Good, Fair, Poor

# 1. Factor weights (from AHP or expert judgment)
A = np.array([0.4, 0.3, 0.2, 0.1])  # Sum = 1

# 2. Membership matrix R (from surveys/experts)
# Each row: one factor's membership to [Excellent, Good, Fair, Poor]
R = np.array([
    [0.5, 0.3, 0.15, 0.05],  # Food Quality
    [0.3, 0.4, 0.2, 0.1],    # Service
    [0.2, 0.3, 0.3, 0.2],    # Environment
    [0.1, 0.2, 0.4, 0.3]     # Price
])

# 3. Fuzzy operation (weighted average)
B = np.dot(A, R)

print("Evaluation result (membership to each grade):")
print(f"Excellent: {B[0]:.3f}")
print(f"Good: {B[1]:.3f}")
print(f"Fair: {B[2]:.3f}")
print(f"Poor: {B[3]:.3f}")

# 4. Final grade (max membership or weighted average)
grades = ['Excellent', 'Good', 'Fair', 'Poor']
max_idx = np.argmax(B)
print(f"\nFinal grade: {grades[max_idx]} (membership={B[max_idx]:.3f})")

# Or compute weighted score (Excellent=4, Good=3, Fair=2, Poor=1)
scores = np.array([4, 3, 2, 1])
final_score = np.dot(B, scores)
print(f"Weighted score: {final_score:.2f}/4")
```

### MATLAB Implementation

```matlab
% Factor weights
A = [0.4, 0.3, 0.2, 0.1];

% Membership matrix
R = [0.5, 0.3, 0.15, 0.05;
     0.3, 0.4, 0.2, 0.1;
     0.2, 0.3, 0.3, 0.2;
     0.1, 0.2, 0.4, 0.3];

% Fuzzy operation
B = A * R;

fprintf('Evaluation result:\n');
fprintf('Excellent: %.3f\n', B(1));
fprintf('Good: %.3f\n', B(2));
fprintf('Fair: %.3f\n', B(3));
fprintf('Poor: %.3f\n', B(4));

% Final grade
[max_val, max_idx] = max(B);
grades = {'Excellent', 'Good', 'Fair', 'Poor'};
fprintf('\nFinal grade: %s (%.3f)\n', grades{max_idx}, max_val);
```

## Standard Procedure

### Step 1: Define Factor Set $U$

Identify evaluation criteria:
- $U = \{u_1, u_2, ..., u_n\}$
- Example: {Quality, Service, Environment, Price}

### Step 2: Define Evaluation Set $V$

Set evaluation grades:
- $V = \{v_1, v_2, ..., v_m\}$
- Common: {Excellent, Good, Fair, Poor} or {High, Medium, Low}

### Step 3: Construct Membership Matrix $R$

For each factor, determine membership to each grade:
- **Expert survey**: Ask experts to rate (convert to percentages)
- **Statistical data**: Count frequency in each grade
- **Membership functions**: Triangular, trapezoidal, Gaussian

$$R = \begin{bmatrix}
r_{11} & r_{12} & \cdots & r_{1m} \\
r_{21} & r_{22} & \cdots & r_{2m} \\
\vdots & \vdots & \ddots & \vdots \\
r_{n1} & r_{n2} & \cdots & r_{nm}
\end{bmatrix}$$

Each row: $\sum_{j=1}^m r_{ij} = 1$ (or ≈ 1)

### Step 4: Determine Weight Vector $A$

Assign importance to each factor:
- Use `ahp-method` for subjective weights
- Use `entropy-weight-method` for objective weights
- Or combine both (weighted average)

### Step 5: Fuzzy Composition $B = A \circ R$

Two common methods:

**1. Weighted Average (most common)**:
$$B = A \cdot R = \sum_{i=1}^n a_i \cdot r_{ij}$$

**2. Max-Min Method**:
$$b_j = \bigvee_{i=1}^n (a_i \wedge r_{ij}) = \max_i \min(a_i, r_{ij})$$

### Step 6: Interpret Results

- **Maximum membership**: Choose grade with highest $b_j$
- **Weighted score**: $\text{Score} = \sum_{j=1}^m b_j \cdot s_j$ (assign scores to grades)

## Examples in Skill

See `examples/` folder:

- **`模糊综合评价.py`**: Multi-level fuzzy evaluation (3 levels: product → sales → market)
- **`Mohuzonghe.m` / `untitled.mlx`**: MATLAB implementation of fuzzy evaluation

## Competition Tips

### Problem Recognition (Day 1)

**Fuzzy evaluation indicators**:
- "Evaluate quality/satisfaction/performance"
- Indicators described by **linguistic terms** (good/bad, high/low)
- **Subjective judgments** from experts
- No precise numerical measurements
- "Comprehensive evaluation considering multiple factors"

**Use fuzzy evaluation when**:
- Data is qualitative or subjective
- Indicators cannot be precisely measured
- Need to aggregate expert opinions

### Formulation Steps (Day 1-2)

1. **Identify factors and grades** (Step 1-2)
2. **Collect membership data** (surveys, expert panels)
3. **Construct membership matrix** (Step 3)
4. **Determine weights** (AHP or entropy method) (Step 4)
5. **Compute fuzzy composition** (Step 5)
6. **Interpret and rank** (Step 6)

### Implementation Template

```python
import numpy as np

# 1. Define problem
factors = ['Factor1', 'Factor2', 'Factor3']
grades = ['Excellent', 'Good', 'Fair', 'Poor']

# 2. Factor weights (from AHP)
A = np.array([0.5, 0.3, 0.2])  # Must sum to 1

# 3. Membership matrix (from surveys/experts)
R = np.array([
    [0.4, 0.3, 0.2, 0.1],  # Factor1
    [0.3, 0.4, 0.2, 0.1],  # Factor2
    [0.2, 0.3, 0.3, 0.2]   # Factor3
])

# 4. Fuzzy composition
B = np.dot(A, R)

# 5. Results
print("Membership to each grade:")
for grade, membership in zip(grades, B):
    print(f"{grade}: {membership:.3f}")

# 6. Final decision
max_idx = np.argmax(B)
print(f"\nFinal grade: {grades[max_idx]}")
```

### Validation (Day 3)

- **Check normalization**: Each row of $R$ should sum to ≈ 1
- **Verify weights**: $\sum a_i = 1$
- **Sensitivity analysis**: How do results change with different weights?
- **Compare methods**: Try both weighted average and max-min

### Common Pitfalls

1. **Unnormalized memberships**: Rows don't sum to 1
   - **Fix**: Normalize: $r_{ij}' = r_{ij} / \sum_j r_{ij}$

2. **Arbitrary weights**: No justification for $A$
   - **Fix**: Use AHP or entropy method

3. **Too many grades**: Hard to distinguish (e.g., 10 grades)
   - **Fix**: Use 3-5 grades (Excellent/Good/Fair/Poor)

4. **Ignoring uncertainty**: Treating fuzzy results as crisp
   - **Fix**: Report membership vector $B$, not just max grade

5. **Mixing with TOPSIS**: Different methods for different problems
   - Fuzzy: Qualitative, linguistic data
   - TOPSIS: Quantitative, numerical data

## Advanced: Multi-Level Fuzzy Evaluation

For complex problems with hierarchical factors:

**Example**: Evaluate company performance
- Level 1: Overall performance
- Level 2: Product quality, Sales ability, Market demand
- Level 3: Sub-factors under each Level 2 factor

**Procedure**:
1. Evaluate Level 3 → get $B_1, B_2, B_3$ (for each Level 2 factor)
2. Use $B_i$ as membership rows for Level 2 matrix
3. Evaluate Level 2 → get final $B$

```python
# Level 2 evaluation (example from code)
R1 = np.array([...])  # Product quality sub-factors
A1 = np.array([...])
B1 = np.dot(A1, R1)

R2 = np.array([...])  # Sales ability sub-factors
A2 = np.array([...])
B2 = np.dot(A2, R2)

# Level 1 evaluation
R = np.array([B1, B2, B3])  # Use Level 2 results
A = np.array([0.4, 0.3, 0.3])
B = np.dot(A, R)
```

## Comparison with Other Methods

| Method | Data Type | Weights | When to Use |
|--------|-----------|---------|-------------|
| **Fuzzy Evaluation** | Qualitative/linguistic | Subjective (AHP) | Vague indicators, expert opinions |
| **AHP** | Pairwise comparisons | Subjective | Hierarchical decisions |
| **TOPSIS** | Quantitative | Objective/subjective | Numerical data, clear metrics |
| **Entropy** | Quantitative | Objective | Data-driven weighting |

## References

- `references/4-模糊综合评价【微信公众号丨B站：数模加油站】.pdf`: Complete tutorial
- Fuzzy set theory: Zadeh, L.A. (1965) "Fuzzy Sets"

## Time Budget

- **Problem definition**: 20-30 min (factors and grades)
- **Data collection**: 30-60 min (surveys, expert judgments)
- **Implementation**: 15-30 min
- **Validation**: 20-30 min
- **Total**: 1.5-2.5 hours

## Related Skills

- `ahp-method`: For determining factor weights
- `entropy-weight-method`: Alternative weighting method
- `topsis-scorer`: For quantitative evaluation (not fuzzy)
- `grey-relation`: For small-sample correlation analysis
