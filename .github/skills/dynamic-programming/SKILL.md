---
name: dynamic-programming
description: Dynamic Programming for MCM/ICM competitions. Use for multi-stage decision problems with optimal substructure (knapsack, shortest path, resource allocation, coin change). Breaks complex problems into overlapping subproblems and stores solutions to avoid recomputation.
---

# Dynamic Programming

Solve optimization problems by breaking them into simpler overlapping subproblems and storing solutions (memoization).

## When to Use

- **Knapsack problem**: Select items to maximize value within weight limit
- **Shortest path**: Find optimal path with multiple stages
- **Resource allocation**: Distribute limited resources optimally
- **Coin change**: Minimum coins to make amount
- **Sequence alignment**: DNA/text matching
- **Production scheduling**: Multi-period optimization

**Key characteristics**:
1. **Optimal substructure**: Optimal solution contains optimal solutions to subproblems
2. **Overlapping subproblems**: Same subproblems solved repeatedly
3. **No greedy choice**: Greedy algorithms don't work

## Quick Start

### Classic Knapsack Problem

**Problem**: Given n items with weights w[i] and values v[i], maximize total value without exceeding capacity W.

#### Python (Bottom-Up)

```python
def knapsack(weights, values, capacity):
    n = len(weights)
    # dp[i][w] = max value using first i items with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i
            dp[i][w] = dp[i-1][w]
            
            # Take item i (if fits)
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], 
                              dp[i-1][w - weights[i-1]] + values[i-1])
    
    return dp[n][capacity]

# Example
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 8

max_value = knapsack(weights, values, capacity)
print(f"Maximum value: {max_value}")  # Output: 10
```

#### MATLAB

```matlab
function max_value = knapsack(weights, values, capacity)
    n = length(weights);
    dp = zeros(n+1, capacity+1);
    
    for i = 2:n+1
        for w = 1:capacity+1
            dp(i,w) = dp(i-1,w);  % Don't take
            
            if weights(i-1) <= w-1
                dp(i,w) = max(dp(i,w), ...
                    dp(i-1, w-weights(i-1)) + values(i-1));
            end
        end
    end
    
    max_value = dp(n+1, capacity+1);
end
```

### Coin Change Problem

**Problem**: Minimum number of coins to make amount.

```python
def coin_change(coins, amount):
    # dp[i] = min coins to make amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # 0 coins for amount 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1

# Example
coins = [1, 2, 5]
amount = 11
print(coin_change(coins, amount))  # Output: 3 (5+5+1)
```

## Core Concepts

### 1. State Definition

Define what `dp[i]` or `dp[i][j]` represents:
- `dp[i]`: Optimal solution for subproblem of size i
- `dp[i][j]`: Optimal solution using first i items with constraint j

### 2. State Transition (Recurrence Relation)

Express current state in terms of previous states:
```
dp[i] = f(dp[i-1], dp[i-2], ...)
```

### 3. Base Cases

Initialize trivial cases:
```python
dp[0] = 0  # or 1, depending on problem
```

### 4. Computation Order

Bottom-up (iteration) or top-down (recursion + memoization):
- **Bottom-up**: Iterate from base cases to final answer
- **Top-down**: Recursion with cache to avoid recomputation

## Examples in Skill

See `examples/` folder:
- `knapsack.py` / `knapsack.m`: 0-1 knapsack implementation
- `CoinChange.py` / `CoinChange.mlx`: Coin change problem
- `demo.m`: Additional DP examples

## Competition Tips

### Problem Recognition (Day 1)

**DP indicators**:
- Asks for "maximum/minimum" or "count ways"
- Involves sequences, arrays, or multi-stage decisions
- Greedy approach fails (need to consider all possibilities)
- Constraints suggest polynomial time (n ≤ 1000)

**Common DP problem types**:
1. **Knapsack variants**: 0-1, unbounded, multi-dimensional
2. **Path problems**: Grid paths, shortest path with stages
3. **Subsequence**: Longest common/increasing subsequence
4. **Partitioning**: Divide array/string optimally
5. **Game theory**: Optimal strategy for two players

### Formulation Steps (Day 1-2)

1. **Define state**: What does `dp[i]` represent?
2. **Find recurrence**: How does `dp[i]` relate to previous states?
3. **Identify base cases**: What are the trivial subproblems?
4. **Determine order**: Bottom-up or top-down?
5. **Optimize space**: Can we reduce dimensions?

### Implementation Template

```python
def dp_solution(input_data):
    n = len(input_data)
    
    # Step 1: Initialize DP table
    dp = [0] * (n + 1)  # or 2D: [[0]*m for _ in range(n)]
    
    # Step 2: Base cases
    dp[0] = base_value
    
    # Step 3: Fill DP table
    for i in range(1, n + 1):
        # Recurrence relation
        dp[i] = compute_from_previous(dp, i)
    
    # Step 4: Return answer
    return dp[n]
```

### Optimization Techniques

1. **Space optimization**: If `dp[i]` only depends on `dp[i-1]`, use two variables instead of array
   ```python
   prev, curr = 0, 1
   for i in range(n):
       prev, curr = curr, prev + curr
   ```

2. **Memoization (Top-Down)**:
   ```python
   memo = {}
   def dp(i):
       if i in memo:
           return memo[i]
       memo[i] = compute(i)
       return memo[i]
   ```

3. **Dimension reduction**: For 2D DP, sometimes can reduce to 1D by processing row-by-row

### Common Pitfalls

1. **Wrong state definition**: State doesn't capture all necessary information
2. **Missing base cases**: Leads to index errors or wrong answers
3. **Wrong order**: Computing `dp[i]` before its dependencies
4. **Integer overflow**: Use appropriate data types for large values
5. **Time limit**: O(n³) may be too slow; optimize to O(n²) or O(n log n)

## Advanced: Multi-Dimensional DP

### 2D DP: Edit Distance

```python
def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # Delete
                    dp[i][j-1],    # Insert
                    dp[i-1][j-1]   # Replace
                )
    
    return dp[m][n]
```

## Comparison with Other Methods

| Method | When to Use | Example |
|--------|-------------|---------|
| **Greedy** | Locally optimal = globally optimal | Activity selection, Huffman coding |
| **DP** | Overlapping subproblems, optimal substructure | Knapsack, LCS, shortest path |
| **Divide & Conquer** | Independent subproblems | Merge sort, quick sort |
| **Backtracking** | Need all solutions, not just optimal | N-queens, Sudoku |

## References

- `references/13-动态规划【微信公众号丨B站：数模加油站】.pdf`: Complete tutorial with theory and examples
- Classic DP problems: https://leetcode.com/tag/dynamic-programming/

## Time Budget

- **Problem recognition**: 15-30 min
- **State formulation**: 30-60 min (most critical!)
- **Implementation**: 20-40 min
- **Testing & debugging**: 20-30 min
- **Total**: 1.5-2.5 hours

## Related Skills

- `linear-programming`: For continuous optimization
- `integer-programming`: For discrete optimization without stages
- `graph-theory`: For path-based DP problems
- `automated-sweep`: For parameter search if DP too complex
