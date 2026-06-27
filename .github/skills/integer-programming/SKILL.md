---
name: integer-programming
description: Integer Programming for MCM/ICM competitions. Use when decision variables must be integers (0/1 decisions, discrete quantities) - knapsack, assignment, scheduling, facility location. Extends linear programming with integrality constraints.
---

# Integer Programming

Solve optimization problems where some or all decision variables must take integer values (not continuous).

## When to Use

- **0-1 decisions**: Select/don't select (project selection, facility location)
- **Discrete quantities**: Number of units (production, staffing - must be whole numbers)
- **Assignment problems**: Assign tasks to workers (each task to exactly one worker)
- **Scheduling**: Shift scheduling, course timetabling
- **Knapsack variants**: Select items with discrete choices
- **Network design**: Select edges/nodes in a network

**Key difference from linear programming**: Variables are restricted to integers, making problems NP-hard (much harder to solve).

## Quick Start

### Python (scipy.optimize.milp)

```python
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

# 0-1 Knapsack: maximize profit within weight limit
profit = np.array([540, 200, 180, 350, 60])
weight = np.array([6, 3, 4, 5, 1])
capacity = 10

n = len(profit)
c = -profit  # Negate for maximization

# Constraint: weight @ x <= capacity
A = weight.reshape(1, -1)
b = np.array([capacity])
constraints = LinearConstraint(A, lb=-np.inf, ub=b)

# Variables: 0 or 1 (binary)
bounds = Bounds(lb=np.zeros(n), ub=np.ones(n))
integrality = np.ones(n, dtype=int)  # All integer

result = milp(c=c, integrality=integrality, 
              constraints=[constraints], bounds=bounds)

if result.success:
    x = np.round(result.x).astype(int)
    print(f"Selected items: {x}")
    print(f"Total profit: {-result.fun}")
    print(f"Total weight: {weight @ x}")
```

### MATLAB (intlinprog)

```matlab
% 0-1 Knapsack
profit = [540; 200; 180; 350; 60];
weight = [6; 3; 4; 5; 1];
capacity = 10;

n = length(profit);
f = -profit;  % Negate for maximization

% Constraint: weight' * x <= capacity
A = weight';
b = capacity;

% Variables: 0 or 1
lb = zeros(n, 1);
ub = ones(n, 1);
intcon = 1:n;  % All variables are integers

[x, fval] = intlinprog(f, intcon, A, b, [], [], lb, ub);

fprintf('Selected items: %s\n', mat2str(x));
fprintf('Total profit: %.2f\n', -fval);
fprintf('Total weight: %.2f\n', weight' * x);
```

## Standard Form

**Maximize**: $z = c^T x$

**Subject to**:
- $Ax \leq b$ (linear constraints)
- $Aeq \cdot x = beq$ (equality constraints)
- $x_i \in \mathbb{Z}$ for $i \in I$ (integrality constraints)
- $x_i \in \{0, 1\}$ for binary variables

**Types**:
1. **Pure IP**: All variables are integers
2. **Mixed IP (MIP)**: Some variables are integers, some continuous
3. **Binary IP (BIP)**: All variables are 0 or 1

## Examples in Skill

See `examples/` folder:

- **`beibao.py` / `beibao.m`**: 0-1 knapsack problem (select items to maximize profit within weight limit)
- **`youxi.py` / `youxi.mlx`**: Game strategy optimization (discrete choices)
- **`zhipai.py` / `zhipai.m`**: Assignment problem (assign tasks to workers, minimize cost)

## Competition Tips

### Problem Recognition (Day 1)

**IP indicators**:
- "Select", "choose", "assign", "schedule" (discrete decisions)
- "Integer number of...", "whole units"
- "Either... or..." (binary choice)
- "Each task to exactly one..." (assignment)

**Common IP types**:
1. **0-1 Knapsack**: Select subset with maximum value
2. **Assignment**: One-to-one matching (Hungarian algorithm for special case)
3. **Set covering**: Minimum sets to cover all elements
4. **Facility location**: Where to build facilities (binary + continuous)
5. **Traveling Salesman**: Visit all cities once (very hard!)

### Formulation Steps (Day 1-2)

1. **Define decision variables**: 
   - Binary: $x_i \in \{0, 1\}$ (select item i or not)
   - Integer: $x_i \in \mathbb{Z}^+$ (number of units)

2. **Write objective**: Same as linear programming

3. **Add constraints**:
   - Resource limits (like LP)
   - Logical constraints: "If A then B" → $x_A \leq x_B$
   - Exactly one: $\sum x_i = 1$

4. **Specify integrality**: Which variables must be integers?

### Implementation Template

```python
from scipy.optimize import milp, Bounds, LinearConstraint
import numpy as np

# Decision variables: x = [x1, x2, ..., xn]
n = 10

# Objective: minimize c @ x (negate for maximization)
c = np.array([...])

# Inequality: A @ x <= b
A = np.array([[...], [...]])
b = np.array([...])
constraints = LinearConstraint(A, lb=-np.inf, ub=b)

# Bounds: 0 <= x <= ub
bounds = Bounds(lb=np.zeros(n), ub=np.array([...]))

# Integrality: 1 for integer, 0 for continuous
integrality = np.ones(n, dtype=int)  # All integer

# Solve
result = milp(c=c, integrality=integrality,
              constraints=[constraints], bounds=bounds)

if result.success:
    x = np.round(result.x).astype(int)
    print(f"Solution: {x}")
    print(f"Objective: {result.fun}")
else:
    print("No solution found")
```

### Validation (Day 3)

- **Check integrality**: Ensure solution is truly integer (use `np.round`)
- **Verify constraints**: Manually check feasibility
- **Sensitivity**: How does solution change with small parameter changes?
- **Relaxation comparison**: Solve LP relaxation (drop integrality) - gives upper bound

### Common Pitfalls

1. **Computational complexity**: IP is NP-hard - large problems (n > 1000) may be slow
2. **Infeasibility**: Integer constraints can make feasible LP infeasible
3. **Gap**: LP relaxation gives bound, but IP solution may be far from it
4. **Solver limits**: Set time limits (`options={'time_limit': 300}`)
5. **Rounding LP solution**: Don't just round LP solution - may be infeasible or suboptimal

## Advanced: Modeling Tricks

### Logical Constraints

**"If $x_1 = 1$ then $x_2 = 1$"**: $x_1 \leq x_2$

**"At most k of n"**: $\sum_{i=1}^n x_i \leq k$

**"Exactly one"**: $\sum_{i=1}^n x_i = 1$

### Big-M Method

For conditional constraints: "If $x = 1$ then $ay \leq b$"

$$ay \leq b + M(1 - x)$$

where $M$ is a large constant.

## Comparison with Other Methods

| Method | Variables | Complexity | When to Use |
|--------|-----------|------------|-------------|
| **Linear Programming** | Continuous | Polynomial | Fractional solutions OK |
| **Integer Programming** | Integer | NP-hard | Discrete decisions required |
| **Dynamic Programming** | N/A | Pseudo-polynomial | Knapsack with small capacity |
| **Genetic Algorithm** | Any | Heuristic | Very large IP (approximate solution) |

## References

- `references/10-整数规划和0-1规划模型【微信公众号丨B站：数模加油站】.pdf`: Complete tutorial
- SciPy docs: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html
- MATLAB docs: https://www.mathworks.com/help/optim/ug/intlinprog.html

## Time Budget

- **Formulation**: 30-60 min (define variables and constraints)
- **Implementation**: 20-40 min
- **Solving**: 10 min - 1 hour (depends on problem size!)
- **Validation**: 20-30 min
- **Total**: 1.5-3 hours

## Related Skills

- `linear-programming`: Continuous version (LP relaxation)
- `dynamic-programming`: Alternative for knapsack problems
- `genetic-algorithm`: Heuristic for large-scale IP
- `shortest-path`: Special case of network IP
