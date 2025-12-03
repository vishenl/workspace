---
allowed-tools:
  - Bash
  - Glob
  - Read
  - Write
  - Edit
  - Grep
  - WebFetch
  - mcp__airtable__create_record
  - mcp__airtable__list_records
  - mcp__airtable__search_records
description: "Transform any talk transcript into a complete content suite: student guide, presentation feedback, and slide deck"
tags: [talk, transcript, slides, presentation, feedback, guide, content]
version: "1.0.0"
---

# Talk-to-Content Suite Generator

Transform any talk transcript into three professional deliverables with the same sophistication as the Gary Brecka content suite.

## Overview

When a user uploads or pastes a talk transcript, you will create:

1. **Student Guide** (`[speaker]-guide.html`) - A comprehensive post-training reference guide
2. **Presentation Feedback** (`[speaker]-presentation-feedback.html`) - Detailed instructor feedback with scores and recommendations
3. **Slide Deck** (`[speaker]-slides.html`) - Interactive presentation with speaker notes

## Step 1: Ask Clarifying Questions (Max 7)

Before creating anything, ask ONLY the questions needed. Skip any that are already answered in the transcript or obvious from context.

**Required Questions:**
1. **Speaker name?** (for file naming, titles, and attribution)
2. **Talk title or topic?** (if not clear from transcript)

**Conditional Questions (ask only if needed):**
3. **Target audience?** (students, executives, practitioners, general public)
4. **What's the primary transformation or outcome the speaker delivers?**
5. **Any specific frameworks, methodologies, or proprietary concepts to highlight?**
6. **Speaker's website, brand URL, or image URL?** (for branding the deliverables)
7. **Any sections to emphasize or skip?**

**DO NOT ask more than 7 questions total. Use your judgment to skip obvious ones.**

## Step 2: Analyze the Transcript

Before creating content, analyze:

### Content Analysis
- Identify the **core thesis/big idea** (the "One Thing" principle)
- Extract **key frameworks** and proprietary concepts
- Find **memorable quotes** that should be highlighted
- Identify **stories and case studies** with emotional impact
- Map the **transformation arc** (before → during → after)
- Note **statistics, numbers, and specific claims**
- Identify **actionable takeaways** and protocols

### Structure Analysis
- Current pacing (what's too long, too short)
- Opening hook effectiveness
- Story placement and emotional beats
- Call-to-action clarity
- Q&A setup

### Quality Assessment
- Content quality (1-10)
- Structure (1-10)
- Pacing (1-10)
- Transformation arc (1-10)

## Step 3: Create the Student Guide

**File:** `[speaker-slug]-guide.html`

### Design System
- **Theme:** Dark mode (#0a0a0a background)
- **Accent color:** Brand color or #00d4aa (teal) as default
- **Font:** Inter via Google Fonts
- **Style:** Premium, modern, sophisticated

### Required Sections
1. **Navigation** - Fixed nav with section links
2. **Hero Section**
   - Speaker badge with image
   - Main headline with gradient text
   - Subtitle/description
   - Key stats grid (4 cards with big numbers)
3. **Testimonials/Social Proof** (if available in transcript)
4. **Modules** - Each major concept as a numbered module card
   - Module number badge
   - Title and subtitle
   - Quote card (key quote from that section)
   - Key takeaways list
   - Info boxes (accent, warning, purple variants)
   - Pathway diagrams (if applicable)
5. **Protocols/Action Items** - Visual cards with images
6. **Implementation Checklist** - Interactive checkboxes by week/phase
7. **Quick Reference Cards** - 6-card grid summarizing key concepts
8. **Big Ideas Section** - Memorable quotes in gradient cards
9. **About the Speaker** - Photo + bio
10. **Footer** - Attribution and disclaimer

### Code Quality
- Fully responsive (mobile-first)
- CSS custom properties for theming
- Smooth scroll navigation
- Interactive checkboxes with JavaScript
- Print-friendly styles

## Step 4: Create the Presentation Feedback

**File:** `[speaker-slug]-presentation-feedback.html`

### Design System
- Same dark theme as student guide
- Clean, professional report style
- Color-coded severity (green=success, yellow=warning, red=danger)

### Required Sections

1. **Header** - Badge + title + subtitle
2. **Executive Summary**
   - 4-score grid (Content, Structure, Pacing, Transformation Arc)
   - Overall assessment paragraph
   - Key opportunity highlight box
3. **Pacing Analysis**
   - Front-loaded complexity issues
   - Energy dips
   - Recommended pacing table (Current vs Recommended times)
4. **Structural Recommendations**
   - Current problem (linear information dump)
   - Solution (nested loop structure)
   - Timeline visualization of recommended structure
5. **Transformation Theory Integration**
   - Hero's Journey mapping table
   - Eugene Schwartz awareness levels
   - Belief shifting techniques table
   - Transformation gap statement
6. **Specific Tactical Improvements**
   - What's working (green check list)
   - What needs work (yellow warning list)
   - What to cut (red danger list)
   - Language upgrades table (Current → Recommended → Why)
7. **Specific Quote Analysis**
   - Brilliant lines (keep exactly) with analysis
   - Lines that need improvement with rewrites
   - Quotes that need repositioning
8. **Optimized Talk Structure** - Full timeline of recommended flow
9. **Final Thoughts** - Closing recommendation and summary

### Frameworks to Apply
- Joseph Campbell's Hero's Journey
- Eugene Schwartz's 5 Awareness Levels
- Nested Loop storytelling technique
- Belief shifting methodology
- Mindvalley transformation theory

## Step 5: Create the Slide Deck

**File:** `[speaker-slug]-slides.html`

### Design System
- Full-screen slides (100vh/100vw)
- Dark theme with accent color gradients
- Large typography (72px h1, 56px h2)
- Minimal text per slide

### Required Features
1. **Progress bar** - Top of screen
2. **Slide numbers** - Top left
3. **Logo** - Top right (speaker's brand)
4. **Navigation** - Bottom center arrows
5. **Speaker notes toggle** - Bottom right
6. **Keyboard support** - Arrow keys, N for notes, Space to advance
7. **Touch/swipe support** - Mobile navigation

### Slide Types to Include
1. **Title Slide** - Name, talk title, event
2. **Big Number Slides** - Key statistics
3. **Quote Slides** - Memorable lines
4. **Split Layout Slides** - Image + content (left/right variations)
5. **Pathway Diagrams** - Process flows
6. **Scale Visualizations** - Numbered progressions
7. **Card Grids** - 2-3 column feature cards
8. **Donut Charts** - Statistical breakdowns
9. **Protocol Grids** - Visual action items
10. **List Slides** - Bulleted points with icons
11. **Call-to-Action Slides** - Next steps
12. **Closing Slide** - Summary + Q&A invitation

### Speaker Notes
Every slide MUST have a `data-notes` attribute with:
- Delivery instructions
- Timing cues
- Emotional beats to hit
- Audience interaction prompts

### Slide Count
Aim for 20-30 slides for a 45-60 minute talk.

## Step 6: Sync to Airtable

After creating all three files, sync them to the Claude Pages table:

**Airtable Configuration:**
- Base ID: `appoX9UV0ewM07Mi1`
- Table ID: `tblqm3DEjztJg0qRl`

**For each file, create a record with:**
- Name: Page title
- Github URL: `https://vishenl.github.io/workspace/[filename]`
- LOCALHOST URL: `http://localhost:5500/[filename]`
- Type: Appropriate type (Training Guide, Class Report, Presentation Slides)
- Status: Done
- Desc: Brief description

## Step 7: Deliver Summary

Present the user with:

```markdown
## Content Suite Created

### Files Generated
| File | Type | Purpose |
|------|------|---------|
| `[speaker]-guide.html` | Training Guide | Student reference document |
| `[speaker]-presentation-feedback.html` | Class Report | Instructor feedback |
| `[speaker]-slides.html` | Presentation Slides | Interactive slide deck |

### Quick Links
- [Student Guide](http://localhost:5500/[speaker]-guide.html)
- [Presentation Feedback](http://localhost:5500/[speaker]-presentation-feedback.html)
- [Slide Deck](http://localhost:5500/[speaker]-slides.html)

### Airtable Records
All pages synced to Claude Pages table.

### Scores
- Content Quality: X/10
- Structure: X/10
- Pacing: X/10
- Transformation Arc: X/10
```

## Quality Standards

### Visual Quality
- Must match or exceed the Gary Brecka examples
- All CSS inline (single-file HTML)
- Responsive on all devices
- Dark theme with accent color gradients
- Professional typography hierarchy

### Content Quality
- Extract genuine insights from transcript
- Apply transformation theory frameworks
- Provide actionable, specific recommendations
- Include exact quotes with analysis
- Offer concrete rewrites, not just criticism

### Technical Quality
- Valid HTML5
- Accessible (alt tags, semantic markup)
- Fast-loading (no external dependencies except fonts)
- Print-friendly where applicable
- Interactive elements work correctly

## Reference Files

For exact styling and structure reference, see:
- `/Users/vishen/Documents/Github/workspace/gary-brecka-guide.html`
- `/Users/vishen/Documents/Github/workspace/gary-brecka-presentation-feedback.html`
- `/Users/vishen/Documents/Github/workspace/gary-brecka-slides.html`

These are your gold standard. Match their quality exactly.
