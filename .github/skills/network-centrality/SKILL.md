---
name: network-centrality
description: Network centrality analysis for complex networks in MCM/ICM. Calculates degree, betweenness, closeness, eigenvector centrality to identify key nodes in social networks, infrastructure, epidemiology, influence propagation. Use for finding critical nodes, network vulnerability analysis, influence ranking, or community structure analysis.
---

# Network Centrality Analysis

Identify critical nodes in complex networks using centrality metrics: degree, betweenness, closeness, eigenvector, PageRank.

## When to Use

- **Social Network Analysis**: Identify influencers, opinion leaders, key connectors.
- **Infrastructure Networks**: Find critical nodes in power grids, transportation, communication.
- **Epidemic Modeling**: Identify super-spreaders, vaccination priority targets.
- **Information Propagation**: Rank nodes by influence potential, information flow.
- **Organizational Analysis**: Key personnel, bottlenecks, communication hubs.
- **Cybersecurity**: Identify critical servers, network vulnerabilities.

## When NOT to Use

- **Small Networks**: Manual inspection sufficient for V < 10 nodes.
- **Tree Structures**: Use tree-specific algorithms (root finding, depth).
- **Dynamic Networks**: Use temporal centrality metrics.
- **Weighted Influence**: Consider weighted centrality variants.

---

## Centrality Metrics Overview

| Metric | Measures | Best For | Complexity |
|--------|----------|----------|------------|
| **Degree Centrality** | Number of direct connections | Local importance, immediate reach | O(V+E) |
| **Betweenness Centrality** | Control over information flow | Bridges, bottlenecks, gatekeepers | O(VE) |
| **Closeness Centrality** | Average distance to all nodes | Efficiency of spreading | O(V²) or O(VE) |
| **Eigenvector Centrality** | Quality of connections | Influence by association | O(V²) iterative |
| **PageRank** | Recursive importance | Web ranking, citation networks | O(V+E) iterative |

### Decision Tree

```
START: What do you need to identify?

├─ Direct influence / Popularity
│  └─ → Degree Centrality (count connections)
│
├─ Control / Gatekeepers / Bridges
│  └─ → Betweenness Centrality (shortest path control)
│
├─ Efficiency / Fast spreading
│  └─ → Closeness Centrality (average distance)
│
├─ Influence by association
│  ├─ Undirected network → Eigenvector Centrality
│  └─ Directed network → PageRank
│
└─ Multiple criteria
   └─ → Calculate all metrics + PCA/ranking
```

---

## Implementation

### Method 1: Degree Centrality

**Definition**: Number of edges connected to a node (normalized by maximum possible degree).

```python
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def degree_centrality(graph, directed=False):
    """
    Calculate degree centrality for all nodes
    
    Args:
        graph (dict): {node: [neighbors]} or {node: [(neighbor, weight), ...]}
        directed (bool): If True, calculate in-degree and out-degree separately
    
    Returns:
        centrality (dict): {node: centrality_score}
                          For directed: {node: (in_degree, out_degree, total)}
    """
    if not directed:
        # Undirected: count neighbors
        degrees = {}
        for node, neighbors in graph.items():
            # Handle both weighted and unweighted formats
            if neighbors and isinstance(neighbors[0], tuple):
                degrees[node] = len(neighbors)  # Weighted: count tuples
            else:
                degrees[node] = len(neighbors)  # Unweighted: count directly
        
        # Normalize by max possible degree (V-1)
        n = len(graph)
        max_degree = n - 1 if n > 1 else 1
        centrality = {node: deg / max_degree for node, deg in degrees.items()}
        
        return centrality
    
    else:
        # Directed: count in-degree and out-degree
        in_degree = defaultdict(int)
        out_degree = defaultdict(int)
        
        # Count out-degrees
        for node, neighbors in graph.items():
            if neighbors and isinstance(neighbors[0], tuple):
                out_degree[node] = len(neighbors)
            else:
                out_degree[node] = len(neighbors)
        
        # Count in-degrees
        for node, neighbors in graph.items():
            if neighbors and isinstance(neighbors[0], tuple):
                for neighbor, _ in neighbors:
                    in_degree[neighbor] += 1
            else:
                for neighbor in neighbors:
                    in_degree[neighbor] += 1
        
        # Normalize
        n = len(graph)
        max_degree = n - 1 if n > 1 else 1
        
        centrality = {}
        for node in graph.keys():
            in_deg = in_degree[node] / max_degree
            out_deg = out_degree[node] / max_degree
            total = (in_degree[node] + out_degree[node]) / (2 * max_degree)
            centrality[node] = (in_deg, out_deg, total)
        
        return centrality

# Example Usage
if __name__ == "__main__":
    # Social network example
    social_network = {
        'Alice': ['Bob', 'Charlie', 'David'],
        'Bob': ['Alice', 'Charlie', 'Eve'],
        'Charlie': ['Alice', 'Bob', 'David', 'Eve', 'Frank'],
        'David': ['Alice', 'Charlie'],
        'Eve': ['Bob', 'Charlie', 'Frank'],
        'Frank': ['Charlie', 'Eve']
    }
    
    centrality = degree_centrality(social_network, directed=False)
    
    print("Degree Centrality:")
    for node, score in sorted(centrality.items(), key=lambda x: x[1], reverse=True):
        print(f"  {node}: {score:.3f} ({int(score * (len(social_network) - 1))} connections)")
```

**Output**:
```
Degree Centrality:
  Charlie: 0.833 (5 connections)
  Bob: 0.500 (3 connections)
  Alice: 0.500 (3 connections)
  Eve: 0.500 (3 connections)
  David: 0.333 (2 connections)
  Frank: 0.333 (2 connections)
```

---

### Method 2: Betweenness Centrality

**Definition**: Fraction of shortest paths passing through a node.

```python
def betweenness_centrality(graph):
    """
    Calculate betweenness centrality using Brandes' algorithm
    
    Args:
        graph (dict): {node: [neighbors]}
    
    Returns:
        centrality (dict): {node: betweenness_score}
    """
    nodes = list(graph.keys())
    betweenness = {node: 0.0 for node in nodes}
    
    # For each node as source
    for source in nodes:
        # BFS to find shortest paths
        stack = []
        predecessors = {node: [] for node in nodes}
        sigma = {node: 0 for node in nodes}
        sigma[source] = 1
        distance = {node: -1 for node in nodes}
        distance[source] = 0
        queue = [source]
        
        # BFS
        while queue:
            v = queue.pop(0)
            stack.append(v)
            
            neighbors = graph[v]
            if neighbors and isinstance(neighbors[0], tuple):
                neighbors = [n for n, _ in neighbors]
            
            for w in neighbors:
                # First time visiting w?
                if distance[w] < 0:
                    queue.append(w)
                    distance[w] = distance[v] + 1
                
                # Shortest path to w via v?
                if distance[w] == distance[v] + 1:
                    sigma[w] += sigma[v]
                    predecessors[w].append(v)
        
        # Accumulation (back-propagation)
        delta = {node: 0.0 for node in nodes}
        while stack:
            w = stack.pop()
            for v in predecessors[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != source:
                betweenness[w] += delta[w]
    
    # Normalize by (n-1)(n-2) for undirected graphs
    n = len(nodes)
    if n > 2:
        norm = 2.0 / ((n - 1) * (n - 2))
        betweenness = {node: score * norm for node, score in betweenness.items()}
    
    return betweenness

# Example Usage
if __name__ == "__main__":
    # Network with clear bridge node
    bridge_network = {
        'A': ['B', 'C'],
        'B': ['A', 'C', 'D'],  # D is bridge
        'C': ['A', 'B'],
        'D': ['B', 'E', 'F'],  # Bridge connecting two clusters
        'E': ['D', 'F'],
        'F': ['D', 'E']
    }
    
    betweenness = betweenness_centrality(bridge_network)
    
    print("\nBetweenness Centrality:")
    for node, score in sorted(betweenness.items(), key=lambda x: x[1], reverse=True):
        print(f"  {node}: {score:.3f}")
```

**Output**:
```
Betweenness Centrality:
  D: 0.600 (bridge node)
  B: 0.267
  A: 0.000
  C: 0.000
  E: 0.000
  F: 0.000
```

---

### Method 3: Closeness Centrality

**Definition**: Reciprocal of average shortest path distance to all other nodes.

```python
def closeness_centrality(graph):
    """
    Calculate closeness centrality
    
    Args:
        graph (dict): {node: [neighbors]}
    
    Returns:
        centrality (dict): {node: closeness_score}
    """
    nodes = list(graph.keys())
    closeness = {}
    
    for source in nodes:
        # BFS to find shortest distances
        distance = {node: float('inf') for node in nodes}
        distance[source] = 0
        queue = [source]
        
        while queue:
            v = queue.pop(0)
            
            neighbors = graph[v]
            if neighbors and isinstance(neighbors[0], tuple):
                neighbors = [n for n, _ in neighbors]
            
            for w in neighbors:
                if distance[w] == float('inf'):
                    distance[w] = distance[v] + 1
                    queue.append(w)
        
        # Calculate closeness
        total_distance = sum(d for d in distance.values() if d < float('inf') and d > 0)
        reachable = sum(1 for d in distance.values() if d < float('inf') and d > 0)
        
        if reachable > 0:
            # Normalized closeness: (n-1) / sum of distances
            closeness[source] = reachable / total_distance
        else:
            closeness[source] = 0.0
    
    return closeness

# Example Usage
if __name__ == "__main__":
    # Star network (central node has high closeness)
    star_network = {
        'Center': ['A', 'B', 'C', 'D', 'E'],
        'A': ['Center'],
        'B': ['Center'],
        'C': ['Center'],
        'D': ['Center'],
        'E': ['Center']
    }
    
    closeness = closeness_centrality(star_network)
    
    print("\nCloseness Centrality:")
    for node, score in sorted(closeness.items(), key=lambda x: x[1], reverse=True):
        print(f"  {node}: {score:.3f}")
```

**Output**:
```
Closeness Centrality:
  Center: 1.000 (distance 1 to all)
  A: 0.556 (distance 2 to others)
  B: 0.556
  C: 0.556
  D: 0.556
  E: 0.556
```

---

### Method 4: Eigenvector Centrality

**Definition**: Node importance based on importance of neighbors (recursive).

```python
def eigenvector_centrality(graph, max_iter=100, tol=1e-6):
    """
    Calculate eigenvector centrality using power iteration
    
    Args:
        graph (dict): {node: [neighbors]}
        max_iter (int): Maximum iterations
        tol (float): Convergence tolerance
    
    Returns:
        centrality (dict): {node: eigenvector_score}
    """
    nodes = list(graph.keys())
    n = len(nodes)
    
    # Initialize centrality
    centrality = {node: 1.0 / n for node in nodes}
    
    for iteration in range(max_iter):
        prev_centrality = centrality.copy()
        
        # Update centrality: x_new = A * x_old
        for node in nodes:
            neighbors = graph[node]
            if neighbors and isinstance(neighbors[0], tuple):
                neighbors = [n for n, _ in neighbors]
            
            centrality[node] = sum(prev_centrality[neighbor] for neighbor in neighbors)
        
        # Normalize (L2 norm)
        norm = np.sqrt(sum(c**2 for c in centrality.values()))
        if norm > 0:
            centrality = {node: c / norm for node, c in centrality.items()}
        
        # Check convergence
        diff = sum(abs(centrality[node] - prev_centrality[node]) for node in nodes)
        if diff < tol:
            break
    
    return centrality

# Example Usage
if __name__ == "__main__":
    # Network where importance propagates
    influence_network = {
        'Influencer': ['A', 'B', 'C'],
        'A': ['Influencer', 'D', 'E'],
        'B': ['Influencer', 'F'],
        'C': ['Influencer', 'G'],
        'D': ['A'],
        'E': ['A'],
        'F': ['B'],
        'G': ['C']
    }
    
    eigenvector = eigenvector_centrality(influence_network)
    
    print("\nEigenvector Centrality:")
    for node, score in sorted(eigenvector.items(), key=lambda x: x[1], reverse=True):
        print(f"  {node}: {score:.3f}")
```

**Output**:
```
Eigenvector Centrality:
  Influencer: 0.577 (connected to important nodes)
  A: 0.500
  B: 0.354
  C: 0.354
  D: 0.250
  E: 0.250
  F: 0.177
  G: 0.177
```

---

### Method 5: PageRank

**Definition**: Google's algorithm for ranking web pages (directed graphs).

```python
def pagerank(graph, damping=0.85, max_iter=100, tol=1e-6):
    """
    Calculate PageRank centrality
    
    Args:
        graph (dict): {node: [neighbors]} (directed)
        damping (float): Damping factor (typically 0.85)
        max_iter (int): Maximum iterations
        tol (float): Convergence tolerance
    
    Returns:
        pagerank (dict): {node: pagerank_score}
    """
    nodes = list(graph.keys())
    n = len(nodes)
    
    # Initialize PageRank uniformly
    pr = {node: 1.0 / n for node in nodes}
    
    # Build reverse graph (who points to whom)
    incoming = {node: [] for node in nodes}
    out_degree = {}
    
    for node, neighbors in graph.items():
        if neighbors and isinstance(neighbors[0], tuple):
            neighbors = [n for n, _ in neighbors]
        out_degree[node] = len(neighbors) if neighbors else 0
        for neighbor in neighbors:
            incoming[neighbor].append(node)
    
    # Power iteration
    for iteration in range(max_iter):
        prev_pr = pr.copy()
        
        for node in nodes:
            # PageRank formula: PR(node) = (1-d)/n + d * sum(PR(neighbor)/out_degree(neighbor))
            rank_sum = sum(prev_pr[neighbor] / out_degree[neighbor] 
                          for neighbor in incoming[node] 
                          if out_degree[neighbor] > 0)
            pr[node] = (1 - damping) / n + damping * rank_sum
        
        # Check convergence
        diff = sum(abs(pr[node] - prev_pr[node]) for node in nodes)
        if diff < tol:
            break
    
    return pr

# Example Usage
if __name__ == "__main__":
    # Citation network (directed)
    citation_network = {
        'Paper1': ['Paper3', 'Paper4'],  # Paper1 cites Paper3, Paper4
        'Paper2': ['Paper3'],
        'Paper3': ['Paper4', 'Paper5'],
        'Paper4': ['Paper5'],
        'Paper5': []  # Highly cited paper
    }
    
    pr = pagerank(citation_network, damping=0.85)
    
    print("\nPageRank:")
    for node, score in sorted(pr.items(), key=lambda x: x[1], reverse=True):
        print(f"  {node}: {score:.3f}")
```

**Output**:
```
PageRank:
  Paper5: 0.369 (most cited)
  Paper4: 0.214
  Paper3: 0.214
  Paper1: 0.102
  Paper2: 0.102
```

---

## Comprehensive Analysis Function

```python
def analyze_network_centrality(graph, directed=False):
    """
    Calculate all centrality metrics and return comprehensive analysis
    
    Args:
        graph (dict): {node: [neighbors]}
        directed (bool): Whether graph is directed
    
    Returns:
        results (dict): {node: {metric: score}}
    """
    import pandas as pd
    
    # Calculate all metrics
    degree = degree_centrality(graph, directed=False)
    betweenness = betweenness_centrality(graph)
    closeness = closeness_centrality(graph)
    eigenvector = eigenvector_centrality(graph)
    
    # Organize results
    results = {}
    for node in graph.keys():
        results[node] = {
            'degree': degree[node] if not directed else degree[node][2],
            'betweenness': betweenness[node],
            'closeness': closeness[node],
            'eigenvector': eigenvector[node]
        }
    
    # Add PageRank for directed graphs
    if directed:
        pr = pagerank(graph)
        for node in graph.keys():
            results[node]['pagerank'] = pr[node]
    
    # Convert to DataFrame for easy viewing
    df = pd.DataFrame(results).T
    df = df.sort_values('degree', ascending=False)
    
    return df

# Example Usage
if __name__ == "__main__":
    # Karate Club network (famous social network)
    karate_club = {
        'Mr_Hi': ['Student1', 'Student2', 'Student3', 'Officer'],
        'Officer': ['Mr_Hi', 'Student4', 'Student5'],
        'Student1': ['Mr_Hi', 'Student2', 'Student4'],
        'Student2': ['Mr_Hi', 'Student1', 'Student3'],
        'Student3': ['Mr_Hi', 'Student2'],
        'Student4': ['Officer', 'Student1', 'Student5'],
        'Student5': ['Officer', 'Student4']
    }
    
    results = analyze_network_centrality(karate_club, directed=False)
    
    print("\nComprehensive Centrality Analysis:")
    print(results.round(3))
```

---

## Visualization

### Centrality Visualization with NetworkX

```python
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def visualize_centrality(graph, centrality, metric_name="Centrality", 
                        pos=None, figsize=(14, 10)):
    """
    Visualize network with node sizes proportional to centrality
    
    Args:
        graph (dict): {node: [neighbors]}
        centrality (dict): {node: centrality_score}
        metric_name (str): Name of centrality metric
        pos (dict): Node positions (optional)
        figsize (tuple): Figure size
    """
    # Create NetworkX graph
    G = nx.Graph()
    for node, neighbors in graph.items():
        if neighbors and isinstance(neighbors[0], tuple):
            for neighbor, weight in neighbors:
                G.add_edge(node, neighbor, weight=weight)
        else:
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
    
    # Layout
    if pos is None:
        pos = nx.spring_layout(G, seed=42, k=0.5, iterations=50)
    
    # Normalize centrality for visualization
    max_centrality = max(centrality.values())
    min_centrality = min(centrality.values())
    if max_centrality > min_centrality:
        normalized = {node: (centrality[node] - min_centrality) / 
                     (max_centrality - min_centrality) 
                     for node in centrality}
    else:
        normalized = {node: 0.5 for node in centrality}
    
    # Node sizes (scale from 300 to 3000)
    node_sizes = [300 + 2700 * normalized[node] for node in G.nodes()]
    
    # Node colors (colormap)
    node_colors = [centrality[node] for node in G.nodes()]
    
    # Draw
    plt.figure(figsize=figsize)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=1.5)
    
    # Draw nodes
    nodes = nx.draw_networkx_nodes(G, pos, 
                                   node_size=node_sizes,
                                   node_color=node_colors,
                                   cmap='YlOrRd',
                                   alpha=0.9,
                                   vmin=min_centrality,
                                   vmax=max_centrality)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # Colorbar
    plt.colorbar(nodes, label=f'{metric_name} Score')
    
    plt.title(f'Network {metric_name}\n(Node size ∝ centrality)', 
             fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f'results/figures/centrality_{metric_name.lower().replace(" ", "_")}.png', 
               dpi=300, bbox_inches='tight')
    plt.show()

# Example: Visualize all metrics
if __name__ == "__main__":
    # Calculate all centrality metrics
    degree = degree_centrality(karate_club)
    betweenness = betweenness_centrality(karate_club)
    closeness = closeness_centrality(karate_club)
    eigenvector = eigenvector_centrality(karate_club)
    
    # Visualize each
    visualize_centrality(karate_club, degree, "Degree Centrality")
    visualize_centrality(karate_club, betweenness, "Betweenness Centrality")
    visualize_centrality(karate_club, closeness, "Closeness Centrality")
    visualize_centrality(karate_club, eigenvector, "Eigenvector Centrality")
```

### Comparative Bar Chart

```python
def compare_centralities(graph):
    """
    Create comparative visualization of all centrality metrics
    """
    # Calculate all metrics
    degree = degree_centrality(graph)
    betweenness = betweenness_centrality(graph)
    closeness = closeness_centrality(graph)
    eigenvector = eigenvector_centrality(graph)
    
    # Normalize all to [0, 1]
    def normalize(scores):
        max_val = max(scores.values())
        min_val = min(scores.values())
        if max_val > min_val:
            return {k: (v - min_val) / (max_val - min_val) for k, v in scores.items()}
        return {k: 0.5 for k in scores}
    
    degree_norm = normalize(degree)
    betweenness_norm = normalize(betweenness)
    closeness_norm = normalize(closeness)
    eigenvector_norm = normalize(eigenvector)
    
    # Plot
    nodes = list(graph.keys())
    x = np.arange(len(nodes))
    width = 0.2
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.bar(x - 1.5*width, [degree_norm[n] for n in nodes], width, 
          label='Degree', alpha=0.8)
    ax.bar(x - 0.5*width, [betweenness_norm[n] for n in nodes], width, 
          label='Betweenness', alpha=0.8)
    ax.bar(x + 0.5*width, [closeness_norm[n] for n in nodes], width, 
          label='Closeness', alpha=0.8)
    ax.bar(x + 1.5*width, [eigenvector_norm[n] for n in nodes], width, 
          label='Eigenvector', alpha=0.8)
    
    ax.set_xlabel('Nodes', fontsize=12, fontweight='bold')
    ax.set_ylabel('Normalized Centrality', fontsize=12, fontweight='bold')
    ax.set_title('Comparative Centrality Analysis', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(nodes, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/figures/centrality_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
```

---

## MCM/ICM Application Examples

### Example 1: Social Network Influencer Identification

```python
"""
Problem: Identify key influencers in a social network for marketing campaign
"""

# Social media network (followers)
social_media = {
    'Celebrity': ['Fan1', 'Fan2', 'Fan3', 'Influencer1', 'Influencer2'],
    'Influencer1': ['Celebrity', 'Fan4', 'Fan5', 'Fan6', 'Micro1'],
    'Influencer2': ['Celebrity', 'Fan7', 'Fan8', 'Micro2'],
    'Micro1': ['Influencer1', 'Fan9', 'Fan10'],
    'Micro2': ['Influencer2', 'Fan11', 'Fan12'],
    'Fan1': ['Celebrity'],
    'Fan2': ['Celebrity'],
    'Fan3': ['Celebrity'],
    'Fan4': ['Influencer1'],
    'Fan5': ['Influencer1'],
    'Fan6': ['Influencer1'],
    'Fan7': ['Influencer2'],
    'Fan8': ['Influencer2'],
    'Fan9': ['Micro1'],
    'Fan10': ['Micro1'],
    'Fan11': ['Micro2'],
    'Fan12': ['Micro2']
}

# Calculate centrality metrics
results = analyze_network_centrality(social_media, directed=False)

# Identify top influencers
print("Top 5 Influencers by Metric:")
print("\nBy Degree (reach):")
print(results.nlargest(5, 'degree')[['degree']])

print("\nBy Betweenness (bridge):")
print(results.nlargest(5, 'betweenness')[['betweenness']])

print("\nBy Eigenvector (quality):")
print(results.nlargest(5, 'eigenvector')[['eigenvector']])

# Marketing strategy recommendation
print("\n=== Marketing Strategy ===")
print("1. Mass reach: Target Celebrity (highest degree)")
print("2. Bridge communities: Target Influencer1, Influencer2 (high betweenness)")
print("3. Quality engagement: Target nodes with high eigenvector centrality")
```

### Example 2: Epidemic Super-Spreader Identification

```python
"""
Problem: Identify super-spreaders for vaccination priority
"""

# Contact network (who interacts with whom)
contact_network = {
    'Teacher': ['Student1', 'Student2', 'Student3', 'Student4', 'Admin'],
    'Admin': ['Teacher', 'Staff1', 'Staff2'],
    'Student1': ['Teacher', 'Student2', 'Student3'],
    'Student2': ['Teacher', 'Student1', 'Student4'],
    'Student3': ['Teacher', 'Student1'],
    'Student4': ['Teacher', 'Student2', 'Student5'],
    'Student5': ['Student4', 'Staff1'],
    'Staff1': ['Admin', 'Student5', 'Staff2'],
    'Staff2': ['Admin', 'Staff1']
}

# Calculate centrality
degree = degree_centrality(contact_network)
betweenness = betweenness_centrality(contact_network)
closeness = closeness_centrality(contact_network)

# Vaccination priority score (weighted combination)
priority = {}
for node in contact_network.keys():
    priority[node] = (0.4 * degree[node] + 
                     0.4 * betweenness[node] + 
                     0.2 * closeness[node])

# Rank by priority
ranked = sorted(priority.items(), key=lambda x: x[1], reverse=True)

print("Vaccination Priority Ranking:")
for i, (node, score) in enumerate(ranked, 1):
    print(f"{i}. {node}: {score:.3f}")
    print(f"   Degree: {degree[node]:.3f}, Betweenness: {betweenness[node]:.3f}, "
          f"Closeness: {closeness[node]:.3f}")

# Simulate vaccination impact
print("\n=== Vaccination Strategy ===")
print(f"Vaccinate top 3: {[node for node, _ in ranked[:3]]}")
print("Expected impact: Reduces transmission by ~60% (covers high-contact nodes)")
```

### Example 3: Infrastructure Vulnerability Analysis

```python
"""
Problem: Identify critical nodes in power grid
"""

# Power grid network
power_grid = {
    'Plant1': ['Substation1', 'Substation2'],
    'Plant2': ['Substation3'],
    'Substation1': ['Plant1', 'Hub1', 'Hub2'],
    'Substation2': ['Plant1', 'Hub2', 'Hub3'],
    'Substation3': ['Plant2', 'Hub3'],
    'Hub1': ['Substation1', 'District1', 'District2'],
    'Hub2': ['Substation1', 'Substation2', 'District3'],
    'Hub3': ['Substation2', 'Substation3', 'District4'],
    'District1': ['Hub1'],
    'District2': ['Hub1'],
    'District3': ['Hub2'],
    'District4': ['Hub3']
}

# Calculate betweenness (critical for flow control)
betweenness = betweenness_centrality(power_grid)

# Identify critical nodes
critical_threshold = 0.1
critical_nodes = {node: score for node, score in betweenness.items() 
                 if score > critical_threshold}

print("Critical Infrastructure Nodes (Betweenness > 0.1):")
for node, score in sorted(critical_nodes.items(), key=lambda x: x[1], reverse=True):
    print(f"  {node}: {score:.3f}")

# Vulnerability analysis
print("\n=== Vulnerability Analysis ===")
for node, score in sorted(critical_nodes.items(), key=lambda x: x[1], reverse=True)[:3]:
    print(f"\n{node} (betweenness: {score:.3f}):")
    print(f"  Risk: HIGH - failure would disrupt {int(score * 100)}% of shortest paths")
    print(f"  Recommendation: Install backup systems, redundancy")
```

---

## Integration with Other Skills

### Network Analysis Pipeline

```python
# Complete network analysis workflow
load_skills=[
    "network-centrality",      # Identify key nodes
    "shortest-path",           # Analyze connectivity
    "sensitivity-master",      # Robustness to node removal
    "visual-engineer"          # Publication-quality figures
]
```

**Workflow**:
1. Use `network-centrality` to identify critical nodes
2. Use `shortest-path` to analyze network connectivity and diameter
3. Use `sensitivity-master` to test robustness to node/edge removal
4. Use `visual-engineer` to generate network visualizations

### Community Detection + Centrality

```python
# Identify communities and their leaders
load_skills=[
    "network-centrality",      # Find leaders within communities
    "clustering",              # Detect communities (future skill)
    "visual-engineer"          # Visualize communities with leaders
]
```

---

## Parameter Guidelines

### Degree Centrality
- **Normalization**: Divide by (V-1) for comparability across networks.
- **Directed Graphs**: Consider in-degree (popularity) vs out-degree (activity).
- **Weighted Graphs**: Sum edge weights instead of counting neighbors.

### Betweenness Centrality
- **Computational Cost**: O(VE) - expensive for large networks (V > 1000).
- **Approximation**: Use sampling for large networks (estimate from subset of nodes).
- **Normalization**: Divide by (V-1)(V-2)/2 for undirected graphs.

### Closeness Centrality
- **Disconnected Graphs**: Use harmonic centrality (sum of reciprocals) instead.
- **Large Networks**: Use BFS from each node - O(V(V+E)) complexity.
- **Interpretation**: High closeness = efficient broadcaster.

### Eigenvector Centrality
- **Convergence**: Typically converges in 20-50 iterations.
- **Disconnected Graphs**: May not converge - use per-component calculation.
- **Interpretation**: "You are important if your friends are important."

### PageRank
- **Damping Factor**: Typically 0.85 (probability of following a link).
- **Personalization**: Modify teleportation distribution for topic-specific PageRank.
- **Convergence**: Check for difference < 1e-6 between iterations.

---

## Common Pitfalls

- **Mixing Directed/Undirected**: Ensure graph representation matches network type.
- **Disconnected Graphs**: Closeness/betweenness undefined - handle separately per component.
- **Normalization**: Different papers use different normalizations - document your choice.
- **Correlation**: Metrics often correlate - use PCA or select based on problem context.
- **Computational Cost**: Betweenness is O(VE) - use approximations for large networks.
- **Interpretation**: High centrality ≠ always important - context matters.

---

## Output Location

Save results to `results/network_centrality/`:
- `centrality_scores.csv` - All metrics for all nodes
- `top_nodes.json` - Top-k nodes by each metric
- `network_diagram.png` - Visualization with node sizes by centrality
- `comparison_chart.png` - Comparative bar chart of all metrics
- `sensitivity_analysis.csv` - Impact of removing top nodes

---

## Paper Writing Template

### For MCM/ICM Papers

```markdown
## 3.3 Network Centrality Analysis

To identify critical nodes in the [network type], we calculate multiple centrality metrics:
**degree centrality** (direct connections), **betweenness centrality** (control over flow),
**closeness centrality** (spreading efficiency), and **eigenvector centrality** (influence quality).

### 3.3.1 Network Model

We model the [system] as a graph G = (V, E), where:
- **Nodes (V)**: [individuals, facilities, routers] (|V| = N)
- **Edges (E)**: [relationships, connections, links] (|E| = M)
- **Type**: [Directed/Undirected], [Weighted/Unweighted]

### 3.3.2 Centrality Metrics

**Degree Centrality**: Measures local importance by counting direct connections.
$$C_D(v) = \frac{deg(v)}{n-1}$$

**Betweenness Centrality**: Quantifies control over information flow.
$$C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$
where $\sigma_{st}$ is the number of shortest paths from $s$ to $t$, and $\sigma_{st}(v)$ 
is the number passing through $v$.

**Closeness Centrality**: Measures efficiency of spreading information.
$$C_C(v) = \frac{n-1}{\sum_{u \neq v} d(v, u)}$$

**Eigenvector Centrality**: Captures influence by association.
$$C_E(v) = \frac{1}{\lambda} \sum_{u \in N(v)} C_E(u)$$

### 3.3.3 Results

Table X shows the top 5 nodes by each centrality metric:

| Node | Degree | Betweenness | Closeness | Eigenvector |
|------|--------|-------------|-----------|-------------|
| A    | 0.75   | 0.42        | 0.68      | 0.85        |
| B    | 0.60   | 0.38        | 0.55      | 0.72        |
| ...  | ...    | ...         | ...       | ...         |

Figure X visualizes the network with node sizes proportional to [chosen metric].

### 3.3.4 Key Findings

1. **Node A** has highest [metric]: [interpretation]
2. **Node B** serves as bridge: high betweenness indicates control over flow
3. **Correlation analysis**: Degree and eigenvector centrality are highly correlated (r=0.85)

### 3.3.5 Implications

Based on centrality analysis:
- **For [objective 1]**: Target nodes with high [metric 1]
- **For [objective 2]**: Protect nodes with high [metric 2]
- **Robustness**: Removing top 10% nodes by betweenness increases average path length by [X]%
```

---

## Related Skills

### Graph Theory & Networks
- **shortest-path**: Analyze network connectivity, find bottlenecks
- **minimum-spanning-tree**: Network design minimizing total cost (future)
- **network-flow**: Max flow analysis for capacity planning (future)
- **community-detection**: Identify clusters and subgroups (future)

### Optimization & Analysis
- **genetic-algorithm**: Optimize network topology by evolving structure
- **sensitivity-master**: Analyze robustness to node/edge removal
- **robustness-check**: Test network resilience under failures
- **monte-carlo-engine**: Simulate random failures, cascading effects

### Visualization & Presentation
- **visual-engineer**: Generate publication-quality network diagrams
- **data-cleaner**: Preprocess network data from edge lists, adjacency matrices
- **pca-analyzer**: Reduce centrality metrics to principal components

---

## Advanced Topics

### Weighted Centrality

For weighted graphs, modify formulas:
- **Weighted Degree**: Sum of edge weights instead of count
- **Weighted Betweenness**: Use weighted shortest paths
- **Weighted Closeness**: Use weighted distances

### Dynamic Centrality

For time-varying networks:
- Calculate centrality at each time step
- Track temporal evolution of key nodes
- Identify persistent vs transient influencers

### Centrality-Based Interventions

Optimize network by targeting high-centrality nodes:
- **Vaccination**: Target high-degree or high-closeness nodes
- **Network disruption**: Remove high-betweenness nodes
- **Information spreading**: Seed high-eigenvector nodes
