---
name: latex-coauthoring
description: "MCM/ICM LaTeX Paper Co-Authoring Workflow with O-Award Writing Patterns. Use when the team needs to draft, edit, or polish sections of the competition solution paper in LaTeX. Specializes in: (1) Structuring the paper skeleton with mandatory sections (Problem Restatement, Assumptions with Justifications, Notation Table, Our Work roadmap), (2) Drafting mathematical models with proper equation formatting, (3) Polishing the critical Summary Sheet using proven high-scoring templates, (4) Implementing academic tone and LaTeX best practices, (5) Avoiding common pitfalls that lose points. Includes mcmthesis template configuration and references to high-scoring writing patterns from O-award papers. Assumes LaTeX/Overleaf workflow for MCM/ICM competitions."
---

# MCM/ICM LaTeX Co-Authoring Specialist

## Overview

You are the LaTeX Writing Expert for an MCM/ICM team. Your mission: help the team produce a **publication-quality solution paper** in LaTeX within 96 hours, with special emphasis on the **Summary Sheet** — the single most important page that determines whether judges read the full paper.

**Critical Understanding**: In MCM/ICM, the Summary Sheet is read first. If it fails to impress in 60 seconds, the paper is effectively disqualified from top prizes. The Summary Sheet must be polished **first** (outline) and **last** (final polish).

## Competition Context

**MCM/ICM Paper Requirements**:
- **Summary Sheet**: Exactly 1 page, standalone, non-technical language, includes title + keywords
- **Main Paper**: Up to 25 pages including figures, excluding appendices
- **Mandatory Sections**: 
  - Introduction (with Background, Literature Review, Problem Restatement, Our Work)
  - Notations and Assumptions (with Justifications for EVERY assumption)
  - Model Development (with Data Preparation subsection)
  - Results (with specific numerical findings)
  - Sensitivity Analysis (CRITICAL for O-award)
  - Conclusions
  - Strengths and Weaknesses
- **Document Class**: `mcmthesis` (standard MCM template)
- **Font**: Palatino (recommended), 12pt
- **Tooling**: LaTeX (Overleaf or local compiler), must generate PDF

**Time Allocation** (typical):
- Hours 0-24: Problem analysis, data exploration (minimal writing)
- Hours 24-36: Draft paper skeleton with "Our Work" roadmap
- Hours 36-60: Model building, coding (draft structure in parallel)
- Hours 60-84: Results generation, paper drafting (heavy writing)
- Hours 84-92: Summary Sheet polish (CRITICAL - this is where O-awards are won)
- Hours 92-96: Final proofreading, pitfall checking, submission

**Critical Success Factors** (from O-award analysis):
- Summary Sheet quality determines if judges read beyond page 1
- Specific model names (e.g., "ARIMA(2,1,3)") not generic "we built a model"
- Quantitative results with numbers (e.g., "15% improvement") not vague claims
- Sensitivity analysis is non-negotiable for high awards
- Every assumption must have justification
- "Our Work" roadmap + flow diagram shows professional organization

## Reference Documents (Progressive Disclosure)

This skill includes three specialized reference documents. Load them as needed:

### When to Read Each Reference

**1. `references/mcm-writing-patterns.md`** - High-Scoring Templates
- **When**: Drafting any section (Introduction, Results, Conclusion, etc.)
- **What**: Proven sentence structures, paragraph patterns, and templates from O-award papers
- **Use for**: "How should I structure the Introduction?" or "What's a good Results section format?"

**2. `references/mcmthesis-template.md`** - LaTeX Technical Reference  
- **When**: Setting up document or troubleshooting LaTeX issues
- **What**: Complete mcmthesis class configuration, package setup, formatting solutions
- **Use for**: "How do I configure mcmthesis?" or "How to fix figure placement issues?"

**3. `references/common-pitfalls.md`** - Error Prevention Guide
- **When**: Hour 0 (prevention), Hour 48 (mid-check), Hour 90 (final check)
- **What**: Critical mistakes that lose points, with fixes and checklists
- **Use for**: "What mistakes should I avoid?" or "Final submission checklist"

**Loading Strategy**:
- Don't load all references at once (context window efficiency)
- Load specific reference when user needs that type of help
- Example: User asks "How to write Introduction?" → Load `mcm-writing-patterns.md` Introduction section

---

## Core Workflow: Three-Stage Writing Process

### Stage 1: Structural Blueprint (Hours 24-36)

**Goal**: Define the paper skeleton before writing prose. This prevents scope creep and ensures logical flow.

#### Step 1.1: Problem Restatement
**Input**: User provides the original problem statement.
**Output**: A concise, clear restatement in 2-3 paragraphs.

**LaTeX Template**:
```latex
\section{Problem Restatement}

The problem requires us to [concise description of the core task]. Specifically, we must [list 2-3 key objectives]:

\begin{itemize}
    \item Objective 1: [description]
    \item Objective 2: [description]
    \item Objective 3: [description]
\end{itemize}

The solution must [key constraints or deliverables].
```

#### Step 1.2: Assumptions (MANDATORY Justifications)
**Goal**: List 3-7 core assumptions with detailed justifications.

**CRITICAL REQUIREMENT**: Every assumption MUST have a justification. This is a common pitfall that loses points.

**LaTeX Template**:
```latex
\subsection{Assumptions}

To simplify the problem while maintaining realism, we make the following assumptions:

\begin{enumerate}
    \item \textbf{Assumption 1}: [Clear, specific statement]
    
    \textit{Justification}: [Why this is reasonable - cite data, literature, or logic. 
    Be specific: "Historical data shows X" or "According to [Reference], Y"]
    
    \item \textbf{Assumption 2}: [Clear, specific statement]
    
    \textit{Justification}: [Detailed reasoning with evidence]
    
    % Continue for 3-7 assumptions
\end{enumerate}
```

**Good Justification Examples**:
```latex
\item \textbf{Data Accuracy}: We assume the provided dataset is free from 
systematic measurement errors.

\textit{Justification}: The data source is [authoritative organization] which 
follows ISO [standard] protocols. Random errors are addressed through our 
outlier detection procedure using the IQR method.

\item \textbf{Linear Wear Pattern}: We assume wear depth increases linearly 
with foot traffic below 500 visitors per day.

\textit{Justification}: Archard's wear law (1953) demonstrates linear wear 
for moderate loads. Our data visualization (Figure 2) confirms this relationship 
for traffic levels below the threshold.
```

**Assumptions to AVOID** (see `references/common-pitfalls.md` for full list):
- ❌ "We assume the data is accurate" (without justification)
- ❌ "We assume the problem is solvable"
- ❌ "We assume our model is correct"
- ❌ Circular reasoning: "We assume X exists because we need to find X"

**Best Practices**:
- Every justification should cite data, literature, or logical reasoning
- Quantify when possible (e.g., "temperature varies by <5°C")
- Acknowledge impact if assumption is violated
- 3-7 assumptions is typical; more than 10 suggests over-simplification

#### Step 1.3: Notation Table (Include Units)
**Goal**: Create a comprehensive symbols table for ALL variables used in the paper.

**CRITICAL**: Include units column. Omitting units is a common pitfall.

**LaTeX Template (Three-Column Format - Recommended)**:
```latex
\subsection{Notations}

\begin{table}[htbp]
    \centering
    \caption{Notation and Symbols}
    \label{tab:notation}
    \begin{threeparttable}
    \begin{tabular}{cll}
        \toprule
        \textbf{Symbol} & \textbf{Definition} & \textbf{Unit} \\
        \midrule
        $N$ & Total population size & persons \\
        $S(t)$ & Susceptible individuals at time $t$ & persons \\
        $I(t)$ & Infected individuals at time $t$ & persons \\
        $R(t)$ & Recovered individuals at time $t$ & persons \\
        $\beta$ & Transmission rate & day$^{-1}$ \\
        $\gamma$ & Recovery rate & day$^{-1}$ \\
        $R_0$ & Basic reproduction number & dimensionless \\
        \bottomrule
    \end{tabular}
    \begin{tablenotes}
        \footnotesize
        \item Note: ${\ast}$ denotes significance at the 5\% level.
    \end{tablenotes}
    \end{threeparttable}
\end{table}
```

**Alternative: Grouped Format (for many variables)**:
```latex
\begin{table}[htbp]
    \centering
    \caption{Notation and Symbols}
    \begin{tabular}{cl}
        \toprule
        \textbf{Symbol} & \textbf{Definition} \\
        \midrule
        \multicolumn{2}{l}{\textit{Model Parameters}} \\
        $\alpha$ & Material wear coefficient (m$^3$/Nm) \\
        $H$ & Material hardness (GPa) \\
        \midrule
        \multicolumn{2}{l}{\textit{State Variables}} \\
        $h(x,y,t)$ & Wear depth at position $(x,y)$ and time $t$ (mm) \\
        $N(t)$ & Cumulative foot traffic (persons) \\
        \midrule
        \multicolumn{2}{l}{\textit{Derived Quantities}} \\
        $\mu_h$ & Mean wear depth (mm) \\
        \bottomrule
    \end{tabular}
\end{table}
```

**Required Packages**:
```latex
\usepackage{booktabs}        % For professional tables
\usepackage{threeparttable}  % For table notes
\usepackage{float}           % For [H] placement (if needed)
```

**Best Practices**:
- List ALL symbols used in equations (check every equation in paper)
- Include units for dimensional quantities
- Use "dimensionless" for ratios and normalized quantities
- Group related symbols if table is long (>15 entries)
- Place table early (Section 2.1) before equations appear

#### Step 1.4: "Our Work" Roadmap (HIGH-SCORING PATTERN)
**Goal**: Provide judges with a clear roadmap of your entire approach.

**CRITICAL**: O-award papers almost always include an "Our Work" subsection with flow diagram. This is a key differentiator.

**LaTeX Template**:
```latex
\subsection{Our Work}

To address these challenges, we develop a comprehensive framework structured as follows:

\begin{enumerate}
    \item \textbf{Data Preparation}: We clean the raw data by handling missing 
          values using [method] and removing outliers beyond [threshold]. We then 
          visualize correlations and distributions to identify key patterns.
    
    \item \textbf{Model 1 - [Specific Name]}: We establish a [model type, e.g., 
          ARIMA(2,1,3)] model to [specific purpose]. This captures [aspect] of 
          the problem.
    
    \item \textbf{Model 2 - [Specific Name]}: We construct a [model type] to 
          [specific purpose]. This addresses [aspect] that Model 1 does not capture.
    
    \item \textbf{Model Integration}: We combine Models 1 and 2 through [method] 
          to optimize [objective function].
    
    \item \textbf{Sensitivity Analysis}: We test the model's robustness by varying 
          key parameters by ±[X]\% and analyzing the impact on outputs.
    
    \item \textbf{Application}: We demonstrate the model's effectiveness on 
          [case study/dataset].
\end{enumerate}

Figure \ref{fig:flowchart} illustrates the overall workflow and connections 
between model components.

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\textwidth]{figures/flowchart.png}
    \caption{Overall workflow showing data flow and model integration. 
    The framework consists of [brief description of main stages].}
    \label{fig:flowchart}
\end{figure}
```

**Why This Matters**:
- Judges read 100+ papers; clear roadmap helps them follow your logic
- Shows professional organization and planning
- References this roadmap throughout paper: "As outlined in Section 1.4..."
- Flow diagram provides visual summary of complex approach

**Flow Diagram Best Practices**:
- Use boxes for processes, arrows for data flow
- Include all major steps from data input to final output
- Show feedback loops if models are iterative
- Keep it simple; details come in later sections

#### Step 1.5: Model Sections Outline
**Goal**: Define 2-3 distinct models or major components with clear purposes.

**LaTeX Template**:
```latex
\section{Model Development}

\subsection{Data Preparation}
\subsubsection{Data Cleaning}
[Describe missing value handling, outlier detection, data quality checks]

\subsubsection{Data Visualization}
[Show correlation analysis, distribution plots, key patterns discovered]

\subsection{Model 1: [Specific Name, e.g., ARIMA(2,1,3) Forecasting Model]}
\textit{Purpose}: [Specific purpose, e.g., "Predict daily foot traffic based on 
historical patterns"]

\subsubsection{Model Formulation}
[Mathematical equations with clear variable definitions]

\subsubsection{Parameter Estimation}
[Method used: least squares, maximum likelihood, etc.]

\subsubsection{Model Validation}
[How you verified the model works: RMSE, R², cross-validation]

\subsection{Model 2: [Specific Name, e.g., Archard Wear Model]}
\textit{Purpose}: [Specific purpose]

[Similar structure as Model 1]

\subsection{Model Integration}
\textit{How models connect}: [Detailed description of how Model 1 output feeds 
into Model 2, or how they jointly optimize objective]
```

**Key Improvements from Generic Approach**:
- ✅ Specific model names (not just "Model 1")
- ✅ Data Preparation subsection (shows professionalism)
- ✅ Clear purpose statement for each model
- ✅ Validation subsection (proves model works)

---

### Stage 2: Section Drafting (Hours 60-80)

**Goal**: Convert raw math and logic into polished LaTeX sections.

#### Step 2.1: Equation Formatting

**Single Equations** (numbered, for reference):
```latex
The SIR model is governed by:
\begin{equation}
    \frac{dS}{dt} = -\beta S I
    \label{eq:sir_s}
\end{equation}

From Equation \eqref{eq:sir_s}, we observe that...
```

**Multi-line Equations** (aligned):
```latex
\begin{align}
    \frac{dS}{dt} &= -\beta S I \label{eq:sir_s} \\
    \frac{dI}{dt} &= \beta S I - \gamma I \label{eq:sir_i} \\
    \frac{dR}{dt} &= \gamma I \label{eq:sir_r}
\end{align}
```

**Inline Math** (for text flow):
```latex
The basic reproduction number $R_0 = \beta / \gamma$ determines epidemic spread.
```

**Piecewise Functions**:
```latex
\begin{equation}
    f(x) = 
    \begin{cases}
        0 & \text{if } x < 0 \\
        x^2 & \text{if } 0 \leq x < 1 \\
        1 & \text{if } x \geq 1
    \end{cases}
\end{equation}
```

#### Step 2.2: Algorithm Descriptions

**Use `algorithm2e` package**:
```latex
\usepackage[ruled,vlined]{algorithm2e}

\begin{algorithm}[H]
\caption{Genetic Algorithm for Optimization}
\KwIn{Population size $N$, generations $G$, mutation rate $p_m$}
\KwOut{Optimal solution $x^*$}

Initialize population $P_0$ randomly\;
\For{$g = 1$ \KwTo $G$}{
    Evaluate fitness for each individual in $P_g$\;
    Select parents using tournament selection\;
    Apply crossover and mutation\;
    Create new generation $P_{g+1}$\;
}
\Return best individual from $P_G$\;
\end{algorithm}
```

#### Step 2.3: Figure Integration

**Best Practices**:
- Save figures as `.png` (300 DPI) or `.pdf` (vector graphics)
- Use descriptive filenames: `sir_model_results.png`
- Always include captions that explain what the figure shows

**LaTeX Template**:
```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/sir_model_results.png}
    \caption{SIR Model Predictions: The model accurately captures the epidemic peak at day 45, with a maximum of 3,200 infected individuals. The shaded region represents 95\% confidence intervals from Monte Carlo simulations.}
    \label{fig:sir_results}
\end{figure}

As shown in Figure \ref{fig:sir_results}, the epidemic peaks around day 45.
```

#### Step 2.4: Academic Tone Guidelines

**Passive Voice** (preferred in formal writing):
- ✅ "The model was validated using historical data."
- ❌ "We validated the model using historical data."

**Objective Language**:
- ✅ "The results indicate a strong correlation ($r = 0.92$)."
- ❌ "Our amazing results show a super strong correlation."

**Precise Quantification**:
- ✅ "The algorithm converged in 47 iterations with a tolerance of $10^{-6}$."
- ❌ "The algorithm converged pretty quickly."

**Logical Connectors**:
- Use: "Furthermore", "Consequently", "In contrast", "Specifically"
- Avoid: "Also", "But", "So", "Basically"

---

### Stage 3: The Summary Sheet (Hours 84-92)

**Critical Phase**: This is the **last** thing written but the **first** thing read by judges. O-awards are won or lost here.

#### Step 3.1: Summary Sheet Structure (HIGH-SCORING TEMPLATES)

**Format**: Exactly one page using `mcmthesis` abstract environment.

**CRITICAL RULES**:
- Must be exactly 1 page (test print to verify)
- Non-technical language (write for non-experts)
- Include specific model names (not "we built a model")
- Include quantitative results with numbers
- Include 3-6 keywords at end

**Template 1: Problem-Driven Structure** (Most Common):
```latex
\begin{abstract}
% Title is auto-generated by mcmthesis from \title{}

% Opening (Background) - 2-3 sentences
With the development of [field], the [problem] has become a critical challenge 
in [domain]. [Context sentence]. This paper addresses the problem of [specific task].

% Body (By Question) - One paragraph per sub-problem
For question 1, we establish a [SPECIFIC model name, e.g., ARIMA(2,1,3)] model 
to analyze [specific aspect]. The model reveals that [specific quantitative finding]. 
Specifically, we find that [key result with numbers].

For question 2, we utilize a [SPECIFIC method, e.g., Genetic Algorithm with elitism] 
combined with [technique]. Our analysis shows that [quantitative result], which 
represents a [X]% improvement over [baseline].

For question 3, we construct a [SPECIFIC model type] to optimize [objective]. 
The results demonstrate that [specific outcome with numbers]. Sensitivity analysis 
confirms robustness under ±[X]% parameter variations.

% Conclusion - 1-2 sentences
Finally, our comprehensive framework provides [main contribution]. The model 
achieves [performance metric] and offers practical guidance for [application].

\begin{keywords}
keyword1; keyword2; keyword3; keyword4; keyword5
\end{keywords}
\end{abstract}
```

**Template 2: Model-Centric Structure** (For Complex Multi-Model Papers):
```latex
\begin{abstract}
% Opening (Problem Statement) - 2 sentences
This paper addresses the challenge of [problem]. The core objectives are 
[list 2-3 key goals].

% Model Overview - 3-4 sentences with specific names
We develop a multi-stage modeling framework consisting of: (1) A [Model 1 
SPECIFIC NAME, e.g., SIR differential equation model] for [purpose], (2) A 
[Model 2 SPECIFIC NAME, e.g., K-means clustering algorithm] for [purpose], 
and (3) An integrated [Model 3 SPECIFIC NAME] for [purpose]. The models are 
calibrated using [data source] and validated through [method].

% Key Results - Specific numbers
Our key findings include: [Result 1 with specific percentage/numbers], 
[Result 2 with quantitative comparison], and [Result 3 with performance metric]. 
Compared to [baseline], our approach achieves [X]% improvement in [metric].

% Validation & Conclusion - 2 sentences
Sensitivity analysis confirms the model's robustness under ±[X]% parameter 
variations. The proposed framework provides [practical value] and can be 
extended to [applications].

\begin{keywords}
keyword1; keyword2; keyword3; keyword4; keyword5
\end{keywords}
\end{abstract}
```

**Key Differences from Generic Approach**:
- ✅ Uses `mcmthesis` abstract environment (not separate document)
- ✅ Specific model names (e.g., "ARIMA(2,1,3)" not "time series model")
- ✅ Quantitative results with numbers (e.g., "23% improvement")
- ✅ Keywords included (required by mcmthesis)
- ✅ Structured by question (matches problem format)

#### Step 3.2: Judge Perspective Review

**Critical Questions** (ask these before finalizing):
1. **Can a non-technical judge understand the first paragraph?**
   - If no: Simplify language, remove jargon.
2. **Are the numeric results prominent and specific?**
   - If no: Add percentages, concrete numbers, comparisons.
3. **Does it fit on one page with readable font (12pt)?**
   - If no: Cut unnecessary details, tighten prose.
4. **Does it convey confidence without arrogance?**
   - If no: Use phrases like "Our analysis suggests" instead of "We definitively prove".

#### Step 3.3: Final Polish Checklist

- [ ] No typos or grammatical errors
- [ ] No undefined acronyms (spell out on first use)
- [ ] No references to "Section 3.2" or "Figure 4" (Summary Sheet is standalone)
- [ ] Results are quantified with units
- [ ] Limitations are acknowledged (shows maturity)
- [ ] Printed version looks professional (test print to PDF)

---

## LaTeX Best Practices for MCM/ICM

### Document Class and Packages

**MCM Standard: mcmthesis Document Class**

**Recommended Preamble** (see `references/mcmthesis-template.md` for complete setup):
```latex
\documentclass{mcmthesis}
\mcmsetup{
    CTeX = false,              % Set to false for English papers
    tcn = 1234567,             % YOUR Team Control Number
    problem = A,               % YOUR Problem Letter (A/B/C/D/E/F)
    sheet = true,              % Generate summary sheet
    titleinsheet = true,       % Include title in summary
    keywordsinsheet = true,    % Include keywords in summary
    titlepage = false,         % No separate title page
    abstract = true            % Include abstract environment
}

% Essential packages
\usepackage{palatino}          % Professional font (recommended)
\usepackage{amsmath, amssymb, amsthm}
\usepackage{graphicx}
\usepackage{subfig}            % For subfigures (use \subfloat)
\usepackage{float}
\usepackage{booktabs}          % Professional tables
\usepackage{threeparttable}    % Tables with footnotes
\usepackage{siunitx}           % Numerical alignment
\usepackage{algorithm}
\usepackage{algpseudocode}
\usepackage{indentfirst}       % Indent first paragraph
\usepackage{mdframed}          % For AI report boxes
\usepackage{hyperref}
\usepackage{cite}

% Paragraph formatting
\setlength{\parindent}{2em}

% Optional: Superscript citations
\makeatletter
\renewcommand\@cite[1]{\textsuperscript{[#1]}}
\makeatother

% Siunitx configuration for tables
\sisetup{
    table-number-alignment = center,
    round-mode = places,
    round-precision = 2
}

\title{Your Paper's Title}
```

**Alternative: Standard Article Class** (if mcmthesis not available):
```latex
\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath, amssymb, amsthm}
\usepackage{graphicx}
\usepackage{float}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{cite}
\usepackage[ruled,vlined]{algorithm2e}

\title{Solution to MCM Problem [X]: [Title]}
\author{Team \# [Your Team Number]}
\date{\today}
```

**CRITICAL**: Always verify Team Control Number (tcn) and Problem Letter are correct before final submission. Wrong TCN/Problem = potential disqualification.

### Float Placement

**Problem**: Figures/tables float to unexpected locations.
**Solution**: Use `[H]` (requires `\usepackage{float}`):
```latex
\begin{figure}[H]  % Forces "Here" placement
    \centering
    \includegraphics[width=0.7\textwidth]{figure.png}
    \caption{Caption text}
\end{figure}
```

### Citations

**Use BibTeX** for automatic formatting:
```latex
% In main.tex
\bibliographystyle{plain}
\bibliography{references}

% In references.bib
@article{smith2020,
    author = {Smith, John},
    title = {A Study on Epidemic Models},
    journal = {Journal of Mathematical Biology},
    year = {2020},
    volume = {45},
    pages = {123--145}
}

% In text
According to Smith \cite{smith2020}, the SIR model is effective for...
```

### Common LaTeX Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Undefined control sequence` | Typo in command name | Check spelling: `\frac{}{}` not `\frac{}` |
| `Missing $ inserted` | Math mode outside `$...$` | Wrap math: `$x^2$` not `x^2` |
| `Float too large` | Figure exceeds page height | Reduce `width=` parameter |
| `Citation undefined` | BibTeX not run | Compile sequence: `pdflatex → bibtex → pdflatex × 2` |

---

## Workflow Integration

### When to Use This Skill

**Trigger Phrases**:
- "Draft the Introduction section"
- "Format these equations in LaTeX"
- "Polish the Summary Sheet"
- "Create a notation table"
- "Convert this algorithm to LaTeX pseudocode"

### Handoff to Other Skills

- **After latex-coauthoring**: Use `visual-engineer` to create high-quality figures for `\includegraphics`
- **Before latex-coauthoring**: Use `xlsx` to generate data tables, `topsis-scorer` to get ranking results
- **Parallel with latex-coauthoring**: Use `pdf` to extract equations from literature for citation

---

## Time-Saving Tips for Competition

### Quick Drafting (Hours 60-72)
**Goal**: Get ideas on paper fast, polish later.

**Strategy**:
- Use `\section{}` and `\subsection{}` liberally to organize
- Write equations first, prose second
- Leave `[TODO: explain X]` markers for later
- Don't worry about perfect wording yet

### Rapid Equation Entry
**Use LaTeX shortcuts**:
- `\newcommand{\dd}[2]{\frac{d#1}{d#2}}` → `\dd{S}{t}` instead of `\frac{dS}{dt}`
- `\newcommand{\R}{\mathbb{R}}` → `\R^n` instead of `\mathbb{R}^n`

### Collaborative Editing (Overleaf)
**Best Practices**:
- **Assign sections**: Person A writes Model 1, Person B writes Model 2
- **Use comments**: `% TODO: Add sensitivity analysis here`
- **Track history**: Overleaf auto-saves, use "History" to revert mistakes
- **Avoid merge conflicts**: Don't edit the same paragraph simultaneously

---

## Output Standards

### File Organization
```
project/
├── main.tex              # Main paper
├── summary_sheet.tex     # Separate Summary Sheet file
├── references.bib        # BibTeX bibliography
├── figures/
│   ├── model_diagram.png
│   ├── results_plot.png
│   └── sensitivity_analysis.png
└── compiled/
    ├── main.pdf
    └── summary_sheet.pdf
```

### Quality Checklist (Before Submission)

**Content**:
- [ ] Problem Restatement is clear and concise
- [ ] All assumptions are justified
- [ ] All variables are defined in Notation table
- [ ] Equations are numbered and referenced in text
- [ ] Figures have descriptive captions
- [ ] Results are quantified with units and uncertainties
- [ ] Sensitivity analysis is included
- [ ] Summary Sheet is polished and standalone

**Formatting**:
- [ ] 12pt font, 1-inch margins
- [ ] All figures are high-resolution (300 DPI)
- [ ] Tables use `booktabs` style (professional)
- [ ] No overfull hbox warnings (text overflowing margins)
- [ ] Page count ≤ 25 pages (excluding appendices)

**LaTeX Compilation**:
- [ ] Compiles without errors
- [ ] All references resolved (no `[?]` in PDF)
- [ ] Hyperlinks work (if using `hyperref`)

---

## Advanced Techniques

### Multi-Column Layouts (for Summary Sheet)
```latex
\usepackage{multicol}

\begin{multicols}{2}
[Content flows across two columns automatically]
\end{multicols}
```

### Custom Theorem Environments
```latex
\usepackage{amsthm}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}

\begin{theorem}
If $R_0 < 1$, the disease-free equilibrium is stable.
\end{theorem}
```

### Subfigures (Multiple Plots Side-by-Side)
```latex
\usepackage{subcaption}

\begin{figure}[H]
    \centering
    \begin{subfigure}{0.45\textwidth}
        \includegraphics[width=\textwidth]{plot1.png}
        \caption{Scenario A}
    \end{subfigure}
    \hfill
    \begin{subfigure}{0.45\textwidth}
        \includegraphics[width=\textwidth]{plot2.png}
        \caption{Scenario B}
    \end{subfigure}
    \caption{Comparison of two scenarios}
\end{figure}
```

---

## Common MCM/ICM Writing Pitfalls

### Pitfall 1: Over-Technical Summary Sheet
**Problem**: Using jargon like "We employ a multi-objective NSGA-II algorithm with Pareto-optimal frontiers..."
**Fix**: Simplify to "We use an optimization method to balance competing goals..."

### Pitfall 2: Undefined Variables
**Problem**: Using $\beta$ in equations without defining it first.
**Fix**: Always define variables before or immediately after first use.

### Pitfall 3: Results Without Context
**Problem**: "The optimal value is 42."
**Fix**: "The optimal facility location reduces total transportation costs by 42% compared to the baseline."

### Pitfall 4: No Sensitivity Analysis
**Problem**: Presenting results as absolute truth without testing robustness.
**Fix**: Always include a "Sensitivity Analysis" section testing key parameter variations.

---

## Final Reminder: The Summary Sheet is King

**Competition Reality**:
- Judges read 100+ papers in a short time
- If the Summary Sheet doesn't grab attention in 60 seconds, the paper is skipped
- Even a brilliant 25-page paper is worthless if the Summary Sheet fails

**Strategy**:
1. **Hour 24-36**: Draft a rough Summary Sheet outline (forces clarity of thought)
2. **Hour 60-84**: Focus on main paper (Summary Sheet outline guides writing)
3. **Hour 84-92**: Polish Summary Sheet obsessively (this is where medals are won)
4. **Hour 92-96**: Final proofread, test print, submit

**The Golden Rule**: If you only have time to polish one thing, polish the Summary Sheet.

---

## High-Scoring Strategies (O-Award Differentiators)

### What O-Award Papers Do Differently

Based on analysis of O-award winning papers, these patterns consistently appear:

**1. Specific Model Names**
- ❌ "We use a time series model"
- ✅ "We use an ARIMA(2,1,3) model"

**2. Quantitative Results**
- ❌ "The model performs well"
- ✅ "The model achieves 94.3% accuracy (RMSE = 0.023)"

**3. Professional Organization**
- ✅ "Our Work" roadmap with flow diagram
- ✅ Data Preparation subsection showing cleaning steps
- ✅ Every assumption has detailed justification

**4. Comprehensive Validation**
- ✅ Sensitivity analysis section (non-negotiable)
- ✅ Robustness checks under different scenarios
- ✅ Comparison to baseline or alternative approaches

**5. Honest Evaluation**
- ✅ Strengths and Weaknesses section with specific examples
- ✅ Limitations acknowledged with suggested improvements
- ✅ Clear scope of applicability stated

**6. Attention to Detail**
- ✅ Every figure has caption and is referenced in text
- ✅ All variables defined in notation table with units
- ✅ No LaTeX compilation warnings
- ✅ Consistent notation throughout paper

**For complete writing patterns and templates**, see `references/mcm-writing-patterns.md`.

**For error prevention**, see `references/common-pitfalls.md`.

**For LaTeX technical details**, see `references/mcmthesis-template.md`.

---

## Quick Reference: When to Load References

| User Need | Load This Reference |
|-----------|---------------------|
| "How do I structure the Introduction?" | `mcm-writing-patterns.md` (Introduction section) |
| "What's a good Summary Sheet template?" | `mcm-writing-patterns.md` (Summary Sheet section) |
| "How to write Assumptions with justifications?" | `mcm-writing-patterns.md` (Assumptions section) |
| "How do I set up mcmthesis?" | `mcmthesis-template.md` (Document Class Setup) |
| "Figure placement issues in LaTeX" | `mcmthesis-template.md` (Common Issues section) |
| "What mistakes should I avoid?" | `common-pitfalls.md` (relevant error category) |
| "Final submission checklist" | `common-pitfalls.md` (Final Checklist section) |

---

## Final Reminder: The Summary Sheet is King
