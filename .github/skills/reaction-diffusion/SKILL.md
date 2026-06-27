---
name: reaction-diffusion
description: Spatiotemporal modeling using partial differential equations (PDEs). Captures both local reactions and spatial diffusion. Essential for pattern formation, disease spread, pollution dispersal, and ecological invasion problems in MCM/ICM.
---

# Reaction-Diffusion Models

Partial differential equations (PDEs) describing how quantities evolve in both time and space through local reactions and spatial diffusion.

## When to Use

- **Spatial Epidemic Spread**: Disease propagating across geographic regions.
- **Ecological Invasion**: Invasive species spreading through a habitat.
- **Pattern Formation**: Animal coat patterns, chemical oscillations (Turing patterns).
- **Pollution Dispersal**: Contaminant diffusion in air/water.
- **Fire Spread**: Forest fire propagation.
- **Tumor Growth**: Cancer cells invading tissue.

## When NOT to Use

- **No Spatial Structure**: Use ODE models (**`logistic-growth`**, **`lotka-volterra`**).
- **Discrete Space**: Use cellular automata or agent-based models.
- **Advection Dominant**: Use advection-diffusion equations (different PDE).
- **Very Small Scale**: Use stochastic particle models.

## Mathematical Foundation

### General Form
$$\frac{\partial u}{\partial t} = D \nabla^2 u + f(u)$$

Where:
- $u(x, t)$: Concentration/density at position $x$ and time $t$
- $D$: Diffusion coefficient (spatial spread rate)
- $\nabla^2 u$: Laplacian operator (measures local curvature)
- $f(u)$: Reaction term (local dynamics)

### 1D Laplacian (Finite Difference)
$$\nabla^2 u \approx \frac{u_{i+1} - 2u_i + u_{i-1}}{\Delta x^2}$$

### 2D Laplacian
$$\nabla^2 u \approx \frac{u_{i+1,j} + u_{i-1,j} + u_{i,j+1} + u_{i,j-1} - 4u_{i,j}}{\Delta x^2}$$

## Classic Models

### 1. Fisher-KPP Equation (Single Species)
$$\frac{\partial u}{\partial t} = D \frac{\partial^2 u}{\partial x^2} + ru\left(1 - \frac{u}{K}\right)$$

- **Interpretation**: Population diffusion + Logistic growth
- **Application**: Invasive species, gene spread
- **Wave Speed**: $c = 2\sqrt{Dr}$ (minimum speed of traveling wave)

### 2. Gray-Scott Model (Pattern Formation)
$$\begin{cases}
\frac{\partial u}{\partial t} = D_u \nabla^2 u - uv^2 + F(1-u) \\
\frac{\partial v}{\partial t} = D_v \nabla^2 v + uv^2 - (F+k)v
\end{cases}$$

- **Interpretation**: Two chemicals reacting and diffusing
- **Application**: Turing patterns, self-organization
- **Parameters**: $F$ (feed rate), $k$ (kill rate)

### 3. SIR Spatial Model (Epidemic Spread)
$$\begin{cases}
\frac{\partial S}{\partial t} = D_S \nabla^2 S - \beta SI \\
\frac{\partial I}{\partial t} = D_I \nabla^2 I + \beta SI - \gamma I \\
\frac{\partial R}{\partial t} = D_R \nabla^2 R + \gamma I
\end{cases}$$

- **Interpretation**: Susceptible-Infected-Recovered with spatial movement
- **Application**: Disease spread across cities/regions

## Implementation Template

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')

class ReactionDiffusion1D:
    """
    1D Reaction-Diffusion solver using finite difference method
    """
    
    def __init__(self, L, N, D, reaction_func, boundary='neumann'):
        """
        Args:
            L (float): Spatial domain length
            N (int): Number of spatial grid points
            D (float): Diffusion coefficient
            reaction_func (callable): Reaction term f(u)
            boundary (str): 'neumann' (no-flux) or 'dirichlet' (fixed) or 'periodic'
        """
        self.L = L
        self.N = N
        self.dx = L / (N - 1)
        self.x = np.linspace(0, L, N)
        self.D = D
        self.reaction_func = reaction_func
        self.boundary = boundary
        
        # Stability condition: dt <= dx^2 / (2*D)
        self.dt_max = self.dx**2 / (2 * D)
        self.dt = 0.9 * self.dt_max  # Use 90% of max for safety
        
        self.u_history = []
        self.t_history = []
        
    def laplacian(self, u):
        """
        Compute Laplacian using finite differences
        """
        lapl = np.zeros_like(u)
        
        # Interior points
        lapl[1:-1] = (u[2:] - 2*u[1:-1] + u[:-2]) / self.dx**2
        
        # Boundary conditions
        if self.boundary == 'neumann':
            # Zero flux: du/dx = 0 at boundaries
            lapl[0] = (u[1] - u[0]) / self.dx**2
            lapl[-1] = (u[-2] - u[-1]) / self.dx**2
        elif self.boundary == 'dirichlet':
            # Fixed value (already set to 0 by initialization)
            lapl[0] = 0
            lapl[-1] = 0
        elif self.boundary == 'periodic':
            lapl[0] = (u[1] - 2*u[0] + u[-2]) / self.dx**2
            lapl[-1] = (u[1] - 2*u[-1] + u[-2]) / self.dx**2
        
        return lapl
    
    def step(self, u):
        """
        Single time step using explicit Euler method
        """
        lapl = self.laplacian(u)
        reaction = self.reaction_func(u)
        
        u_new = u + self.dt * (self.D * lapl + reaction)
        
        return u_new
    
    def solve(self, u0, T, save_interval=10):
        """
        Solve the PDE from t=0 to t=T
        
        Args:
            u0 (array): Initial condition
            T (float): Final time
            save_interval (int): Save every N steps
            
        Returns:
            tuple: (u_history, t_history)
        """
        u = u0.copy()
        t = 0
        step_count = 0
        
        self.u_history = [u.copy()]
        self.t_history = [t]
        
        while t < T:
            u = self.step(u)
            t += self.dt
            step_count += 1
            
            if step_count % save_interval == 0:
                self.u_history.append(u.copy())
                self.t_history.append(t)
        
        return np.array(self.u_history), np.array(self.t_history)

class ReactionDiffusion2D:
    """
    2D Reaction-Diffusion solver for pattern formation
    """
    
    def __init__(self, Lx, Ly, Nx, Ny, Du, Dv, reaction_func):
        """
        Args:
            Lx, Ly (float): Domain size
            Nx, Ny (int): Grid points
            Du, Dv (float): Diffusion coefficients for u and v
            reaction_func (callable): Returns (f_u, f_v) reaction terms
        """
        self.Lx, self.Ly = Lx, Ly
        self.Nx, self.Ny = Nx, Ny
        self.dx = Lx / (Nx - 1)
        self.dy = Ly / (Ny - 1)
        self.Du, self.Dv = Du, Dv
        self.reaction_func = reaction_func
        
        # Stability condition (2D)
        dt_max = min(self.dx**2, self.dy**2) / (4 * max(Du, Dv))
        self.dt = 0.5 * dt_max
        
        self.x = np.linspace(0, Lx, Nx)
        self.y = np.linspace(0, Ly, Ny)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
    def laplacian_2d(self, u):
        """
        Compute 2D Laplacian with periodic boundary
        """
        lapl = np.zeros_like(u)
        
        # Use roll for periodic boundaries
        lapl += (np.roll(u, 1, axis=0) - 2*u + np.roll(u, -1, axis=0)) / self.dx**2
        lapl += (np.roll(u, 1, axis=1) - 2*u + np.roll(u, -1, axis=1)) / self.dy**2
        
        return lapl
    
    def step(self, u, v):
        """
        Single time step for two-component system
        """
        lapl_u = self.laplacian_2d(u)
        lapl_v = self.laplacian_2d(v)
        
        f_u, f_v = self.reaction_func(u, v)
        
        u_new = u + self.dt * (self.Du * lapl_u + f_u)
        v_new = v + self.dt * (self.Dv * lapl_v + f_v)
        
        return u_new, v_new
    
    def solve(self, u0, v0, T, save_interval=100):
        """
        Solve 2D system
        """
        u, v = u0.copy(), v0.copy()
        t = 0
        step_count = 0
        
        u_history = [u.copy()]
        v_history = [v.copy()]
        t_history = [t]
        
        n_steps = int(T / self.dt)
        
        for i in range(n_steps):
            u, v = self.step(u, v)
            t += self.dt
            step_count += 1
            
            if step_count % save_interval == 0:
                u_history.append(u.copy())
                v_history.append(v.copy())
                t_history.append(t)
        
        return np.array(u_history), np.array(v_history), np.array(t_history)

# --- Fisher-KPP Example ---
def fisher_kpp_example():
    """
    Fisher-KPP equation: Invasive species spread
    """
    print("=" * 60)
    print("FISHER-KPP EQUATION (Invasive Species)")
    print("=" * 60)
    
    # Parameters
    L = 100  # Domain length
    N = 200  # Grid points
    D = 0.1  # Diffusion coefficient
    r = 1.0  # Growth rate
    K = 1.0  # Carrying capacity
    
    # Reaction term: Logistic growth
    def reaction(u):
        return r * u * (1 - u / K)
    
    # Initialize solver
    solver = ReactionDiffusion1D(L, N, D, reaction, boundary='neumann')
    
    # Initial condition: localized population
    u0 = np.zeros(N)
    center = N // 4
    width = 10
    u0[center-width:center+width] = K
    
    # Solve
    T = 50
    u_history, t_history = solver.solve(u0, T, save_interval=20)
    
    # Theoretical wave speed
    wave_speed = 2 * np.sqrt(D * r)
    print(f"\nTheoretical wave speed: c = 2√(Dr) = {wave_speed:.3f}")
    
    # Plot snapshots
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # Spatial profiles at different times
    ax1 = axes[0]
    for i in range(0, len(t_history), len(t_history)//5):
        ax1.plot(solver.x, u_history[i], label=f't={t_history[i]:.1f}')
    ax1.set_xlabel('Position (x)', fontsize=12)
    ax1.set_ylabel('Population Density (u)', fontsize=12)
    ax1.set_title('Fisher-KPP: Traveling Wave', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Spacetime plot
    ax2 = axes[1]
    im = ax2.imshow(u_history, aspect='auto', origin='lower', 
                    extent=[0, L, 0, T], cmap='viridis')
    ax2.set_xlabel('Position (x)', fontsize=12)
    ax2.set_ylabel('Time (t)', fontsize=12)
    ax2.set_title('Spacetime Diagram', fontsize=14, fontweight='bold')
    plt.colorbar(im, ax=ax2, label='Density')
    
    plt.tight_layout()
    plt.savefig('fisher_kpp_analysis.png', dpi=300)
    plt.show()
    
    return solver, u_history, t_history

# --- Gray-Scott Example ---
def gray_scott_example():
    """
    Gray-Scott model: Pattern formation (Turing patterns)
    """
    print("\n" + "=" * 60)
    print("GRAY-SCOTT MODEL (Turing Patterns)")
    print("=" * 60)
    
    # Parameters
    Lx, Ly = 2.5, 2.5
    Nx, Ny = 200, 200
    Du = 2e-5  # Diffusion of u
    Dv = 1e-5  # Diffusion of v
    
    # Reaction parameters (spots pattern)
    F = 0.055  # Feed rate
    k = 0.062  # Kill rate
    
    def reaction(u, v):
        uvv = u * v * v
        f_u = -uvv + F * (1 - u)
        f_v = uvv - (F + k) * v
        return f_u, f_v
    
    # Initialize solver
    solver = ReactionDiffusion2D(Lx, Ly, Nx, Ny, Du, Dv, reaction)
    
    # Initial condition: uniform with small perturbation
    u0 = np.ones((Ny, Nx))
    v0 = np.zeros((Ny, Nx))
    
    # Add random perturbation in center
    center_x, center_y = Nx // 2, Ny // 2
    size = 20
    u0[center_y-size:center_y+size, center_x-size:center_x+size] = 0.5
    v0[center_y-size:center_y+size, center_x-size:center_x+size] = 0.25
    
    # Add random noise
    u0 += 0.01 * np.random.random((Ny, Nx))
    v0 += 0.01 * np.random.random((Ny, Nx))
    
    # Solve
    T = 10000
    print(f"Simulating for T={T} time units...")
    u_history, v_history, t_history = solver.solve(u0, v0, T, save_interval=500)
    
    print(f"Generated {len(t_history)} frames")
    
    # Plot final pattern
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    ax1 = axes[0]
    im1 = ax1.imshow(u_history[-1], cmap='viridis', origin='lower')
    ax1.set_title('Component u (Final)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    plt.colorbar(im1, ax=ax1)
    
    ax2 = axes[1]
    im2 = ax2.imshow(v_history[-1], cmap='plasma', origin='lower')
    ax2.set_title('Component v (Final)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    plt.colorbar(im2, ax=ax2)
    
    plt.tight_layout()
    plt.savefig('gray_scott_patterns.png', dpi=300)
    plt.show()
    
    return solver, u_history, v_history, t_history

# --- Run Examples ---
if __name__ == "__main__":
    # 1. Fisher-KPP
    solver_fisher, u_hist, t_hist = fisher_kpp_example()
    
    # 2. Gray-Scott
    solver_gs, u_hist_gs, v_hist_gs, t_hist_gs = gray_scott_example()
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print("Generated visualizations:")
    print("  - fisher_kpp_analysis.png")
    print("  - gray_scott_patterns.png")
```

## Numerical Stability

### Stability Condition (1D Explicit Euler)
$$\Delta t \leq \frac{\Delta x^2}{2D}$$

If violated, solution will explode (numerical instability).

### Improving Stability
1.  **Implicit Methods**: Crank-Nicolson (unconditionally stable but requires solving linear system).
2.  **Smaller Time Step**: Reduce $\Delta t$ (but slower computation).
3.  **Adaptive Time Stepping**: Adjust $\Delta t$ based on solution behavior.

## Pattern Formation (Turing Instability)

For two-component systems, patterns emerge when:
1.  **Differential diffusion**: $D_u \neq D_v$ (typically $D_v < D_u$)
2.  **Activator-inhibitor**: One species activates, other inhibits
3.  **Specific parameter ranges**: Critical values of $F$, $k$ in Gray-Scott

### Gray-Scott Parameter Regimes
| F | k | Pattern |
|---|---|---------|
| 0.055 | 0.062 | Spots |
| 0.035 | 0.065 | Stripes |
| 0.012 | 0.050 | Waves |
| 0.090 | 0.059 | Holes |

## Common Pitfalls

1.  **Violating Stability Condition**: Always check $\Delta t \leq \frac{\Delta x^2}{2D}$.
2.  **Wrong Boundary Conditions**: Neumann (no-flux) is most common for biological systems.
3.  **Insufficient Resolution**: Use at least 100 grid points for 1D, 100×100 for 2D.
4.  **Too Short Simulation**: Patterns may take 10,000+ time units to develop.
5.  **Ignoring Wave Speed**: For Fisher-KPP, measure and compare with theory $c = 2\sqrt{Dr}$.

## Integration Workflow

- **Parameter Estimation**: Use **`automated-sweep`** to find parameter ranges that produce desired patterns.
- **Sensitivity Analysis**: Use **`sensitivity-master`** to identify which parameters most affect wave speed or pattern type.
- **Comparison**: Compare with ODE models (**`logistic-growth`**) to show spatial effects.
- **Visualization**: Use **`visual-engineer`** to create publication-quality heatmaps and animations.
- **Uncertainty**: Use **`monte-carlo-engine`** to propagate parameter uncertainty to wave speed predictions.

## Output Requirements for Paper

1.  **PDE Formulation**: Display the full equation with all terms explained.
2.  **Numerical Method**: "We used finite difference with explicit Euler (Δx=0.5, Δt=0.001)."
3.  **Stability Check**: "The stability condition Δt ≤ Δx²/(2D) was satisfied throughout."
4.  **Wave Speed**: "The invasion front propagated at c=0.63, matching the theoretical prediction of 2√(Dr)=0.63."
5.  **Spatial Visualization**: Show spacetime diagrams or pattern snapshots at multiple times.
6.  **Biological Interpretation**: "The diffusion coefficient D=0.1 corresponds to a dispersal distance of ~3 km/year."

## Extensions

### 1. Advection-Diffusion
$$\frac{\partial u}{\partial t} = D \frac{\partial^2 u}{\partial x^2} - v \frac{\partial u}{\partial x} + f(u)$$

Adds directed flow (wind, river current).

### 2. Anisotropic Diffusion
$$\frac{\partial u}{\partial t} = D_x \frac{\partial^2 u}{\partial x^2} + D_y \frac{\partial^2 u}{\partial y^2} + f(u)$$

Different diffusion rates in different directions.

### 3. Fractional Diffusion
$$\frac{\partial u}{\partial t} = D \frac{\partial^\alpha u}{\partial x^\alpha} + f(u)$$

Models anomalous diffusion (Lévy flights).

## Decision Guide: When to Use RD Models

| Scenario | Use Reaction-Diffusion? |
|----------|-------------------------|
| Spatial spread is critical | ✅ Yes |
| Only temporal dynamics matter | ❌ No (use ODEs) |
| Pattern formation needed | ✅ Yes (Gray-Scott) |
| Discrete space (cities, networks) | ❌ No (use graphs/networks) |
| Need wave speed predictions | ✅ Yes (Fisher-KPP) |
| Stochastic effects dominant | ❌ No (use stochastic PDEs) |

## Advanced: Animation Creation

```python
def create_animation(u_history, t_history, filename='rd_animation.gif'):
    """
    Create animated GIF of reaction-diffusion evolution
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    def update(frame):
        ax.clear()
        ax.imshow(u_history[frame], cmap='viridis', origin='lower')
        ax.set_title(f'Time: {t_history[frame]:.2f}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    
    anim = animation.FuncAnimation(fig, update, frames=len(t_history), 
                                   interval=100, repeat=True)
    anim.save(filename, writer='pillow', fps=10)
    plt.close()
```
