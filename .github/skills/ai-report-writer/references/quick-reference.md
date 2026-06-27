# AI Report Quick Reference Card

## 🚨 Critical Reminders

### Must-Do Actions
- ✅ **Log immediately** after each AI interaction (don't wait)
- ✅ **Copy-paste exact prompts** (never paraphrase)
- ✅ **Verify all AI-generated citations** (check Google Scholar)
- ✅ **Report ALL AI use** (including translation, code copilots)
- ✅ **Start report assembly at Hour 92** (not Hour 95!)

### Disqualification Triggers
- ❌ Undisclosed AI use
- ❌ Fake/hallucinated citations
- ❌ Unverified AI content
- ❌ Plagiarized AI-generated text

---

## 📋 Two-Phase Workflow

### Phase 1: Real-Time Logging (Hours 0-92)
**Time per log entry**: 2-3 minutes
**Total time**: ~1-2 hours spread over 4 days

**Actions**:
1. Create log file at Hour 0
2. Log every AI interaction immediately
3. Use template: Time → Query → Output → Verification

### Phase 2: Report Assembly (Hours 92-96)
**Time budget**: 1 hour (Hour 92-93)

**Actions**:
1. Convert log to LaTeX (45 min)
2. Create summary table (10 min)
3. Write integrity statement (5 min)
4. Proofread (10 min)

---

## 📝 Log Entry Checklist

For each AI interaction, record:
- [ ] **Time**: YYYY-MM-DD HH:MM
- [ ] **Tool/Model**: Full name + version
- [ ] **Type**: LLM / Translation / Code Copilot / Other
- [ ] **Purpose**: Why you used it
- [ ] **Location**: Where in paper/code
- [ ] **Query**: Exact prompt (copy-paste)
- [ ] **Output**: Full response (copy-paste)
- [ ] **Verified**: Specific checks performed
- [ ] **Revised**: Specific changes made
- [ ] **Final Usage**: How much used (percentage)

---

## 🎯 What to Log

### MUST Log ✅
| Category | Examples |
|----------|----------|
| **LLMs** | ChatGPT, Claude, Gemini, Llama |
| **Translation** | DeepL, Google Translate, Baidu Fanyi |
| **Code Copilots** | GitHub Copilot, Cursor, Tabnine |
| **Math AI** | Wolfram Alpha AI mode |
| **Writing AI** | Grammarly AI (major rewrites) |

### Do NOT Log ❌
| Category | Examples |
|----------|----------|
| **Search Engines** | Google Scholar, Web of Science |
| **Calculators** | Standard calculators (non-AI) |
| **Standard Libraries** | numpy, scipy (unless using AI code completion) |
| **Manual Work** | Your own code, writing, analysis |

---

## 📄 Report Structure (5 Sections)

### Section 1: Usage Overview
**Format**: Summary table
**Content**: All tools used (one row per tool)

### Section 2: Detailed LLM Logs
**Format**: Interaction logs
**Content**: Every LLM interaction with full prompts/outputs

**Required for each interaction**:
- Time
- Exact query
- Complete output
- Verification (what you checked)
- Revision (what you changed)
- Final usage (how much used)

### Section 3: Translation Tools
**Format**: Usage statement
**Content**: What was translated, proofreading notes

**Special rule**: Full input text NOT required

### Section 4: Code Copilots
**Format**: Usage description
**Content**: File locations, verification notes

### Section 5: Integrity Statement
**Format**: Formal declaration
**Content**: 
- Verified all AI content
- No fake citations
- Human-led critical decisions
- Full responsibility
- Complete disclosure

---

## ⚡ Time-Saving Tips

### During Competition
1. **Use shared log file** (Google Docs, Overleaf)
2. **Assign "AI Logger"** role to one team member
3. **Set rule**: "No AI use without logging"
4. **Keep template handy** for quick copy-paste

### Hour 92-93 (Report Assembly)
1. **Use LaTeX template** (assets/ai_report_template.tex)
2. **Group by tool type** (LLM, Translation, Code)
3. **Generate summary table** from log entries
4. **Proofread for completeness**

---

## 🔍 Verification Best Practices

### For LLM Text
- [ ] Check all citations exist (Google Scholar)
- [ ] Verify facts against original sources
- [ ] Confirm formulas match references
- [ ] Ensure no plagiarism (run through Turnitin if available)

### For LLM Code
- [ ] Test with sample data
- [ ] Verify logic matches your model
- [ ] Check edge cases
- [ ] Add error handling

### For Translations
- [ ] Cross-check technical terms with dictionaries
- [ ] Verify logical consistency with original
- [ ] Confirm terminology matches English literature

---

## 📊 Verification Note Quality

### ❌ Generic (Bad)
- "We checked it"
- "We verified the output"
- "It looks correct"

### ✅ Specific (Good)
- "Verified citation [Smith 2020] exists in Google Scholar, DOI: 10.1234/example"
- "Tested function on 100 sample data points, output matched manual calculation"
- "Cross-checked formula with original paper [Jones 2019, p. 45], confirmed match"

---

## 🎓 Special Cases

### Multiple Similar Interactions
If you have 10+ similar interactions (e.g., debugging sessions):
- Group them in log
- Provide one representative example
- Summarize verification across all

### Very Long Outputs
If AI output is >1000 words:
- Include full text in log
- Add brief summary in "Final Usage"
- Highlight key parts that were used

### Translation Tools
- Full input text NOT required
- Provide usage statement (what, how much)
- Include proofreading notes

### Code Copilots
- List file paths and line numbers
- Estimate percentage (human vs. AI)
- Describe testing and modifications

---

## 🚀 Hour-by-Hour Guide

### Hour 0 (Competition Start)
- [ ] Create log file (5 min)
- [ ] Share with team (Google Docs)
- [ ] Assign AI Logger role

### Hours 0-92 (Throughout Competition)
- [ ] Log every AI interaction (2-3 min each)
- [ ] Verify AI content immediately
- [ ] Keep log updated in real-time

### Hour 92 (Report Assembly Start)
- [ ] Review log for completeness (5 min)
- [ ] Start LaTeX conversion (30 min)

### Hour 93 (Report Assembly Continue)
- [ ] Generate summary table (10 min)
- [ ] Write integrity statement (5 min)
- [ ] Proofread report (10 min)

### Hour 94 (Integration)
- [ ] Add AI citations to main paper (15 min)
- [ ] Merge AI report with main paper PDF (10 min)

### Hour 95 (Final Check)
- [ ] Verify report completeness (10 min)
- [ ] Check PDF formatting (5 min)

### Hour 96 (Submission)
- [ ] Submit!

---

## 📞 Emergency Troubleshooting

### Problem: Forgot to log some AI interactions
**Solution**: 
1. Recall as much as possible (check browser history, chat logs)
2. Note in report: "Reconstructed from memory, may not be exact"
3. Better to disclose imperfectly than not at all

### Problem: AI generated fake citation
**Solution**:
1. Remove citation from paper immediately
2. Find real citation to replace it
3. Note in report: "Detected hallucinated citation, replaced with verified source"

### Problem: Running out of time at Hour 95
**Solution**:
1. Use template to speed up (assets/ai_report_template.tex)
2. Focus on completeness over polish
3. Ensure integrity statement is included
4. Better to submit complete report than perfect paper without report

### Problem: Unsure if tool counts as "AI"
**Solution**:
- **When in doubt, report it**
- Over-reporting is safe, under-reporting is risky
- COMAP prefers transparency

---

## 🏆 Quality Standards

### Minimum Acceptable
- All AI use disclosed
- Exact prompts included
- Basic verification notes
- Integrity statement signed

### Good Quality
- Detailed verification notes
- Specific revision descriptions
- Percentage estimates of usage
- Well-organized structure

### Excellent Quality (O-Award Level)
- Comprehensive logging
- Specific verification with sources
- Quantified usage percentages
- Demonstrates deep human oversight
- Shows critical thinking about AI outputs

---

## 📚 Key Files

### In Skill Package
- `SKILL.md` - Main instructions
- `references/comap-policy.md` - Official COMAP requirements
- `references/log-template.md` - Detailed logging guide
- `references/quick-reference.md` - This file
- `assets/ai_report_template.tex` - LaTeX template

### To Create During Competition
- `ai_usage_log.md` - Your real-time log (working document)
- `ai_report.tex` - Final LaTeX report (generated at Hour 92)
- `ai_report.pdf` - Compiled report (merged with main paper)

---

## 💡 Pro Tips

1. **Log immediately**: Memory fades fast, exact prompts are hard to recall
2. **Be honest**: Transparency builds trust with judges
3. **Be specific**: Generic verification notes look suspicious
4. **Start early**: Don't wait until Hour 95 to create report
5. **Use templates**: Save time with pre-made structures
6. **Assign roles**: One person enforces logging discipline
7. **Test compile**: Verify LaTeX compiles at Hour 93, not Hour 95
8. **Over-report**: When in doubt, include it

---

## 🎯 Success Criteria

Your AI report is complete when:
- [ ] All AI use is disclosed (no omissions)
- [ ] Prompts are exact (copy-pasted)
- [ ] Outputs are complete (not summarized)
- [ ] Verification notes are specific (not generic)
- [ ] Integrity statement is signed
- [ ] Report compiles to PDF without errors
- [ ] Report is merged with main paper
- [ ] AI citations are in main paper references

---

**Remember**: The AI report is not a penalty. It's proof of integrity. Transparent teams are trusted teams. 🏆
