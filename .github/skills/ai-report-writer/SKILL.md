---
name: ai-report-writer
description: "COMAP MCM/ICM AI Tool Usage Report Generator. MUST USE when the team needs to create the mandatory 'Report on Use of AI Tools' appendix for competition submission. Specializes in: (1) Logging AI interactions (prompts/outputs) during the competition, (2) Generating compliant report structure with all required sections, (3) Ensuring transparency and verification documentation per COMAP policy, (4) Creating proper AI tool citations for the main paper. Use this skill during the competition (for logging) and in the final hours (for report assembly)."
---

# COMAP AI Tool Usage Report Writer

## Overview

You are the AI Report Compliance Expert for MCM/ICM teams. Your mission: help teams create a **fully compliant "Report on Use of AI Tools"** that satisfies COMAP's transparency requirements and prevents disqualification.

**Critical Understanding**: Starting from MCM/ICM 2024, COMAP **requires** all teams to submit a detailed AI usage report as an appendix. Failure to disclose AI use or including unverified AI-generated content (hallucinations, fake citations) can result in **disqualification**.

## Competition Context

### COMAP AI Policy Core Principles

1. **Openness and Honesty**: Teams must disclose **all** AI use, including embedded AI in software (e.g., Wolfram Alpha AI, translation tools).
2. **Transparency**: The more transparent the disclosure, the more the work is trusted by judges.
3. **Human-Centric**: AI is a productivity tool, not a replacement for human creativity. Critical decisions (model selection, result interpretation, conclusions) must be human-led.
4. **Responsibility**: Teams are 100% responsible for verifying AI-generated content. Unverified hallucinations or fake citations lead to disqualification.

### Report Requirements

- **Placement**: Appendix after the 25-page solution
- **Page Limit**: No limit (does NOT count toward 25-page limit)
- **Language**: English (standard for MCM/ICM)
- **Content**: Must include exact prompts and complete outputs for generative AI

## Core Workflow: Two-Phase Process

### Phase 1: Real-Time Logging (Hours 0-92)

**Goal**: Capture AI interactions as they happen during the competition.

#### Step 1.1: Set Up Log Template

At the start of the competition (Hour 0), create a logging file to track all AI use.

**Log Template** (Markdown/Text format):
```markdown
# AI Usage Log - Team [Number] - Problem [X]

## Log Entry Template
**Time**: YYYY-MM-DD HH:MM
**Tool/Model**: [e.g., OpenAI ChatGPT GPT-4, Claude 3.5 Sonnet]
**Type**: [LLM / Translation / Code Copilot / Math Software AI]
**Purpose**: [e.g., Polishing introduction, debugging Python code]
**Location**: [e.g., Section 2.1, file: simulation.py, lines 45-67]

**Query (Exact Wording)**:
```
[Paste the exact prompt here]
```

**Output (Complete Response)**:
```
[Paste the full AI response here]
```

**Verification and Revision**:
1. **Verified**: [What was checked - e.g., "Checked all cited papers exist in Google Scholar"]
2. **Revised**: [What was changed - e.g., "Corrected formula notation from X to Y"]
3. **Final Usage**: [How much used - e.g., "Used 30% of output after heavy revision"]

---
```

**Best Practices**:
- Assign one team member as "AI Logger" to maintain the log
- Log **immediately** after each AI interaction (don't rely on memory)
- Use copy-paste for exact prompts and outputs (don't paraphrase)
- For long outputs (>500 words), include full text but summarize key points in "Final Usage"

#### Step 1.2: What to Log

**MUST Log**:
- ✅ ChatGPT, Claude, Gemini, etc. (LLM interactions)
- ✅ GitHub Copilot, Cursor, Tabnine (code assistance)
- ✅ DeepL, Google Translate, Baidu Fanyi (translation)
- ✅ Wolfram Alpha AI mode (symbolic computation)
- ✅ Grammarly AI suggestions (if used for major rewrites)
- ✅ Any AI that generates text, code, or ideas

**Optional to Log** (but recommended):
- 🔶 Matplotlib default styles (not AI-generated)
- 🔶 Standard Python libraries (numpy, scipy) - not AI unless using AI-assisted code completion

**Do NOT Log**:
- ❌ Manual literature searches (Google Scholar, Web of Science)
- ❌ Standard calculators (non-AI)
- ❌ Excel formulas (non-AI)

#### Step 1.3: Special Cases

**Translation Tools**:
For translation tools, teams are **not required** to include full input text. Instead, provide a usage statement:

```markdown
**Tool/Model**: DeepL Translator (2026-01-29 version)
**Type**: Translation
**Purpose**: Translate Chinese literature abstracts to English
**Location**: Literature review notes (not in final paper)

**Usage Statement**:
We used DeepL to translate 5 Chinese academic paper abstracts (approximately 2000 words total) to understand relevant prior work. All translations were manually proofread by native English speakers for terminology accuracy.

**Verification**:
- Checked technical terms against domain-specific dictionaries
- Compared translations with original Chinese for logical consistency
```

**Code Copilots**:
For code assistance tools, focus on which files/functions were assisted:

```markdown
**Tool/Model**: GitHub Copilot (VSCode extension, 2026-01-29)
**Type**: Code Copilot
**Purpose**: Auto-complete Python functions for data preprocessing
**Location**: code/data_cleaner.py (lines 23-45, 78-92)

**Verification**:
- Tested all generated functions with unit tests
- Modified variable names for clarity
- Added error handling that Copilot did not generate
- Final code is ~60% human-written, 40% Copilot-assisted
```

---

### Phase 2: Report Assembly (Hours 92-96)

**Goal**: Convert the log into the formal "Report on Use of AI Tools" appendix.

#### Step 2.1: Report Structure

**Complete LaTeX Template**:

```latex
\newpage
\appendix
\section*{Report on Use of AI Tools}

\subsection*{Basic Information}
\begin{itemize}
    \item \textbf{Contest}: MCM/ICM 2026
    \item \textbf{Team Number}: [Your Team Number]
    \item \textbf{Problem}: [A/B/C/D/E/F]
    \item \textbf{Report Language}: English
\end{itemize}

\subsection*{1. Usage Overview}

\begin{table}[H]
\centering
\caption{Summary of AI Tools Used}
\begin{tabular}{p{3cm}p{2.5cm}p{2cm}p{3cm}p{3cm}}
\toprule
\textbf{Tool/Model} & \textbf{Version/Date} & \textbf{Type} & \textbf{Purpose} & \textbf{Location} \\
\midrule
OpenAI ChatGPT GPT-4 & 2026-01-29 & LLM & Polishing introduction & Section 1 \\
Claude 3.5 Sonnet & 2026-01-30 & LLM & Debugging Python code & code/model.py \\
DeepL Translator & 2026-01-29 & Translation & Literature translation & Literature notes \\
GitHub Copilot & VSCode 2026-01 & Code Copilot & Auto-complete functions & code/data\_cleaner.py \\
\bottomrule
\end{tabular}
\end{table}

\subsection*{2. Detailed Records of LLM / Generative AI}

\subsubsection*{2.1 Tool/Model Information}
\textbf{Tool}: OpenAI ChatGPT GPT-4 \\
\textbf{Version}: Accessed on 2026-01-29 via web interface (chat.openai.com) \\
\textbf{Purpose}: Polishing the introduction section for clarity and academic tone

\subsubsection*{2.2 Interaction Log}

\paragraph{Interaction 1: Introduction Polishing}
\textbf{Time}: 2026-01-29 14:30 \\
\textbf{Query (Exact Wording)}:
\begin{quote}
\textit{``Please polish the following paragraph for academic tone and clarity: [Original paragraph text]''}
\end{quote}

\textbf{Output (Complete Response)}:
\begin{quote}
\textit{[Full AI response text]}
\end{quote}

\textbf{Verification and Revision}:
\begin{itemize}
    \item \textbf{Verified}: Checked that no new factual claims were introduced by the AI. Confirmed all terminology matches our model definitions.
    \item \textbf{Revised}: Changed ``utilize'' back to ``use'' for simplicity. Removed one sentence that was too verbose.
    \item \textbf{Final Usage}: Used approximately 70\% of the AI output. The final paragraph in Section 1 is a combination of AI suggestions and our original wording.
\end{itemize}

% Repeat for each LLM interaction

\subsection*{3. Translation Tools}

\textbf{Tool/Model}: DeepL Translator (2026-01-29 version) \\
\textbf{Usage Statement}: We used DeepL to translate 5 Chinese academic paper abstracts (approximately 2000 words total) to understand relevant prior work. All translations were manually proofread by native English speakers for terminology accuracy. \\
\textbf{Proofreading Notes}: Verified technical terms (e.g., ``非线性规划'' → ``nonlinear programming'') against standard references. Confirmed logical consistency between original and translated text.

\subsection*{4. Code Copilots / Auto-complete / Mathematical Software AI}

\textbf{Tool/Model}: GitHub Copilot (VSCode extension, 2026-01-29) \\
\textbf{Purpose}: Auto-complete Python functions for data preprocessing \\
\textbf{Usage Location}: code/data\_cleaner.py (lines 23-45, 78-92) \\
\textbf{Verification Notes}: 
\begin{itemize}
    \item Tested all generated functions with unit tests on sample data
    \item Modified variable names for clarity and consistency with our codebase
    \item Added error handling (try-except blocks) that Copilot did not generate
    \item Final code is approximately 60\% human-written, 40\% Copilot-assisted
\end{itemize}

\subsection*{5. Integrity, Verification, and Responsibility Statement}

We, Team [Number], declare that:
\begin{enumerate}
    \item All AI-generated content has been verified for accuracy and consistency with our models and data.
    \item We have checked all citations and references for authenticity. No ``hallucinated'' citations have been included.
    \item All critical decisions (model selection, result interpretation, conclusions) were made by human team members.
    \item We take full responsibility for the accuracy and integrity of our submission.
    \item This report represents a complete and honest disclosure of all AI tools used in our solution.
\end{enumerate}

\textbf{Team Members}: [Names] \\
\textbf{Date}: 2026-02-01

\end{document}
```

#### Step 2.2: Converting Log to LaTeX

**Workflow**:
1. **Extract from Log**: Copy all log entries from Phase 1
2. **Group by Tool Type**: Separate LLM, Translation, Code Copilot entries
3. **Fill Template**: Insert entries into the LaTeX template above
4. **Generate Summary Table**: Create the "Usage Overview" table from all entries
5. **Write Integrity Statement**: Customize the final declaration

**Time Budget**:
- Log conversion: 30-45 minutes
- LaTeX formatting: 15-20 minutes
- Proofreading: 10-15 minutes
- **Total**: ~1 hour (Hour 92-93)

#### Step 2.3: Quality Checklist

Before finalizing the report, verify:

**Completeness**:
- [ ] All AI tools used are listed in Section 1 (Usage Overview)
- [ ] Every LLM interaction has: Time, Query, Output, Verification notes
- [ ] Translation tools have usage statements and proofreading notes
- [ ] Code Copilots have file locations and verification notes
- [ ] Integrity Statement is signed and dated

**Accuracy**:
- [ ] Prompts are **exact** (copy-pasted, not paraphrased)
- [ ] Outputs are **complete** (not summarized for LLMs)
- [ ] Verification notes are **specific** (not generic like "we checked it")
- [ ] Version/date information is correct for all tools

**Compliance**:
- [ ] No unverified AI content in the main paper
- [ ] All AI-cited sources have been checked for existence
- [ ] Verification notes demonstrate human oversight
- [ ] Report is placed **after** the 25-page solution

---

## AI Citation in Main Paper

In addition to the appendix, teams must cite AI tools in the main paper where they were used.

### Citation Format

**In-Text Citation** (where AI was used):
```latex
The introduction was polished with assistance from ChatGPT~\cite{openai2026chatgpt}.
```

**Reference Entry** (in bibliography):
```latex
@misc{openai2026chatgpt,
    author = {{OpenAI}},
    title = {ChatGPT (GPT-4)},
    year = {2026},
    note = {Accessed January 29, 2026. \url{https://chat.openai.com}},
    howpublished = {Query: ``Please polish the following paragraph...'' Output: [Summarized output]}
}
```

**Alternative Format** (if not using BibTeX):
```
[1] OpenAI. ChatGPT (GPT-4). Accessed January 29, 2026. https://chat.openai.com. Query: "Please polish the following paragraph..." Output: [Summarized output].
```

### When to Cite

**MUST Cite** (in main paper):
- ✅ Any section where AI-generated text was used (even if heavily revised)
- ✅ Code files where AI assistance was significant (>30% of code)
- ✅ Figures/tables if AI helped generate the visualization code

**Optional to Cite** (but include in appendix):
- 🔶 Minor grammar fixes by Grammarly
- 🔶 Translation of non-English sources (cite the original source, note translation in appendix)

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Incomplete Logging
**Problem**: Team forgets to log some AI interactions during the competition.
**Fix**: 
- Set a rule: "No AI use without logging"
- Use a shared document (Google Docs) for real-time logging
- Assign one person as "AI Logger" to enforce this

### Pitfall 2: Generic Verification Notes
**Problem**: Verification notes like "We checked it and it's fine."
**Fix**: Be specific:
- ❌ "We verified the output."
- ✅ "We verified that the cited paper [Smith 2020] exists in Google Scholar and confirmed the formula matches the original source."

### Pitfall 3: Paraphrasing Prompts
**Problem**: Log says "We asked ChatGPT to help with the model" instead of exact prompt.
**Fix**: Always copy-paste the **exact prompt** used.

### Pitfall 4: Omitting Embedded AI
**Problem**: Team uses Wolfram Alpha AI mode but doesn't report it.
**Fix**: Report **all** AI, including:
- Wolfram Alpha AI mode
- Grammarly AI suggestions
- Excel's "Ideas" feature (if used)
- Any tool with "AI" in its description

### Pitfall 5: Unverified Citations
**Problem**: AI generates fake citations (hallucinations), team includes them without checking.
**Fix**: 
- **Always** verify citations by searching Google Scholar, Web of Science, or the journal website
- In verification notes, explicitly state: "Verified citation [X] exists and is relevant"

---

## Integration with Other Skills

### Before ai-report-writer
- **latex-coauthoring**: While writing the main paper, log any AI assistance
- **xlsx**, **data-cleaner**: If using AI for data processing, log it
- **visual-engineer**: If AI helps generate visualization code, log it

### After ai-report-writer
- **pdf**: Merge the AI report appendix with the main paper PDF for submission
- **latex-coauthoring**: Ensure AI citations are added to the main paper's reference section

---

## Time Management Strategy

### During Competition (Hours 0-92)
**Continuous Logging** (5-10 minutes per interaction):
- Hour 0: Set up log template
- Hours 0-92: Log every AI interaction immediately
- **Total Time**: ~1-2 hours spread across 4 days

### Final Hours (Hours 92-96)
**Report Assembly** (1 hour):
- Hour 92-93: Convert log to LaTeX report
- Hour 93: Proofread and verify completeness
- Hour 94: Add AI citations to main paper references
- Hour 95: Final check and PDF merge

**Critical**: Do NOT leave report assembly to the last 30 minutes. Start at Hour 92 to allow time for errors.

---

## Output Standards

### File Organization
```
project/
├── main.tex                    # Main 25-page solution
├── ai_report.tex               # AI usage report (separate file)
├── ai_usage_log.md             # Real-time log (working document)
├── references.bib              # Bibliography (includes AI citations)
└── compiled/
    ├── main.pdf                # Main paper
    ├── ai_report.pdf           # AI report
    └── final_submission.pdf    # Merged PDF (main + AI report)
```

### Quality Standards

**Content Quality**:
- Prompts are exact (copy-pasted)
- Outputs are complete (not summarized)
- Verification notes are specific and detailed
- All AI use is disclosed (no omissions)

**Format Quality**:
- LaTeX compiles without errors
- Tables are properly formatted (use `booktabs`)
- Report is placed after the 25-page solution
- Page numbers are continuous

**Compliance Quality**:
- Meets all COMAP policy requirements
- Demonstrates human oversight and responsibility
- No unverified content in main paper
- Integrity statement is signed

---

## Advanced: Automated Log Conversion

For teams comfortable with scripting, consider automating log-to-LaTeX conversion.

**Python Script Outline**:
```python
import re
from datetime import datetime

def parse_log_entry(entry_text):
    """Extract time, query, output, verification from log entry"""
    # Use regex to extract structured data
    pass

def generate_latex_entry(entry_data):
    """Convert parsed entry to LaTeX format"""
    template = r"""
\paragraph{Interaction {num}: {purpose}}
\textbf{Time}: {time} \\
\textbf{Query (Exact Wording)}:
\begin{quote}
\textit{``{query}''}
\end{quote}

\textbf{Output (Complete Response)}:
\begin{quote}
\textit{[{output_summary}]}
\end{quote}

\textbf{Verification and Revision}:
\begin{itemize}
    \item \textbf{Verified}: {verified}
    \item \textbf{Revised}: {revised}
    \item \textbf{Final Usage}: {final_usage}
\end{itemize}
"""
    return template.format(**entry_data)

# Main conversion logic
with open('ai_usage_log.md', 'r') as f:
    log_text = f.read()

entries = parse_log_entries(log_text)
latex_output = '\n'.join([generate_latex_entry(e) for e in entries])

with open('ai_report_generated.tex', 'w') as f:
    f.write(latex_output)
```

**Time Savings**: Reduces Hour 92-93 work from 45 minutes to 10 minutes.

---

## Final Reminder: Transparency is Your Shield

**Competition Reality**:
- Judges appreciate honesty about AI use
- Transparent teams are trusted more than teams that hide AI use
- The AI report is **not** a penalty — it's a demonstration of integrity
- Teams that fail to report AI use risk disqualification

**Strategy**:
1. **Log everything** (over-report rather than under-report)
2. **Verify all AI content** (don't trust AI blindly)
3. **Be specific in verification notes** (show you did the work)
4. **Submit early** (don't rush the report in the last 10 minutes)

**The Golden Rule**: If you used AI, report it. If you reported it, verify it. If you verified it, document it.
