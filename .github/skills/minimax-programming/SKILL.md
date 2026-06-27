---
name: minimax-programming
description: Minimax Programming for MCM/ICM competitions. Use for worst-case optimization (minimize maximum loss, maximize minimum gain). Handles robust design, risk management, game theory. Transforms into standard optimization by introducing auxiliary variable.
---

# Minimax Programming

Optimize for the worst-case scenario: minimize the maximum value or maximize the minimum value.

## When to Use

- **Robust optimization**: Design that performs well in worst case
- **Risk management**: Minimize maximum loss across scenarios
- **Game theory**: Maximize your minimum payoff (against adversary)
- **Engineering design**: Minimize maximum stress/deviation
- **Portfolio**: Maximize minimum return across market conditions
- **Facility location**: Minimize maximum distance to any customer

**Key concept**: Instead of optimizing average or total, optimize the **worst outcome**.

## Quick Start

### Problem Types

1. **Minimize Maximum** (most common):
   $$\min_x \max_i f_i(x)$$
   Example: Minimize maximum delivery time

2. **Maximize Minimum**:
   $$\max_x \min_i f_i(x)$$
   Example: Maximize minimum profit

### Transformation Trick

Convert minimax to standard optimization by introducing auxiliary variable $t$:

**Original**: $\min_x \max_i f_i(x)$

**Transformed**:
$$\min_{x, t} \quad t$$
$$\text{subject to} \quad f_i(x) \leq t, \quad \forall i$$

The auxiliary variable $t$ becomes an upper bound on all $f_i(x)$.

### Python Implementation

```python
import numpy as np
from scipy.optimize import minimize

# Example: Minimize max distance to 3 points
points = np.array([[1, 2], [3, 4], [5, 1]])

def distance(x, point):
    return np.sqrt((x[0] - point[0])**2 + (x[1] - point[1])**2)

# Objective: minimize t
def objective(z):
    return z[2]  # z = [x1, x2, t]

# Constraints: distance_i <= t for all i
def make_constraint(i):
    return {'type': 'ineq',
            'fun': lambda z, i=i: z[2] - distance(z[:2], points[i])}

constraints = [make_constraint(i) for i in range(len(points))]

# Initial guess
z0 = np.array([3.0, 2.0, 5.0])  # [x1, x2, t_initial]

# Solve
result = minimize(objective, z0, method='SLSQP', constraints=constraints)

x_opt = result.x[:2]
t_opt = result.x[2]

print(f"Optimal location: {x_opt}")
print(f"Maximum distance: {t_opt}")
```

### MATLAB Implementation

```matlab
% Minimize max distance to 3 points
points = [1, 2; 3, 4; 5, 1];

% Objective: minimize t (variable x = [x1, x2, t])
fun = @(x) x(3);

% Nonlinear constraints: distance_i - t <= 0
function [c, ceq] = nonlcon(x, points)
    n = size(points, 1);
    c = zeros(n, 1);
    for i = 1:n
        dist = sqrt((x(1) - points(i,1))^2 + (x(2) - points(i,2))^2);
        c(i) = dist - x(3);  % dist <= t
    end
    ceq = [];
end

% Initial guess
x0 = [3, 2, 5];

% Solve
options = optimoptions('fmincon', 'Display', 'iter');
[x, fval] = fmincon(fun, x0, [], [], [], [], [], [], ...
                    @(x) nonlcon(x, points), options);

fprintf('Optimal location: [%.4f, %.4f]\n', x(1), x(2));
fprintf('Maximum distance: %.4f\n', x(3));
```

## Standard Forms

### Minimize Maximum (Min-Max)

**Original**:
$$\min_x \max_{i=1,\ldots,m} f_i(x)$$
$$\text{subject to} \quad g_j(x) \leq 0$$

**Transformed**:
$$\min_{x, t} \quad t$$
$$\text{subject to} \quad f_i(x) \leq t, \quad i=1,\ldots,m$$
$$g_j(x) \leq 0$$

### Maximize Minimum (Max-Min)

**Original**:
$$\max_x \min_{i=1,\ldots,m} f_i(x)$$

**Transformed**:
$$\max_{x, t} \quad t$$
$$\text{subject to} \quad f_i(x) \geq t, \quad i=1,\ldots,m$$

Or equivalently (minimization):
$$\min_{x, t} \quad -t$$
$$\text{subject to} \quad t - f_i(x) \leq 0$$

## Examples in Skill

See `examples/` folder:

- **`maxmin.py` / `maxmin.m`**: Classic minimax optimization example
- **`fun.py` / `Fun.m`**: Multi-objective function definitions
- Demonstrates transformation from minimax to standard constrained optimization

## Competition Tips

### Problem Recognition (Day 1)

**Minimax indicators**:
- "Minimize the **worst-case**..."
- "Minimize **maximum** deviation/error/cost"
- "Maximize **minimum** return/profit/performance"
- "Robust design" (perform well in all scenarios)
- "Worst-case analysis"
- "Minimize the largest..."

**Common applications**:
1. **Facility location**: Minimize max distance (emergency response)
2. **Scheduling**: Minimize maximum completion time (makespan)
3. **Resource allocation**: Maximize minimum satisfaction
4. **Game theory**: Maximize minimum payoff (conservative strategy)
5. **Engineering**: Minimize maximum stress/temperature

### Formulation Steps (Day 1-2)

1. **Identify the "max" or "min" inside**:
   - What are the multiple scenarios/objectives $f_1, f_2, \ldots, f_m$?

2. **Introduce auxiliary variable $t$**:
   - For min-max: $t$ is upper bound on all $f_i$
   - For max-min: $t$ is lower bound on all $f_i$

3. **Write transformed problem**:
   ```python
   # Decision variables: [x1, x2, ..., xn, t]
   # Objective: minimize (or maximize) t
   # Constraints: f_i(x) <= t (or >= t)
   ```

4. **Add original constraints**: Don't forget constraints on $x$!

### Implementation Template

```python
from scipy.optimize import minimize
import numpy as np

# 1. Define component functions f_i(x)
def f1(x):
    return x[0]**2 + x[1]**2

def f2(x):
    return (x[0] - 3)**2 + (x[1] - 4)**2

functions = [f1, f2]

# 2. Objective: minimize t
def objective(z):
    return z[-1]  # Last variable is t

# 3. Constraints: f_i(x) <= t
def make_constraint(func):
    return {'type': 'ineq',
            'fun': lambda z, f=func: z[-1] - f(z[:-1])}

constraints = [make_constraint(f) for f in functions]

# 4. Initial guess (include t!)
n = 2  # Number of x variables
z0 = np.zeros(n + 1)
z0[-1] = 10.0  # Initial t (make it large enough)

# 5. Solve
result = minimize(objective, z0, method='SLSQP', constraints=constraints)

x_opt = result.x[:-1]
t_opt = result.x[-1]

print(f"Optimal x: {x_opt}")
print(f"Minimax value: {t_opt}")
```

### Validation (Day 3)

- **Check all components**: Verify $f_i(x^*) \leq t^*$ for all $i$
- **Identify active constraint**: Which $f_i$ achieves maximum? (should equal $t^*$)
- **Sensitivity**: How does $t^*$ change with scenario parameters?
- **Compare with average**: Is minimax solution different from minimizing average?

### Common Pitfalls

1. **Forgot to add $t$**: Must include auxiliary variable in decision vector
2. **Wrong constraint direction**: Min-max uses $\leq$, max-min uses $\geq$
3. **Poor initial $t$**: If $t_0$ too small, constraints infeasible
   - **Fix**: Set $t_0 = \max_i f_i(x_0) + \epsilon$
4. **Ignored original constraints**: Don't forget constraints on $x$
5. **Local optima**: Nonlinear minimax may have multiple local solutions

## Advanced: Linear Minimax

If all $f_i(x)$ are linear, the transformed problem is a **linear program**!

**Example**: $\min_x \max_i (a_i^T x + b_i)$

**Transformed LP**:
$$\min_{x, t} \quad t$$
$$\text{subject to} \quad a_i^T x \leq t - b_i, \quad \forall i$$

Use `scipy.optimize.linprog` for faster solving.

## Comparison with Other Methods

| Method | Objective | When to Use |
|--------|-----------|-------------|
| **Least Squares** | Minimize sum of squares | Average-case optimization |
| **Minimax** | Minimize maximum | Worst-case optimization, robustness |
| **Weighted Sum** | Minimize weighted average | Known scenario probabilities |
| **Robust Optimization** | Minimax + uncertainty sets | Uncertain parameters |

## References

- `references/11-最大最小化规划模型【微信公众号丨B站：数模加油站】.pdf`: Complete tutorial
- Boyd & Vandenberghe, "Convex Optimization", Chapter 6.1.2

## Time Budget

- **Formulation**: 20-40 min (transformation is key!)
- **Implementation**: 15-30 min
- **Testing**: 20-30 min
- **Validation**: 15-20 min
- **Total**: 1-2 hours

## Related Skills

- `nonlinear-programming`: General framework (minimax is special case)
- `linear-programming`: For linear minimax problems
- `robustness-check`: For analyzing worst-case scenarios
- `multi-objective-optimization`: Alternative approach (Pareto frontier)
