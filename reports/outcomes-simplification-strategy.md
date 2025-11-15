# Mindvalley Outcomes Simplification Strategy

**Date:** November 11, 2025
**Objective:** Reduce outcomes from 200-300 to a more manageable number through systematic deletion and merging

## Executive Summary

This document provides a comprehensive strategy for simplifying the Mindvalley Outcomes table (SARE) based on usage metrics and semantic similarity analysis.

**Target:** Reduce outcomes by 40-60% through:
- **Deletion:** Remove outcomes with no or very low usage (≤2 total uses)
- **Merging:** Consolidate semantically similar outcomes into primary outcomes with highest usage

---

## Analysis Criteria

### 1. DELETION CRITERIA

Mark `UPDATE TYPE` as "Deleted" if:

- **Zero Usage:** `Program Count = 0 AND Meditation Count = 0 AND Audio Count = 0`
- **Very Low Usage:** Total usage `(Program + Meditation + Audio Count) ≤ 2`

**Rationale:** Outcomes with no usage provide no value and can be safely removed. Outcomes with ≤2 uses likely represent:
- Experimental outcomes that didn't gain traction
- Duplicate variations that split usage
- Over-specific outcomes that should be generalized

### 2. MERGE CRITERIA

Mark `UPDATE TYPE` as "Merged" if:

- **Identical Descriptions:** Two outcomes have the exact same description
- **Semantic Similarity:** Outcomes belong to the same semantic group (see below)
- **Primary Selection:** When merging, the outcome with the highest usage becomes the primary

**Merge Process:**
1. Identify semantically similar outcomes
2. Calculate total usage for each
3. Select highest usage as primary
4. Mark others for merge with note pointing to primary

---

## Semantic Groups for Merge Analysis

These groups represent outcomes that express similar concepts and should be evaluated for merging:

### Emotional States

1. **Stress/Tension Group**
   - stress, anxiety, worry, tension, anxious, worried, tense, stressed

2. **Happiness/Joy Group**
   - happiness, joy, bliss, contentment, happy, joyful, blissful, content

3. **Calm/Peace Group**
   - calm, peace, tranquility, serenity, peaceful, tranquil, serene, calmness

4. **Anger/Frustration Group**
   - anger, frustration, irritation, angry, frustrated, irritated

5. **Fear Group**
   - fear, scared, frightened, afraid, fearful

6. **Sadness Group**
   - sadness, depression, melancholy, sad, depressed

7. **Love Group**
   - love, loving, self-love, loving-kindness

### Cognitive States

8. **Focus/Concentration Group**
   - focus, concentration, attention, focused, concentrate, attentive

9. **Clarity Group**
   - clarity, clear-thinking, mental clarity, clear, clearness

10. **Mindfulness/Presence Group**
    - mindfulness, presence, awareness, mindful, present, aware

11. **Creativity Group**
    - creativity, innovation, imagination, creative, innovative, imaginative

### Physical States

12. **Energy Group**
    - energy, vitality, vigor, energized, energetic, vital, vigorous

13. **Relaxation/Rest Group**
    - relaxation, rest, recovery, relax, relaxed, rested, recover

14. **Sleep Group**
    - sleep, rest, sleep quality, sleeping, restful

15. **Pain Group**
    - pain, pain relief, chronic pain, back pain

16. **Healing Group**
    - healing, recovery, restoration, heal, restore, recovered

### Personal Development

17. **Confidence Group**
    - confidence, self-esteem, self-worth, self-confidence, confident

18. **Motivation Group**
    - motivation, drive, ambition, motivated, driven, ambitious

19. **Resilience Group**
    - resilience, strength, fortitude, resilient, strong

20. **Self-Awareness Group**
    - self-awareness, self-discovery, self-knowledge

21. **Purpose Group**
    - purpose, life purpose, meaning, meaningful

### Interpersonal/Social

22. **Gratitude Group**
    - gratitude, thankfulness, appreciation, grateful, thankful, appreciative

23. **Compassion Group**
    - compassion, empathy, kindness, compassionate, empathetic, kind

24. **Connection Group**
    - connection, social connection, belonging, connected

25. **Forgiveness Group**
    - forgiveness, letting go, release, forgive, let go

### Spiritual/Material

26. **Spiritual Group**
    - spiritual, spirituality, spiritual growth, spiritual awakening

27. **Intuition Group**
    - intuition, inner wisdom, gut feeling, intuitive, instinct

28. **Abundance Group**
    - abundance, prosperity, wealth, abundant, prosperous, wealthy

29. **Success Group**
    - success, achievement, accomplishment, successful, achieve

30. **Balance Group**
    - balance, harmony, equilibrium, balanced, harmonious

---

## Implementation Process

### Phase 1: Data Collection & Initial Analysis

1. **Fetch Outcomes Data**
   ```python
   # Use provided Python script: fetch-and-analyze-outcomes.py
   # Requires: AIRTABLE_API_KEY environment variable
   ```

2. **Generate Analysis Report**
   - Identify all outcomes with zero usage
   - Identify all outcomes with ≤2 total usage
   - Map all outcomes to semantic groups
   - Identify merge candidates within each group

### Phase 2: Review & Validation

1. **Review Deletion Candidates**
   - Verify usage counts are accurate
   - Check if any zero-usage outcomes are strategically important
   - Identify any false positives

2. **Review Merge Candidates**
   - Verify semantic groupings are appropriate
   - Confirm primary outcome selection (highest usage)
   - Check for any nuanced differences that warrant keeping separate

### Phase 3: Batch Updates

1. **Update Records in Batches of 10**
   ```python
   # Use MCP Airtable update_records tool
   # Format: baseId="app4ulN4GnBRvcfAL", tableId="tblLA13fGO7KM1JHA"
   ```

2. **Set UPDATE TYPE and UPDATE NOTE**
   - Deleted: `"No usage"` or `"Low usage: Total=X"`
   - Merged: `"Merge into [Primary Outcome] (usage=Y)"`

### Phase 4: Content Migration

After marking outcomes for merge:

1. **Migrate Usage**
   - Update Programs, Meditations, Audios to use primary outcome
   - Redirect any references from merged outcomes to primary

2. **Preserve Data**
   - Keep merged outcomes in archive view
   - Don't permanently delete until migration complete

---

## Expected Results

Based on typical outcome distributions:

### Estimated Reductions

| Category | Expected Count | Notes |
|----------|---------------|-------|
| Total Outcomes | 200-300 | Starting point |
| Zero Usage | 40-60 (15-20%) | Immediate deletion candidates |
| Low Usage (≤2) | 30-50 (10-17%) | Deletion candidates |
| Merge Candidates | 50-80 (17-27%) | Semantic consolidation |
| **Final Count** | **80-150** | **40-60% reduction** |

### Benefits

1. **Improved Discoverability**
   - Fewer, more focused outcomes
   - Reduced decision paralysis for users
   - Clearer outcome definitions

2. **Better Usage Metrics**
   - Consolidated usage data
   - More meaningful analytics
   - Easier to identify popular outcomes

3. **Simplified Maintenance**
   - Fewer records to manage
   - Clearer outcome hierarchy
   - Reduced duplication

4. **Enhanced Quality**
   - Each outcome has sufficient usage data
   - More robust recommendations
   - Better user experience

---

## Example Merge Scenarios

### Example 1: Stress/Anxiety Group

**Before:**
- "Reduce stress" (Program=5, Meditation=12, Audio=8) → Usage: 25
- "Manage anxiety" (Program=2, Meditation=6, Audio=3) → Usage: 11
- "Less worry" (Program=0, Meditation=2, Audio=1) → Usage: 3
- "Release tension" (Program=1, Meditation=4, Audio=2) → Usage: 7

**After:**
- **Primary:** "Reduce stress" (Usage: 25) → KEEP
- "Manage anxiety" → MERGE (note: "Merge into 'Reduce stress'")
- "Less worry" → DELETE (low usage)
- "Release tension" → MERGE (note: "Merge into 'Reduce stress'")

**Result:** 4 outcomes → 1 outcome (75% reduction)

### Example 2: Sleep Group

**Before:**
- "Better sleep" (Program=8, Meditation=15, Audio=12) → Usage: 35
- "Improve sleep quality" (Program=3, Meditation=7, Audio=4) → Usage: 14
- "Restful sleep" (Program=1, Meditation=3, Audio=2) → Usage: 6
- "Fall asleep faster" (Program=2, Meditation=5, Audio=3) → Usage: 10

**After:**
- **Primary:** "Better sleep" (Usage: 35) → KEEP
- "Improve sleep quality" → MERGE
- "Restful sleep" → MERGE
- "Fall asleep faster" → KEEP (specific enough to warrant separate outcome)

**Result:** 4 outcomes → 2 outcomes (50% reduction)

---

## Quality Assurance Checklist

Before finalizing updates:

- [ ] All zero-usage outcomes marked for deletion
- [ ] All ≤2 usage outcomes reviewed
- [ ] Semantic groups validated
- [ ] Primary outcomes have highest usage in their group
- [ ] UPDATE NOTE provides clear reasoning
- [ ] No strategically important outcomes accidentally deleted
- [ ] Migration plan in place for merged outcomes
- [ ] Stakeholders notified of changes

---

## Tools & Scripts

### 1. Analysis Script

**File:** `/scripts/fetch-and-analyze-outcomes.py`

**Usage:**
```bash
export AIRTABLE_API_KEY="your_key_here"
python3 scripts/fetch-and-analyze-outcomes.py
```

**Output:**
- Console report with recommendations
- `outcome-updates.json` with batch update data

### 2. Update Script Template

```python
# Use MCP Airtable tools
from mcp__airtable__update_records import update_records

# Load batch from outcome-updates.json
with open('outcome-updates.json') as f:
    data = json.load(f)

# Update each batch
for batch in data['batches']:
    update_records(
        baseId="app4ulN4GnBRvcfAL",
        tableId="tblLA13fGO7KM1JHA",
        records=batch
    )
    time.sleep(0.5)  # Rate limiting
```

---

## Next Steps

1. **Immediate:**
   - Run analysis script to generate current state report
   - Review and validate recommendations
   - Get stakeholder approval

2. **Short-term:**
   - Execute batch updates for deletions
   - Execute batch updates for merges
   - Verify UPDATE TYPE and UPDATE NOTE fields

3. **Medium-term:**
   - Migrate content from merged outcomes to primary
   - Update any hardcoded references
   - Archive deleted/merged outcomes

4. **Long-term:**
   - Monitor usage of consolidated outcomes
   - Establish governance for new outcome creation
   - Regular audits to prevent future bloat

---

## Contact & Support

For questions about this strategy:
- **Created by:** Claude Code
- **Date:** November 11, 2025
- **Base ID:** app4ulN4GnBRvcfAL
- **Table ID:** tblLA13fGO7KM1JHA

---

## Appendix: Field Definitions

| Field Name | Field ID | Purpose |
|-----------|----------|---------|
| Outcome | fldCP33pFkB25Ynee | Outcome name |
| Program Count | fldE9oQRoudmUiZ2I | Number of programs using this outcome |
| Meditation Count | fldkVIkUgZcbBwkaD | Number of meditations using this outcome |
| Audio Count | fldTmPvCIb4e2Bm98 | Number of audios using this outcome |
| Description | fldpAfFrmwipYiYAw | Outcome description |
| UPDATE TYPE | flddtQoH4JfAU0uTv | Simplification action (Deleted/Merged) |
| UPDATE NOTE | fldo4SmxBXYHqOu4R | Reasoning for action |
| SIMPLIFY | fld8ZyXVebrFFmeOR | Additional simplification tracking |

