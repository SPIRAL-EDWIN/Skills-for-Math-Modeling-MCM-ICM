# Optimization Skills Integration Guide

## Three Independent Metaheuristic Skills

✅ **genetic-algorithm** - Best for discrete/combinatorial problems
✅ **simulated-annealing** - Best for multimodal continuous problems  
✅ **particle-swarm** - Best for smooth continuous problems (fastest)

## Connection to Multi-Objective Optimization

**NSGA-II = GA + Pareto Selection**
- Uses genetic-algorithm's crossover and mutation
- Adds non-dominated sorting and crowding distance

**MOEA/D = Decomposition + SA Acceptance**
- Decomposes multi-objective into subproblems
- Uses simulated-annealing-like acceptance criterion

**MOPSO = PSO + Archive**
- Extends particle-swarm with Pareto archive
- Multiple leaders instead of single global best

## Usage Pattern

1. Start with single-objective (GA/SA/PSO)
2. If trade-offs emerge → upgrade to multi-objective-optimization
3. Use topsis-scorer to select final solution from Pareto frontier
