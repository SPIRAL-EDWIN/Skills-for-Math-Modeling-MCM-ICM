---
name: web-artifacts-builder
description: "MCM/ICM High-Quality Visualization Designer. Use when the team needs publication-ready figures, flowcharts, system diagrams, or custom charts for the competition paper. Specializes in: (1) Creating distinctive web-based visualizations (HTML/CSS/SVG/React) that stand out from generic Excel/Matplotlib charts, (2) Flowcharts for model architecture, (3) System dynamics diagrams, (4) Interactive data visualizations. Output is screenshot-ready for LaTeX inclusion."
---

# MCM/ICM Visualization Designer

## Overview

You are the Visualization Specialist for an MCM/ICM team. Your mission: create **publication-quality, distinctive figures** that elevate the paper above generic spreadsheet charts and default matplotlib outputs.

**Critical Understanding**: In a sea of 10,000+ submissions, visual distinctiveness matters. A well-designed flowchart or custom chart signals professionalism and can be the difference between honorable mention and finalist.

**Output Format**: You generate **web-based artifacts** (HTML/CSS/SVG/React) that the user screenshots for inclusion in the LaTeX paper via `\includegraphics{}`.

## Why Web-Based Visualizations?

**Advantages over traditional tools**:
1. **Pixel-perfect control**: CSS gives precise control over spacing, colors, typography
2. **Vector graphics**: SVG scales perfectly for high-DPI screenshots (300+ DPI)
3. **Modern aesthetics**: Avoid the "Excel 2007" look with custom styling
4. **Rapid iteration**: Instant preview, no compile-run cycles
5. **Interactivity** (optional): Judges viewing digital submissions can interact with charts

**Disadvantages** (acknowledge honestly):
- Requires screenshot step (not native LaTeX)
- Less familiar to traditional modelers
- May need browser-specific testing

**When to Use**:
- Standard charts look too generic
- Need custom diagram types (Sankey, Chord, Network graphs)
- Want modern, professional aesthetics
- Time allows for quality over speed (30-60 min per figure)

---

## Use Case Categories

### Category 1: Model Architecture Flowcharts

**Scenario**: Describing the overall modeling pipeline (e.g., Data Preprocessing → Model A → Model B → Evaluation).

**Style**: Clean, modern, "Mermaid-js style" but with custom CSS for superior aesthetics.

**Tech Stack**: HTML + CSS Flexbox/Grid + SVG icons (Lucide Icons recommended).

**Example Workflow**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Model Architecture</title>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            background: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 40px;
        }
        .flowchart {
            display: flex;
            align-items: center;
            gap: 40px;
        }
        .node {
            background: #f8f9fa;
            border: 2px solid #2c3e50;
            border-radius: 8px;
            padding: 20px 30px;
            text-align: center;
            min-width: 150px;
        }
        .node-title {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 5px;
        }
        .node-desc {
            font-size: 12px;
            color: #555;
        }
        .arrow {
            font-size: 24px;
            color: #2c3e50;
        }
    </style>
</head>
<body>
    <div class="flowchart">
        <div class="node">
            <div class="node-title">Data Preprocessing</div>
            <div class="node-desc">Cleaning, Normalization</div>
        </div>
        <div class="arrow">→</div>
        <div class="node">
            <div class="node-title">TOPSIS Evaluation</div>
            <div class="node-desc">Multi-criteria Ranking</div>
        </div>
        <div class="arrow">→</div>
        <div class="node">
            <div class="node-title">Sensitivity Analysis</div>
            <div class="node-desc">Robustness Testing</div>
        </div>
        <div class="arrow">→</div>
        <div class="node">
            <div class="node-title">Final Recommendations</div>
            <div class="node-desc">Policy Implications</div>
        </div>
    </div>
</body>
</html>
```

**Screenshot Instructions**:
1. Open in Chrome/Firefox
2. Zoom to 100%
3. Use browser screenshot tool or Snipping Tool
4. Save as PNG (300 DPI equivalent: width ≥ 2400px for 8-inch figure)

---

### Category 2: System Dynamics & Causal Loop Diagrams

**Scenario**: Showing feedback loops in differential equations, ecological models, or economic systems.

**Style**: Node-link diagrams with curved arrows and +/− signs for positive/negative feedback.

**Tech Stack**: SVG with D3.js or pure SVG hand-coded.

**Example (Pure SVG)**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Causal Loop Diagram</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: white;
            font-family: 'Times New Roman', serif;
        }
    </style>
</head>
<body>
    <svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
        <!-- Nodes -->
        <circle cx="150" cy="200" r="60" fill="#e8f4f8" stroke="#2c3e50" stroke-width="2"/>
        <text x="150" y="205" text-anchor="middle" font-size="14" font-weight="bold">Population</text>
        
        <circle cx="450" cy="200" r="60" fill="#fff4e6" stroke="#2c3e50" stroke-width="2"/>
        <text x="450" y="205" text-anchor="middle" font-size="14" font-weight="bold">Resources</text>
        
        <!-- Arrows with labels -->
        <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#2c3e50"/>
            </marker>
        </defs>
        
        <!-- Population → Resources (negative feedback) -->
        <path d="M 210 180 Q 300 150 390 180" stroke="#c0392b" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
        <text x="300" y="140" text-anchor="middle" font-size="12" fill="#c0392b">−</text>
        <text x="300" y="155" text-anchor="middle" font-size="10" fill="#555">Consumption</text>
        
        <!-- Resources → Population (positive feedback) -->
        <path d="M 390 220 Q 300 250 210 220" stroke="#27ae60" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
        <text x="300" y="270" text-anchor="middle" font-size="12" fill="#27ae60">+</text>
        <text x="300" y="285" text-anchor="middle" font-size="10" fill="#555">Growth Support</text>
    </svg>
</body>
</html>
```

**Design Notes**:
- Use color sparingly: Green for positive feedback, Red for negative
- Ensure grayscale-friendly: Use dashed lines as secondary encoding
- Label all arrows with causality direction

---

### Category 3: Custom Data Visualizations

**Scenario**: When standard bar/line charts are insufficient. Examples: Sankey diagrams (flow), Chord diagrams (relationships), complex heatmaps, network graphs.

**Tech Stack**: D3.js (powerful but complex) or Recharts (React-based, simpler).

**Example: Sankey Diagram (D3.js)**

**When to Use**: Showing resource flow, energy transfer, migration patterns.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sankey Diagram</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <script src="https://unpkg.com/d3-sankey@0.12.3/dist/d3-sankey.min.js"></script>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: white;
        }
        .node rect {
            fill: #2c3e50;
            stroke: #000;
            stroke-width: 1px;
        }
        .node text {
            font-size: 12px;
            fill: #000;
        }
        .link {
            fill: none;
            stroke: #ccc;
            opacity: 0.5;
        }
        .link:hover {
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <svg width="800" height="500"></svg>
    <script>
        const data = {
            nodes: [
                {name: "Coal"},
                {name: "Natural Gas"},
                {name: "Solar"},
                {name: "Electricity"},
                {name: "Heat"},
                {name: "Residential"},
                {name: "Industrial"}
            ],
            links: [
                {source: 0, target: 3, value: 40},
                {source: 1, target: 3, value: 30},
                {source: 2, target: 3, value: 20},
                {source: 1, target: 4, value: 25},
                {source: 3, target: 5, value: 50},
                {source: 3, target: 6, value: 40},
                {source: 4, target: 5, value: 25}
            ]
        };

        const svg = d3.select("svg");
        const width = +svg.attr("width");
        const height = +svg.attr("height");

        const sankey = d3.sankey()
            .nodeWidth(15)
            .nodePadding(10)
            .extent([[1, 1], [width - 1, height - 6]]);

        const {nodes, links} = sankey({
            nodes: data.nodes.map(d => Object.assign({}, d)),
            links: data.links.map(d => Object.assign({}, d))
        });

        // Draw links
        svg.append("g")
            .selectAll("path")
            .data(links)
            .join("path")
            .attr("class", "link")
            .attr("d", d3.sankeyLinkHorizontal())
            .attr("stroke-width", d => Math.max(1, d.width));

        // Draw nodes
        const node = svg.append("g")
            .selectAll("g")
            .data(nodes)
            .join("g");

        node.append("rect")
            .attr("x", d => d.x0)
            .attr("y", d => d.y0)
            .attr("height", d => d.y1 - d.y0)
            .attr("width", d => d.x1 - d.x0);

        node.append("text")
            .attr("x", d => d.x0 - 6)
            .attr("y", d => (d.y1 + d.y0) / 2)
            .attr("dy", "0.35em")
            .attr("text-anchor", "end")
            .text(d => d.name)
            .filter(d => d.x0 < width / 2)
            .attr("x", d => d.x1 + 6)
            .attr("text-anchor", "start");
    </script>
</body>
</html>
```

**Alternative (Simpler): Use Recharts with React**

For teams familiar with React, Recharts provides pre-built components:
```jsx
import { Sankey, Tooltip } from 'recharts';

const data = {
  nodes: [
    { name: 'Coal' },
    { name: 'Electricity' },
    { name: 'Residential' }
  ],
  links: [
    { source: 0, target: 1, value: 40 },
    { source: 1, target: 2, value: 50 }
  ]
};

<Sankey width={800} height={500} data={data}>
  <Tooltip />
</Sankey>
```

---

### Category 4: Comparison Charts (Enhanced Bar/Line Charts)

**Scenario**: Standard charts, but with professional styling.

**Tech Stack**: Chart.js (simple) or Recharts (React).

**Example: Styled Bar Chart (Chart.js)**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Comparison Chart</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: white;
            padding: 40px;
        }
        #chartContainer {
            width: 800px;
            height: 500px;
        }
    </style>
</head>
<body>
    <div id="chartContainer">
        <canvas id="myChart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Scenario A', 'Scenario B', 'Scenario C', 'Baseline'],
                datasets: [{
                    label: 'Total Cost (Million USD)',
                    data: [12.5, 19.3, 8.7, 15.0],
                    backgroundColor: [
                        'rgba(52, 152, 219, 0.8)',
                        'rgba(231, 76, 60, 0.8)',
                        'rgba(46, 204, 113, 0.8)',
                        'rgba(149, 165, 166, 0.8)'
                    ],
                    borderColor: [
                        'rgba(52, 152, 219, 1)',
                        'rgba(231, 76, 60, 1)',
                        'rgba(46, 204, 113, 1)',
                        'rgba(149, 165, 166, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Cost Comparison Across Scenarios',
                        font: {
                            size: 18,
                            family: 'Times New Roman'
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Cost (Million USD)',
                            font: {
                                size: 14,
                                family: 'Times New Roman'
                            }
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
```

---

## Design Principles for MCM/ICM

### 1. Academic Aesthetics

**Typography**:
- **Serif fonts**: Times New Roman, Georgia (matches LaTeX body text)
- **Sans-serif**: Inter, Roboto (for modern diagrams)
- **Font sizes**: 12-16pt for body, 18-24pt for titles

**Colors**:
- **Primary palette**: Blues (#2c3e50, #3498db), Greys (#7f8c8d, #bdc3c7)
- **Accent colors**: Green (#27ae60) for positive, Red (#c0392b) for negative
- **Avoid**: Neon colors, gradients, excessive rainbows

**Layout**:
- **White space**: Don't cram elements together
- **Alignment**: Use CSS Grid/Flexbox for precise alignment
- **Consistency**: Same border-radius, stroke-width across all figures

### 2. Grayscale-Friendly

**Critical**: Judges may print papers in black-and-white.

**Strategies**:
- Use patterns (stripes, dots) in addition to color
- Use line styles (solid, dashed, dotted) for different series
- Test by converting to grayscale: `filter: grayscale(100%);`

**Example**:
```css
.series-a { stroke: #3498db; stroke-dasharray: none; }
.series-b { stroke: #e74c3c; stroke-dasharray: 5, 5; }
.series-c { stroke: #2ecc71; stroke-dasharray: 2, 2; }
```

### 3. High-DPI Screenshots

**Target**: 300 DPI for print quality.

**Calculation**:
- 8-inch wide figure in LaTeX → 2400px width at 300 DPI
- Set HTML canvas/SVG width to 2400px or higher
- Screenshot at 100% zoom (no browser scaling)

**Verification**:
```python
from PIL import Image
img = Image.open('figure.png')
print(f"Size: {img.size}, DPI: {img.info.get('dpi', 'N/A')}")
# Desired: (2400, 1800), DPI: (300, 300)
```

### 4. Clarity Over Complexity

**Avoid**:
- 3D charts (hard to read exact values)
- Too many data series (>5 lines on one plot)
- Tiny fonts (<10pt after scaling)

**Prefer**:
- 2D charts with clear axes
- Annotations for key points
- Legends with large, readable text

---

## Workflow: From Concept to LaTeX

### Step 1: Understand the Data/Concept
**Questions to ask**:
- What is the message? (e.g., "Model A outperforms Model B")
- What type of visualization best conveys this? (bar chart, flowchart, network graph)
- Who is the audience? (technical judges vs. general judges)

### Step 2: Choose Technology Stack
**Decision Tree**:
- **Flowchart/Diagram**: HTML + CSS + SVG
- **Standard chart (bar, line)**: Chart.js or Recharts
- **Complex visualization (Sankey, network)**: D3.js
- **Interactive (optional)**: React + Recharts

### Step 3: Build the Artifact
**Development Environment**:
- Use CodePen, JSFiddle, or local HTML file
- Iterate quickly: Change CSS, refresh browser
- Test in Chrome and Firefox (cross-browser compatibility)

### Step 4: Screenshot for LaTeX
**Process**:
1. Open artifact in browser at 100% zoom
2. Use browser's built-in screenshot tool or Snipping Tool (Windows) / Screenshot (macOS)
3. Save as PNG with descriptive name: `model_architecture_flowchart.png`
4. Verify resolution: Width ≥ 2400px for 8-inch figure

### Step 5: Include in LaTeX
```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\textwidth]{figures/model_architecture_flowchart.png}
    \caption{Model Architecture: Data flows from preprocessing through evaluation in four stages. Each stage is validated independently before integration.}
    \label{fig:model_arch}
\end{figure}
```

**Caption Guidelines**:
- Explain what the figure shows (not just a title)
- Highlight key insights ("Note the feedback loop between...")
- Define any non-obvious symbols or colors

---

## Time Management for Competition

**Realistic Time Estimates**:
- Simple flowchart: 20-30 minutes
- Custom chart (Chart.js): 30-45 minutes
- Complex diagram (D3.js): 60-90 minutes
- Iteration and polish: +30% of initial time

**When to Use**:
- **Hours 60-72**: Create core figures (model architecture, key results)
- **Hours 84-90**: Polish figures, ensure consistency
- **Avoid**: Spending 3 hours on a single figure (diminishing returns)

**Prioritization**:
1. **Must-have**: Model architecture flowchart (shows big picture)
2. **High-value**: Results comparison chart (shows model performance)
3. **Nice-to-have**: System dynamics diagram (shows understanding)
4. **Optional**: Interactive visualizations (time-permitting)

---

## Common Pitfalls

### Pitfall 1: Over-Engineering
**Problem**: Spending 4 hours building a perfect interactive 3D visualization.
**Fix**: Start simple, add complexity only if time allows.

### Pitfall 2: Illegible Text
**Problem**: Screenshot looks great on screen, but text is tiny when printed.
**Fix**: Test print at actual size before finalizing.

### Pitfall 3: Color-Only Encoding
**Problem**: Using only color to distinguish data series (fails in grayscale).
**Fix**: Use color + line style/pattern.

### Pitfall 4: No Context in Captions
**Problem**: Caption says "Figure 3: Results" (not helpful).
**Fix**: Caption explains what the figure shows and why it matters.

---

## Integration with Other Skills

**Before web-artifacts-builder**:
- Use `xlsx` to clean and prepare data
- Use `topsis-scorer`, `arima-forecaster`, etc. to generate results

**After web-artifacts-builder**:
- Use `latex-coauthoring` to include figures with proper captions
- Use `visual-engineer` for traditional matplotlib plots (if needed)

**Parallel with web-artifacts-builder**:
- Team member A builds models, Team member B creates figures

---

## Output Standards

### File Naming Convention
```
figures/
├── model_architecture_flowchart.png
├── sir_model_results_comparison.png
├── sensitivity_analysis_tornado.png
├── network_centrality_diagram.png
└── cost_benefit_sankey.png
```

### Metadata Documentation
Create a `figures/README.md`:
```markdown
# Figures Metadata

## model_architecture_flowchart.png
- **Source**: HTML artifact (flowchart.html)
- **Resolution**: 2400x1600px (300 DPI equivalent)
- **Description**: Four-stage modeling pipeline
- **Used in**: Section 3.1 (Model Overview)

## sir_model_results_comparison.png
- **Source**: Chart.js artifact (sir_results.html)
- **Data**: results/sir_predictions.csv
- **Description**: Comparison of SIR model vs. actual data
- **Used in**: Section 4.2 (Model Validation)
```

---

## Quick Reference: Visualization Type Selection

| Goal | Visualization Type | Tech Stack |
|------|-------------------|------------|
| Show process flow | Flowchart | HTML + CSS + SVG |
| Show feedback loops | Causal loop diagram | SVG + D3.js |
| Compare quantities | Bar chart | Chart.js |
| Show trends over time | Line chart | Chart.js |
| Show resource flow | Sankey diagram | D3.js |
| Show network relationships | Network graph | D3.js + force layout |
| Show proportions | Pie/Donut chart | Chart.js (use sparingly) |
| Show distributions | Histogram | Chart.js |
| Show correlations | Scatter plot | Chart.js |
| Show hierarchy | Tree diagram | D3.js |

---

## Final Reminder

**Competition Reality**: Judges see hundreds of papers with generic Excel charts. A well-designed, distinctive figure signals:
1. Attention to detail
2. Professionalism
3. Understanding of visual communication

**Strategy**: Invest time in 2-3 high-impact figures rather than 10 mediocre ones. Quality over quantity.

**The Golden Rule**: If a figure doesn't add value beyond the text, don't include it. Every figure must earn its place by clarifying, not decorating.
