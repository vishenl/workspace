# Mindvalley Outcomes Simplification Project

**Complete analysis framework and tools for reducing Mindvalley Outcomes from 200-300 to 80-150**

---

## Quick Start

### For Technical Users (Automated Approach)

```bash
# 1. Set your Airtable API key
export AIRTABLE_API_KEY="your_key_here"

# 2. Run the analysis script
cd /Users/vishen/Documents/Github/workspace
python3 scripts/fetch-and-analyze-outcomes.py

# 3. Review the output
# - Console will show detailed report
# - outcome-updates.json will contain batch updates

# 4. Apply updates using MCP tools (see strategy doc)
```

**Time:** 1-2 days
**Output:** Automated recommendations with usage data

### For Non-Technical Users (Manual Approach)

1. Open the Manual Analysis Guide: `/reports/outcomes-manual-analysis-guide.md`
2. Follow the step-by-step process
3. Use Airtable filters and batch updates
4. Track progress using the CSV template

**Time:** 4-5 days
**Output:** Manual recommendations with full control

---

## Project Structure

```
workspace/
├── reports/
│   ├── README-OUTCOMES-ANALYSIS.md          ← You are here
│   ├── outcomes-analysis-executive-summary.md   ← Start here for overview
│   ├── outcomes-simplification-strategy.md      ← Complete methodology
│   ├── outcomes-manual-analysis-guide.md        ← Step-by-step process
│   └── outcomes-analysis-template.csv          ← Progress tracking template
│
└── scripts/
    ├── fetch-and-analyze-outcomes.py           ← Main analysis script
    ├── analyze-outcomes.py                     ← Core analysis logic
    ├── outcomes-analyzer.py                    ← Extended analyzer
    └── process-outcomes-analysis.sh            ← Bash wrapper
```

---

## Documents Overview

### 1. Executive Summary
**File:** `outcomes-analysis-executive-summary.md`
**Purpose:** High-level overview for stakeholders
**Contents:**
- Key findings and recommendations
- Expected results (40-60% reduction)
- Implementation plan (6-8 days)
- Risk assessment
- Resource requirements

**Read this first** if you need to understand the project at a glance or present to stakeholders.

### 2. Simplification Strategy
**File:** `outcomes-simplification-strategy.md`
**Purpose:** Complete methodology and framework
**Contents:**
- Detailed deletion criteria
- Detailed merge criteria
- 30 semantic groups with examples
- Implementation process (5 phases)
- Example merge scenarios
- Quality assurance checklist
- Tools and scripts documentation

**Read this** for the complete technical approach and methodology.

### 3. Manual Analysis Guide
**File:** `outcomes-manual-analysis-guide.md`
**Purpose:** Step-by-step instructions for manual analysis
**Contents:**
- Quick start checklist
- Phase-by-phase process
- All 30 semantic groups with search terms
- Decision tree for each outcome
- Batch update workflow
- Quality control checklist
- Example work session (2 hours)
- Progress tracking

**Use this** if you're doing manual analysis in Airtable interface.

### 4. Analysis Template
**File:** `outcomes-analysis-template.csv`
**Purpose:** Track your progress
**Contents:**
- CSV template with all necessary columns
- Example entries showing format
- Can be imported into Excel/Google Sheets

**Use this** to track which outcomes you've reviewed and your decisions.

---

## Analysis Criteria Summary

### Deletion (Zero Usage)
```
IF Program Count = 0
   AND Meditation Count = 0
   AND Audio Count = 0
THEN UPDATE TYPE = "Deleted"
     UPDATE NOTE = "No usage: Program Count=0, Meditation Count=0, Audio Count=0"
```

### Deletion (Low Usage)
```
IF (Program Count + Meditation Count + Audio Count) <= 2
THEN UPDATE TYPE = "Deleted"
     UPDATE NOTE = "Low usage: Total=X (Program=Y, Meditation=Z, Audio=W)"
```

### Merge (Semantic Similarity)
```
IF Outcome matches semantic group
   AND NOT highest usage in group
THEN UPDATE TYPE = "Merged"
     UPDATE NOTE = "Merge into '[Primary]' (usage=X). Current usage=Y. Semantic group: [terms]"
```

---

## Semantic Groups Quick Reference

30 semantic groups identified for merge analysis:

**Emotional States:**
1. Stress/Anxiety/Worry
2. Happiness/Joy/Bliss
3. Calm/Peace/Serenity
4. Anger/Frustration
5. Fear/Scared
6. Sadness/Depression
7. Love/Loving

**Cognitive States:**
8. Focus/Concentration
9. Clarity/Clear-thinking
10. Mindfulness/Presence
11. Creativity/Innovation

**Physical States:**
12. Energy/Vitality
13. Relaxation/Rest
14. Sleep/Sleeping
15. Pain/Pain relief
16. Healing/Recovery

**Personal Development:**
17. Confidence/Self-esteem
18. Motivation/Drive
19. Resilience/Strength
20. Self-awareness
21. Purpose/Meaning

**Interpersonal:**
22. Gratitude/Appreciation
23. Compassion/Empathy
24. Connection/Belonging
25. Forgiveness/Release

**Spiritual/Material:**
26. Spiritual/Spirituality
27. Intuition/Wisdom
28. Abundance/Prosperity
29. Success/Achievement
30. Balance/Harmony

---

## Expected Results

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total Outcomes | 200-300 | 80-150 | -40% to -60% |
| Zero Usage | 40-60 | 0 | -100% |
| Low Usage (≤2) | 30-50 | 0 | -100% |
| Semantic Duplicates | 50-80 | 10-20 | -70% to -80% |

---

## Implementation Timeline

### Automated Approach (1-2 days)
- **Day 1 AM:** Run Python script, review recommendations
- **Day 1 PM:** Stakeholder review and approval
- **Day 2 AM:** Apply batch updates via MCP tools
- **Day 2 PM:** Validate results

### Manual Approach (4-5 days)
- **Day 1:** Setup + Zero usage deletions (~40-60 outcomes)
- **Day 2:** Low usage deletions (~30-50 outcomes)
- **Day 3:** Semantic groups 1-15 (~25-40 merges)
- **Day 4:** Semantic groups 16-30 (~25-40 merges)
- **Day 5:** Review + quality control

### Content Migration (2-3 days)
- Update Programs to use primary outcomes
- Update Meditations to use primary outcomes
- Update Audios to use primary outcomes
- Verify all references updated

**Total Time:**
- Automated: 3-5 days (including migration)
- Manual: 6-8 days (including migration)

---

## Airtable Information

### Base & Table
- **Base ID:** app4ulN4GnBRvcfAL
- **Base Name:** Mindvalley Brain
- **Table ID:** tblLA13fGO7KM1JHA
- **Table Name:** 🪽Outcomes
- **Recommended View:** 🔧 by AOG (viwoAhFaw8vu6ADUm)

### Key Fields
| Field Name | Field ID | Type | Purpose |
|-----------|----------|------|---------|
| Outcome | fldCP33pFkB25Ynee | Single Line Text | Outcome name |
| Program Count | fldE9oQRoudmUiZ2I | Count | Number of programs |
| Meditation Count | fldkVIkUgZcbBwkaD | Count | Number of meditations |
| Audio Count | fldTmPvCIb4e2Bm98 | Count | Number of audios |
| Description | fldpAfFrmwipYiYAw | Single Line Text | Outcome description |
| UPDATE TYPE | flddtQoH4JfAU0uTv | Single Select | "Deleted" or "Merged" |
| UPDATE NOTE | fldo4SmxBXYHqOu4R | Single Line Text | Reasoning |

---

## Tools & Scripts

### Python Analysis Script

**File:** `/scripts/fetch-and-analyze-outcomes.py`

**Features:**
- Fetches all outcomes without UPDATE TYPE
- Applies deletion criteria automatically
- Identifies semantic groups
- Generates merge recommendations
- Outputs detailed console report
- Creates `outcome-updates.json` for batch processing

**Requirements:**
- Python 3.x
- `requests` library (`pip install requests`)
- AIRTABLE_API_KEY environment variable

**Usage:**
```bash
export AIRTABLE_API_KEY="your_key"
python3 scripts/fetch-and-analyze-outcomes.py
```

**Output:**
```
Fetching outcomes from Airtable...
  Fetched 100 records so far...
  Fetched 200 records so far...
Total outcomes fetched: 247

Analyzing outcomes...

================================================================================
MINDVALLEY OUTCOMES ANALYSIS REPORT
================================================================================

Total outcomes analyzed: 247
Recommended for DELETION: 89
Recommended for MERGE: 63
To KEEP: 95

Estimated final count: 95
Reduction: 152 outcomes (61.5%)

[... detailed breakdown follows ...]
```

### Support Scripts

1. **analyze-outcomes.py** - Core analysis logic
2. **outcomes-analyzer.py** - Extended analyzer with detailed grouping
3. **process-outcomes-analysis.sh** - Bash wrapper for automation

---

## Workflow Examples

### Example 1: Zero Usage Deletion

**Before:**
```
Outcome: "Reduce procrastination"
Program Count: 0
Meditation Count: 0
Audio Count: 0
UPDATE TYPE: [blank]
```

**After:**
```
Outcome: "Reduce procrastination"
Program Count: 0
Meditation Count: 0
Audio Count: 0
UPDATE TYPE: "Deleted"
UPDATE NOTE: "No usage: Program Count=0, Meditation Count=0, Audio Count=0"
```

### Example 2: Semantic Merge

**Before:**
```
Outcome A: "Reduce stress" (Program=8, Meditation=15, Audio=12) Total: 35
Outcome B: "Manage anxiety" (Program=3, Meditation=7, Audio=4) Total: 14
Outcome C: "Less worry" (Program=1, Meditation=3, Audio=2) Total: 6
```

**After:**
```
Outcome A: "Reduce stress" (Primary) - KEEP
UPDATE TYPE: [blank]

Outcome B: "Manage anxiety" - MERGE
UPDATE TYPE: "Merged"
UPDATE NOTE: "Merge into 'Reduce stress' (usage=35). Current usage=14. Semantic group: stress/anxiety/worry"

Outcome C: "Less worry" - MERGE
UPDATE TYPE: "Merged"
UPDATE NOTE: "Merge into 'Reduce stress' (usage=35). Current usage=6. Semantic group: stress/anxiety/worry"
```

**Result:** 3 outcomes → 1 outcome (66% reduction in this group)

---

## Quality Assurance

### Before Finalizing

- [ ] All zero-usage outcomes reviewed
- [ ] All low-usage outcomes reviewed
- [ ] Semantic groupings validated
- [ ] Primary selections confirmed (highest usage)
- [ ] UPDATE NOTEs are clear and specific
- [ ] No strategic outcomes accidentally deleted
- [ ] Stakeholder approval obtained

### After Updates

- [ ] All UPDATE TYPEs set correctly
- [ ] All UPDATE NOTEs present and clear
- [ ] Spot-check 20 random updates
- [ ] Verify no unexpected outcomes marked
- [ ] Document any edge cases or exceptions

---

## Common Questions

### Q: What if an outcome has zero usage but is strategically important?

**A:** Mark it with a note "Strategic outcome - new feature pending" and skip the deletion. Review again in 30 days.

### Q: Should "fall asleep faster" merge with "better sleep"?

**A:** No - this is specific enough to warrant separate outcome. Keep both if both have >5 usage.

### Q: What if two outcomes have same usage?

**A:** Choose the one with clearer, more intuitive name as primary.

### Q: Can I undo a merge?

**A:** Yes - outcomes are soft-deleted (marked but not removed). Can be reverted within 30 days.

### Q: How do I handle outcomes with identical descriptions?

**A:** Always merge these - they're true duplicates. Keep the one with better name or higher usage.

---

## Success Metrics

Track these metrics before and after:

### Quantitative
- Total outcomes count
- Outcomes with zero usage
- Outcomes with ≤2 usage
- Number of semantic groups with multiple outcomes
- Average usage per outcome

### Qualitative
- User feedback on outcome selection
- Content team feedback on management
- Data team feedback on analytics

### Operational
- Time to find relevant outcome
- Number of outcome-related support tickets
- Outcome creation rate (should slow)

---

## Next Steps

1. **Choose Your Approach:**
   - Technical/Fast: Use Python script
   - Manual/Control: Use manual guide

2. **Review Documentation:**
   - Read executive summary for overview
   - Read strategy for methodology
   - Read manual guide for process

3. **Setup:**
   - Get Airtable access
   - Set up API key (if automated)
   - Download CSV template

4. **Execute:**
   - Run analysis
   - Review results
   - Get approval
   - Apply updates

5. **Validate:**
   - Check results
   - Migrate content
   - Document learnings
   - Establish governance

---

## Support & Resources

### Documentation
- All documents in `/reports/` directory
- All scripts in `/scripts/` directory
- CSV template for tracking

### Technical Support
- For script issues: Check Python version and dependencies
- For Airtable issues: Verify API key and permissions
- For MCP issues: Check MCP Airtable tool availability

### Process Support
- Refer to manual analysis guide for step-by-step
- Use decision tree for edge cases
- Document unusual situations for team review

---

## Project Status

**Current State:** Analysis framework complete
**Deliverables:** All documentation and scripts ready
**Next Step:** Choose approach and begin analysis
**Timeline:** 6-12 days to complete depending on approach

---

## Version History

- **v1.0** (2025-11-11): Initial analysis framework complete
  - Executive summary created
  - Strategy document created
  - Manual guide created
  - Python scripts created
  - CSV template created

---

## Contact

For questions or support:
- **Data/Analytics Team:** Usage analysis and metrics
- **Content Team:** Outcome definitions and migrations
- **Product Team:** User experience impact assessment
- **Technical Team:** Script execution and automation

---

**Ready to begin?** Start with the Executive Summary for overview, then choose your approach (automated vs manual) and dive in!

