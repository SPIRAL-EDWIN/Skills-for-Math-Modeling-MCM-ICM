---
name: graph-theory
description: Graph Theory fundamentals for MCM/ICM competitions. Use for network analysis, connectivity, paths, and relationships. Covers graph representations (adjacency matrix/list), traversal algorithms (DFS/BFS), connected components, and basic graph properties.
---

# Graph Theory

Model and analyze relationships between objects using graphs (vertices and edges).

## When to Use

- **Social networks**: Friendship connections, influence analysis
- **Transportation**: Road networks, flight routes, delivery paths
- **Communication**: Internet topology, network reliability
- **Dependencies**: Task prerequisites, course requirements
- **Biological**: Food webs, protein interactions
- **Infrastructure**: Power grids, water distribution

**Key concept**: If your problem involves **entities** (nodes) and **relationships** (edges), use graph theory.

## Quick Start

### Basic Concepts

- **Graph**: $G = (V, E)$ where $V$ = vertices (nodes), $E$ = edges (connections)
- **Directed graph**: Edges have direction (A → B ≠ B → A)
- **Undirected graph**: Edges are bidirectional (A — B)
- **Weighted graph**: Edges have costs/distances
- **Degree**: Number of edges connected to a vertex
- **Path**: Sequence of vertices connected by edges
- **Connected**: Path exists between any two vertices

### Python (NetworkX)

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create undirected graph
G = nx.Graph()

# Add nodes
G.add_nodes_from([1, 2, 3, 4, 5])

# Add edges (automatically adds nodes if missing)
G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)])

# Add weighted edges
G.add_edge(1, 2, weight=4.5)

# Graph properties
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")
print(f"Degree of node 3: {G.degree(3)}")

# Check connectivity
print(f"Is connected: {nx.is_connected(G)}")

# Find connected components
components = list(nx.connected_components(G))
print(f"Connected components: {components}")

# Shortest path (unweighted)
path = nx.shortest_path(G, source=1, target=5)
print(f"Shortest path 1→5: {path}")

# Visualize
nx.draw(G, with_labels=True, node_color='lightblue', 
        node_size=500, font_size=16)
plt.show()
```

### MATLAB (graph objects)

```matlab
% Create undirected graph
nodes = [1 2 1 2 3 4];
edges = [2 3 3 4 4 5];
G = graph(nodes, edges);

% Add weighted edges
weights = [4.5, 2, 3, 1, 2, 1.5];
G = graph(nodes, edges, weights);

% Graph properties
fprintf('Number of nodes: %d\n', numnodes(G));
fprintf('Number of edges: %d\n', numedges(G));
fprintf('Degree of node 3: %d\n', degree(G, 3));

% Check connectivity
bins = conncomp(G);
fprintf('Number of components: %d\n', max(bins));

% Shortest path
[path, dist] = shortestpath(G, 1, 5);
fprintf('Shortest path 1→5: %s (distance: %.2f)\n', ...
        mat2str(path), dist);

% Visualize
plot(G, 'Layout', 'force', 'EdgeLabel', G.Edges.Weight);
```

## Graph Representations

### 1. Adjacency Matrix

$n \times n$ matrix where $A[i][j] = 1$ if edge $(i, j)$ exists.

```python
import numpy as np

# 5 nodes
n = 5
adj_matrix = np.zeros((n, n), dtype=int)

# Add edges
edges = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)]
for i, j in edges:
    adj_matrix[i][j] = 1
    adj_matrix[j][i] = 1  # Undirected

print(adj_matrix)
```

**Pros**: Fast edge lookup $O(1)$, easy matrix operations  
**Cons**: $O(n^2)$ space (wasteful for sparse graphs)

### 2. Adjacency List

Dictionary mapping each node to list of neighbors.

```python
adj_list = {
    1: [2, 3],
    2: [1, 3, 4],
    3: [1, 2, 4],
    4: [2, 3, 5],
    5: [4]
}
```

**Pros**: $O(V + E)$ space (efficient for sparse graphs)  
**Cons**: Slower edge lookup $O(degree)$

## Core Algorithms

### Depth-First Search (DFS)

Explore as far as possible before backtracking.

```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(start, end=' ')
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    
    return visited

# Example
graph = {1: [2, 3], 2: [4], 3: [4], 4: []}
dfs(graph, 1)  # Output: 1 2 4 3
```

**Use cases**: Detect cycles, topological sort, connected components

### Breadth-First Search (BFS)

Explore neighbors level by level.

```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        print(node, end=' ')
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# Example
bfs(graph, 1)  # Output: 1 2 3 4
```

**Use cases**: Shortest path (unweighted), level-order traversal

## Examples in Skill

See `examples/` folder:

- **`code_graph.py` / `code_graph.m`**: Graph creation, traversal (DFS/BFS), connectivity analysis

## Competition Tips

### Problem Recognition (Day 1)

**Graph theory indicators**:
- "Network of...", "connections between..."
- "Find path from A to B"
- "Is the network connected?"
- "Critical nodes/edges" (if removed, network fails)
- "Influence spreads through..."
- "Dependencies", "prerequisites"

**Common graph problems**:
1. **Connectivity**: Is graph connected? How many components?
2. **Shortest path**: Minimum distance/cost between nodes
3. **Spanning tree**: Connect all nodes with minimum edges/cost
4. **Centrality**: Which nodes are most important?
5. **Cycle detection**: Does graph contain cycles?
6. **Matching**: Pair nodes optimally

### Formulation Steps (Day 1-2)

1. **Define vertices**: What are the entities?
2. **Define edges**: What relationships exist?
3. **Directed or undirected?**: Is relationship symmetric?
4. **Weighted or unweighted?**: Do edges have costs?
5. **Choose representation**: Matrix (dense) or list (sparse)?

### Implementation Template

```python
import networkx as nx

# 1. Create graph
G = nx.Graph()  # Or DiGraph() for directed

# 2. Add nodes and edges
G.add_edges_from([(1, 2), (2, 3), (3, 4)])

# 3. Analyze properties
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print(f"Connected: {nx.is_connected(G)}")

# 4. Find paths
if nx.has_path(G, 1, 4):
    path = nx.shortest_path(G, 1, 4)
    print(f"Path: {path}")

# 5. Identify important nodes
centrality = nx.betweenness_centrality(G)
print(f"Centrality: {centrality}")

# 6. Visualize
nx.draw(G, with_labels=True)
```

### Validation (Day 3)

- **Check connectivity**: Use `nx.is_connected()` or `conncomp()`
- **Verify paths**: Manually trace shortest paths
- **Count components**: Should match problem description
- **Edge cases**: Isolated nodes, self-loops, multiple edges

### Common Pitfalls

1. **Directed vs undirected**: Using wrong graph type
   - **Fix**: Directed for one-way (A→B), undirected for symmetric (A—B)

2. **0-indexed vs 1-indexed**: Python uses 0, MATLAB uses 1
   - **Fix**: Be consistent, document clearly

3. **Disconnected graphs**: Assuming all nodes reachable
   - **Fix**: Check connectivity first

4. **Large graphs**: $n > 10,000$ may be slow for some algorithms
   - **Fix**: Use sparse representations, optimized libraries

5. **Self-loops and multi-edges**: Not always allowed
   - **Fix**: Check problem constraints, use `nx.MultiGraph()` if needed

## Advanced: Graph Metrics

### Centrality Measures

```python
import networkx as nx

G = nx.karate_club_graph()  # Example social network

# Degree centrality (number of connections)
deg_cent = nx.degree_centrality(G)

# Betweenness centrality (node on many shortest paths)
bet_cent = nx.betweenness_centrality(G)

# Closeness centrality (average distance to all nodes)
close_cent = nx.closeness_centrality(G)

# Find most central node
most_central = max(bet_cent, key=bet_cent.get)
print(f"Most central node: {most_central}")
```

## Comparison with Other Skills

| Skill | Focus | When to Use |
|-------|-------|-------------|
| **graph-theory** | Structure, connectivity | Network topology, relationships |
| **shortest-path** | Optimal paths | Route planning, logistics |
| **minimum-spanning-tree** | Minimum cost connection | Network design, clustering |
| **network-centrality** | Important nodes | Influence, vulnerability analysis |

## References

- `references/14-图论【微信公众号丨B站：数模加油站】.pdf`: Complete tutorial
- NetworkX docs: https://networkx.org/documentation/stable/
- MATLAB graph docs: https://www.mathworks.com/help/matlab/graph-and-network-algorithms.html

## Time Budget

- **Modeling**: 20-40 min (define nodes and edges)
- **Implementation**: 15-30 min
- **Analysis**: 20-40 min (connectivity, paths, centrality)
- **Visualization**: 10-20 min
- **Total**: 1-1.5 hours

## Related Skills

- `shortest-path`: Find optimal paths (Dijkstra, Floyd)
- `minimum-spanning-tree`: Connect all nodes with minimum cost
- `network-centrality`: Identify key nodes
- `data-cleaner`: Preprocess network data
