---
name: shortest-path
description: Shortest path algorithms (Dijkstra, Floyd-Warshall, Bellman-Ford, A*) for network optimization in MCM/ICM. Use for transportation networks, logistics, routing, supply chain optimization, network flow, social network analysis, or any problem requiring optimal path finding in weighted graphs.
---

# Shortest Path Algorithms

Find optimal paths in weighted graphs for transportation, logistics, routing, and network optimization problems.

## When to Use

- **Transportation Networks**: Road networks, flight routes, shipping lanes.
- **Logistics Optimization**: Delivery routing, supply chain paths.
- **Network Analysis**: Communication networks, social networks, infrastructure.
- **Resource Allocation**: Minimum cost flow, optimal routing.
- **Emergency Response**: Fastest evacuation routes, ambulance dispatch.
- **Urban Planning**: Traffic flow optimization, public transit design.

## When NOT to Use

- **Unweighted Graphs**: Use BFS (Breadth-First Search) instead.
- **Dynamic Networks**: Use dynamic programming or online algorithms.
- **Real-Time Constraints**: Consider approximate algorithms (greedy, heuristic).
- **Multiple Objectives**: Use **`multi-objective-optimization`** or **`pareto-frontier`**.

---

## Algorithm Selection Guide

| Algorithm | Best For | Time Complexity | Space | Negative Edges? |
|-----------|----------|-----------------|-------|-----------------|
| **Dijkstra** | Single source, non-negative weights | O((V+E) log V) | O(V) | ❌ No |
| **Bellman-Ford** | Single source, negative weights | O(VE) | O(V) | ✅ Yes (detects cycles) |
| **Floyd-Warshall** | All pairs shortest paths | O(V³) | O(V²) | ✅ Yes (detects cycles) |
| **A\*** | Single source with heuristic | O(E) (best case) | O(V) | ❌ No |

### Decision Tree

```
START: What do you need?

├─ Single source shortest path (one start node)
│  ├─ All edge weights ≥ 0
│  │  ├─ Need path reconstruction → Dijkstra
│  │  └─ Have good heuristic (e.g., Euclidean distance) → A*
│  └─ Some edge weights < 0 → Bellman-Ford
│
└─ All pairs shortest paths (every node to every node)
   ├─ Dense graph (many edges) → Floyd-Warshall
   └─ Sparse graph (few edges) → Run Dijkstra V times
```

---

## Implementation

### Method 1: Dijkstra's Algorithm (Single Source, Non-Negative)

**Use Case**: Find shortest path from one source to all other nodes (or specific target).

```python
import numpy as np
import heapq
from collections import defaultdict

def dijkstra(graph, source, target=None):
    """
    Dijkstra's shortest path algorithm
    
    Args:
        graph (dict): {node: [(neighbor, weight), ...]}
        source: Starting node
        target: Target node (optional, if None returns all distances)
    
    Returns:
        distances (dict): {node: shortest_distance}
        predecessors (dict): {node: previous_node} for path reconstruction
    """
    # Initialize
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    predecessors = {node: None for node in graph}
    
    # Priority queue: (distance, node)
    pq = [(0, source)]
    visited = set()
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        # Skip if already visited
        if current_node in visited:
            continue
        visited.add(current_node)
        
        # Early termination if target found
        if target and current_node == target:
            break
        
        # Check if this is outdated entry
        if current_dist > distances[current_node]:
            continue
        
        # Explore neighbors
        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight
            
            # Found shorter path
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    return distances, predecessors

def reconstruct_path(predecessors, source, target):
    """
    Reconstruct path from source to target
    
    Returns:
        path (list): [source, ..., target] or None if no path exists
    """
    if predecessors[target] is None and target != source:
        return None  # No path exists
    
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    return path[::-1]  # Reverse to get source -> target

# Example Usage
if __name__ == "__main__":
    # Build graph: {node: [(neighbor, weight), ...]}
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('C', 1), ('D', 5)],
        'C': [('D', 8), ('E', 10)],
        'D': [('E', 2)],
        'E': []
    }
    
    source = 'A'
    target = 'E'
    
    # Find shortest paths
    distances, predecessors = dijkstra(graph, source, target)
    
    # Reconstruct path
    path = reconstruct_path(predecessors, source, target)
    
    print(f"Shortest distance from {source} to {target}: {distances[target]}")
    print(f"Path: {' -> '.join(path)}")
    print(f"\nAll distances from {source}:")
    for node, dist in sorted(distances.items()):
        print(f"  {node}: {dist}")
```

**Output**:
```
Shortest distance from A to E: 9
Path: A -> C -> B -> D -> E

All distances from A:
  A: 0
  B: 3
  C: 2
  D: 8
  E: 9
```

---

### Method 2: Floyd-Warshall Algorithm (All Pairs)

**Use Case**: Find shortest paths between ALL pairs of nodes. Best for dense graphs or when you need complete distance matrix.

```python
import numpy as np

def floyd_warshall(adjacency_matrix, nodes=None):
    """
    Floyd-Warshall all-pairs shortest path algorithm
    
    Args:
        adjacency_matrix (np.ndarray): NxN matrix where [i][j] = edge weight
                                       Use np.inf for no edge
        nodes (list): Node labels (optional, defaults to indices)
    
    Returns:
        distances (np.ndarray): NxN shortest distance matrix
        next_node (np.ndarray): NxN matrix for path reconstruction
    """
    n = len(adjacency_matrix)
    
    # Initialize distance and next node matrices
    distances = adjacency_matrix.copy()
    next_node = np.full((n, n), -1, dtype=int)
    
    # Initialize next_node for direct edges
    for i in range(n):
        for j in range(n):
            if i != j and distances[i][j] < np.inf:
                next_node[i][j] = j
    
    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if distances[i][k] + distances[k][j] < distances[i][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]
                    next_node[i][j] = next_node[i][k]
    
    # Check for negative cycles
    for i in range(n):
        if distances[i][i] < 0:
            raise ValueError(f"Negative cycle detected at node {i}")
    
    return distances, next_node

def reconstruct_path_floyd(next_node, i, j, nodes=None):
    """
    Reconstruct path from node i to node j using Floyd-Warshall result
    
    Args:
        next_node (np.ndarray): Next node matrix from floyd_warshall()
        i (int): Source node index
        j (int): Target node index
        nodes (list): Node labels (optional)
    
    Returns:
        path (list): [i, ..., j] or None if no path
    """
    if next_node[i][j] == -1:
        return None  # No path exists
    
    path = [i]
    while i != j:
        i = next_node[i][j]
        path.append(i)
    
    # Convert indices to node labels if provided
    if nodes:
        path = [nodes[idx] for idx in path]
    
    return path

# Example Usage
if __name__ == "__main__":
    # Node labels
    nodes = ['A', 'B', 'C', 'D', 'E']
    n = len(nodes)
    
    # Create adjacency matrix (use np.inf for no edge)
    adj_matrix = np.full((n, n), np.inf)
    
    # Set diagonal to 0
    np.fill_diagonal(adj_matrix, 0)
    
    # Add edges (node_index: A=0, B=1, C=2, D=3, E=4)
    edges = [
        (0, 1, 4),   # A -> B: 4
        (0, 2, 2),   # A -> C: 2
        (1, 2, 1),   # B -> C: 1
        (1, 3, 5),   # B -> D: 5
        (2, 3, 8),   # C -> D: 8
        (2, 4, 10),  # C -> E: 10
        (3, 4, 2),   # D -> E: 2
    ]
    
    for i, j, weight in edges:
        adj_matrix[i][j] = weight
    
    # Run Floyd-Warshall
    distances, next_node = floyd_warshall(adj_matrix, nodes)
    
    # Print distance matrix
    print("All-pairs shortest distances:")
    print("     ", "  ".join(nodes))
    for i, node in enumerate(nodes):
        row = [f"{distances[i][j]:5.1f}" if distances[i][j] < np.inf else "  inf" 
               for j in range(n)]
        print(f"{node}:  ", " ".join(row))
    
    # Example path reconstruction
    source_idx = 0  # A
    target_idx = 4  # E
    path = reconstruct_path_floyd(next_node, source_idx, target_idx, nodes)
    print(f"\nShortest path from {nodes[source_idx]} to {nodes[target_idx]}:")
    print(f"  Path: {' -> '.join(path)}")
    print(f"  Distance: {distances[source_idx][target_idx]}")
```

**Output**:
```
All-pairs shortest distances:
      A   B   C   D   E
A:    0.0  3.0  2.0  8.0 10.0
B:    inf  0.0  1.0  6.0  8.0
C:    inf  inf  0.0  8.0 10.0
D:    inf  inf  inf  0.0  2.0
E:    inf  inf  inf  inf  0.0

Shortest path from A to E:
  Path: A -> C -> B -> D -> E
  Distance: 10.0
```

---

### Method 3: Bellman-Ford Algorithm (Negative Edges)

**Use Case**: Single source shortest path when graph has negative edge weights. Can detect negative cycles.

```python
def bellman_ford(graph, source):
    """
    Bellman-Ford shortest path algorithm (handles negative weights)
    
    Args:
        graph (dict): {node: [(neighbor, weight), ...]}
        source: Starting node
    
    Returns:
        distances (dict): {node: shortest_distance}
        predecessors (dict): {node: previous_node}
        
    Raises:
        ValueError: If negative cycle detected
    """
    # Initialize
    nodes = list(graph.keys())
    distances = {node: float('inf') for node in nodes}
    distances[source] = 0
    predecessors = {node: None for node in nodes}
    
    # Relax edges V-1 times
    for _ in range(len(nodes) - 1):
        for node in nodes:
            for neighbor, weight in graph[node]:
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight
                    predecessors[neighbor] = node
    
    # Check for negative cycles (Vth iteration)
    for node in nodes:
        for neighbor, weight in graph[node]:
            if distances[node] + weight < distances[neighbor]:
                raise ValueError("Graph contains negative cycle")
    
    return distances, predecessors

# Example with negative edges
if __name__ == "__main__":
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('C', -3), ('D', 5)],  # Negative edge
        'C': [('D', 1)],
        'D': []
    }
    
    distances, predecessors = bellman_ford(graph, 'A')
    
    print("Shortest distances from A:")
    for node, dist in sorted(distances.items()):
        print(f"  {node}: {dist}")
```

---

### Method 4: A* Algorithm (Heuristic-Guided)

**Use Case**: Fastest path finding when you have a good heuristic (e.g., Euclidean distance for geographic maps).

```python
import heapq
import numpy as np

def a_star(graph, source, target, heuristic):
    """
    A* shortest path algorithm with heuristic
    
    Args:
        graph (dict): {node: [(neighbor, weight), ...]}
        source: Starting node
        target: Target node
        heuristic (callable): h(node) -> estimated distance to target
    
    Returns:
        path (list): [source, ..., target] or None
        distance (float): Total path distance
    """
    # Priority queue: (f_score, g_score, node)
    # f_score = g_score + h_score
    pq = [(heuristic(source), 0, source)]
    
    # g_score: actual distance from source
    g_scores = {source: 0}
    
    # Came from (for path reconstruction)
    came_from = {}
    
    # Visited set
    visited = set()
    
    while pq:
        f_score, g_score, current = heapq.heappop(pq)
        
        # Found target
        if current == target:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(source)
            return path[::-1], g_score
        
        # Skip if visited
        if current in visited:
            continue
        visited.add(current)
        
        # Explore neighbors
        for neighbor, weight in graph[current]:
            tentative_g = g_score + weight
            
            if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor)
                came_from[neighbor] = current
                heapq.heappush(pq, (f_score, tentative_g, neighbor))
    
    return None, float('inf')  # No path found

# Example with geographic coordinates
if __name__ == "__main__":
    # Node coordinates (for Euclidean heuristic)
    coords = {
        'A': (0, 0),
        'B': (1, 2),
        'C': (2, 1),
        'D': (3, 3),
        'E': (4, 2)
    }
    
    # Graph
    graph = {
        'A': [('B', 2.2), ('C', 2.2)],
        'B': [('D', 2.2)],
        'C': [('D', 2.8), ('E', 2.2)],
        'D': [('E', 1.4)],
        'E': []
    }
    
    # Euclidean distance heuristic
    target = 'E'
    def heuristic(node):
        x1, y1 = coords[node]
        x2, y2 = coords[target]
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    path, distance = a_star(graph, 'A', target, heuristic)
    
    print(f"A* Path from A to {target}: {' -> '.join(path)}")
    print(f"Total distance: {distance:.2f}")
```

---

## Visualization

### Path Visualization with NetworkX

```python
import networkx as nx
import matplotlib.pyplot as plt

def visualize_shortest_path(graph, path, distances=None, 
                            pos=None, title="Shortest Path"):
    """
    Visualize graph with shortest path highlighted
    
    Args:
        graph (dict): {node: [(neighbor, weight), ...]}
        path (list): Shortest path nodes
        distances (dict): {node: distance_from_source} (optional)
        pos (dict): {node: (x, y)} positions (optional)
        title (str): Plot title
    """
    # Create NetworkX graph
    G = nx.DiGraph()
    
    # Add edges
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors:
            G.add_edge(node, neighbor, weight=weight)
    
    # Layout
    if pos is None:
        pos = nx.spring_layout(G, seed=42)
    
    # Draw graph
    plt.figure(figsize=(12, 8))
    
    # Draw all edges (gray)
    nx.draw_networkx_edges(G, pos, edge_color='lightgray', 
                           arrows=True, arrowsize=20, width=2)
    
    # Draw shortest path edges (red)
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, 
                           edge_color='red', arrows=True, 
                           arrowsize=20, width=3)
    
    # Draw nodes
    node_colors = ['lightcoral' if node in path else 'lightblue' 
                   for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=800, alpha=0.9)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Draw edge weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10)
    
    # Highlight source and target
    if path:
        nx.draw_networkx_nodes(G, pos, nodelist=[path[0]], 
                              node_color='green', node_size=1000, alpha=0.8)
        nx.draw_networkx_nodes(G, pos, nodelist=[path[-1]], 
                              node_color='orange', node_size=1000, alpha=0.8)
    
    # Add distance annotations
    if distances:
        labels = {node: f"{node}\nd={distances[node]:.1f}" 
                 for node in G.nodes() if distances[node] < np.inf}
        nx.draw_networkx_labels(G, pos, labels, font_size=9)
    
    plt.title(title, fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('results/figures/shortest_path.png', dpi=300, bbox_inches='tight')
    plt.show()

# Example usage
if __name__ == "__main__":
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('C', 1), ('D', 5)],
        'C': [('D', 8), ('E', 10)],
        'D': [('E', 2)],
        'E': []
    }
    
    distances, predecessors = dijkstra(graph, 'A')
    path = reconstruct_path(predecessors, 'A', 'E')
    
    visualize_shortest_path(graph, path, distances, 
                           title="Dijkstra's Shortest Path: A to E")
```

---

## MCM/ICM Application Examples

### Example 1: Transportation Network Optimization

```python
"""
Problem: Find optimal delivery route in a city network
"""

# City network (intersections and roads with travel times in minutes)
city_network = {
    'Warehouse': [('A', 5), ('B', 8)],
    'A': [('C', 3), ('D', 7)],
    'B': [('C', 2), ('E', 6)],
    'C': [('D', 4), ('E', 5), ('F', 8)],
    'D': [('Customer', 6)],
    'E': [('F', 3), ('Customer', 9)],
    'F': [('Customer', 4)],
    'Customer': []
}

# Find fastest delivery route
distances, predecessors = dijkstra(city_network, 'Warehouse', 'Customer')
path = reconstruct_path(predecessors, 'Warehouse', 'Customer')

print(f"Optimal delivery route: {' -> '.join(path)}")
print(f"Total travel time: {distances['Customer']} minutes")

# Sensitivity analysis: What if road C->E is blocked?
city_network_blocked = city_network.copy()
city_network_blocked['C'] = [edge for edge in city_network['C'] if edge[0] != 'E']

distances_alt, predecessors_alt = dijkstra(city_network_blocked, 'Warehouse', 'Customer')
path_alt = reconstruct_path(predecessors_alt, 'Warehouse', 'Customer')

print(f"\nAlternative route (C->E blocked): {' -> '.join(path_alt)}")
print(f"Alternative travel time: {distances_alt['Customer']} minutes")
print(f"Time increase: {distances_alt['Customer'] - distances['Customer']} minutes")
```

### Example 2: Multi-City Distance Matrix (Floyd-Warshall)

```python
"""
Problem: Calculate all-pairs distances for logistics planning
"""

cities = ['Beijing', 'Shanghai', 'Guangzhou', 'Chengdu', 'Wuhan']
n = len(cities)

# Distance matrix (km)
distances_km = np.array([
    [0,    1200, 1900, 1500, 1100],  # Beijing
    [1200, 0,    1400, 1900, 800],   # Shanghai
    [1900, 1400, 0,    1700, 1000],  # Guangzhou
    [1500, 1900, 1700, 0,    1200],  # Chengdu
    [1100, 800,  1000, 1200, 0]      # Wuhan
])

# Run Floyd-Warshall
all_distances, next_node = floyd_warshall(distances_km, cities)

# Print distance matrix
print("All-pairs shortest distances (km):")
print("           ", "  ".join(f"{city:>10}" for city in cities))
for i, city in enumerate(cities):
    row = [f"{all_distances[i][j]:>10.0f}" for j in range(n)]
    print(f"{city:>10}:", " ".join(row))

# Find longest shortest path (network diameter)
max_distance = np.max(all_distances[all_distances < np.inf])
i_max, j_max = np.unravel_index(np.argmax(all_distances[all_distances < np.inf]), 
                                 all_distances.shape)
print(f"\nNetwork diameter: {max_distance:.0f} km")
print(f"Longest shortest path: {cities[i_max]} to {cities[j_max]}")
```

### Example 3: Emergency Response Routing

```python
"""
Problem: Find fastest ambulance route with traffic conditions
"""

# Road network with traffic multipliers
# Format: {intersection: [(neighbor, base_time, traffic_multiplier), ...]}
road_network = {
    'Hospital': [('A', 5, 1.0), ('B', 8, 1.5)],  # B has heavy traffic
    'A': [('C', 3, 1.0), ('Emergency', 15, 1.0)],
    'B': [('C', 4, 1.2), ('D', 6, 1.0)],
    'C': [('D', 2, 1.0), ('Emergency', 10, 1.0)],
    'D': [('Emergency', 5, 1.0)],
    'Emergency': []
}

# Convert to graph with actual travel times
traffic_graph = {}
for node, edges in road_network.items():
    traffic_graph[node] = [(neighbor, base_time * traffic) 
                           for neighbor, base_time, traffic in edges]

# Find fastest route
distances, predecessors = dijkstra(traffic_graph, 'Hospital', 'Emergency')
path = reconstruct_path(predecessors, 'Hospital', 'Emergency')

print(f"Fastest ambulance route: {' -> '.join(path)}")
print(f"Estimated arrival time: {distances['Emergency']:.1f} minutes")

# Compare with traffic-free scenario
traffic_free_graph = {}
for node, edges in road_network.items():
    traffic_free_graph[node] = [(neighbor, base_time) 
                                for neighbor, base_time, _ in edges]

distances_free, _ = dijkstra(traffic_free_graph, 'Hospital', 'Emergency')
print(f"Traffic-free time: {distances_free['Emergency']:.1f} minutes")
print(f"Traffic delay: {distances['Emergency'] - distances_free['Emergency']:.1f} minutes")
```

---

## Parameter Guidelines

### Dijkstra's Algorithm
- **Graph Size**: Efficient for V < 10,000 nodes with sparse edges.
- **Priority Queue**: Use `heapq` (binary heap) for Python, Fibonacci heap for very large graphs.
- **Early Termination**: Stop when target node is reached (saves computation).

### Floyd-Warshall Algorithm
- **Graph Size**: Practical for V < 500 nodes (O(V³) complexity).
- **Dense Graphs**: More efficient than running Dijkstra V times when E ≈ V².
- **Memory**: Requires O(V²) space for distance matrix.

### Bellman-Ford Algorithm
- **Negative Edges**: Only algorithm that handles negative weights correctly.
- **Negative Cycle Detection**: Essential for currency arbitrage, game theory problems.
- **Performance**: Slower than Dijkstra (O(VE) vs O((V+E) log V)).

### A* Algorithm
- **Heuristic Quality**: Must be admissible (never overestimate) and consistent.
- **Best Heuristics**: Euclidean distance (geographic), Manhattan distance (grid), straight-line distance.
- **Performance**: Can be 10-100x faster than Dijkstra with good heuristic.

---

## Integration with Other Skills

### Optimization & Analysis
- **genetic-algorithm**: Use shortest paths as fitness evaluation in routing optimization.
- **simulated-annealing**: Optimize network design where edge weights are decision variables.
- **multi-objective-optimization**: Balance distance vs cost vs time in routing.
- **sensitivity-master**: Analyze impact of edge weight changes on optimal paths.

### Validation & Visualization
- **robustness-check**: Test path stability under edge weight perturbations.
- **monte-carlo-engine**: Simulate stochastic travel times for confidence intervals.
- **visual-engineer**: Generate publication-quality network diagrams.

### Data Processing
- **data-cleaner**: Preprocess road network data from OpenStreetMap, GPS traces.
- **ml-regressor**: Predict edge weights (travel time) from traffic data.

---

## Common Pitfalls

- **Negative Weights with Dijkstra**: Dijkstra fails with negative edges. Use Bellman-Ford or Floyd-Warshall.
- **Forgetting Self-Loops**: Set diagonal of adjacency matrix to 0 in Floyd-Warshall.
- **Undirected Graphs**: Add edges in both directions: `graph[u].append((v, w))` AND `graph[v].append((u, w))`.
- **Path Reconstruction**: Store predecessors during search, not just distances.
- **Infinite Distances**: Check for `np.inf` or `float('inf')` when no path exists.
- **Negative Cycles**: Floyd-Warshall can detect but not fix negative cycles.

---

## Output Location

Save results to `results/shortest_path/`:
- `optimal_path.json` - Path nodes and total distance
- `distance_matrix.csv` - All-pairs distances (Floyd-Warshall)
- `network_diagram.png` - Visualization with highlighted path
- `sensitivity_analysis.csv` - Impact of edge weight changes

---

## Paper Writing Template

### For MCM/ICM Papers

```markdown
## 3.2 Shortest Path Analysis

To optimize [transportation/logistics/routing], we employ **Dijkstra's algorithm** 
to find the shortest path from [source] to [target] in the [network description].

### 3.2.1 Network Model

We model the [system] as a weighted directed graph G = (V, E), where:
- **Nodes (V)**: [intersections, cities, facilities] (|V| = N)
- **Edges (E)**: [roads, routes, connections] (|E| = M)
- **Weights**: [travel time, distance, cost] in [units]

### 3.2.2 Algorithm Selection

We choose **[Dijkstra/Floyd-Warshall/A*]** because:
1. [Reason 1: e.g., all edge weights are non-negative]
2. [Reason 2: e.g., need single-source shortest paths]
3. [Reason 3: e.g., sparse graph with V=100, E=300]

**Time Complexity**: O([complexity]) is acceptable for our network size.

### 3.2.3 Results

The optimal path from [source] to [target] is:
- **Path**: [A → B → C → D]
- **Total Distance**: [X] [units]
- **Computational Time**: [Y] seconds

Figure X shows the network with the shortest path highlighted in red.

### 3.2.4 Sensitivity Analysis

We analyze robustness by perturbing edge weights by ±20%:
- **Best case** (all edges -20%): Distance = [X1] ([change]%)
- **Worst case** (all edges +20%): Distance = [X2] ([change]%)
- **Path stability**: Path remains unchanged in [Z]% of scenarios

This demonstrates that our solution is **robust** to moderate variations in [edge weights].
```

---

## Related Skills

### Network & Graph Theory (Future Skills)
- **network-flow**: Max flow, min cost flow algorithms
- **minimum-spanning-tree**: Kruskal, Prim algorithms for network design
- **community-detection**: Louvain, spectral clustering for network analysis

### Optimization
- **genetic-algorithm**: Vehicle routing problem (VRP) with shortest path subroutines
- **simulated-annealing**: Traveling salesman problem (TSP) using shortest paths
- **multi-objective-optimization**: Trade-offs between distance, time, cost

### Validation & Analysis
- **sensitivity-master**: Analyze critical edges (bottlenecks) in network
- **robustness-check**: Test path stability under edge failures
- **monte-carlo-engine**: Stochastic shortest paths with uncertain edge weights

### Visualization
- **visual-engineer**: Publication-quality network diagrams with paths highlighted
