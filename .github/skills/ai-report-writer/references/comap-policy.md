# COMAP AI Policy - Official Requirements

## Policy Overview

This document contains the official COMAP policy on AI tool usage for MCM/ICM competitions, extracted from official COMAP documentation.

## Core Policy Principles

### 1. Mandatory Disclosure
**Requirement**: All teams must disclose all AI tool usage in a separate "Report on Use of AI Tools" appendix.

**Scope of Disclosure**:
- Large Language Models (ChatGPT, Claude, Gemini, etc.)
- Translation tools (DeepL, Google Translate, etc.)
- Code assistance tools (GitHub Copilot, Cursor, Tabnine, etc.)
- Mathematical software with AI features (Wolfram Alpha AI mode)
- Grammar/writing assistants with AI (Grammarly AI suggestions)
- Any other AI-powered tools used in the solution process

**Exemptions** (do not need to report):
- Standard calculators without AI features
- Traditional search engines (Google, Bing) for literature search
- Standard Python/MATLAB libraries (numpy, scipy) unless using AI-assisted code completion
- Excel formulas without AI "Ideas" feature

### 2. Transparency Requirement
**Requirement**: The more transparent the disclosure, the more the work is trusted.

**What Transparency Means**:
- Exact prompts used (not paraphrased)
- Complete outputs received (not summarized, except for translation tools)
- Specific verification steps taken (not generic statements)
- Honest assessment of how much AI content was used in final submission

**Transparency Benefits**:
- Demonstrates integrity and academic honesty
- Shows human oversight and critical thinking
- Builds trust with judges
- Differentiates from teams that hide AI use

### 3. Human-Centric Principle
**Requirement**: AI is a productivity tool, not a replacement for human creativity and judgment.

**Human Responsibilities** (cannot be delegated to AI):
- Problem understanding and interpretation
- Model selection and justification
- Critical evaluation of AI outputs
- Result interpretation and conclusions
- Creative insights and novel approaches

**Acceptable AI Use**:
- Polishing language and grammar
- Debugging code
- Generating boilerplate code
- Translating non-English sources
- Brainstorming ideas (with human evaluation)

**Unacceptable AI Use**:
- Blindly copying AI-generated solutions without understanding
- Using AI to make critical modeling decisions without human judgment
- Including AI-generated citations without verification
- Submitting AI-generated content as original work without attribution

### 4. Verification and Responsibility
**Requirement**: Teams are 100% responsible for the accuracy of all content, including AI-generated content.

**Verification Obligations**:
- Check all AI-generated citations for authenticity
- Verify factual claims made by AI
- Test all AI-generated code
- Confirm mathematical formulas from AI match original sources
- Ensure AI-generated text does not plagiarize copyrighted material

**Consequences of Non-Verification**:
- Inclusion of "hallucinated" (fake) citations → Disqualification
- Unverified factual errors → Reduced score or disqualification
- Plagiarized content → Disqualification
- Undisclosed AI use → Disqualification

## Report Structure Requirements

### Mandatory Sections

#### Section 1: Usage Overview
**Content**: Summary table of all AI tools used
**Required Fields**:
- Tool/Model name
- Version/Date accessed
- Type (LLM, Translation, Code Copilot, etc.)
- Purpose (why it was used)
- Location (where in the solution)

#### Section 2: Detailed Records of LLM/Generative AI
**Content**: Complete interaction logs for content generation tools
**Required Fields**:
- Tool/Model information
- Time of interaction
- Exact query/prompt
- Complete output
- Verification and revision notes

**Verification Notes Must Include**:
1. What was verified (specific checks performed)
2. What was revised (specific changes made)
3. Final usage (how much of the AI output was actually used)

#### Section 3: Translation Tools
**Content**: Usage statements for translation services
**Required Fields**:
- Tool/Model information
- Usage statement (what was translated, approximate word count)
- Proofreading notes (how translations were verified)

**Special Rule**: Full input text is **not required** for translation tools (to avoid page bloat).

#### Section 4: Code Copilots/Auto-complete/Mathematical Software AI
**Content**: Details of technical assistance tools
**Required Fields**:
- Tool/Model information
- Purpose
- Usage location (file paths, line numbers)
- Verification notes (testing, modifications)

#### Section 5: Integrity, Verification, and Responsibility Statement
**Content**: Formal declaration of human oversight
**Required Elements**:
- Statement that all AI content has been verified
- Confirmation that no hallucinated citations are included
- Declaration that critical decisions were human-led
- Acceptance of full responsibility
- Team member signatures and date

## Citation Requirements

### In Main Paper
**Requirement**: AI tools must be cited in the main 25-page solution where they were used.

**In-Text Citation Example**:
```
The introduction was polished with assistance from ChatGPT [1].
```

**Reference Entry Example**:
```
[1] OpenAI. ChatGPT (GPT-4). Accessed January 29, 2026. 
https://chat.openai.com. Query: "Please polish the following 
paragraph..." Output: [Summarized output].
```

### In Appendix
**Requirement**: Full details must be provided in the "Report on Use of AI Tools" appendix.

**Relationship**: In-text citations point to brief references, appendix provides complete logs.

## Format Requirements

### Placement
- **Location**: After the 25-page solution, before code appendices
- **Order**: Main Paper → AI Report → Code Appendices

### Page Limits
- **AI Report**: No page limit (does not count toward 25-page limit)
- **Main Paper**: 25 pages maximum (excluding appendices)

### Language
- **Standard**: English (as per MCM/ICM requirements)
- **Exception**: If team workflow involved multiple languages, note this in the report

### Content Detail
- **Prompts**: Must be exact wording (copy-pasted)
- **Outputs**: Must be complete for LLMs (not summarized)
- **Verification**: Must be specific (not generic statements)

## Disqualification Triggers

### Automatic Disqualification
The following will result in immediate disqualification:

1. **Undisclosed AI Use**: Using AI tools without reporting them
2. **Fake Citations**: Including AI-generated "hallucinated" citations without verification
3. **Plagiarism**: Submitting AI-generated text that plagiarizes copyrighted sources
4. **False Verification**: Claiming to have verified content that was not actually checked

### Reduced Scores
The following may result in point deductions:

1. **Incomplete Disclosure**: Reporting some but not all AI use
2. **Generic Verification**: Providing vague verification notes (e.g., "we checked it")
3. **Over-Reliance on AI**: Using AI for critical decisions without sufficient human judgment
4. **Poor Integration**: Including AI content that contradicts other parts of the solution

## Best Practices (Recommended by COMAP)

### During Competition
1. **Log Immediately**: Record AI interactions as they happen (don't rely on memory)
2. **Copy-Paste**: Use exact prompts and outputs (don't paraphrase)
3. **Verify Immediately**: Check AI content right away while context is fresh
4. **Be Specific**: Document exact verification steps taken

### Before Submission
1. **Review Completeness**: Ensure all AI use is disclosed
2. **Check Citations**: Verify every AI-generated citation exists
3. **Proofread Report**: Ensure report is clear and professional
4. **Test PDF**: Confirm AI report is properly merged with main paper

### Cultural Mindset
1. **Transparency is Strength**: Honest disclosure demonstrates integrity
2. **AI is a Tool**: Use AI to enhance human work, not replace it
3. **Verification is Key**: Never trust AI blindly
4. **Documentation is Evidence**: Detailed logs prove human oversight

## Policy Evolution

### Historical Context
- **2023 and Earlier**: No formal AI reporting requirement
- **2024**: First year of mandatory AI usage reports
- **2025**: Refined requirements based on 2024 experience
- **2026**: Current policy (as documented here)

### Future Expectations
COMAP may update this policy as AI technology evolves. Teams should:
- Check official COMAP website for latest policy updates
- Review contest rules carefully each year
- When in doubt, over-report rather than under-report

## Official Resources

### COMAP Official Documents
- Contest Rules: https://www.comap.com/contests/mcm-icm
- AI Policy Statement: [Provided in contest materials]
- Report Template: [Available on contest website]

### Contact for Questions
- COMAP Support: info@comap.com
- Contest Coordinator: [Listed in contest materials]

---

**Last Updated**: 2026-01-29 (Based on MCM/ICM 2026 official policy)
**Source**: COMAP Official Contest Rules and AI Policy Documents
