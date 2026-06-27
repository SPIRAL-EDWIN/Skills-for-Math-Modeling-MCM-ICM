# MCM/ICM Common Pitfalls Guide (防踩坑指南)

## Purpose
This reference catalogs critical mistakes that cost teams points in MCM/ICM competitions. Read this BEFORE starting your paper and use it as a final checklist before submission.

---

## 🚨 Critical Errors (Immediate Disqualification or Major Point Loss)

### 1. Missing or Incomplete AI Usage Report
**Error**: Failing to submit the mandatory "Report on Use of AI Tools" appendix
**Consequence**: Disqualification or severe point deduction (2024+ rule)
**Fix**: 
- Use `ai-report-writer` skill to create compliant report
- Include ALL AI interactions (ChatGPT, DeepL, GitHub Copilot, etc.)
- Provide exact prompts and complete outputs
- Document verification steps

**Checklist**:
- [ ] AI report exists as appendix
- [ ] All AI tools disclosed
- [ ] Verification notes are specific
- [ ] Integrity statement signed

---

### 2. Wrong Problem Identifier or Team Control Number
**Error**: Entering incorrect problem letter (A/B/C/D/E/F) or Team Control Number
**Consequence**: Paper may be rejected or assigned to wrong problem
**Fix**:
```latex
\mcmsetup{
    tcn = 1234567,    % CHECK THIS: Your actual TCN
    problem = A,      % CHECK THIS: Your actual problem letter
    % ... other settings
}
```

**Verification Steps**:
1. Check email confirmation from COMAP for correct TCN
2. Verify problem letter matches the problem you solved
3. Have teammate double-check before final submission
4. Test compile and verify header shows correct information

---

### 3. Exceeding Page Limit
**Error**: Main paper exceeds 25 pages (excluding appendices)
**Consequence**: Automatic point deduction or disqualification
**Fix**:
- Count pages carefully: Summary Sheet + Main Body ≤ 25 pages
- Appendices (code, AI report) do NOT count toward limit
- Use `\newpage` before appendices to ensure clear separation
- Reduce figure sizes or move supplementary figures to appendix

**Page Count Verification**:
```latex
% After main conclusions section:
\newpage  % Ensures appendices start on new page

\begin{appendices}
% Code and supplementary materials here
\end{appendices}

\newpage
\section*{\centering Report on Use of AI}
% AI report here
```

---

### 4. Missing Sensitivity Analysis
**Error**: No sensitivity analysis section in paper
**Consequence**: Perceived as "weak" model; unlikely to achieve high awards
**Fix**:
- Always include Section 6 or later: "Sensitivity Analysis"
- Test at least 3 key parameters with ±15-20% variations
- Show results visually (tornado diagram, spider plot)
- Interpret what the sensitivity means for model robustness

**Minimum Requirements**:
- Identify 3-5 key parameters
- Vary each parameter independently
- Show impact on model output
- Conclude whether model is robust

---

### 5. Unverified AI-Generated Citations
**Error**: Including fake "hallucinated" citations from AI without verification
**Consequence**: Academic dishonesty; disqualification
**Fix**:
- Check EVERY citation using Google Scholar or Web of Science
- Verify author names, journal names, publication years
- If citation doesn't exist, remove it or find correct reference
- Document verification in AI usage report

**Verification Process**:
1. Copy citation to Google Scholar
2. Confirm exact match (author, title, year, journal)
3. If no match found, search for similar paper or remove citation
4. Note in AI report: "Verified citation [X] exists via Google Scholar"

---

## ⚠️ Major Errors (Significant Point Loss)

### 6. Summary Sheet Exceeds One Page
**Error**: Summary sheet is longer than one page
**Consequence**: Major formatting violation; judges may not read beyond first page
**Fix**:
- Test print to PDF and verify exactly 1 page
- Reduce font size ONLY if absolutely necessary (12pt is standard)
- Cut unnecessary details; focus on key results
- Remove equations unless absolutely essential

**Summary Sheet Length Check**:
```latex
\begin{abstract}
[Keep to ~300-400 words maximum]
[ONE key equation maximum, if needed]
\begin{keywords}
[3-6 keywords only]
\end{keywords}
\end{abstract}
```

---

### 7. No Justification for Assumptions
**Error**: Listing assumptions without explaining why they're reasonable
**Consequence**: Appears arbitrary; reduces model credibility
**Fix**:
```latex
% WRONG:
\item \textbf{Assumption 1}: We assume constant temperature.

% CORRECT:
\item \textbf{Assumption 1}: We assume constant temperature.

\textit{Justification}: Historical weather data shows temperature 
varies by less than 5°C during the study period (May-August). 
According to [Reference], material properties change negligibly 
within this range.
```

**Every Assumption Must Have**:
- Clear statement of what is assumed
- Justification citing data, literature, or logical reasoning
- Assessment of impact if assumption is violated

---

### 8. Undefined Variables in Equations
**Error**: Using mathematical symbols without defining them
**Consequence**: Equations are incomprehensible; appears careless
**Fix**:
- Create comprehensive Notation table (Section 2.1)
- Define variables immediately after first use in text
- Use consistent notation throughout paper

**Example**:
```latex
% In Notation section:
\begin{table}[htbp]
    \centering
    \caption{Notation and Symbols}
    \begin{tabular}{cll}
        \toprule
        \textbf{Symbol} & \textbf{Definition} & \textbf{Unit} \\
        \midrule
        $\beta$ & Transmission rate & day$^{-1}$ \\
        % ... all symbols used
        \bottomrule
    \end{tabular}
\end{table}

% In text, when first using:
The transmission rate $\beta$ (infections per contact per day) 
determines the spread rate.
```

---

### 9. Figures Without Captions or References
**Error**: Including figures that aren't explained or cited in text
**Consequence**: Figures appear decorative rather than substantive
**Fix**:
```latex
% Every figure needs:
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{result.png}
    \caption{Detailed caption explaining what the figure shows.
    Key observations: [highlight important features].}
    \label{fig:result}
\end{figure}

% And must be referenced in text:
Figure \ref{fig:result} shows the time evolution of infected individuals.
As illustrated in Figure \ref{fig:result}, the epidemic peaks at day 45.
```

**Figure Checklist**:
- [ ] Has descriptive caption
- [ ] Caption explains what to observe
- [ ] Referenced in main text
- [ ] Label matches reference (`\label` and `\ref`)

---

### 10. Vague or Generic Results
**Error**: Stating results without specific numbers
**Consequence**: Appears unscientific; impossible to evaluate claims
**Fix**:
```latex
% WRONG:
Our model performs very well and is much better than the baseline.

% CORRECT:
Our model achieves 94.3% accuracy (RMSE = 0.023), representing 
a 15% improvement over the baseline method (accuracy = 82.1%, RMSE = 0.027).
```

**All Results Must Include**:
- Specific numerical values
- Units of measurement
- Comparison to baseline or threshold
- Statistical significance if applicable

---

## ⚡ Common Formatting Errors

### 11. Inconsistent Citation Format
**Error**: Mixing citation styles or missing citations
**Fix**:
- Use BibTeX for consistency
- Choose one style (plain, IEEEtran, etc.) and stick to it
- Cite ALL external sources, including data sources

**Correct Citation**:
```latex
According to Smith \cite{smith2020}, the SIR model is effective.

% In references.bib:
@article{smith2020,
    author = {Smith, John},
    title = {Epidemic Modeling},
    journal = {J. Math. Biology},
    year = {2020},
    volume = {45},
    pages = {123--145}
}
```

---

### 12. Poor Figure Quality
**Error**: Low-resolution or illegible figures
**Consequence**: Appears unprofessional; information lost
**Fix**:
- Save figures at 300 DPI minimum
- Use vector formats (PDF, EPS) when possible
- Ensure text in figures is readable (12pt minimum)
- Use color-blind friendly palettes

**Figure Quality Checklist**:
- [ ] Resolution ≥ 300 DPI
- [ ] Axis labels visible and readable
- [ ] Legend included if multiple series
- [ ] File size reasonable (<5 MB per figure)

---

### 13. Inconsistent Notation
**Error**: Using same symbol for different quantities or vice versa
**Consequence**: Confusing; appears careless
**Fix**:
- Create notation table at start
- Use consistent symbols throughout
- Avoid reusing symbols (e.g., don't use $t$ for both time and temperature)

**Notation Discipline**:
- $t$ = time (always)
- $T$ = temperature (always)
- $\alpha$ = specific parameter (always)
- Don't switch mid-paper

---

### 14. Overfull/Underfull Boxes
**Error**: LaTeX warnings about text overflowing margins
**Consequence**: Unprofessional appearance
**Fix**:
```latex
% For long equations:
\begin{equation}
\begin{split}
    [Long part 1] \\
    &\quad + [Long part 2]
\end{split}
\end{equation}

% For long URLs:
\usepackage{url}
\url{https://...}  % Allows line breaks

% For long words:
\usepackage{hyphenat}
Add\-itional\-ly  % Suggests hyphenation points
```

---

## 📝 Writing Style Errors

### 15. Over-Technical Summary Sheet
**Error**: Using jargon and technical details in summary
**Consequence**: Non-expert judges can't understand; paper gets low initial score
**Fix**:
```
% WRONG (Summary Sheet):
We employ a multi-objective NSGA-II algorithm with Pareto-optimal 
frontiers to minimize the Kullback-Leibler divergence...

% CORRECT (Summary Sheet):
We use an optimization method to balance multiple competing goals, 
finding solutions that improve both cost and quality...
```

**Summary Sheet Rules**:
- No jargon (write for non-experts)
- No equation numbers or figure references
- Focus on WHAT you found, not HOW you found it
- Include specific numerical results

---

### 16. Passive Voice Overuse
**Error**: Awkward passive constructions that obscure meaning
**Balance**: Use passive voice for objectivity, but don't overdo it
**Fix**:
```
% TOO PASSIVE (awkward):
It was found by us that the model was validated using data that 
had been collected.

% BETTER (clear):
We validated the model using collected data.
OR
The model was validated using collected data.
```

---

### 17. Missing Logical Transitions
**Error**: Jumping between topics without connectors
**Consequence**: Paper feels disjointed; hard to follow
**Fix**:
```
% Use transition phrases:
- "Building upon this foundation, we..."
- "To address this challenge, we..."
- "Consequently, we develop..."
- "In contrast to previous approaches..."
- "Furthermore, our analysis reveals..."
```

---

### 18. Undefined Acronyms
**Error**: Using acronyms without spelling them out first
**Consequence**: Confusing for readers unfamiliar with field
**Fix**:
```
% First use:
We use the Susceptible-Infected-Recovered (SIR) model...

% Subsequent uses:
The SIR model predicts...
```

---

## 🔧 Technical Errors

### 19. Equations Not Referenced
**Error**: Including equations that are never mentioned in text
**Consequence**: Equations appear decorative; unclear why they're important
**Fix**:
```latex
\begin{equation}
    \frac{dS}{dt} = -\beta S I
    \label{eq:sir_s}
\end{equation}

From Equation \eqref{eq:sir_s}, we observe that the susceptible 
population decreases proportionally to contacts between S and I.
```

---

### 20. No Model Validation
**Error**: Presenting model without showing it works
**Consequence**: Model appears untested; results not credible
**Fix**:
- Include validation section
- Compare predictions to known data
- Show error metrics (RMSE, R², etc.)
- Discuss where model succeeds and fails

**Minimum Validation**:
```
\subsection{Model Validation}

We validate the model using [data source]. Figure [X] compares 
model predictions (solid line) to observed data (points).

The model achieves RMSE = [value] and R² = [value], indicating 
[interpretation]. The model successfully captures [aspect] but 
slightly underestimates [aspect] in [condition].
```

---

## 📊 Data and Analysis Errors

### 21. No Data Preprocessing Section
**Error**: Jumping straight to modeling without showing data preparation
**Consequence**: Appears to use raw data without quality checks
**Fix**:
```
\section{Model Development}
\subsection{Data Preparation}
\subsubsection{Data Cleaning}
We handle missing values using [method]. Outliers beyond [threshold] 
are removed, affecting [X]% of data points.

\subsubsection{Data Visualization}
Figure [X] shows the correlation matrix, revealing [finding].
Figure [Y] shows the distribution of key variables.
```

**Data Preparation Checklist**:
- [ ] Missing value handling described
- [ ] Outlier detection method specified
- [ ] Data visualization included
- [ ] Summary statistics provided

---

### 22. Cherry-Picking Results
**Error**: Only showing results that support your model
**Consequence**: Appears biased; reduces credibility
**Fix**:
- Show both successful and challenging cases
- Discuss limitations honestly
- Include sensitivity analysis showing where model breaks down
- Present weaknesses section with specific examples

---

### 23. Ignoring Units
**Error**: Presenting numbers without units
**Consequence**: Results are meaningless without units
**Fix**:
```
% WRONG:
The optimal value is 42.

% CORRECT:
The optimal facility location reduces transportation costs by 
42% compared to the baseline.

OR

The wear rate is 2.3 × 10⁻⁹ m³/Nm.
```

---

## 🎯 Strategic Errors

### 24. No "Our Work" Roadmap
**Error**: Diving into details without providing overview
**Consequence**: Judges lose track of paper structure
**Fix**:
- Include "Our Work" subsection in Introduction
- Provide numbered list of main steps
- Include flow diagram showing model structure
- Reference this roadmap throughout paper

---

### 25. Weak Conclusion
**Error**: Conclusion just repeats introduction
**Consequence**: Misses opportunity to emphasize contributions
**Fix**:
```
\section{Conclusions}

[Summary of approach - 2 sentences]
[Key findings with numbers - bullet list]
[Practical implications - 2 sentences]
[Limitations and future work - 2 sentences]
[Strong closing statement - 1 sentence]
```

---

### 26. Missing Strengths and Weaknesses Section
**Error**: No critical evaluation of own model
**Consequence**: Appears unaware of limitations
**Fix**:
- Include dedicated section (usually Section 8 or 9)
- Be honest about weaknesses
- Provide specific examples for both strengths and weaknesses
- Suggest how weaknesses could be addressed in future work

---

## 📤 Submission Errors

### 27. Wrong File Format
**Error**: Submitting non-PDF file or corrupted PDF
**Consequence**: File may not be readable by judges
**Fix**:
- Always submit PDF
- Test open PDF on different device
- Verify all figures appear correctly
- Check file size is reasonable (<10 MB)

---

### 28. Missing Control Sheet
**Error**: Forgetting to include official control sheet
**Consequence**: Paper may be rejected
**Fix**:
- Download control sheet from COMAP website
- Fill out completely and accurately
- Place as FIRST page of submission
- Verify TCN and problem letter are correct

---

### 29. Late Submission
**Error**: Submitting after deadline
**Consequence**: Automatic disqualification
**Fix**:
- Submit at least 1 hour before deadline
- Account for time zone differences
- Test upload process early
- Keep backup of final PDF

---

## 🔍 Final Pre-Submission Checklist

### Content Checklist
- [ ] Summary Sheet is exactly 1 page
- [ ] Summary Sheet includes specific results with numbers
- [ ] All assumptions have justifications
- [ ] Notation table includes all symbols
- [ ] All figures have captions and are referenced in text
- [ ] All equations are numbered and referenced in text
- [ ] Sensitivity analysis section included
- [ ] Strengths and weaknesses section included
- [ ] AI usage report included (if any AI used)
- [ ] References are properly formatted
- [ ] Page count ≤ 25 (excluding appendices)

### Formatting Checklist
- [ ] Team Control Number is correct
- [ ] Problem letter is correct
- [ ] Font is readable (12pt recommended)
- [ ] Figures are high resolution (300 DPI)
- [ ] Tables use professional formatting (booktabs)
- [ ] No LaTeX compilation errors
- [ ] No overfull/underfull box warnings
- [ ] PDF opens correctly on different devices

### Quality Checklist
- [ ] No typos in title or summary
- [ ] All acronyms defined on first use
- [ ] Consistent notation throughout
- [ ] Results include specific numbers with units
- [ ] Model validation included
- [ ] Data preprocessing described
- [ ] Logical flow with clear transitions
- [ ] Academic tone maintained

### Submission Checklist
- [ ] Control sheet is first page
- [ ] Final PDF is under size limit
- [ ] File opens correctly
- [ ] Submitted at least 1 hour before deadline
- [ ] Confirmation email received

---

## 🚀 Quick Fix Priority

If you're running out of time, fix errors in this order:

**Priority 1 (Must Fix)**:
1. Correct TCN and problem letter
2. AI usage report (if applicable)
3. Page limit compliance
4. Summary sheet is 1 page

**Priority 2 (Should Fix)**:
5. Add sensitivity analysis section
6. Verify all citations exist
7. Add justifications to assumptions
8. Reference all figures in text

**Priority 3 (Nice to Fix)**:
9. Improve figure quality
10. Polish Summary Sheet language
11. Fix minor formatting issues
12. Add more quantitative results

---

**Remember**: Prevention is better than cure. Review this guide at Hour 0, Hour 48, and Hour 90 to catch issues early.
