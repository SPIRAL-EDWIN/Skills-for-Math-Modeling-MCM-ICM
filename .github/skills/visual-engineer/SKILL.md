---
name: visual-engineer
description: Academic-quality visualization for MCM/ICM competitions. Use when creating figures for papers requiring publication-standard formatting (Times New Roman, 300 DPI, proper colormaps, clean layouts). Automatically saves to organized results directory. Essential for O-prize presentation quality.
---

# Visual-Engineer

Create publication-quality figures that meet academic standards for mathematical modeling competitions.

## Core Principles

1. **Clarity over decoration**: Every element must serve a purpose
2. **Accessibility**: Colorblind-friendly palettes, readable fonts
3. **Consistency**: Same style across all figures
4. **Reproducibility**: All figures generated from code, not manual editing

## Standard Configuration

### Global Matplotlib Settings

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set publication-quality defaults
plt.rcParams.update({
    # Font
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    
    # Figure
    'figure.figsize': (8, 6),
    'figure.dpi': 100,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
    
    # Lines and markers
    'lines.linewidth': 2,
    'lines.markersize': 6,
    
    # Axes
    'axes.linewidth': 1.2,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    
    # Legend
    'legend.frameon': True,
    'legend.framealpha': 0.8,
    'legend.edgecolor': 'black',
    
    # Colors
    'axes.prop_cycle': plt.cycler('color', 
        ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', 
         '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'])
})

# Seaborn style for cleaner look
sns.set_style("whitegrid")
sns.set_context("paper")
```

## Common Plot Types

### 1. Time Series Plot

```python
def plot_time_series(time, data, labels=None, title='Time Series', 
                     xlabel='Time', ylabel='Value', 
                     filename='results/time_series.png'):
    """
    Plot one or more time series
    
    Parameters:
    - time: 1D array of time points
    - data: 2D array (n_series, n_points) or 1D array
    - labels: List of series names
    """
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Handle single series
    if data.ndim == 1:
        data = data.reshape(1, -1)
        labels = [labels] if labels else ['Series']
    
    # Plot each series
    for i, series in enumerate(data):
        label = labels[i] if labels else f'Series {i+1}'
        ax.plot(time, series, linewidth=2, label=label, marker='o', 
                markersize=4, markevery=max(1, len(time)//20))
    
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(title, fontweight='bold', pad=15)
    ax.legend(loc='best', frameon=True)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved: {filename}")
```

### 2. Scatter Plot with Regression

```python
def plot_scatter_regression(x, y, title='Scatter Plot', 
                            xlabel='X', ylabel='Y',
                            filename='results/scatter.png'):
    """Scatter plot with regression line and statistics"""
    
    from scipy import stats
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Scatter
    ax.scatter(x, y, alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
    
    # Regression line
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    line_x = np.array([x.min(), x.max()])
    line_y = slope * line_x + intercept
    ax.plot(line_x, line_y, 'r-', linewidth=2, 
            label=f'y = {slope:.3f}x + {intercept:.3f}')
    
    # Statistics box
    textstr = f'R² = {r_value**2:.4f}\np-value = {p_value:.4e}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, 
            fontsize=10, verticalalignment='top', bbox=props)
    
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(title, fontweight='bold', pad=15)
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    
    print(f"Saved: {filename}")
```

### 3. Heatmap

```python
def plot_heatmap(data, row_labels=None, col_labels=None, 
                 title='Heatmap', cmap='viridis',
                 filename='results/heatmap.png'):
    """
    Create annotated heatmap
    
    Parameters:
    - data: 2D array
    - cmap: 'viridis', 'RdYlGn', 'coolwarm', 'Blues'
    """
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    im = ax.imshow(data, cmap=cmap, aspect='auto')
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('Value', rotation=270, labelpad=20, fontweight='bold')
    
    # Ticks
    if row_labels is not None:
        ax.set_yticks(np.arange(len(row_labels)))
        ax.set_yticklabels(row_labels)
    if col_labels is not None:
        ax.set_xticks(np.arange(len(col_labels)))
        ax.set_xticklabels(col_labels, rotation=45, ha='right')
    
    # Annotations (for small matrices)
    if data.shape[0] <= 10 and data.shape[1] <= 10:
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                text = ax.text(j, i, f'{data[i, j]:.2f}',
                             ha="center", va="center", color="white" 
                             if data[i, j] > data.max()/2 else "black")
    
    ax.set_title(title, fontweight='bold', pad=15)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    
    print(f"Saved: {filename}")
```

### 4. Bar Chart with Error Bars

```python
def plot_bar_chart(categories, values, errors=None, 
                   title='Bar Chart', ylabel='Value',
                   filename='results/bar_chart.png'):
    """Bar chart with optional error bars"""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(categories))
    bars = ax.bar(x, values, width=0.6, alpha=0.8, 
                  edgecolor='black', linewidth=1.2)
    
    # Error bars
    if errors is not None:
        ax.errorbar(x, values, yerr=errors, fmt='none', 
                   ecolor='black', capsize=5, capthick=2)
    
    # Value labels on bars
    for i, (bar, val) in enumerate(zip(bars, values)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(title, fontweight='bold', pad=15)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    
    print(f"Saved: {filename}")
```

### 5. Multi-Panel Figure

```python
def plot_multi_panel(data_dict, title='Multi-Panel Figure',
                     filename='results/multi_panel.png'):
    """
    Create figure with multiple subplots
    
    Parameters:
    - data_dict: {'subplot_title': (x, y), ...}
    """
    
    n_plots = len(data_dict)
    n_cols = min(2, n_plots)
    n_rows = (n_plots + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 4*n_rows))
    
    if n_plots == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    for ax, (subtitle, (x, y)) in zip(axes, data_dict.items()):
        ax.plot(x, y, linewidth=2, marker='o', markersize=4)
        ax.set_title(subtitle, fontweight='bold')
        ax.set_xlabel('X', fontweight='bold')
        ax.set_ylabel('Y', fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    # Hide extra subplots
    for i in range(n_plots, len(axes)):
        axes[i].axis('off')
    
    fig.suptitle(title, fontsize=16, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved: {filename}")
```

## Color Schemes

### Colorblind-Friendly Palettes

```python
# Sequential (for continuous data)
SEQUENTIAL = {
    'blue': 'Blues',
    'green': 'Greens',
    'orange': 'Oranges',
    'viridis': 'viridis',  # Perceptually uniform
    'plasma': 'plasma'
}

# Diverging (for data with meaningful center)
DIVERGING = {
    'red_blue': 'RdBu_r',
    'red_green': 'RdYlGn',
    'cool_warm': 'coolwarm'
}

# Qualitative (for categories)
QUALITATIVE = [
    '#1f77b4',  # Blue
    '#ff7f0e',  # Orange
    '#2ca02c',  # Green
    '#d62728',  # Red
    '#9467bd',  # Purple
    '#8c564b',  # Brown
    '#e377c2',  # Pink
    '#7f7f7f'   # Gray
]
```

## LaTeX Integration

### For LaTeX-rendered Text

```python
# Enable LaTeX rendering (requires LaTeX installation)
plt.rcParams.update({
    'text.usetex': True,
    'text.latex.preamble': r'\usepackage{amsmath}'
})

# Use in labels
ax.set_xlabel(r'$\alpha$ (growth rate)', fontsize=12)
ax.set_ylabel(r'$P(t)$ (population)', fontsize=12)
ax.set_title(r'Model: $\frac{dP}{dt} = \alpha P(1 - \frac{P}{K})$')
```

## File Organization

```python
import os

def ensure_results_dir():
    """Create organized results directory"""
    dirs = [
        'results/figures',
        'results/tables',
        'results/animations'
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

# Use at start of visualization script
ensure_results_dir()
```

## Quality Checklist

Before submitting figures:
- [ ] Font is Times New Roman or serif equivalent
- [ ] DPI is 300 or higher
- [ ] Axes are labeled with units
- [ ] Legend is present and clear
- [ ] Colors are colorblind-friendly
- [ ] Grid lines are subtle (alpha < 0.5)
- [ ] No unnecessary decorations (3D effects, shadows)
- [ ] File size is reasonable (< 5MB per figure)
- [ ] All text is readable when printed

## Common Mistakes to Avoid

1. **Rainbow colormap**: Use 'viridis' instead of 'jet'
2. **Tiny fonts**: Minimum 10pt for readability
3. **No labels**: Always label axes with units
4. **Too much data**: Simplify or use sampling
5. **3D when 2D works**: 3D plots are hard to read
6. **Pie charts**: Use bar charts instead
7. **Default colors**: Customize for consistency
8. **Low DPI**: Always save at 300 DPI minimum

## Advanced: Animation

```python
from matplotlib.animation import FuncAnimation

def create_animation(data_over_time, filename='results/animation.mp4'):
    """Create animation of time-evolving data"""
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    line, = ax.plot([], [], linewidth=2)
    ax.set_xlim(0, len(data_over_time[0]))
    ax.set_ylim(data_over_time.min(), data_over_time.max())
    
    def init():
        line.set_data([], [])
        return line,
    
    def update(frame):
        x = np.arange(len(data_over_time[frame]))
        y = data_over_time[frame]
        line.set_data(x, y)
        ax.set_title(f'Time Step: {frame}', fontweight='bold')
        return line,
    
    anim = FuncAnimation(fig, update, frames=len(data_over_time),
                        init_func=init, blit=True, interval=100)
    
    anim.save(filename, writer='ffmpeg', fps=10, dpi=150)
    plt.close()
    
    print(f"Saved animation: {filename}")
```

## Output Naming Convention

Use descriptive, systematic names:
```
results/figures/
├── fig1_time_series_population.png
├── fig2_heatmap_parameter_sweep.png
├── fig3_scatter_correlation.png
└── fig4_bar_comparison.png
```

Not:
```
plot.png
figure_final_v3_FINAL.png
untitled.png
```
