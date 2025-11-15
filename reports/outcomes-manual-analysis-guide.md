# Manual Analysis Guide: Mindvalley Outcomes Simplification

**Quick Reference Guide for Systematic Outcome Analysis**

---

## Quick Start Checklist

### Step 1: Setup Your Workspace

1. Open Airtable base: `app4ulN4GnBRvcfAL`
2. Navigate to table: `🪽Outcomes` (`tblLA13fGO7KM1JHA`)
3. Use view: `🔧 by AOG` (`viwoAhFaw8vu6ADUm`)
4. Add columns if not visible:
   - Program Count
   - Meditation Count
   - Audio Count
   - UPDATE TYPE
   - UPDATE NOTE

### Step 2: Create Helper Formulas

Add these formula fields to help with analysis:

**Total Usage:**
```
{Program Count} + {Meditation Count} + {Audio Count}
```

**Recommendation:**
```
IF(
  AND({Program Count}=0, {Meditation Count}=0, {Audio Count}=0),
  "DELETE: No usage",
  IF(
    ({Program Count} + {Meditation Count} + {Audio Count}) <= 2,
    "DELETE: Low usage",
    "REVIEW: Check for merges"
  )
)
```

---

## Analysis Process

### Phase 1: Identify Deletion Candidates (30 minutes)

#### A. Zero Usage Outcomes

1. **Filter:**
   - Program Count = 0
   - Meditation Count = 0
   - Audio Count = 0

2. **Review:** Sort alphabetically and scan for any that seem strategically important

3. **Action:** For each outcome to delete:
   - UPDATE TYPE: `Deleted`
   - UPDATE NOTE: `No usage: Program Count=0, Meditation Count=0, Audio Count=0`

**Batch Update Template:**
```
Mark all outcomes where:
- Program Count = 0 AND Meditation Count = 0 AND Audio Count = 0
- UPDATE TYPE = "Deleted"
- UPDATE NOTE = "No usage: Program Count=0, Meditation Count=0, Audio Count=0"
```

#### B. Low Usage Outcomes (≤2)

1. **Filter:**
   - Total Usage ≤ 2
   - Exclude already marked for deletion

2. **Review:** Check if any have strategic importance despite low usage

3. **Action:** For each outcome to delete:
   - UPDATE TYPE: `Deleted`
   - UPDATE NOTE: `Low usage: Total=X (Program=Y, Meditation=Z, Audio=W)`

---

### Phase 2: Identify Merge Candidates (60 minutes)

Use the semantic groups below. For each group:

1. Filter outcomes containing any of the group terms
2. Sort by Total Usage (highest first)
3. Select the highest usage as PRIMARY
4. Mark others for MERGE with reference to primary

#### Semantic Group Quick Reference

**For each outcome, ask:**
1. Does it contain any of these terms?
2. If yes, what's its usage compared to others in the group?
3. If not the highest, should it merge?

---

## Semantic Groups with Search Terms

### Group 1: STRESS/ANXIETY
**Search:** stress, anxiety, worry, tension, anxious, worried, tense

**Analysis Process:**
1. Search for "stress" → List all results
2. Search for "anxiety" → Add to list
3. Search for "worry" → Add to list
4. Sort by usage
5. Top result = PRIMARY, rest = MERGE

**Example UPDATE NOTE:**
```
Merge into "Reduce stress" (usage=25). Current usage=11. Semantic group: stress/anxiety/worry
```

### Group 2: HAPPINESS/JOY
**Search:** happiness, joy, bliss, contentment, happy, joyful

### Group 3: CALM/PEACE
**Search:** calm, peace, tranquility, serenity, peaceful, tranquil

### Group 4: FOCUS/CONCENTRATION
**Search:** focus, concentration, attention, focused, concentrate

### Group 5: ENERGY/VITALITY
**Search:** energy, vitality, vigor, energized, energetic

### Group 6: CONFIDENCE
**Search:** confidence, self-esteem, self-worth, confident

### Group 7: CREATIVITY
**Search:** creativity, innovation, imagination, creative

### Group 8: MOTIVATION
**Search:** motivation, drive, ambition, motivated, driven

### Group 9: RELAXATION/REST
**Search:** relaxation, rest, recovery, relax, relaxed

### Group 10: CLARITY
**Search:** clarity, clear-thinking, mental clarity, clear

### Group 11: GRATITUDE
**Search:** gratitude, thankfulness, appreciation, grateful

### Group 12: COMPASSION
**Search:** compassion, empathy, kindness, compassionate

### Group 13: RESILIENCE
**Search:** resilience, strength, fortitude, resilient

### Group 14: MINDFULNESS
**Search:** mindfulness, presence, awareness, mindful, aware

### Group 15: SLEEP
**Search:** sleep, sleeping, restful, insomnia

**Note:** "Fall asleep faster" is specific enough to keep separate

### Group 16: ABUNDANCE
**Search:** abundance, prosperity, wealth, abundant, prosperous

### Group 17: HEALING
**Search:** healing, recovery, restoration, heal, restore

### Group 18: BALANCE
**Search:** balance, harmony, equilibrium, balanced

### Group 19: FORGIVENESS
**Search:** forgiveness, letting go, release, forgive

### Group 20: INTUITION
**Search:** intuition, inner wisdom, gut feeling, intuitive

### Group 21: LOVE
**Search:** love, loving, self-love, loving-kindness

### Group 22: PAIN
**Search:** pain, pain relief, chronic pain, back pain

### Group 23: ANGER
**Search:** anger, frustration, irritation, angry, frustrated

### Group 24: FEAR
**Search:** fear, scared, frightened, afraid, fearful

### Group 25: SADNESS
**Search:** sadness, depression, melancholy, sad, depressed

### Group 26: SUCCESS
**Search:** success, achievement, accomplishment, successful

### Group 27: SPIRITUAL
**Search:** spiritual, spirituality, spiritual growth, awakening

### Group 28: SELF-AWARENESS
**Search:** self-awareness, self-discovery, self-knowledge

### Group 29: PURPOSE
**Search:** purpose, life purpose, meaning, meaningful

### Group 30: CONNECTION
**Search:** connection, social connection, belonging, connected

---

## Decision Tree for Each Outcome

```
START
  |
  ├─ Usage = 0?
  |    └─ YES → DELETE (No usage)
  |    └─ NO → Continue
  |
  ├─ Usage ≤ 2?
  |    └─ YES → DELETE (Low usage)
  |    └─ NO → Continue
  |
  ├─ Matches semantic group?
  |    └─ NO → KEEP (Unique outcome)
  |    └─ YES → Continue
  |         |
  |         ├─ Highest usage in group?
  |         |    └─ YES → KEEP (Primary for group)
  |         |    └─ NO → MERGE (Into primary)
  |
  └─ DONE
```

---

## Batch Update Workflow

### Using Airtable Interface

1. **Filter for deletion candidates:**
   ```
   AND(
     {Program Count} = 0,
     {Meditation Count} = 0,
     {Audio Count} = 0,
     {UPDATE TYPE} = BLANK()
   )
   ```

2. **Select all filtered records**

3. **Batch update:**
   - UPDATE TYPE: `Deleted`
   - UPDATE NOTE: `No usage: Program Count=0, Meditation Count=0, Audio Count=0`

4. **Repeat for low usage:**
   ```
   AND(
     ({Program Count} + {Meditation Count} + {Audio Count}) <= 2,
     {UPDATE TYPE} = BLANK()
   )
   ```

### Using Scripts

If you have Airtable API access, use the Python scripts:

```bash
# Set your API key
export AIRTABLE_API_KEY="your_key"

# Run analysis
python3 scripts/fetch-and-analyze-outcomes.py

# Review output
cat outcome-updates.json

# Apply updates (use MCP tools or API)
```

---

## Quality Control Checklist

After each batch of updates:

- [ ] Verified usage counts are accurate
- [ ] Checked for false positives
- [ ] Reviewed primary outcome selection
- [ ] Ensured UPDATE NOTE is clear and specific
- [ ] No duplicate UPDATE TYPEs on same record
- [ ] Spot-checked 5-10 random updates

---

## Common Edge Cases

### Case 1: Specialized Outcomes

**Example:** "Fall asleep faster" vs "Better sleep"

**Decision:** Keep both if:
- Sufficiently different user intent
- Each has reasonable usage (>5)
- Specific outcome adds value

**Action:** Mark both as KEEP with note explaining rationale

### Case 2: Similar but Different

**Example:** "Reduce stress" vs "Manage anxiety"

**Decision:**
- If clinically distinct: Keep both
- If used interchangeably: Merge into higher usage

**Action:** Review usage context before merging

### Case 3: Strategic Outcomes

**Example:** Zero usage but part of new feature launch

**Decision:** Keep if:
- Part of planned feature
- Strategically important
- Will have usage within 30 days

**Action:** Add note "Strategic outcome - new feature pending"

### Case 4: Description-based Merges

**Example:** Two outcomes with identical descriptions but different names

**Decision:** ALWAYS merge these

**Action:**
- Merge into the one with better name clarity
- If equal, merge into higher usage

---

## Progress Tracking

### Daily Goal

Aim to process 50-75 outcomes per day:
- 30-40 deletions (zero/low usage)
- 20-35 merges (semantic groups)

### Weekly Goal

Complete analysis of all 200-300 outcomes in 4-5 days:
- Day 1: Setup + Zero usage deletions
- Day 2: Low usage deletions
- Day 3: Semantic groups 1-15
- Day 4: Semantic groups 16-30
- Day 5: Review + quality control

---

## Example Work Session (2 hours)

**Hour 1: Deletions**

1. Filter zero usage (15 min)
2. Review for false positives (10 min)
3. Batch update DELETE (10 min)
4. Filter low usage (10 min)
5. Review + batch update (15 min)

**Hour 2: Merges**

1. Process Groups 1-5 (12 min each):
   - Search for group terms
   - Identify primary
   - Mark others for merge
   - Update UPDATE NOTE

**Expected Output:**
- 40-60 outcomes marked for deletion
- 15-20 outcomes marked for merge
- Clear notes on all updates

---

## Support & Resources

### Key Files

- Strategy doc: `/reports/outcomes-simplification-strategy.md`
- Analysis script: `/scripts/fetch-and-analyze-outcomes.py`
- This guide: `/reports/outcomes-manual-analysis-guide.md`

### Airtable Access

- Base: `app4ulN4GnBRvcfAL`
- Table: `tblLA13fGO7KM1JHA`
- Recommended view: `🔧 by AOG` (viwoAhFaw8vu6ADUm)

### Questions?

Common questions answered in strategy doc appendix.

---

## Quick Tips

1. **Use keyboard shortcuts:** Airtable supports keyboard navigation
2. **Create custom views:** One for deletions, one for each semantic group
3. **Work in batches:** Don't try to do everything at once
4. **Take breaks:** Merge analysis requires focus
5. **Document edge cases:** Add notes for unusual situations
6. **Get second opinions:** For borderline cases, consult team

---

## Success Metrics

Track your progress:

- **Outcomes reviewed:** [____] / ~250
- **Deletions marked:** [____] (Target: 70-110)
- **Merges marked:** [____] (Target: 50-80)
- **Final count:** [____] (Target: 80-150)
- **Reduction:** [____]% (Target: 40-60%)

---

**Remember:** The goal is not to delete as many as possible, but to create a cleaner, more usable outcomes system. When in doubt, keep the outcome and mark for later review.

