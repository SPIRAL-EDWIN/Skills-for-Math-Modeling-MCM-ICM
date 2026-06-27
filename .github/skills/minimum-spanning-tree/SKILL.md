---
name: minimum-spanning-tree
description: Minimum Spanning Tree for MCM/ICM competitions. Use for network design problems - connect all nodes with minimum total edge weight. Implements Prim's and Kruskal's algorithms. Applications: road construction, pipeline installation, network cabling.
---

# Minimum Spanning Tree (MST)

Find a tree that connects all vertices with the minimum total edge weight.

## When to Use

- **Network design**: Design road/cable network connecting all cities with minimum cost
- **Pipeline installation**: Connect facilities with minimum pipe length
- **Circuit design**: Wire components with minimum wire length
- **Clustering**: Group similar data points (hierarchical clustering)
- **Approximation**: Traveling Salesman Problem (TSP) approximation

**Key concept**: A **spanning tree** connects all $n$ vertices using exactly $n-1$ edges (no cycles). The **minimum** spanning tree has the smallest total edge weight.

## Quick Start

### Problem Definition

**Input**: Undirected weighted graph $G = (V, E)$ with edge weights $w(e)$

**Output**: Tree $T \subseteq E$ such that:
1. All vertices are connected
2. No cycles exist
3. Total weight $\sum_{e \in T} w(e)$ is minimized

### Python (NetworkX)

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create weighted graph
G = nx.Graph()
edges = [
    (1, 2, 4), (1, 3, 2), (2, 3, 1),
    (2, 4, 5), (3, 4, 8), (3, 5, 10),
    (4, 5, 2), (4, 6, 6), (5, 6, 3)
]
G.add_weighted_edges_from(edges)

# Compute MST (uses Kruskal's algorithm by default)
mst = nx.minimum_spanning_tree(G)

# Results
print(f"MST edges: {list(mst.edges(data='weight'))}")
print(f"Total weight: {mst.size(weight='weight')}")

# Visualize
pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(12, 5))

# Original graph
plt.subplot(121)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Original Graph")

# MST
plt.subplot(122)
nx.draw(mst, pos, with_labels=True, node_color='lightgreen', node_size=500)
labels = nx.get_edge_attributes(mst, 'weight')
nx.draw_networkx_edge_labels(mst, pos, edge_labels=labels)
plt.title(f"MST (weight={mst.size(weight='weight')})")

plt.show()
```

### MATLAB (minspantree)

```matlab
% Create weighted graph
s = [1 1 2 2 3 3 4 4 5];
t = [2 3 3 4 4 5 5 6 6];
weights = [4 2 1 5 8 10 2 6 3];

G = graph(s, t, weights);

% Compute MST
[T, pred] = minspantree(G);

% Results
fprintf('MST total weight: %.2f\n', sum(T.Edges.Weight));
fprintf('MST edges:\n');
disp(T.Edges);

% Visualize
figure;
subplot(1,2,1);
plot(G, 'EdgeLabel', G.Edges.Weight, 'LineWidth', 2);
title('Original Graph');

subplot(1,2,2);
plot(T, 'EdgeLabel', T.Edges.Weight, 'LineWidth', 2);
title(sprintf('MST (weight=%.2f)', sum(T.Edges.Weight)));
```

## Algorithms

### 1. Prim's Algorithm (Vertex-Based)

**Idea**: Grow tree from a starting vertex, always adding the minimum-weight edge connecting tree to non-tree vertex.

**Steps**:
1. Start with any vertex
2. Repeat until all vertices in tree:
   - Find minimum-weight edge connecting tree to non-tree vertex
   - Add this edge and vertex to tree

**Complexity**: $O(E \log V)$ with priority queue

```python
def prim_mst(graph, start):
    import heapq
    
    mst_edges = []
    visited = {start}
    edges = [(weight, start, neighbor) 
             for neighbor, weight in graph[start].items()]
    heapq.heapify(edges)
    
    while edges:
        weight, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            mst_edges.append((u, v, weight))
            
            for neighbor, w in graph[v].items():
                if neighbor not in visited:
                    heapq.heappush(edges, (w, v, neighbor))
    
    return mst_edges
```

### 2. Kruskal's Algorithm (Edge-Based)

**Idea**: Sort all edges by weight, add edges in order if they don't create a cycle.

**Steps**:
1. Sort all edges by weight (ascending)
2. For each edge in sorted order:
   - If adding edge doesn't create cycle, add to MST
   - Stop when $n-1$ edges added

**Complexity**: $O(E \log E)$ (dominated by sorting)

**Cycle detection**: Use **Union-Find** (Disjoint Set Union) data structure

```python
def kruskal_mst(edges, n_vertices):
    # Union-Find data structure
    parent = list(range(n_vertices))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            return True
        return False
    
    # Sort edges by weight
    edges.sort(key=lambda e: e[2])
    
    mst = []
    for u, v, weight in edges:
        if union(u, v):
            mst.append((u, v, weight))
            if len(mst) == n_vertices - 1:
                break
    
    return mst
```

## Examples in Skill

See `examples/` folder:

- **`minspantree.py` / `minspantree.mlx`**: Complete MST implementation with visualization

## Competition Tips

### Problem Recognition (Day 1)

**MST indicators**:
- "Connect all nodes/cities with **minimum total cost**"
- "Design network with **minimum cable/pipe length**"
- "Minimum cost to make graph connected"
- Network design, infrastructure planning

**NOT MST**:
- "Find shortest path from A to B" → use `shortest-path`
- "Visit all nodes once" → Traveling Salesman (much harder!)
- "Maximum flow" → different problem

### Formulation Steps (Day 1)

1. **Model as graph**:
   - Vertices: Cities/facilities/points
   - Edges: Possible connections
   - Weights: Costs/distances

2. **Check assumptions**:
   - Graph is connected (otherwise no spanning tree exists)
   - Weights are non-negative (usually true for costs)

3. **Choose algorithm**:
   - **Prim**: Dense graphs, need specific starting point
   - **Kruskal**: Sparse graphs, simpler to implement

### Implementation Template

```python
import networkx as nx

# 1. Create graph from data
G = nx.Graph()

# Add edges with weights (cost/distance)
edges = [
    (city1, city2, cost),
    (city2, city3, cost),
    # ...
]
G.add_weighted_edges_from(edges)

# 2. Compute MST
mst = nx.minimum_spanning_tree(G)

# 3. Extract results
total_cost = mst.size(weight='weight')
mst_edges = list(mst.edges(data='weight'))

print(f"Minimum total cost: {total_cost}")
print(f"Connections to build: {mst_edges}")

# 4. Visualize
import matplotlib.pyplot as plt
pos = nx.spring_layout(G)
nx.draw(mst, pos, with_labels=True, node_color='lightgreen')
edge_labels = nx.get_edge_attributes(mst, 'weight')
nx.draw_networkx_edge_labels(mst, pos, edge_labels=edge_labels)
plt.show()
```

### Validation (Day 3)

- **Check connectivity**: MST should connect all vertices
- **Count edges**: MST has exactly $n-1$ edges (n = number of vertices)
- **No cycles**: Tree structure (can verify by DFS)
- **Compare with manual**: For small graphs, verify by hand
- **Uniqueness**: If edge weights are distinct, MST is unique

### Common Pitfalls

1. **Disconnected graph**: No spanning tree exists
   - **Fix**: Check connectivity first, find MST for each component

2. **Directed graph**: MST defined for undirected graphs
   - **Fix**: Use "minimum spanning arborescence" for directed graphs

3. **Negative weights**: Algorithms still work, but unusual for cost problems
   - **Fix**: Check problem formulation

4. **Multiple MSTs**: If edge weights have ties, multiple MSTs may exist
   - **Note**: All have same total weight, just different edge sets

5. **Confusing with shortest path**: MST ≠ shortest paths from one node
   - MST: Connects all nodes with minimum total weight
   - Shortest path: Minimum distance from source to target

## Advanced: Applications

### 1. Clustering (Single Linkage)

Remove $k-1$ heaviest edges from MST to get $k$ clusters:

```python
mst = nx.minimum_spanning_tree(G)

# Get edges sorted by weight (descending)
edges_sorted = sorted(mst.edges(data='weight'), 
                     key=lambda x: x[2], reverse=True)

# Remove k-1 heaviest edges for k clusters
k = 3
for u, v, w in edges_sorted[:k-1]:
    mst.remove_edge(u, v)

# Each connected component is a cluster
clusters = list(nx.connected_components(mst))
print(f"{k} clusters: {clusters}")
```

### 2. TSP Approximation

MST gives 2-approximation for metric TSP (triangle inequality holds):

1. Compute MST
2. Do DFS traversal of MST
3. Output vertices in DFS order

Guaranteed: $\text{TSP cost} \leq 2 \times \text{MST cost}$

## Comparison with Other Methods

| Problem | Algorithm | Complexity |
|---------|-----------|------------|
| **Minimum Spanning Tree** | Prim/Kruskal | $O(E \log V)$ |
| **Shortest Path (single source)** | Dijkstra | $O(E \log V)$ |
| **Shortest Path (all pairs)** | Floyd-Warshall | $O(V^3)$ |
| **Traveling Salesman** | Exact | $O(2^n n^2)$ (NP-hard) |

## References

- `references/16-最小生成树【微信公众号丨B站：数模加油站】.pdf`: Complete tutorial
- NetworkX MST docs: https://networkx.org/documentation/stable/reference/algorithms/tree.html
- MATLAB minspantree: https://www.mathworks.com/help/matlab/ref/graph.minspantree.html

## Time Budget

- **Modeling**: 15-30 min (define graph)
- **Implementation**: 10-20 min (NetworkX is fast!)
- **Validation**: 15-20 min
- **Visualization**: 10-15 min
- **Total**: 50-85 min

## Related Skills

- `graph-theory`: Graph fundamentals (prerequisite)
- `shortest-path`: Different problem (paths, not trees)
- `network-centrality`: Identify important nodes
- `integer-programming`: Alternative formulation for network design
