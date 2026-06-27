---
name: nonlinear-programming
description: Nonlinear Programming for MCM/ICM competitions. Use when objective function or constraints contain nonlinear terms (x², xy, sin(x), sqrt(x)). Handles engineering design, optimal control, parameter fitting. Requires initial guess and may find local optima.
---

# Nonlinear Programming

Solve optimization problems where the objective function or constraints are nonlinear (not just linear combinations of variables).

## When to Use

- **Engineering design**: Minimize material cost with nonlinear stress constraints
- **Parameter fitting**: Minimize squared error (sum of (y - f(x))²)
- **Optimal control**: Minimize energy with dynamics constraints
- **Portfolio optimization**: Maximize return with quadratic risk (variance)
- **Facility location**: Minimize sum of Euclidean distances (sqrt terms)
- **Chemical process**: Optimize reaction rates (exponential/logarithmic)

**Key difference from linear programming**: Contains terms like $x^2$, $xy$, $\sin(x)$, $e^x$, $\sqrt{x}$ - not just $ax + b$.

## Quick Start

### Python (scipy.optimize.minimize)

```python
import numpy as np
from scipy.optimize import minimize

# Example: Minimize x1^2 + x2^2 subject to x1 + x2 >= 1
def objective(x):
    return x[0]**2 + x[1]**2

def constraint(x):
    return x[0] + x[1] - 1  # >= 0

# Initial guess (REQUIRED for nonlinear!)
x0 = np.array([0.5, 0.5])

# Constraint dict
cons = {'type': 'ineq', 'fun': constraint}

# Solve
result = minimize(objective, x0, method='SLSQP', constraints=cons)

print(f"Optimal solution: {result.x}")
print(f"Optimal value: {result.fun}")
print(f"Success: {result.success}")
```

### MATLAB (fmincon)

```matlab
% Minimize x1^2 + x2^2 subject to x1 + x2 >= 1

% Objective function
fun = @(x) x(1)^2 + x(2)^2;

% Initial guess (REQUIRED!)
x0 = [0.5, 0.5];

% Linear inequality: -x1 - x2 <= -1  (equivalent to x1 + x2 >= 1)
A = [-1, -1];
b = -1;

% Solve
options = optimoptions('fmincon', 'Display', 'iter');
[x, fval] = fmincon(fun, x0, A, b, [], [], [], [], [], options);

fprintf('Optimal solution: [%.4f, %.4f]\n', x);
fprintf('Optimal value: %.4f\n', fval);
```

## Standard Form

**Minimize**: $f(x)$ (nonlinear objective)

**Subject to**:
- $g_i(x) \leq 0$ (nonlinear inequality constraints)
- $h_j(x) = 0$ (nonlinear equality constraints)
- $lb \leq x \leq ub$ (bounds)

**Key challenge**: May have **local optima** - solution depends on initial guess!

## Examples in Skill

See `examples/` folder:

- **`code1.ipynb` / `code1.m`**: Basic nonlinear optimization examples
- **`fun1.m` / `fun2.py`**: Facility location problem (minimize sum of Euclidean distances)
- **`constraint.m`**: Nonlinear constraint examples

## Competition Tips

### Problem Recognition (Day 1)

**Nonlinear indicators**:
- Objective/constraints contain: $x^2$, $xy$, $\frac{1}{x}$, $\sqrt{x}$, $\sin(x)$, $e^x$, $\log(x)$
- "Minimize distance" (Euclidean: $\sqrt{(x_1-a)^2 + (x_2-b)^2}$)
- "Minimize variance" (quadratic: $\sum (x_i - \bar{x})^2$)
- "Maximize area/volume" with nonlinear relations
- Physical laws (Newton, thermodynamics) - often nonlinear

**Not nonlinear programming**:
- If all terms are $ax + b$ → use `linear-programming`
- If variables must be integers → use `integer-programming` or `nonlinear-programming` + rounding

### Formulation Steps (Day 1-2)

1. **Define decision variables**: $x = [x_1, x_2, ..., x_n]$

2. **Write objective function**: 
   ```python
   def objective(x):
       return x[0]**2 + 2*x[1]**2 - x[0]*x[1]
   ```

3. **Write constraints** (if any):
   ```python
   def constraint1(x):
       return x[0] + x[1] - 5  # >= 0 (inequality)
   
   def constraint2(x):
       return x[0]**2 + x[1]**2 - 10  # == 0 (equality)
   ```

4. **Choose initial guess**: Critical! Try multiple starting points.

5. **Select solver method**:
   - `'SLSQP'`: Sequential Least Squares (good general choice)
   - `'trust-constr'`: Trust-region (handles large problems)
   - `'L-BFGS-B'`: Unconstrained or bounds-only (fast)

### Implementation Template

```python
from scipy.optimize import minimize
import numpy as np

# 1. Define objective
def objective(x):
    # Your nonlinear function
    return x[0]**2 + x[1]**2

# 2. Define constraints (optional)
def constraint_ineq(x):
    # Return >= 0
    return x[0] + x[1] - 1

def constraint_eq(x):
    # Return == 0
    return x[0] - 2*x[1]

constraints = [
    {'type': 'ineq', 'fun': constraint_ineq},
    {'type': 'eq', 'fun': constraint_eq}
]

# 3. Initial guess (CRITICAL!)
x0 = np.array([1.0, 1.0])

# 4. Bounds (optional)
bounds = [(0, None), (0, 10)]  # x[0] >= 0, 0 <= x[1] <= 10

# 5. Solve
result = minimize(objective, x0, method='SLSQP',
                  constraints=constraints, bounds=bounds)

if result.success:
    print(f"Solution: {result.x}")
    print(f"Objective: {result.fun}")
else:
    print(f"Failed: {result.message}")
```

### Validation (Day 3)

- **Multiple initial guesses**: Run with 5-10 different starting points
  ```python
  best_result = None
  for _ in range(10):
      x0 = np.random.rand(n) * 10
      result = minimize(objective, x0, ...)
      if best_result is None or result.fun < best_result.fun:
          best_result = result
  ```

- **Check constraints**: Manually verify solution satisfies all constraints

- **Gradient check**: If providing gradients, verify with finite differences

- **Physical reasonableness**: Does solution make sense?

### Common Pitfalls

1. **Local optima**: Solution depends on initial guess
   - **Fix**: Try multiple starting points, use global optimizer (`differential_evolution`, `basinhopping`)

2. **Poor initial guess**: Solver fails to converge
   - **Fix**: Use domain knowledge, start with feasible point

3. **Unbounded**: Objective goes to -∞
   - **Fix**: Add bounds or constraints

4. **Slow convergence**: Large-scale problems
   - **Fix**: Provide gradient/Hessian, use `'L-BFGS-B'` or `'trust-constr'`

5. **Constraint violation**: Solution doesn't satisfy constraints
   - **Fix**: Check constraint formulation, increase tolerance

## Advanced: Global Optimization

For problems with many local optima, use global solvers:

### Differential Evolution (Python)

```python
from scipy.optimize import differential_evolution

bounds = [(0, 10), (0, 10)]  # Required for global methods

result = differential_evolution(objective, bounds, 
                                constraints=constraints)
```

### Multi-Start (MATLAB)

```matlab
problem = createOptimProblem('fmincon', 'objective', fun, ...
    'x0', x0, 'Aineq', A, 'bineq', b);

gs = GlobalSearch;
[x, fval] = run(gs, problem);
```

## Comparison with Other Methods

| Method | Objective | Constraints | Complexity | Solution |
|--------|-----------|-------------|------------|----------|
| **Linear Programming** | Linear | Linear | Polynomial | Global optimum |
| **Nonlinear Programming** | Nonlinear | Any | NP-hard | Local optimum |
| **Integer Programming** | Linear | Linear + integer | NP-hard | Global optimum |
| **Genetic Algorithm** | Any | Any | Heuristic | Approximate |

## References

- `references/9-非线性规划【微信公众号丨B站：数模加油站】.pdf`: Complete tutorial
- SciPy docs: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
- MATLAB docs: https://www.mathworks.com/help/optim/ug/fmincon.html

## Time Budget

- **Formulation**: 30-60 min
- **Implementation**: 20-40 min
- **Testing initial guesses**: 30-60 min (CRITICAL!)
- **Validation**: 20-30 min
- **Total**: 1.5-3 hours

## Related Skills

- `linear-programming`: Simpler case (no nonlinear terms)
- `particle-swarm`: Global optimization alternative
- `simulated-annealing`: Global optimization for multimodal functions
- `automated-sweep`: Brute-force parameter search
