---
name: modular-modeler
description: Object-oriented architecture for complex system models (System Dynamics, Agent-Based Models) in MCM/ICM competitions. Use when building multi-component models (environment + agents + policies) to avoid spaghetti code and enable mid-competition model swaps. Enforces clean interfaces and module decoupling.
---

# Modular-Modeler

Build complex mathematical models using object-oriented programming to ensure maintainability, testability, and flexibility during competitions.

## When to Use

- Building System Dynamics (SD) models with multiple subsystems
- Agent-Based Models (ABM) with heterogeneous agents
- Models combining multiple phenomena (e.g., climate + economy + policy)
- When model requirements may change mid-competition
- Need to test different sub-model variants independently

## Core Architecture Principle

**Separation of Concerns**: Each module handles ONE aspect of the system and communicates through well-defined interfaces.

```
Model Architecture:
├── Environment (state, physics, external factors)
├── Agents (individual behaviors, decision-making)
├── Policy (rules, interventions, constraints)
└── Simulator (orchestrates interactions, time-stepping)
```

## Implementation Pattern

### 1. Base Class Structure

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class ModelComponent(ABC):
    """Base class for all model components"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.state = {}
    
    @abstractmethod
    def initialize(self):
        """Set up initial state"""
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """Update component for one time step"""
        pass
    
    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        """Return current component state"""
        pass
```

### 2. Environment Module

Handles external conditions and physical processes:

```python
class Environment(ModelComponent):
    """Manages environmental state (climate, resources, etc.)"""
    
    def __init__(self, config):
        super().__init__(config)
        self.temperature = config['initial_temp']
        self.ice_volume = config['initial_ice']
    
    def initialize(self):
        self.state = {
            'temperature': self.temperature,
            'ice_volume': self.ice_volume,
            'melt_rate': 0.0
        }
    
    def update(self, dt: float):
        """Update environmental variables"""
        # Example: Ice melting model
        self.state['melt_rate'] = self._calculate_melt_rate()
        self.state['ice_volume'] -= self.state['melt_rate'] * dt
        self.state['ice_volume'] = max(0, self.state['ice_volume'])
    
    def _calculate_melt_rate(self) -> float:
        """Private method for internal calculations"""
        return self.config['melt_coef'] * (self.state['temperature'] - 0)
    
    def get_state(self) -> Dict[str, Any]:
        return self.state.copy()
    
    def apply_external_forcing(self, forcing: float):
        """Interface for external influences"""
        self.state['temperature'] += forcing
```

### 3. Agent Module

Handles individual entity behaviors:

```python
class Agent(ModelComponent):
    """Base class for individual agents (tourists, companies, etc.)"""
    
    def __init__(self, agent_id: int, config: Dict[str, Any]):
        super().__init__(config)
        self.id = agent_id
    
    @abstractmethod
    def make_decision(self, environment_state: Dict) -> Dict[str, Any]:
        """Agent decision based on environment"""
        pass

class Tourist(Agent):
    """Tourist agent with visit decision logic"""
    
    def initialize(self):
        self.state = {
            'satisfaction': 0.0,
            'visits': 0,
            'willingness_to_pay': self.config['base_wtp']
        }
    
    def update(self, dt: float):
        # Update internal state
        pass
    
    def make_decision(self, environment_state: Dict) -> Dict[str, Any]:
        """Decide whether to visit based on environment"""
        ice_quality = environment_state['ice_volume'] / self.config['ideal_ice']
        visit_prob = 1 / (1 + np.exp(-5 * (ice_quality - 0.5)))
        
        return {
            'will_visit': np.random.random() < visit_prob,
            'wtp': self.state['willingness_to_pay'] * ice_quality
        }
    
    def get_state(self) -> Dict[str, Any]:
        return self.state.copy()
```

### 4. Policy Module

Implements interventions and regulations:

```python
class Policy(ModelComponent):
    """Policy intervention module"""
    
    def __init__(self, config):
        super().__init__(config)
        self.tax_rate = config.get('tax_rate', 0.0)
        self.visitor_cap = config.get('visitor_cap', float('inf'))
    
    def initialize(self):
        self.state = {
            'tax_rate': self.tax_rate,
            'visitor_cap': self.visitor_cap,
            'revenue': 0.0
        }
    
    def update(self, dt: float):
        pass
    
    def apply_policy(self, agent_decisions: list) -> list:
        """Filter/modify agent actions based on policy"""
        visiting_agents = [d for d in agent_decisions if d['will_visit']]
        
        # Apply visitor cap
        if len(visiting_agents) > self.state['visitor_cap']:
            visiting_agents = visiting_agents[:int(self.state['visitor_cap'])]
        
        # Calculate tax revenue
        self.state['revenue'] = sum(
            d['wtp'] * self.state['tax_rate'] 
            for d in visiting_agents
        )
        
        return visiting_agents
    
    def get_state(self) -> Dict[str, Any]:
        return self.state.copy()
```

### 5. Simulator (Orchestrator)

Coordinates all modules:

```python
class Simulator:
    """Main simulation orchestrator"""
    
    def __init__(self, environment: Environment, 
                 agents: list[Agent], 
                 policy: Policy,
                 dt: float = 1.0):
        self.environment = environment
        self.agents = agents
        self.policy = policy
        self.dt = dt
        self.time = 0.0
        self.history = []
    
    def initialize(self):
        """Initialize all components"""
        self.environment.initialize()
        self.policy.initialize()
        for agent in self.agents:
            agent.initialize()
    
    def step(self):
        """Execute one simulation time step"""
        # 1. Get environment state
        env_state = self.environment.get_state()
        
        # 2. Agents make decisions
        decisions = [agent.make_decision(env_state) for agent in self.agents]
        
        # 3. Policy filters/modifies decisions
        approved_decisions = self.policy.apply_policy(decisions)
        
        # 4. Update environment based on actions
        visitor_impact = len(approved_decisions) * 0.01  # Example
        self.environment.apply_external_forcing(visitor_impact)
        
        # 5. Update all components
        self.environment.update(self.dt)
        self.policy.update(self.dt)
        for agent in self.agents:
            agent.update(self.dt)
        
        # 6. Record state
        self.time += self.dt
        self.history.append(self._collect_state())
    
    def run(self, n_steps: int):
        """Run simulation for n steps"""
        self.initialize()
        for _ in range(n_steps):
            self.step()
        return self.history
    
    def _collect_state(self) -> Dict[str, Any]:
        """Aggregate state from all components"""
        return {
            'time': self.time,
            'environment': self.environment.get_state(),
            'policy': self.policy.get_state(),
            'n_agents': len(self.agents)
        }
```

## Usage Example

```python
# Configuration
config = {
    'environment': {'initial_temp': 2.0, 'initial_ice': 1000, 'melt_coef': 0.1},
    'agent': {'base_wtp': 100, 'ideal_ice': 1000},
    'policy': {'tax_rate': 0.1, 'visitor_cap': 500}
}

# Build model
env = Environment(config['environment'])
agents = [Tourist(i, config['agent']) for i in range(1000)]
policy = Policy(config['policy'])

# Run simulation
sim = Simulator(env, agents, policy, dt=1.0)
results = sim.run(n_steps=365)

# Analyze results
import pandas as pd
df = pd.DataFrame(results)
```

## Key Benefits

1. **Swappable components**: Replace `Environment` with different physics without touching agents
2. **Unit testing**: Test each module independently
3. **Parallel development**: Team members work on different modules
4. **Clear interfaces**: `get_state()` and `update()` standardize interactions
5. **Configuration-driven**: Easy to run sensitivity analyses

## Requirements

- Each class must inherit from `ModelComponent` or have equivalent interface
- All inter-module communication through `get_state()` - NO direct attribute access
- Private methods (starting with `_`) for internal calculations
- Configuration passed via dictionaries, not hardcoded
- Type hints for all method signatures

## Output Organization

```
code/
├── models/
│   ├── base.py          # ModelComponent base class
│   ├── environment.py   # Environment implementations
│   ├── agents.py        # Agent classes
│   ├── policy.py        # Policy classes
│   └── simulator.py     # Simulation orchestrator
├── config/
│   └── model_config.yaml  # Configuration file
└── run_simulation.py    # Main entry point
```

## Common Pitfalls

- **Tight coupling**: Agents directly accessing environment attributes
- **God class**: Putting all logic in Simulator instead of modules
- **No abstraction**: Different environment types with incompatible interfaces
- **Hardcoded values**: Parameters buried in method bodies instead of config
