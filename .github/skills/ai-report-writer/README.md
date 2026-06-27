# AI Report Writer - COMAP MCM/ICM Compliance Tool

## 🚨 Critical Information

**Status**: MANDATORY for all MCM/ICM teams starting from 2024  
**Consequence of Non-Compliance**: Disqualification  
**Time Required**: 2-3 hours total (spread across 4 days)

## What is This?

Starting from MCM/ICM 2024, COMAP **requires** all teams to submit a detailed "Report on Use of AI Tools" as an appendix to their solution. This skill provides:

1. **Real-time logging template** for tracking all AI interactions during the competition
2. **Compliant report structure** that meets all COMAP requirements
3. **LaTeX template** for quick report assembly
4. **Verification guidelines** to avoid disqualification triggers

## Why This Matters

### Disqualification Triggers
- ❌ **Undisclosed AI Use**: Using AI without reporting = Academic dishonesty
- ❌ **Fake Citations**: Including AI-generated "hallucinated" citations
- ❌ **Unverified Content**: Submitting AI output without human verification
- ❌ **Incomplete Disclosure**: Reporting some but not all AI use

### Trust Building
- ✅ Transparent disclosure builds judge trust
- ✅ Detailed verification notes demonstrate human oversight
- ✅ Proper reporting shows academic integrity
- ✅ Compliance is expected for O-Award consideration

## Quick Start (5 Minutes)

### Step 1: Set Up Log (Hour 0 of Competition)
1. Open `references/log-template.md`
2. Create `ai_usage_log.md` in your project
3. Assign one team member as "AI Logger"

### Step 2: Log Throughout Competition (Hours 0-92)
For each AI interaction:
1. Copy log entry template
2. Paste exact prompt (don't paraphrase)
3. Paste complete output
4. Write specific verification notes
5. Estimate percentage used

**Time per log**: 2-3 minutes

### Step 3: Assemble Report (Hour 92-93)
1. Open `assets/ai_report_template.tex`
2. Convert log entries to LaTeX format
3. Generate summary table
4. Add integrity statement
5. Compile to PDF

**Time required**: 1 hour

## File Structure

```
ai-report-writer/
├── SKILL.md                          # Main instructions (comprehensive guide)
├── README.md                         # This file (quick overview)
├── references/
│   ├── comap-policy.md              # Official COMAP requirements
│   ├── log-template.md              # Detailed logging guide with examples
│   └── quick-reference.md           # 1-page cheat sheet
└── assets/
    └── ai_report_template.tex       # Complete LaTeX template
```

## What to Log

### MUST Log ✅
- **LLMs**: ChatGPT, Claude, Gemini, Llama
- **Translation**: DeepL, Google Translate, Baidu Fanyi
- **Code Copilots**: GitHub Copilot, Cursor, Tabnine
- **Math AI**: Wolfram Alpha AI mode
- **Writing AI**: Grammarly AI (for major rewrites)

### Do NOT Log ❌
- Standard calculators (non-AI)
- Google Scholar searches (not AI)
- numpy, scipy libraries (unless using AI code completion)
- Your own manual work

## Report Structure (5 Required Sections)

### 1. Usage Overview
Summary table of all AI tools used

### 2. Detailed LLM Logs
For each interaction:
- Time
- Exact query (copy-paste)
- Complete output (copy-paste)
- Verification notes (specific)
- Revision notes (specific)
- Final usage (percentage)

### 3. Translation Tools
Usage statement and proofreading notes  
*Note: Full input text NOT required*

### 4. Code Copilots
File locations and verification notes

### 5. Integrity Statement
Formal declaration of:
- Verified all AI content
- No fake citations
- Human-led critical decisions
- Full responsibility
- Complete disclosure

## Time Budget

| Phase | Activity | Time | When |
|-------|----------|------|------|
| Setup | Create log template | 5 min | Hour 0 |
| Logging | Record each AI interaction | 2-3 min each | Hours 0-92 |
| Total Logging | All interactions | 1-2 hours | Spread over 4 days |
| Assembly | Convert log to LaTeX | 45 min | Hour 92 |
| Proofreading | Verify completeness | 15 min | Hour 93 |
| Integration | Add to main paper | 10 min | Hour 94 |
| **Total** | | **2-3 hours** | |

## Common Mistakes to Avoid

### ❌ Mistake 1: Paraphrasing Prompts
**Bad**: "We asked ChatGPT to help with the introduction"  
**Good**: [Paste exact prompt used]

### ❌ Mistake 2: Generic Verification
**Bad**: "We checked it and it's fine"  
**Good**: "Verified citation [Smith 2020] exists in Google Scholar, DOI: 10.1234/example"

### ❌ Mistake 3: Waiting Until Hour 95
**Bad**: Start report at Hour 95, rush and make errors  
**Good**: Start report assembly at Hour 92, leave time for errors

### ❌ Mistake 4: Forgetting to Log
**Bad**: Use AI, plan to "remember later"  
**Good**: Log immediately after each interaction

## Pro Tips

1. **Log Immediately**: Memory fades fast, exact prompts are hard to recall
2. **Be Honest**: Transparency builds trust with judges
3. **Be Specific**: Generic verification notes look suspicious
4. **Start Early**: Don't wait until Hour 95 to create report
5. **Use Templates**: Save time with pre-made structures
6. **Assign Roles**: One person enforces logging discipline
7. **Over-Report**: When in doubt, include it

## Integration with Competition Workflow

### Hours 0-24 (Problem Analysis)
- Set up log template
- Log any AI used for literature search or brainstorming

### Hours 24-60 (Model Building)
- Log AI used for code generation or debugging
- Log AI used for mathematical derivations

### Hours 60-84 (Results & Writing)
- Log AI used for polishing text
- Log AI used for visualization code

### Hours 84-92 (Final Polish)
- Log AI used for Summary Sheet polish
- Continue logging until competition end

### Hours 92-93 (Report Assembly) 🚨 CRITICAL
- Convert log to LaTeX report
- Generate summary table
- Add integrity statement
- Proofread

### Hours 94-96 (Final Submission)
- Add AI citations to main paper
- Merge AI report with main paper PDF
- Verify completeness
- Submit

## Success Criteria

Your AI report is complete when:
- [ ] All AI use is disclosed (no omissions)
- [ ] Prompts are exact (copy-pasted)
- [ ] Outputs are complete (not summarized, except translations)
- [ ] Verification notes are specific (not generic)
- [ ] Integrity statement is signed
- [ ] Report compiles to PDF without errors
- [ ] Report is merged with main paper
- [ ] AI citations are in main paper references

## Getting Help

### Read These Files First
1. `references/quick-reference.md` - 1-page cheat sheet
2. `references/log-template.md` - Detailed examples
3. `SKILL.md` - Complete instructions

### Common Questions

**Q: Do I need to report basic grammar checks?**  
A: If it's non-AI (basic spell check), no. If it's AI-powered (Grammarly AI suggestions for major rewrites), yes.

**Q: What if I forget to log some interactions?**  
A: Reconstruct from memory (check browser history, chat logs). Note in report: "Reconstructed from memory." Better to disclose imperfectly than not at all.

**Q: How detailed should verification notes be?**  
A: Very detailed. Instead of "we checked it," say "we verified citation [Smith 2020] exists in Google Scholar and confirmed the formula on page 45 matches our implementation."

**Q: Can I use AI to help write the AI report?**  
A: Yes, but you must log that interaction too! (Meta-logging)

**Q: What if I'm running out of time?**  
A: Use the LaTeX template to speed up. Focus on completeness over polish. A complete report is better than a perfect paper without a report.

## Version History

- **v1.0** (2026-01-29): Initial release
  - Complete SKILL.md with two-phase workflow
  - COMAP policy reference document
  - Detailed log template with examples
  - Quick reference card
  - LaTeX report template

## License

This skill is provided for MCM/ICM competition use. Please refer to the main repository LICENSE for full terms.

---

**Remember**: The AI report is not a penalty. It's proof of integrity. Transparent teams are trusted teams. 🏆
