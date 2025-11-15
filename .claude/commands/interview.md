---
allowed-tools: Bash(code-tools:*), Read, Grep, Glob, Write, Edit, WebFetch, mcp__sequential-thinking__sequentialthinking, AskUserQuestion
argument-hint: [vague prompt to interview about]
description: Interactively clarify and refine vague prompts through structured questioning and iterative refinement until production-ready
---

# Optimized Prompt: Structured Prompt Refinement Interview System

<objective>
Transform vague or ambiguous user prompts into production-ready, unambiguous prompts through structured analysis, targeted questioning, iterative refinement, and verification.
</objective>

<context>
- **Target audience**: Users submitting incomplete or unclear prompt requests
- **Expected input**: Any prompt ranging from vague ideas to partially-formed instructions
- **Success metric**: Final prompt achieves clarity score ≥ 8/10
- **Maximum interaction cycles**: 3 clarification rounds before forcing decision
- **Scope**: Generic prompt optimization (coding, analysis, creative, etc.)
</context>

<instructions>

## Phase 1: Initial Analysis (Chain of Thought)

**REQUIRED**: Use `mcp__sequential-thinking__sequentialthinking` tool for this analysis.

Analyze the user's prompt and output:

```
TASK: [One-sentence description of core goal]

AMBIGUITIES:
1. [Specific unclear element #1]
2. [Specific unclear element #2]
3. [etc., maximum 5 items]

MISSING:
- Context: [What background information is absent]
- Constraints: [Unspecified limitations or requirements]
- Output format: [Undefined deliverable structure]
- Success criteria: [Missing measurability/validation]

CLARITY: [X]/10
```

**Scoring guide**:
- 0-3: Fundamentally unclear goal
- 4-5: Goal clear but major gaps in execution details
- 6-7: Mostly clear with minor ambiguities
- 8-10: Production-ready (no refinement needed)

## Phase 2: Iterative Clarification (if clarity < 8)

**REQUIRED**: Use `AskUserQuestion` tool for each clarification round.

**Rules**:
- Ask **1 targeted question per turn**
- Provide **3-4 specific answer options** (always include "Other (specify)")
- After each answer, **re-run sequential thinking** to update understanding
- Recalculate clarity score after each response
- **Stop when**: clarity ≥ 8 OR 3 rounds completed

**Question template**:
```
**Regarding [specific ambiguity from Phase 1]:**

Which approach should be used?

A) [Concrete option 1 with brief context]
B) [Concrete option 2 with brief context]
C) [Concrete option 3 with brief context]
D) Other (please specify)
```

**After each answer**:
1. Use sequential thinking to integrate the new information
2. Update clarity score
3. If clarity < 8 AND rounds < 3, proceed to next question
4. If 3 rounds reached without clarity ≥ 8, **flag unresolved ambiguities** and proceed to Phase 3

## Phase 3: Refactored Prompt Generation

Generate the optimized prompt with **mandatory sections**:

```markdown
<role>
[Clearly defined persona/expertise if applicable, otherwise omit]
</role>

<objective>
[Specific, measurable goal in 1-2 sentences]
</objective>

<context>
- [Relevant background information]
- [Constraints: scope, length, format, etc.]
- [Assumptions explicitly stated]
</context>

<instructions>
1. [Step-by-step directive #1]
2. [Step-by-step directive #2]
[etc.]
</instructions>

<output_format>
[Exact structure of expected deliverable: format, sections, examples]
</output_format>

<success_criteria>
- [Measurable criterion #1]
- [Measurable criterion #2]
[etc.]
</success_criteria>
```

**Requirements**:
- Use XML-style tags for section separation
- Include **only** sections with confirmed information
- Preserve 100% of user's original intent
- Remove all identified ambiguities
- Add explicit constraints discussed in Phase 2

## Phase 4: Verification (Chain of Verification)

Present the refactored prompt with:

```markdown
## Changes Made
- [Specific change #1]
- [Specific change #2]
- [Specific change #3]
[3-5 bullet points total]

## Verification Checklist
- [ ] Preserves original intent (no goal drift)
- [ ] Eliminates all identified ambiguities from Phase 1
- [ ] Includes measurable success criteria
- [ ] Specifies explicit output format
- [ ] States assumptions/constraints explicitly

## Refactored Prompt
[Insert full prompt from Phase 3 in code block]
```

**REQUIRED**: Use `AskUserQuestion` tool to ask:
```
**Review the refactored prompt above.**

What would you like to do?

A) Approve - Use this prompt as-is
B) Revise - Request specific changes (please specify)
C) Clarify - Ask follow-up questions about the refactored version
```

**If unresolved ambiguities exist** (3-round limit reached):
- Add a **"FLAGGED AMBIGUITIES"** section before the verification checklist
- List each unresolved item with: `⚠️ [Ambiguity description] - Assumed: [your default assumption]`

</instructions>

<output_format>
- **Phase 1**: Structured analysis output (TASK/AMBIGUITIES/MISSING/CLARITY format)
- **Phase 2**: Series of single questions with 3-4 options, interleaved with updated clarity scores
- **Phase 3**: Complete refactored prompt using XML-tagged sections
- **Phase 4**: Changes summary + verification checklist + final prompt in code block
</output_format>

<constraints>
- **NEVER invent requirements** not explicitly stated or confirmed by user
- **NEVER proceed to Phase 3** if clarity < 6 after 3 rounds (flag as unresolvable)
- **ALWAYS use tools**: Sequential thinking for analysis, AskUserQuestion for clarification
- **MAXIMUM verbosity per phase**: 200 words (excluding prompt examples)
</constraints>

<examples>

**Example Phase 1 Output**:
```
TASK: Create a Python script for data processing

AMBIGUITIES:
1. Data source format (CSV/JSON/API/database)
2. Processing operations (cleaning/transformation/analysis)
3. Error handling requirements

MISSING:
- Context: Data size, performance requirements
- Constraints: Libraries/dependencies, Python version
- Output format: Console output vs file export vs API response
- Success criteria: Validation tests, performance benchmarks

CLARITY: 4/10
```

**Example Phase 2 Question**:
```
**Regarding data source format:**

What type of data will the script process?

A) CSV files from local filesystem
B) JSON from REST API endpoints
C) SQL database queries
D) Other (please specify)
```

</examples>

---

**User's prompt to refine:** $ARGUMENTS
