# AI Usage Log Template

## Purpose
This template provides a structured format for logging all AI interactions during the MCM/ICM competition. Use this as a working document throughout the 96-hour competition period.

## Setup Instructions

1. **Create Log File**: At Hour 0 (start of competition), create a new file `ai_usage_log.md`
2. **Share with Team**: Use Google Docs, Overleaf, or shared folder for real-time collaboration
3. **Assign Logger**: Designate one team member as "AI Logger" to enforce logging discipline
4. **Set Rule**: "No AI use without logging" — make this a team rule

## Log Entry Template

Copy this template for each AI interaction:

```markdown
---
## Log Entry #[Number]

**Time**: YYYY-MM-DD HH:MM (e.g., 2026-01-29 14:30)
**Tool/Model**: [Full name and version, e.g., OpenAI ChatGPT GPT-4]
**Type**: [Select one: LLM / Translation / Code Copilot / Math Software AI / Other]
**Purpose**: [Brief description, e.g., "Polishing introduction section"]
**Location**: [Where used, e.g., "Section 2.1" or "code/simulation.py lines 45-67"]

### Query (Exact Wording)
```
[Paste the EXACT prompt here - do not paraphrase]
[Include any context you provided to the AI]
```
```

### Output (Complete Response)
```
[Paste the FULL AI response here]
[For very long outputs (>1000 words), include full text but add a summary]
```
```

### Verification and Revision
1. **Verified**: 
   - [Specific check 1, e.g., "Verified citation [Smith 2020] exists in Google Scholar"]
   - [Specific check 2, e.g., "Confirmed formula matches original source"]
   - [Add more as needed]

2. **Revised**: 
   - [Specific change 1, e.g., "Changed 'utilize' to 'use' for simplicity"]
   - [Specific change 2, e.g., "Removed sentence about X because it was incorrect"]
   - [Add more as needed]

3. **Final Usage**: 
   - [Percentage or description, e.g., "Used ~70% of output after revisions"]
   - [What ended up in final paper, e.g., "Final paragraph in Section 1 is 50% AI, 50% human"]

### Notes
[Any additional context, e.g., "This was our third attempt at this prompt"]

---
```

## Quick Reference: What to Log

### MUST Log ✅
- **LLMs**: ChatGPT, Claude, Gemini, Llama, etc.
- **Translation**: DeepL, Google Translate, Baidu Fanyi
- **Code Copilots**: GitHub Copilot, Cursor, Tabnine, Amazon CodeWhisperer
- **Math AI**: Wolfram Alpha AI mode, Maple AI features
- **Writing AI**: Grammarly AI suggestions (if used for major rewrites)

### Optional to Log 🔶
- **Grammar**: Grammarly basic grammar checks (non-AI)
- **Search**: Google Scholar, Web of Science (not AI)

### Do NOT Log ❌
- **Calculators**: Standard calculators without AI
- **Libraries**: numpy, scipy, matplotlib (unless using AI code completion)
- **Manual Work**: Your own code, writing, analysis

## Example Log Entries

### Example 1: LLM for Text Polishing

```markdown
---
## Log Entry #1

**Time**: 2026-01-29 14:30
**Tool/Model**: OpenAI ChatGPT GPT-4 (Web interface, chat.openai.com)
**Type**: LLM
**Purpose**: Polishing introduction paragraph for academic tone
**Location**: Section 1 (Introduction), paragraph 2

### Query (Exact Wording)
```
Please polish the following paragraph for academic tone and clarity:

"Our model uses a SIR model to predict how the disease spreads. We think this is good because it's simple and works well. The model has three parts: S for people who can get sick, I for people who are sick, and R for people who got better."
```
```

### Output (Complete Response)
```
Here's a polished version with improved academic tone:

"Our approach employs a Susceptible-Infected-Recovered (SIR) compartmental model to simulate disease transmission dynamics. This model is particularly well-suited for our analysis due to its parsimony and empirical validation in epidemiological literature. The model partitions the population into three mutually exclusive compartments: Susceptible (S) individuals who are at risk of infection, Infected (I) individuals who are currently infectious, and Recovered (R) individuals who have acquired immunity."
```
```

### Verification and Revision
1. **Verified**: 
   - Confirmed that "parsimony" is appropriate terminology (checked against epidemiology textbooks)
   - Verified that SIR model is indeed validated in literature (cross-referenced with our citations)

2. **Revised**: 
   - Changed "employs" back to "uses" for simplicity
   - Removed "mutually exclusive" as it's implied
   - Kept "compartmental model" terminology as it's standard

3. **Final Usage**: 
   - Used approximately 60% of AI output
   - Final paragraph is a blend of AI suggestions and our original wording
   - Specific phrase "transmission dynamics" was adopted from AI

### Notes
This was our first use of ChatGPT. We were careful to verify terminology against our reference materials.

---
```

### Example 2: Code Copilot

```markdown
---
## Log Entry #5

**Time**: 2026-01-30 09:15
**Tool/Model**: GitHub Copilot (VSCode extension, version 1.150.0)
**Type**: Code Copilot
**Purpose**: Auto-complete data preprocessing functions
**Location**: code/data_cleaner.py, lines 23-45 and 78-92

### Query (Exact Wording)
```
# Context: We had written a comment and function signature:
# Function to remove outliers using IQR method
def remove_outliers(df, column_name):
    # [Copilot auto-completed the rest]
```
```

### Output (Complete Response)
```
# Copilot suggested:
def remove_outliers(df, column_name):
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)]
```
```

### Verification and Revision
1. **Verified**: 
   - Tested function on sample data with known outliers
   - Confirmed IQR formula is correct (1.5 * IQR is standard)
   - Checked that function returns correct DataFrame

2. **Revised**: 
   - Added error handling for empty DataFrame
   - Added docstring explaining parameters and return value
   - Renamed variables for clarity (Q1 → first_quartile)

3. **Final Usage**: 
   - Core logic (80%) is from Copilot
   - Error handling and documentation (20%) is human-added
   - Final function is production-ready after modifications

### Notes
Copilot was very helpful here. The suggested code was mostly correct, but we added robustness features.

---
```

### Example 3: Translation Tool

```markdown
---
## Log Entry #3

**Time**: 2026-01-29 20:45
**Tool/Model**: DeepL Translator (Web interface, deepl.com, accessed 2026-01-29)
**Type**: Translation
**Purpose**: Translate Chinese literature abstracts to English for literature review
**Location**: Literature review notes (not directly in final paper)

### Query (Exact Wording)
```
[NOTE: For translation tools, full input text is NOT required per COMAP policy]

We translated 5 Chinese academic paper abstracts, approximately 2000 words total.
Source papers:
1. Zhang et al. (2023) - 非线性规划方法在资源分配中的应用
2. Li et al. (2022) - 基于遗传算法的多目标优化研究
[... list all sources ...]
```
```

### Output (Complete Response)
```
[NOTE: Full translation output is NOT required per COMAP policy]

DeepL provided English translations for all 5 abstracts.
Key translated terms:
- 非线性规划 → nonlinear programming
- 遗传算法 → genetic algorithm
- 多目标优化 → multi-objective optimization
```
```

### Verification and Revision
1. **Verified**: 
   - Cross-checked technical terms against English-Chinese math dictionary
   - Confirmed translations match standard terminology in English literature
   - Verified logical consistency between Chinese and English versions

2. **Revised**: 
   - Corrected "hereditary algorithm" to "genetic algorithm" (DeepL mistake)
   - Adjusted sentence structure for better English flow

3. **Final Usage**: 
   - Translations were used to understand prior work
   - Did NOT copy-paste translations into our paper
   - Used translations to inform our literature review (cited original Chinese papers)

### Notes
Translation quality was good overall, but technical terms required manual verification.

---
```

## Special Case Templates

### Template for Multiple Similar Interactions

If you have many similar interactions (e.g., 10 debugging sessions with the same tool), you can group them:

```markdown
---
## Log Entry #8-17 (Grouped)

**Time Range**: 2026-01-30 15:00 - 18:30
**Tool/Model**: Claude 3.5 Sonnet (Web interface, claude.ai)
**Type**: LLM
**Purpose**: Debugging Python code for optimization model
**Location**: code/optimizer.py, various functions

### Summary of Interactions
We had 10 debugging sessions with Claude, all following a similar pattern:
1. Paste error message
2. Paste relevant code snippet
3. Claude suggests fix
4. We test and iterate

### Representative Example (Interaction #12)

**Query**:
```
I'm getting this error: "ValueError: operands could not be broadcast together"
Here's the code:
[code snippet]
```
```

**Output**:
```
The error occurs because your arrays have incompatible shapes...
[Claude's explanation and suggested fix]
```
```

### Verification and Revision (Across All 10 Sessions)
1. **Verified**: 
   - Tested every suggested fix on our full dataset
   - Confirmed fixes didn't introduce new bugs
   - Checked that logic matched our model specifications

2. **Revised**: 
   - Average of 40% of Claude's suggestions were used as-is
   - 30% were modified before implementation
   - 30% were rejected in favor of our own solutions

3. **Final Usage**: 
   - Claude helped identify ~8 out of 10 bugs
   - Final code is ~70% human-written, ~30% Claude-assisted
   - All critical logic was human-designed

### Notes
Claude was very helpful for debugging, but we always understood the fixes before implementing them.

---
```

## Time-Saving Tips

### Tip 1: Use Keyboard Shortcuts
- Keep log template in a separate file
- Use Ctrl+C / Ctrl+V for quick copying
- Use text expansion tools for repeated phrases

### Tip 2: Log Immediately
- Don't wait until end of day to log
- Log right after each AI interaction (takes 2-3 minutes)
- Memory fades quickly — exact prompts are hard to recall later

### Tip 3: Use Shared Document
- Google Docs: Real-time collaboration, auto-save
- Overleaf: Integrated with LaTeX workflow
- Dropbox/OneDrive: Sync across devices

### Tip 4: Assign Roles
- **AI Logger**: Enforces logging discipline, maintains log structure
- **AI Users**: Responsible for logging their own interactions
- **Verifier**: Double-checks log completeness before submission

## Conversion to Final Report

At Hour 92, you will convert this log into the formal LaTeX report. The conversion process:

1. **Extract**: Copy all log entries
2. **Group**: Separate by tool type (LLM, Translation, Code Copilot)
3. **Format**: Convert to LaTeX using report template
4. **Summarize**: Create Usage Overview table
5. **Finalize**: Add Integrity Statement

**Time Budget**: 45-60 minutes for conversion

## Quality Checklist

Before considering your log complete, check:

- [ ] Every AI interaction is logged (no omissions)
- [ ] Prompts are exact (copy-pasted, not paraphrased)
- [ ] Outputs are complete (not summarized, except translations)
- [ ] Verification notes are specific (not generic)
- [ ] Time stamps are accurate
- [ ] Tool versions/dates are recorded
- [ ] Location information is precise (section numbers, file paths)

## Common Mistakes to Avoid

### Mistake 1: Paraphrasing Prompts
❌ "We asked ChatGPT to help with the introduction"
✅ [Paste exact prompt used]

### Mistake 2: Summarizing Outputs
❌ "ChatGPT suggested some improvements"
✅ [Paste full AI response]

### Mistake 3: Generic Verification
❌ "We checked it and it's fine"
✅ "We verified citation [Smith 2020] exists in Google Scholar and confirmed the formula on page 45 matches our implementation"

### Mistake 4: Forgetting to Log
❌ Using AI without logging, planning to "remember later"
✅ Log immediately after each interaction

### Mistake 5: Incomplete Location Info
❌ "Used in the paper"
✅ "Section 2.1, paragraph 3, lines 5-8"

---

**Remember**: This log is your evidence of responsible AI use. The more detailed and honest your log, the more judges will trust your work.
