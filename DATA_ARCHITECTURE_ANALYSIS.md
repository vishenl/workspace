# Mindvalley Author Pages: Data Architecture Analysis & Solutions

**Date:** January 2025
**Purpose:** Solve data architecture challenges for building author pages with simplified, scalable data relationships

---

## Executive Summary

This document provides a comprehensive analysis of the Mindvalley Brain Airtable data architecture and proposes concrete solutions for:
1. Deducing primary areas of growth for authors
2. Simplifying the 287 outcomes problem
3. Optimizing data relationships for author page construction
4. Leveraging the Brands table for unique insights

**Key Discovery:** The Programs table already contains a "Primary Area" field that solves the core problem of identifying the main focus area for each program.

---

## 1. Current Data Architecture

### Table Relationships

```
┌─────────────┐
│   Authors   │
│  (56 fields)│
└──────┬──────┘
       │
       │ links to
       ▼
┌─────────────────────┐         ┌──────────────────┐
│     Programs        │────────▶│  Areas of Growth │
│    (80+ fields)     │         │   (15 areas)     │
│                     │         └──────────────────┘
│ • Primary Area ◄────┼─────────────────┘
│ • Areas of Growth   │         (single)
│   (multiple)        │
└──────┬──────────────┘
       │
       │ links to
       ▼
┌─────────────────────┐         ┌──────────────────┐
│     Outcomes        │────────▶│  Areas of Growth │
│   (287 outcomes)    │         └──────────────────┘
└─────────────────────┘
```

### Current Data Flow Issues

**Problem 1: Redundant Lookups**
- Authors table has "Areas of Growth (Lookup) (from Programs)" field
- This creates a flattened list mixing primary and secondary areas
- No way to distinguish importance/priority

**Problem 2: The 287 Outcomes Problem**
- Talks/Podcasts tagged with individual outcomes
- 287 unique outcomes is overwhelming for users
- Outcomes already have parent Areas of Growth, but this relationship isn't leveraged for display

**Problem 3: Multiple Areas Without Priority**
- Programs can have 3-7 "Areas of Growth"
- No clear signal about which is PRIMARY
- **SOLUTION EXISTS:** "Primary Area" field (fldMMoJLDGFs8l7Xx) already present in Programs table

---

## 2. The "Primary Area" Field - Key Discovery

### How It Works

**In Programs Table:**
- **Field Name:** "Primary Area" (fldMMoJLDGFs8l7Xx)
- **Type:** Single Link to Areas of Growth table
- **Purpose:** Identifies the #1 main focus area for a program

**Example: "The 6 Phase Meditation" (Vishen's program)**
- **Areas of Growth (7 total):** Mindfulness, Performance, Spirituality, Resilience, Soul, Mind, Meditation
- **Primary Area (1 only):** rec3EQwjt7duZ4bYf (likely "Mindfulness" or "Spirituality")

### Current Adoption Status

✅ **Field exists** in Programs table
❓ **Unknown:** Percentage of programs with Primary Area populated
❓ **Unknown:** Whether Talks/Podcasts have similar field

---

## 3. Proposed Data Architecture Solutions

### Solution 1: Author Primary Areas Algorithm

**Goal:** Deduce an author's primary areas of growth when they have multiple programs

**Algorithm:**

```
For each Author:
  1. Get all published Programs by author
  2. Extract "Primary Area" from each program
  3. Count frequency of each Primary Area
  4. Weight by:
     - Recency (newer programs weighted higher)
     - Program status (Published > In Discussion)
     - Content type (Quest > Talk)
  5. Return top 3 Primary Areas

Pseudocode:
-----------
primary_areas = {}
for program in author.programs:
  if program.primary_area:
    weight = calculate_weight(program)
    primary_areas[program.primary_area] += weight

return sorted(primary_areas, descending=True)[:3]
```

**Weighting Formula:**
```
Weight = Base Weight × Recency Factor × Status Factor × Type Factor

Base Weight = 1.0
Recency Factor =
  - Last 12 months: 1.5x
  - 1-2 years: 1.2x
  - 2-3 years: 1.0x
  - 3+ years: 0.8x

Status Factor =
  - Published: 1.0x
  - On Hold: 0.5x
  - In Discussion: 0.3x

Type Factor =
  - Quest: 1.0x
  - Mastery: 1.2x
  - Certification: 1.3x
  - Talk: 0.6x
  - Podcast: 0.5x
```

**Benefits:**
- ✅ Uses existing "Primary Area" field
- ✅ Gives more weight to recent, high-value content
- ✅ Produces 1-3 clear "hero" areas for each author
- ✅ Automatically updates as new content is added

---

### Solution 2: Outcomes Simplification Strategy

**The Problem:**
- 287 unique outcomes
- Talks/Podcasts tagged at outcome level
- Too granular for user browsing

**The Solution: Two-Tier Outcome Display**

#### Tier 1: Show Area of Growth (15 areas)
- Group outcomes by their parent Area of Growth
- Display content by these 15 high-level areas
- Example: "Mind" area includes all outcomes related to cognitive performance

#### Tier 2: Show Top Outcomes Per Area (on-demand)
- When user clicks into an area, show top 3-5 outcomes
- Use frequency to determine "top" outcomes

**Implementation:**

```
Area of Growth: Mind
├── Top Outcomes (show these):
│   ├── Better Focus (appears in 45 talks)
│   ├── Faster Learning (appears in 38 talks)
│   └── Enhanced Memory (appears in 32 talks)
└── Other Outcomes (15 more, hidden by default)
```

**Data Structure:**
```json
{
  "author": "Vishen Lakhiani",
  "content_by_area": {
    "Mind": {
      "total_content": 50,
      "programs": [...],
      "talks": [...],
      "primary_outcomes": [
        {"outcome": "Better Focus", "count": 15},
        {"outcome": "Faster Learning", "count": 12}
      ]
    }
  }
}
```

**Benefits:**
- ✅ Reduces 287 outcomes to 15 browseable areas
- ✅ Maintains granular data for search/filters
- ✅ Progressive disclosure (show details on-demand)
- ✅ Leverages existing Outcomes → Areas of Growth links

---

### Solution 3: Simplified Data Relationships for Author Pages

**Current Flow (Complex):**
```
Author → Programs → Areas of Growth (Lookup)
                 → Outcomes
                 → Brands
Author → Talks → Outcomes → Areas of Growth
Author → Podcasts → Outcomes → Areas of Growth
```

**Proposed Flow (Simplified):**
```
For Primary Areas:
------------------
Author → Programs → Primary Area (single)
     → Aggregate top 3 Primary Areas

For Content Grouping:
---------------------
Author → Programs → Primary Area → Group by Primary Area
Author → Talks → Outcomes → Area of Growth → Group by Area
Author → Podcasts → Outcomes → Area of Growth → Group by Area

For Content Counts:
------------------
Author → Direct counts: Talk Count, Program Count, Podcast Count, etc.
```

**New Recommended Fields for Authors Table:**

| Field Name | Type | Purpose | Example |
|-----------|------|---------|---------|
| **Primary Area 1** | Link | Top area of expertise | "Mind" |
| **Primary Area 2** | Link | 2nd area of expertise | "Body" |
| **Primary Area 3** | Link | 3rd area of expertise | "Soul" |
| **Primary Area Weights** | Long Text (JSON) | Store weighted scores | `{"Mind": 4.5, "Body": 3.2}` |
| **Content Distribution** | Long Text (JSON) | Content count by area | `{"Mind": {"programs": 5, "talks": 20}}` |
| **Last Content Update** | Date | For recalculation trigger | "2025-01-15" |

**Benefits:**
- ✅ Clear hierarchy of expertise
- ✅ Fast queries (denormalized for performance)
- ✅ Easy to display in UI
- ✅ Cacheable and updatable

---

## 4. Leveraging the Brands Table

### Current Brands Structure

**Brands → Programs → Authors**

**Unique Insight Opportunities:**

#### 1. **Author Authority by Brand Association**
- Authors who create content for multiple brands show versatility
- Example: "Vishen has created content for Mindvalley, Omvana, and Soulvana"

**Display:**
```
Vishen Lakhiani
├── Mindvalley: 15 programs
├── Omvana: Meditation apps
└── Soulvana: Spiritual content
```

#### 2. **Brand-Specific Content Collections**
- Group author's content by brand
- Show brand logos on author page

**UI Component:**
```html
<section class="author-brands">
  <h3>Content Across Mindvalley Brands</h3>
  <div class="brand-card">
    <img src="mindvalley-logo" />
    <p>12 Quests, 5 Masterclasses</p>
  </div>
</section>
```

#### 3. **Cross-Brand Recommendations**
- "If you liked this author's Mindvalley content, explore their Soulvana collection"

**Benefits:**
- ✅ Shows author's breadth across ecosystem
- ✅ Cross-sell opportunity
- ✅ Establishes authority through brand partnerships

---

## 5. Data Architecture Cleanup Recommendations

### Immediate Actions

#### 1. **Populate Primary Area Field**
- **Priority:** HIGH
- **Action:** Ensure all published programs have Primary Area set
- **Impact:** Enables all author primary area algorithms

**SQL-like Logic:**
```
UPDATE Programs
SET Primary Area = (
  SELECT TOP 1 Area
  FROM Areas of Growth
  WHERE Program.Areas_of_Growth CONTAINS Area
  ORDER BY relevance DESC
)
WHERE Primary Area IS NULL
  AND Status = 'Published'
```

#### 2. **Create Primary Outcomes View**
- **Priority:** MEDIUM
- **Action:** Create calculated field showing top 5 outcomes per Area of Growth
- **Impact:** Simplifies UI, reduces cognitive load

**New Table/View: "Primary Outcomes by Area"**
| Area of Growth | Primary Outcome 1 | Primary Outcome 2 | Primary Outcome 3 |
|----------------|-------------------|-------------------|-------------------|
| Mind | Better Focus | Faster Learning | Enhanced Memory |
| Body | More Energy | Better Sleep | Optimal Fitness |

#### 3. **Add Computed Fields to Authors Table**
- **Priority:** MEDIUM
- **Action:** Add denormalized fields for performance
  - Primary Area 1, 2, 3
  - Content counts by area
  - Last update timestamp

#### 4. **Create Data Refresh Automation**
- **Priority:** LOW
- **Action:** Build automation to recalculate author primary areas
- **Trigger:** When new program is published by author
- **Frequency:** Weekly batch update

---

## 6. Implementation Roadmap

### Phase 1: Data Foundation (Week 1-2)
- [ ] Audit Primary Area field population rate
- [ ] Fill missing Primary Area values
- [ ] Create "Primary Outcomes by Area" view
- [ ] Document current state

### Phase 2: Algorithm Development (Week 2-3)
- [ ] Build Primary Area weighting algorithm
- [ ] Test on 10 sample authors
- [ ] Validate results with content team
- [ ] Refine weighting formula

### Phase 3: Author Table Enhancement (Week 3-4)
- [ ] Add new computed fields to Authors table
- [ ] Build automation script
- [ ] Run initial calculation for all authors
- [ ] QA data quality

### Phase 4: Frontend Integration (Week 4-5)
- [ ] Update author page template
- [ ] Implement content grouping by Primary Area
- [ ] Add Brand association section
- [ ] Implement outcome filtering

---

## 7. Success Metrics

### Data Quality Metrics
- **Primary Area Population:** Target 100% of published programs
- **Author Primary Areas Accuracy:** 95% validated by content team
- **Data Refresh Time:** < 1 hour for all authors

### User Experience Metrics
- **Bounce Rate on Author Pages:** Target < 40%
- **Time on Page:** Target > 2 minutes
- **Content Discovery:** 30% increase in clicks on related content
- **Filter Usage:** 50% of users engage with Area of Growth filters

### Performance Metrics
- **Page Load Time:** < 2 seconds
- **API Response Time:** < 500ms
- **Database Query Time:** < 100ms

---

## 8. Example: Building Vishen's Author Page

### Data Flow

**Step 1: Get Author Data**
```json
{
  "id": "recJqLHyT0uq2NY8w",
  "name": "Vishen Lakhiani",
  "programs": 21,
  "talks": 195,
  "podcasts": 60
}
```

**Step 2: Calculate Primary Areas**
```json
{
  "primary_areas": [
    {"area": "Mind", "weight": 5.2, "program_count": 8},
    {"area": "Performance", "weight": 4.1, "program_count": 6},
    {"area": "Spirituality", "weight": 3.7, "program_count": 7}
  ]
}
```

**Step 3: Group Content by Primary Area**
```json
{
  "content_by_area": {
    "Mind": {
      "programs": [
        {"title": "The 6 Phase Meditation", "type": "Quest"},
        {"title": "Super Reading", "type": "Quest"}
      ],
      "talks": [...],
      "outcomes": ["Better Focus", "Enhanced Memory"]
    },
    "Performance": {...},
    "Spirituality": {...}
  }
}
```

**Step 4: Add Brand Information**
```json
{
  "brands": [
    {"name": "Mindvalley", "program_count": 18},
    {"name": "Omvana", "content_type": "Meditations"}
  ]
}
```

**Step 5: Render Author Page**
- Hero: Name, Title, Primary Areas (3 badges)
- About: Bio, Stats
- Content Tabs:
  - By Area (Mind, Performance, Spirituality)
  - By Type (Programs, Talks, Podcasts)
  - By Brand (Mindvalley, Omvana)

---

## 9. Alternative Approaches Considered

### Approach A: Manual Curation
- **Pros:** Complete control, high quality
- **Cons:** Doesn't scale, requires ongoing maintenance
- **Verdict:** ❌ Not sustainable

### Approach B: User Behavior Data
- **Pros:** Data-driven, reflects actual interest
- **Cons:** Requires analytics integration, cold start problem
- **Verdict:** ⏳ Future enhancement

### Approach C: AI/ML Classification
- **Pros:** Intelligent, can improve over time
- **Cons:** Complex, requires training data, black box
- **Verdict:** ⏳ Future enhancement

### Approach D: Weighted Algorithm (RECOMMENDED)
- **Pros:** Automatic, transparent, scalable, uses existing data
- **Cons:** Requires initial setup, needs validation
- **Verdict:** ✅ Best balance of automation and quality

---

## 10. Frequently Asked Questions

### Q: What if a program has no Primary Area set?
**A:** Fall back to the first Area of Growth in the list. Flag for manual review.

### Q: How do we handle authors with only 1-2 programs?
**A:** Show all their areas. Minimum display is 1 area, maximum is 3.

### Q: Should Talks count as much as Quests?
**A:** No. Use the Type Factor weighting (Quests 1.0x, Talks 0.6x).

### Q: What about discontinued programs?
**A:** Include with reduced weight (Status Factor: On Hold 0.5x).

### Q: How often should we recalculate?
**A:** Weekly batch process + immediate update when author publishes new content.

### Q: Can users filter by specific outcomes?
**A:** Yes, but we show Areas of Growth by default. Outcomes available as advanced filter.

---

## 11. Next Steps

### Immediate (This Week)
1. ✅ Share this document with team
2. ⏳ Get stakeholder approval on approach
3. ⏳ Audit Primary Area field population

### Short-Term (Next 2 Weeks)
1. ⏳ Build weighting algorithm
2. ⏳ Create test dataset
3. ⏳ Validate with content team

### Medium-Term (Next Month)
1. ⏳ Implement computed fields
2. ⏳ Build automation
3. ⏳ Update author page templates

### Long-Term (Next Quarter)
1. ⏳ Add analytics tracking
2. ⏳ Iterate based on user feedback
3. ⏳ Explore ML enhancements

---

## 12. Conclusion

The Mindvalley Brain Airtable already contains the key to solving the author page data architecture challenge: the **Primary Area field**. By leveraging this existing field and applying a weighted aggregation algorithm, we can:

✅ Automatically deduce an author's primary areas of expertise
✅ Simplify the 287 outcomes into 15 browseable areas
✅ Create a scalable, maintainable data architecture
✅ Improve user experience through clear content organization
✅ Enable powerful filtering and discovery features

The proposed solution balances automation with quality, leverages existing data structures, and sets the foundation for future enhancements.

---

**Document Version:** 1.0
**Last Updated:** January 2025
**Next Review:** After Phase 1 implementation
