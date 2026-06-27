---
name: linear-programming
description: Linear Programming solver for MCM/ICM competitions. Use when optimizing linear objective functions subject to linear constraints (resource allocation, production planning, transportation problems). Supports simplex method, interior-point, and graphical solutions.
---

# Linear Programming

Solve linear optimization problems: maximize/minimize a linear objective function subject to linear constraints.

## When to Use

- **Resource allocation**: Maximize profit with limited resources
- **Production planning**: Minimize cost while meeting demand
- **Transportation**: Optimize shipping routes
- **Diet problem**: Minimize cost while meeting nutritional requirements
- **Portfolio optimization**: Maximize return with risk constraints

## Quick Start

### Python (scipy.optimize.linprog)

```python
from scipy.optimize import linprog

# Minimize: c^T * x
# Subject to: A_ub @ x <= b_ub
#            A_eq @ x == b_eq
#            bounds for x

c = [-1, -2]  # Coefficients (negate for maximization)
A_ub = [[1, 1], [2, 1]]  # Inequality constraints
b_ub = [4, 5]

result = linprog(c, A_ub=A_ub, b_ub=b_ub, method='highs')
print(f"Optimal value: {-result.fun}")  # Negate back
print(f"Optimal solution: {result.x}")
```

### MATLAB (linprog)

```matlab
% Minimize: f' * x
% Subject to: A * x <= b
%            Aeq * x == beq
%            lb <= x <= ub

f = [-1; -2];  % Coefficients (negate for maximization)
A = [1, 1; 2, 1];  % Inequality constraints
b = [4; 5];

[x, fval] = linprog(f, A, b);
fprintf('Optimal value: %.4f\n', -fval);
fprintf('Optimal solution: [%.4f, %.4f]\n', x);
```

## Standard Form

**Maximize**: $z = c_1x_1 + c_2x_2 + ... + c_nx_n$

**Subject to**:
- $a_{11}x_1 + a_{12}x_2 + ... + a_{1n}x_n \leq b_1$
- $a_{21}x_1 + a_{22}x_2 + ... + a_{2n}x_n \leq b_2$
- ...
- $x_1, x_2, ..., x_n \geq 0$ (non-negativity)

## Examples in Skill

See `examples/` folder:
- `touzi.ipynb` / `Touzi.mlx`: Investment allocation problem
- `youxi.ipynb` / `youxi.mlx`: Game strategy optimization

## Competition Tips

### Model Formulation (Day 1)

1. **Define decision variables**: What are you optimizing?
2. **Write objective function**: Linear combination of variables
3. **List all constraints**: 
   - Resource limits (≤)
   - Demand requirements (≥)
   - Equality constraints (=)
4. **Check linearity**: All terms are $ax$ (not $x^2$, $xy$, $\sin(x)$, etc.)

### Implementation (Day 2)

```python
# Template
from scipy.optimize import linprog

# Decision variables: x = [x1, x2, ..., xn]

# Objective: minimize c^T * x (negate c for maximization)
c = [...]

# Inequality: A_ub @ x <= b_ub
A_ub = [[...], [...]]
b_ub = [...]

# Equality: A_eq @ x == b_eq (if any)
A_eq = [[...]]
b_eq = [...]

# Bounds: lb <= x <= ub
bounds = [(0, None), (0, 10), ...]  # (min, max) for each variable

# Solve
result = linprog(c, A_ub=A_ub, b_ub=b_ub, 
                 A_eq=A_eq, b_eq=b_eq, 
                 bounds=bounds, method='highs')

if result.success:
    print(f"Optimal: {result.x}")
    print(f"Value: {result.fun}")
else:
    print("No solution found")
```

### Validation (Day 3)

- **Sensitivity analysis**: How does optimal solution change with constraint bounds?
- **Shadow prices**: `result.ineqlin.marginals` (dual values)
- **Graphical check**: For 2D problems, plot feasible region

### Common Pitfalls

1. **Maximization**: Must negate objective coefficients for `linprog` (it minimizes)
2. **Inequality direction**: `linprog` uses ≤, convert ≥ by multiplying by -1
3. **Unbounded**: Check if problem is properly constrained
4. **Infeasible**: Constraints may be contradictory

## Advanced: Integer Programming

If variables must be integers (0/1 decisions, discrete quantities), use:
- Python: `scipy.optimize.milp` or `pulp`
- MATLAB: `intlinprog`

See `integer-programming` skill for details.

## References

- `references/7-线性规划【微信公众号丨B站：数模加油站】.pdf`: Complete tutorial with theory and examples
- SciPy docs: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
- MATLAB docs: https://www.mathworks.com/help/optim/ug/linprog.html

## Time Budget

- **Formulation**: 30-60 min (most critical step)
- **Implementation**: 15-30 min
- **Validation**: 30-60 min
- **Total**: 1.5-2.5 hours

## Related Skills

- `integer-programming`: For discrete decisions
- `nonlinear-programming`: For nonlinear objectives/constraints
- `multi-objective-optimization`: For conflicting objectives
- `sensitivity-master`: For parameter sensitivity analysis
