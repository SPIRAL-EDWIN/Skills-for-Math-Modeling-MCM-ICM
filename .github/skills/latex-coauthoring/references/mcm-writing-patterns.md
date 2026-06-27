# MCM/ICM High-Scoring Writing Patterns (高分写作套路)

## Purpose
This reference provides proven writing patterns, templates, and strategies from O-award winning MCM/ICM papers. Use this when drafting specific sections to ensure your writing follows high-scoring conventions.

---

## Summary Sheet Templates

### Template 1: Problem-Driven Structure
```
[Title: Specific and Professional]
Example: "Crack the Wordle Puzzle: Word Attribute Analysis Approaches"

[Opening Paragraph - Background]
With the development of [field], the [problem] has become a hot topic in [domain]. 
[2-3 sentences describing the problem context and importance]

[Body Paragraphs - By Question]
For question 1, we establish a [specific model name, e.g., ARIMA(2,1,3)] model to analyze [specific aspect]. 
The model reveals that [specific finding with numbers].

For question 2, we utilize a [specific method] approach combined with [technique]. 
Our analysis shows that [quantitative result], which indicates [interpretation].

For question 3, we construct a [model type] to optimize [objective]. 
The results demonstrate that [specific outcome with percentage/numbers].

[Conclusion Paragraph]
Finally, our comprehensive analysis provides [main contribution]. 
The model achieves [performance metric] and offers [practical implication].

[Keywords]
keyword1; keyword2; keyword3; keyword4; keyword5
```

### Template 2: Model-Centric Structure
```
[Title]

[Problem Statement - 2 sentences]
This paper addresses the challenge of [problem]. 
The core objectives are [list 2-3 key goals].

[Model Overview - 3-4 sentences]
We develop a multi-stage modeling framework consisting of:
(1) A [Model 1 name] for [purpose]
(2) A [Model 2 name] for [purpose]  
(3) An integrated [Model 3 name] for [purpose]

[Key Results - Bullet format]
Our key findings include:
• [Result 1 with specific numbers]
• [Result 2 with quantitative comparison]
• [Result 3 with percentage improvement]

[Validation & Conclusion - 2-3 sentences]
Sensitivity analysis confirms the model's robustness under ±[X]% parameter variations.
The proposed framework provides [practical value] and can be extended to [applications].

[Keywords]
```

---

## Introduction Section Patterns

### Pattern 1: Background → Literature → Our Work

**Background (2-3 paragraphs)**:
```
[Context Setting]
In recent years, [phenomenon] has attracted significant attention due to [reason]. 
[2-3 sentences providing context]

[Problem Significance]
Understanding [problem] is crucial for [application/impact]. 
However, existing approaches face challenges such as [challenge 1], [challenge 2], and [challenge 3].

[Research Gap]
While previous studies have explored [existing work], they have not adequately addressed [gap]. 
This motivates our investigation into [specific focus].
```

**Literature Review (1-2 paragraphs)**:
```
[Existing Approaches]
Several methodologies have been proposed to tackle this problem. 
[Author 1] developed [method] which [contribution]. 
[Author 2] proposed [approach] demonstrating [result]. 
However, these methods [limitation].

[Theoretical Foundation]
Our work builds upon [theory/framework] which provides [foundation]. 
We extend this by incorporating [innovation].
```

**Our Work (1 paragraph + flow diagram)**:
```
[Roadmap Statement]
To address these challenges, this paper presents a comprehensive framework structured as follows:

[Enumerated Structure]
1. Data Preparation: We clean and visualize the raw data to identify patterns
2. Model Construction: We establish [Model 1] and [Model 2] to capture [aspects]
3. Model Integration: We combine the models to optimize [objective]
4. Validation: We conduct sensitivity analysis and robustness checks
5. Application: We demonstrate the model's effectiveness on [case study]

[Flow Diagram Reference]
Figure 1 illustrates the overall logic and connections between model components.
```

### Pattern 2: Problem-Driven Introduction

**Problem Restatement**:
```
[Formal Restatement]
The problem requires us to [restate in formal language]. 
Specifically, we must address the following sub-problems:

[Enumerated Sub-problems]
1. [Sub-problem 1]: [Detailed description]
2. [Sub-problem 2]: [Detailed description]  
3. [Sub-problem 3]: [Detailed description]

[Constraints and Deliverables]
The solution must satisfy [constraints] and produce [deliverables].
```

---

## Assumptions Section Patterns

### Standard Format (MANDATORY)
```latex
\subsection{Assumptions}

We make the following assumptions to simplify the problem while maintaining realism:

\begin{enumerate}
    \item \textbf{Assumption 1}: [Clear statement]
    
    \textit{Justification}: [Why this is reasonable - cite data, literature, or logic]
    
    \item \textbf{Assumption 2}: [Clear statement]
    
    \textit{Justification}: [Specific reasoning with evidence]
    
    % Continue for 3-7 assumptions
\end{enumerate}
```

### Good Assumption Examples

**Example 1 - Data Quality**:
```
\textbf{Data Accuracy}: We assume the provided dataset is free from systematic measurement errors.

\textit{Justification}: The data source is [authoritative organization] which follows 
ISO [standard] protocols. Random errors are addressed through our outlier detection procedure.
```

**Example 2 - System Behavior**:
```
\textbf{Linear Wear Pattern}: We assume wear depth increases linearly with foot traffic 
below a threshold of [value] visitors per day.

\textit{Justification}: Archard's wear law (1953) demonstrates linear wear for 
moderate loads. Our data visualization (Figure 2) confirms this relationship for 
traffic levels below [threshold].
```

**Example 3 - Temporal Stability**:
```
\textbf{Stationary Environment}: We assume environmental factors (temperature, humidity) 
remain approximately constant over the study period.

\textit{Justification}: Historical weather data shows temperature variations < 5°C 
during the analysis period (May-August), which has negligible impact on material 
properties according to [Reference].
```

### Assumptions to AVOID

❌ **Trivial Assumptions**:
- "We assume the data is accurate" (without justification)
- "We assume the problem is solvable"
- "We assume our model is correct"

❌ **Circular Assumptions**:
- "We assume the optimal solution exists because we need to find it"

❌ **Unjustified Simplifications**:
- "We assume all factors are independent" (without checking correlations)

---

## Notation Table Patterns

### Format 1: Three-Column (Symbol, Definition, Unit)
```latex
\subsection{Notations}

\begin{table}[htbp]
    \centering
    \caption{Notation and Symbols}
    \label{tab:notation}
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
\end{table}
```

### Format 2: Two-Column with Grouped Categories
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
        $\lambda$ & Weathering rate constant (year$^{-1}$) \\
        \midrule
        \multicolumn{2}{l}{\textit{State Variables}} \\
        $h(x,y,t)$ & Wear depth at position $(x,y)$ and time $t$ (mm) \\
        $N(t)$ & Cumulative foot traffic (persons) \\
        \midrule
        \multicolumn{2}{l}{\textit{Derived Quantities}} \\
        $\mu_h$ & Mean wear depth (mm) \\
        $\sigma_h$ & Standard deviation of wear depth (mm) \\
        \bottomrule
    \end{tabular}
\end{table}
```

---

## Model Development Patterns

### Pattern 1: Multi-Stage Model Structure

**Section Organization**:
```latex
\section{Model Development}

\subsection{Data Preparation}
\subsubsection{Data Cleaning}
[Describe missing value handling, outlier detection]

\subsubsection{Data Visualization}
[Show correlation analysis, distribution plots]
[Reference: Figure X shows the correlation matrix...]

\subsection{Model 1: [Descriptive Name]}
\subsubsection{Model Formulation}
[Mathematical equations with clear variable definitions]

\subsubsection{Parameter Estimation}
[Method used to estimate parameters from data]

\subsubsection{Model Validation}
[How you verified the model works]

\subsection{Model 2: [Descriptive Name]}
[Similar structure as Model 1]

\subsection{Model Integration}
[How models connect and feed into each other]
```

### Pattern 2: Problem-Driven Model Structure

**For Each Sub-Problem**:
```latex
\section{Solution to Problem [Number]}

\subsection{Problem Analysis}
[Break down what the problem is really asking]

\subsection{Modeling Approach}
[Why you chose this particular model]

\subsection{Mathematical Formulation}
[Equations with detailed explanations]

\subsection{Solution Method}
[Algorithm or analytical solution]

\subsection{Results and Interpretation}
[Specific findings with numbers]
```

---

## Results Section Patterns

### Pattern 1: Visual + Quantitative

**Structure**:
```
[Subsection for each key finding]

\subsection{Finding 1: [Descriptive Title]}

[Introduce the result]
Our analysis reveals that [main finding]. Figure [X] illustrates [what the figure shows].

[Present the figure]
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/result1.png}
    \caption{[Detailed caption explaining what the reader should see. 
    The plot shows [description]. Key observations include [highlight important features].]}
    \label{fig:result1}
\end{figure}

[Quantitative details]
Specifically, we observe:
\begin{itemize}
    \item [Metric 1]: [Value] ([Comparison to baseline/threshold])
    \item [Metric 2]: [Value] ([Statistical significance if applicable])
    \item [Metric 3]: [Value] ([Interpretation])
\end{itemize}

[Interpretation]
This finding suggests that [interpretation]. The [percentage/magnitude] improvement 
demonstrates [significance]. Compared to [baseline/alternative], our approach 
achieves [quantitative advantage].
```

### Pattern 2: Comparative Results

**Structure**:
```
\subsection{Comparative Analysis}

To evaluate our model's performance, we compare it against [baseline/alternatives].
Table [X] summarizes the key metrics.

\begin{table}[htbp]
    \centering
    \caption{Performance Comparison}
    \begin{tabular}{lccc}
        \toprule
        \textbf{Method} & \textbf{Metric 1} & \textbf{Metric 2} & \textbf{Metric 3} \\
        \midrule
        Baseline & [value] & [value] & [value] \\
        Method A & [value] & [value] & [value] \\
        Our Model & \textbf{[value]} & \textbf{[value]} & \textbf{[value]} \\
        \bottomrule
    \end{tabular}
\end{table}

Our model outperforms the baseline by [X]% in [metric], demonstrating [advantage].
While Method A achieves comparable results in [aspect], our approach provides 
superior [other aspect], making it more suitable for [application].
```

---

## Sensitivity Analysis Patterns

### Pattern 1: Parameter Perturbation

**Structure**:
```latex
\section{Sensitivity Analysis}

\subsection{Methodology}
To assess the robustness of our model, we perform sensitivity analysis by 
perturbing key parameters within realistic ranges. Specifically, we vary:

\begin{itemize}
    \item Parameter $\alpha$: ±20\% from baseline value
    \item Parameter $\beta$: ±15\% from baseline value
    \item Parameter $\gamma$: ±10\% from baseline value
\end{itemize}

\subsection{Results}
Figure [X] shows the model output as a function of parameter variations.

[Include tornado diagram or spider plot]

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/sensitivity.png}
    \caption{Sensitivity analysis results. The model output shows [description of sensitivity].
    Parameters are ranked by their influence: [ranking].}
    \label{fig:sensitivity}
\end{figure}

\subsection{Interpretation}
The analysis reveals that:
\begin{itemize}
    \item The model is most sensitive to parameter $\alpha$, with a ±20\% variation 
          causing a [X]% change in output
    \item Parameters $\beta$ and $\gamma$ have moderate influence ([Y]% and [Z]% output variation)
    \item The model remains qualitatively consistent across all tested parameter ranges,
          indicating robust conclusions
\end{itemize}
```

### Pattern 2: Scenario Analysis

**Structure**:
```
\subsection{Scenario Testing}

We test the model under three scenarios representing different conditions:

\textbf{Scenario 1: Best Case}
- Assumption: [Optimistic conditions]
- Results: [Outcomes]

\textbf{Scenario 2: Base Case}  
- Assumption: [Expected conditions]
- Results: [Outcomes]

\textbf{Scenario 3: Worst Case}
- Assumption: [Pessimistic conditions]  
- Results: [Outcomes]

Even under the worst-case scenario, the model predicts [minimum performance], 
which still satisfies [requirement]. This demonstrates the model's robustness 
across a wide range of conditions.
```

---

## Strengths and Weaknesses Patterns

### Honest and Balanced Format

**Strengths**:
```latex
\subsection{Strengths}

\begin{itemize}
    \item \textbf{Comprehensive Framework}: Our multi-stage approach integrates 
          [aspects], providing a holistic solution to [problem]. Unlike previous 
          methods that focus solely on [limitation], we address [advantage].
          
    \item \textbf{Data-Driven Validation}: The model is calibrated using [data source] 
          spanning [time period], ensuring empirical grounding. Cross-validation 
          achieves [metric] accuracy.
          
    \item \textbf{Computational Efficiency}: The algorithm converges in [time/iterations], 
          making it practical for real-time applications. Complexity is O([notation]).
          
    \item \textbf{Extensibility}: The modular design allows for easy incorporation 
          of additional factors such as [examples], enabling adaptation to diverse contexts.
\end{itemize}
```

**Weaknesses**:
```latex
\subsection{Weaknesses}

\begin{itemize}
    \item \textbf{Assumption Limitations}: Our model assumes [assumption], which may 
          not hold in [specific cases]. Future work could relax this by [suggestion].
          
    \item \textbf{Data Constraints}: The analysis is limited to [data scope]. 
          Generalization to [broader context] requires validation with additional datasets.
          
    \item \textbf{Simplified Dynamics}: We model [process] as [simplification], 
          neglecting [factors]. While this enables tractability, it may underestimate 
          [effect] in scenarios where [condition].
          
    \item \textbf{Computational Trade-offs}: The model prioritizes [aspect] over [other aspect]. 
          For applications requiring [alternative priority], modifications to [component] 
          would be necessary.
\end{itemize}
```

---

## Conclusion Patterns

### Pattern 1: Summary + Implications + Future Work

**Structure**:
```
\section{Conclusions}

[Summary - 2-3 sentences]
This paper presents a comprehensive framework for [problem]. Our multi-stage approach 
integrates [Model 1], [Model 2], and [Model 3] to achieve [objective]. The model 
demonstrates [key performance metric] and provides [main contribution].

[Key Findings - Bullet format]
Our analysis yields several important findings:
\begin{itemize}
    \item [Finding 1 with quantitative result]
    \item [Finding 2 with quantitative result]
    \item [Finding 3 with quantitative result]
\end{itemize}

[Practical Implications - 2-3 sentences]
These results have significant implications for [application domain]. Specifically, 
[stakeholder] can use our model to [practical use]. The framework provides [benefit] 
while maintaining [constraint].

[Limitations and Future Work - 2-3 sentences]
While our model successfully addresses [aspects], future research could extend the 
framework by [direction 1] and [direction 2]. Additionally, validation with [data type] 
would enhance generalizability to [contexts].

[Closing Statement - 1 sentence]
Overall, this work advances the understanding of [problem] and provides a practical 
tool for [application].
```

---

## Letter/Memo Specific Patterns

### When Problem Requires a Letter or Memo

**Memo Format**:
```latex
\documentclass{mcmthesis}
\mcmsetup{
    tcn = [Your Team Number],
    problem = [A/B/C/D/E/F],
    sheet = true,
    titleinsheet = false,
    keywordsinsheet = false,
    titlepage = false,
    abstract = false
}

% Use memo commands
\memoto{[Recipient Name and Title]}
\memofrom{Team \# [Your Number]}
\memosubject{[Subject Line]}
\memodate{\today}

\begin{document}
\maketitle

% Memo body
[Opening paragraph addressing the recipient]

[Main content with clear sections]

[Closing with recommendations]

[Signature block]
\end{document}
```

**Letter Format**:
```latex
% Similar setup but use letter style
\begin{letter}{[Recipient Address]}
\opening{Dear [Name]:}

[Letter body with professional tone]

\closing{Sincerely,}
\end{letter}
```

**Key Differences from Standard Paper**:
- Address specific persona (e.g., "Marketing Director", "Policy Maker")
- Use less technical language
- Focus on actionable recommendations
- Include executive summary upfront
- Use "you" and "we" appropriately for the audience

---

## Common High-Scoring Phrases

### Transition Phrases
- "Building upon this foundation, we..."
- "To address this challenge, we..."
- "This motivates our investigation into..."
- "Consequently, we develop..."
- "Furthermore, our analysis reveals..."
- "In contrast to previous approaches..."
- "Specifically, we focus on..."

### Results Presentation
- "Our analysis demonstrates that..."
- "The results indicate a strong correlation (r = [value])..."
- "Sensitivity analysis confirms..."
- "Compared to the baseline, our approach achieves..."
- "The model predicts with [X]% accuracy..."
- "These findings suggest that..."

### Limitations and Future Work
- "While our model successfully addresses [X], future work could..."
- "This simplification is justified by [reason], though..."
- "Our approach assumes [X], which may not hold in [case]..."
- "Future research could extend this framework by..."
- "Validation with additional datasets would enhance..."

---

## Anti-Patterns to AVOID

### ❌ Vague Statements
- "Our model is very good"
- "The results are impressive"
- "We got excellent accuracy"

### ✅ Specific Statements
- "Our model achieves 94.3% classification accuracy"
- "The RMSE is 0.023, representing a 15% improvement over the baseline"
- "Sensitivity analysis shows robustness to ±20% parameter variations"

### ❌ Undefined Acronyms
- First mention: "We use the SIR model..." (without defining)

### ✅ Defined Acronyms
- First mention: "We use the Susceptible-Infected-Recovered (SIR) model..."
- Subsequent: "The SIR model predicts..."

### ❌ Missing Figure References
- "The plot shows the results."

### ✅ Proper Figure References
- "Figure 3 shows the time evolution of infected individuals."
- "As illustrated in Figure 3, the epidemic peaks around day 45."

---

**Usage Note**: When drafting sections, refer to the appropriate pattern above. Copy the structure but customize the content to your specific problem. Always include specific numbers, proper citations, and clear logical flow.
