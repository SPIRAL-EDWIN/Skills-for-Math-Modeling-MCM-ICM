---
name: latex-transformer
description: Convert Markdown content to LaTeX format for MCM/ICM paper writing. Use when drafting content in Markdown and need to convert to LaTeX with proper formatting (equations, tables, citations, figures). Handles three-line tables, equation environments, and bibliography integration.
---

# LaTeX-Transformer

Convert Markdown drafts to properly formatted LaTeX code for academic papers.

## When to Use

- Drafting paper content in Markdown for speed
- Converting model descriptions to LaTeX
- Formatting tables from data analysis
- Preparing content for MCM/ICM LaTeX template

## Core Transformations

### 1. Headers

```python
def convert_headers(markdown_text):
    """Convert Markdown headers to LaTeX sections"""
    
    import re
    
    # # Header → \section{}
    markdown_text = re.sub(r'^# (.+)$', r'\\section{\1}', 
                          markdown_text, flags=re.MULTILINE)
    
    # ## Header → \subsection{}
    markdown_text = re.sub(r'^## (.+)$', r'\\subsection{\1}', 
                          markdown_text, flags=re.MULTILINE)
    
    # ### Header → \subsubsection{}
    markdown_text = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', 
                          markdown_text, flags=re.MULTILINE)
    
    return markdown_text
```

### 2. Emphasis and Formatting

```python
def convert_formatting(markdown_text):
    """Convert bold, italic, code"""
    
    import re
    
    # **bold** → \textbf{}
    markdown_text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', markdown_text)
    
    # *italic* → \textit{}
    markdown_text = re.sub(r'\*(.+?)\*', r'\\textit{\1}', markdown_text)
    
    # `code` → \texttt{}
    markdown_text = re.sub(r'`(.+?)`', r'\\texttt{\1}', markdown_text)
    
    return markdown_text
```

### 3. Lists

```python
def convert_lists(markdown_text):
    """Convert bullet and numbered lists"""
    
    import re
    
    lines = markdown_text.split('\n')
    result = []
    in_itemize = False
    in_enumerate = False
    
    for line in lines:
        # Bullet list
        if re.match(r'^[-*+] ', line):
            if not in_itemize:
                result.append('\\begin{itemize}')
                in_itemize = True
            item = re.sub(r'^[-*+] ', '', line)
            result.append(f'  \\item {item}')
        
        # Numbered list
        elif re.match(r'^\d+\. ', line):
            if not in_enumerate:
                result.append('\\begin{enumerate}')
                in_enumerate = True
            item = re.sub(r'^\d+\. ', '', line)
            result.append(f'  \\item {item}')
        
        # End lists
        else:
            if in_itemize:
                result.append('\\end{itemize}')
                in_itemize = False
            if in_enumerate:
                result.append('\\end{enumerate}')
                in_enumerate = False
            result.append(line)
    
    # Close any open lists
    if in_itemize:
        result.append('\\end{itemize}')
    if in_enumerate:
        result.append('\\end{enumerate}')
    
    return '\n'.join(result)
```

### 4. Inline Math

```python
def convert_inline_math(markdown_text):
    """Convert $...$ to LaTeX math mode"""
    
    # Already in LaTeX format, just verify
    # $x$ stays as $x$
    # $$...$$ for display math stays as is
    
    # Optionally convert double dollar to equation environment
    import re
    
    # $$...$$ → \begin{equation}...\end{equation}
    def replace_display_math(match):
        content = match.group(1).strip()
        return f'\\begin{{equation}}\n{content}\n\\end{{equation}}'
    
    markdown_text = re.sub(r'\$\$(.+?)\$\$', replace_display_math, 
                          markdown_text, flags=re.DOTALL)
    
    return markdown_text
```

### 5. Tables (Three-Line Format)

```python
def convert_table_to_latex(markdown_table):
    """
    Convert Markdown table to LaTeX three-line table (booktabs)
    
    Markdown:
    | Header 1 | Header 2 | Header 3 |
    |----------|----------|----------|
    | Data 1   | Data 2   | Data 3   |
    | Data 4   | Data 5   | Data 6   |
    
    LaTeX:
    \\begin{table}[htbp]
    \\centering
    \\caption{Table Caption}
    \\begin{tabular}{lcc}
    \\toprule
    Header 1 & Header 2 & Header 3 \\\\
    \\midrule
    Data 1 & Data 2 & Data 3 \\\\
    Data 4 & Data 5 & Data 6 \\\\
    \\bottomrule
    \\end{tabular}
    \\end{table}
    """
    
    lines = markdown_table.strip().split('\n')
    
    if len(lines) < 3:
        return markdown_table  # Not a valid table
    
    # Parse header
    headers = [h.strip() for h in lines[0].split('|')[1:-1]]
    n_cols = len(headers)
    
    # Parse data rows (skip separator line)
    data_rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) == n_cols:
            data_rows.append(cells)
    
    # Determine column alignment (default: left for first, center for rest)
    col_spec = 'l' + 'c' * (n_cols - 1)
    
    # Build LaTeX
    latex = ['\\begin{table}[htbp]',
             '\\centering',
             '\\caption{Table Caption}',  # User should edit
             f'\\begin{{tabular}}{{{col_spec}}}',
             '\\toprule']
    
    # Headers
    latex.append(' & '.join(headers) + ' \\\\')
    latex.append('\\midrule')
    
    # Data
    for row in data_rows:
        latex.append(' & '.join(row) + ' \\\\')
    
    latex.append('\\bottomrule')
    latex.append('\\end{tabular}')
    latex.append('\\end{table}')
    
    return '\n'.join(latex)
```

### 6. Figures

```python
def convert_figure(markdown_image):
    """
    Convert Markdown image to LaTeX figure
    
    Markdown: ![Caption](path/to/image.png)
    
    LaTeX:
    \\begin{figure}[htbp]
    \\centering
    \\includegraphics[width=0.8\\textwidth]{path/to/image.png}
    \\caption{Caption}
    \\label{fig:label}
    \\end{figure}
    """
    
    import re
    
    def replace_image(match):
        caption = match.group(1)
        path = match.group(2)
        
        # Generate label from caption
        label = caption.lower().replace(' ', '_')
        label = re.sub(r'[^a-z0-9_]', '', label)
        
        latex = [
            '\\begin{figure}[htbp]',
            '\\centering',
            f'\\includegraphics[width=0.8\\textwidth]{{{path}}}',
            f'\\caption{{{caption}}}',
            f'\\label{{fig:{label}}}',
            '\\end{figure}'
        ]
        
        return '\n'.join(latex)
    
    markdown_image = re.sub(r'!\[(.+?)\]\((.+?)\)', replace_image, markdown_image)
    
    return markdown_image
```

### 7. Citations

```python
def convert_citations(markdown_text):
    """
    Convert [Author2023] to \cite{Author2023}
    """
    
    import re
    
    # [Author2023] → \cite{Author2023}
    markdown_text = re.sub(r'\[([A-Z][a-zA-Z0-9]+)\]', r'\\cite{\1}', markdown_text)
    
    return markdown_text
```

## Complete Transformer

```python
def markdown_to_latex(markdown_text):
    """
    Complete Markdown to LaTeX conversion
    
    Usage:
    with open('draft.md', 'r') as f:
        markdown = f.read()
    
    latex = markdown_to_latex(markdown)
    
    with open('output.tex', 'w') as f:
        f.write(latex)
    """
    
    # Apply transformations in order
    latex = markdown_text
    
    latex = convert_headers(latex)
    latex = convert_formatting(latex)
    latex = convert_inline_math(latex)
    latex = convert_lists(latex)
    
    # Tables (process separately to avoid conflicts)
    import re
    table_pattern = r'(\|.+\|\n)+(\|[-:| ]+\|\n)(\|.+\|\n)+'
    tables = re.findall(table_pattern, latex)
    for table in tables:
        table_text = ''.join(table)
        latex_table = convert_table_to_latex(table_text)
        latex = latex.replace(table_text, latex_table)
    
    latex = convert_figure(latex)
    latex = convert_citations(latex)
    
    return latex
```

## Pandas DataFrame to LaTeX Table

```python
def dataframe_to_latex_table(df, caption='Table Caption', label='tab:label'):
    """
    Convert pandas DataFrame to three-line LaTeX table
    
    Usage:
    import pandas as pd
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    latex = dataframe_to_latex_table(df, caption='My Results')
    """
    
    # Use pandas built-in with customization
    latex = df.to_latex(
        index=False,
        column_format='l' + 'c' * (len(df.columns) - 1),
        caption=caption,
        label=label,
        position='htbp',
        escape=False,  # Allow LaTeX commands in data
        float_format='%.3f'  # 3 decimal places for floats
    )
    
    # Replace default lines with booktabs
    latex = latex.replace('\\hline', '')
    latex = latex.replace('\\toprule', '\\toprule')  # Already correct
    latex = latex.replace('\\midrule', '\\midrule')
    latex = latex.replace('\\bottomrule', '\\bottomrule')
    
    return latex
```

## Equation Formatting

```python
def format_equation(equation_str, label=None, numbered=True):
    """
    Format equation with proper LaTeX environment
    
    Usage:
    eq = format_equation('E = mc^2', label='einstein', numbered=True)
    """
    
    if numbered:
        latex = [
            '\\begin{equation}',
            f'  {equation_str}'
        ]
        if label:
            latex.append(f'  \\label{{eq:{label}}}')
        latex.append('\\end{equation}')
    else:
        latex = [
            '\\begin{equation*}',
            f'  {equation_str}',
            '\\end{equation*}'
        ]
    
    return '\n'.join(latex)

def format_aligned_equations(equations_list):
    """
    Format multiple aligned equations
    
    Usage:
    eqs = format_aligned_equations([
        ('x + y', '= 5'),
        ('2x - y', '= 3')
    ])
    """
    
    latex = ['\\begin{align}']
    
    for lhs, rhs in equations_list:
        latex.append(f'  {lhs} &{rhs} \\\\')
    
    latex.append('\\end{align}')
    
    return '\n'.join(latex)
```

## Special Symbols Quick Reference

```python
LATEX_SYMBOLS = {
    # Greek letters
    'alpha': r'\alpha',
    'beta': r'\beta',
    'gamma': r'\gamma',
    'delta': r'\delta',
    'theta': r'\theta',
    'lambda': r'\lambda',
    'mu': r'\mu',
    'sigma': r'\sigma',
    
    # Operators
    'sum': r'\sum',
    'prod': r'\prod',
    'int': r'\int',
    'partial': r'\partial',
    'nabla': r'\nabla',
    
    # Relations
    'leq': r'\leq',
    'geq': r'\geq',
    'neq': r'\neq',
    'approx': r'\approx',
    'propto': r'\propto',
    
    # Arrows
    'rightarrow': r'\rightarrow',
    'Rightarrow': r'\Rightarrow',
    'leftarrow': r'\leftarrow',
    
    # Sets
    'in': r'\in',
    'subset': r'\subset',
    'cup': r'\cup',
    'cap': r'\cap',
    'emptyset': r'\emptyset',
    
    # Others
    'infty': r'\infty',
    'pm': r'\pm',
    'times': r'\times',
    'cdot': r'\cdot',
    'ldots': r'\ldots'
}

def get_symbol(name):
    """Quick lookup for LaTeX symbols"""
    return LATEX_SYMBOLS.get(name, f'\\{name}')
```

## Common Patterns

### Model Description Template

```latex
\subsection{Model Formulation}

We model the system using the following differential equation:

\begin{equation}
\frac{dP}{dt} = rP\left(1 - \frac{P}{K}\right) - hP
\label{eq:logistic}
\end{equation}

where:
\begin{itemize}
  \item $P(t)$ is the population at time $t$
  \item $r$ is the intrinsic growth rate
  \item $K$ is the carrying capacity
  \item $h$ is the harvest rate
\end{itemize}
```

### Results Table Template

```latex
\begin{table}[htbp]
\centering
\caption{Model Performance Comparison}
\label{tab:results}
\begin{tabular}{lccc}
\toprule
Model & RMSE & $R^2$ & Runtime (s) \\
\midrule
Linear Regression & 12.34 & 0.85 & 0.02 \\
Random Forest & 8.91 & 0.92 & 1.45 \\
Neural Network & 7.23 & 0.95 & 12.3 \\
\bottomrule
\end{tabular}
\end{table}
```

## Usage Example

```python
# Read Markdown draft
with open('doc/model_draft.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()

# Convert to LaTeX
latex_content = markdown_to_latex(markdown_content)

# Add document structure if needed
full_latex = f"""
\\documentclass{{article}}
\\usepackage{{amsmath}}
\\usepackage{{graphicx}}
\\usepackage{{booktabs}}

\\begin{{document}}

{latex_content}

\\end{{document}}
"""

# Save
with open('doc/model_section.tex', 'w', encoding='utf-8') as f:
    f.write(full_latex)

print("Converted to LaTeX: doc/model_section.tex")
```

## Output Location

Save converted LaTeX to `doc/`:
- `section_model.tex` - Model description
- `section_results.tex` - Results section
- `section_analysis.tex` - Analysis section

## Common Pitfalls

- **Escaped underscores**: Use `\_` in text, not math mode
- **Missing packages**: Ensure `amsmath`, `booktabs`, `graphicx` are loaded
- **Unescaped special chars**: `%`, `&`, `#`, `$` need escaping in text
- **Incorrect table alignment**: Check column specifications match data
- **Missing labels**: Always label figures, tables, equations for referencing
