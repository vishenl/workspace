# Mindvalley Page Builder: Redesign Workflow Guide

## Overview

The `mindvalley-page-builder` agent can now **analyze and redesign existing pages** in addition to building new ones. This guide explains how to use the redesign capability.

## When to Use Redesign Mode

Use the redesign workflow when you:
- Have an existing page URL that needs optimization
- Want to convert a competitor's page to Mindvalley style
- Need to analyze conversion weaknesses in a current page
- Want to modernize an outdated landing page
- Need to apply Mindvalley's design system to external content

## How It Works: 5-Phase Process

### Phase 1: URL Analysis & Content Extraction
The agent uses Firecrawl to:
- Scrape the page content (markdown + HTML)
- Extract headlines, copy, CTAs, images
- Identify page structure and sections
- Optionally take screenshots for visual analysis

### Phase 2: Conversion Optimization Analysis
The agent analyzes:
- **Hero section**: Value prop clarity, CTA effectiveness
- **Visual hierarchy**: F/Z patterns, white space, font sizes
- **Social proof**: Testimonials, trust signals, positioning
- **Content clarity**: Benefit focus, scannability, objection handling
- **Mobile experience**: Thumb zones, touch targets, simplification
- **Technical issues**: Images, contrast, accessibility, semantics

Then prioritizes improvements by impact (HIGH/MEDIUM/LOW).

### Phase 3: Strategic Questions
The agent asks you:
1. **Conversion goal** - What action do you want users to take?
2. **Audience context** - Cold traffic? Warm leads? Customers?
3. **Optimization priorities** - What matters most?
4. **Content preservation** - Keep all content or condense?
5. **Brand alignment** - What to preserve from original?

Plus optional questions about pricing, images, and CTAs.

### Phase 4: Component Mapping & Rebuild
The agent:
- Maps original sections to Mindvalley components
- Fetches official components from Airtable
- Rebuilds the page using Design Tokens + Typography System
- Applies conversion optimizations identified in analysis
- Documents all improvements made

### Phase 5: Validation & Delivery
The agent delivers:
- ✅ Complete redesigned HTML file
- 📊 Optimization summary (before/after)
- 📈 Expected conversion impact predictions
- ✅ Testing recommendations
- 🔍 Component usage documentation

## Example Usage

### Simple Redesign Request
```
User: "Take this URL and redesign it with better conversion in Mindvalley style:
https://example.com/landing"

Agent: [Automatically enters REDESIGN MODE]
1. Fetches page using Firecrawl
2. Analyzes conversion weaknesses
3. Asks strategic questions
4. Rebuilds using Mindvalley components
5. Delivers optimized page with improvement notes
```

### Detailed Analysis Request
```
User: "Analyze this competitor page and rebuild it for our meditation course:
https://competitor.com/course"

Agent: [REDESIGN MODE]
1. Scrapes competitor page
2. Extracts their value prop, features, pricing
3. Identifies what works (strengths) and what doesn't (weaknesses)
4. Asks about your specific course positioning
5. Rebuilds with Mindvalley components optimized for meditation audience
6. Explains each optimization decision
```

### Quick Optimization
```
User: "This page isn't converting well, can you improve it?
https://mysite.com/offer"

Agent: [REDESIGN MODE]
1. Analyzes current page
2. Identifies top 3 conversion blockers
3. Asks which to prioritize
4. Rebuilds with fixes applied
5. Predicts conversion impact of each change
```

## What the Agent Analyzes

### Conversion Optimization Checklist

**Hero Section:**
- [ ] Clear value proposition
- [ ] Benefit-focused headline
- [ ] Single primary CTA above fold
- [ ] Action-oriented CTA text
- [ ] Supporting hero image

**Visual Hierarchy:**
- [ ] F-pattern or Z-pattern flow
- [ ] CTAs in high-visibility zones
- [ ] 50-100% white space around CTAs
- [ ] 3-4 font sizes maximum
- [ ] No competing elements

**Social Proof:**
- [ ] Authentic testimonials with photos
- [ ] Positioned early (above fold or after hero)
- [ ] Credible statistics
- [ ] Trust signals (logos, badges)

**Content Clarity:**
- [ ] Benefit-focused (not feature-focused)
- [ ] Scannable (bullets, short paragraphs)
- [ ] Objections addressed (FAQ)
- [ ] Clear narrative flow

**Mobile Experience:**
- [ ] CTAs in thumb-friendly zones (bottom third)
- [ ] 44×44px touch targets
- [ ] Condensed content for scanning
- [ ] Simplified forms (≤3 fields)

**Technical Quality:**
- [ ] Image dimensions set (prevent CLS)
- [ ] 4.5:1 color contrast
- [ ] Keyboard accessible
- [ ] Logical heading hierarchy

## Component Mapping Strategy

The agent automatically maps existing page sections to Mindvalley components:

| Original Section | Mindvalley Component |
|-----------------|---------------------|
| Hero section | Hero - Dark Background with Image Overlay |
| Feature cards | Technique Card - White Glass (grid) |
| Course curriculum | Curriculum Module - Two Column with Image |
| Pricing table | Comparison Table - Details Column |
| Stats/metrics | Trust Signals - 4 Column Stats Grid |
| Testimonials | Technique Card - White Glass (adapted) |
| FAQ | FAQ Item - Left Border Accent |
| Important notices | Price Clarification Box - White Glass |

## Expected Outputs

### Redesigned Page Includes:
1. **Full HTML file** with all Mindvalley components integrated
2. **Design Tokens + Typography System** (foundation)
3. **All content** from original page (preserved or optimized)
4. **Conversion optimizations** applied based on analysis
5. **WCAG 2.2 AA compliance** (accessibility)
6. **Mobile-first responsive design** (62.54% traffic)
7. **Core Web Vitals optimization** (LCP, INP, CLS)

### Documentation Includes:
1. **Original page analysis** - What was found, strengths/weaknesses
2. **Optimization improvements** - Specific changes made with rationale
3. **Expected conversion impact** - Research-backed predictions
4. **Component list** - Which components used (with Airtable IDs)
5. **Testing recommendations** - A/B test suggestions, metrics to track

## Research-Backed Predictions

When the agent delivers a redesign, it provides evidence-based impact predictions:

- **CTA above fold**: +20-30% conversion increase
- **Early trust signals**: +40% credibility boost
- **Simplified forms**: +50% completion rate
- **Mobile optimization**: Addresses 62.54% of traffic
- **Benefit-focused headlines**: +371% CTA improvement
- **Authentic social proof**: Significant trust increase

## How to Invoke

### Method 1: Direct URL
```
"Redesign this page: https://example.com/page"
```

### Method 2: Optimization Request
```
"This page isn't converting: https://mysite.com/offer - can you improve it?"
```

### Method 3: Analysis Request
```
"Analyze this competitor page and rebuild it Mindvalley-style: https://competitor.com"
```

### Method 4: Explicit Agent Call
```
"Use the mindvalley-page-builder agent to redesign: https://example.com"
```

## Tips for Best Results

### Be Specific About Goals
❌ "Make this better"
✅ "Optimize this for email signups from cold traffic"

### Provide Context
❌ "Redesign this page"
✅ "Redesign this for our meditation course launch targeting skeptical beginners"

### Answer Strategic Questions
The agent will ask 5-8 strategic questions - thoughtful answers lead to better redesigns:
- Conversion goal
- Target audience
- Optimization priorities
- Content preferences
- Brand requirements

### Review the Analysis
The agent identifies HIGH/MEDIUM/LOW impact opportunities - review these before rebuild to ensure alignment.

## What Makes This Different

### Traditional Page Builder:
- Build from scratch with user specifications
- Generic conversion best practices
- Component assembly only

### Mindvalley Page Builder (Enhanced):
- ✅ Analyzes existing pages intelligently
- ✅ Identifies specific conversion blockers
- ✅ Asks strategic questions for context
- ✅ Maps content to optimal components
- ✅ Applies evidence-based optimizations
- ✅ Predicts conversion impact
- ✅ Documents all improvements
- ✅ Maintains Mindvalley brand consistency

## Related Documentation

- **Component System**: `/Users/vishen/Documents/Github/workspace/README-COMPONENT-SYSTEM.md`
- **Quick Start**: `/Users/vishen/Documents/Github/workspace/QUICK-START-COMPONENTS.md`
- **New Page Checklist**: `/Users/vishen/Documents/Github/workspace/CHECKLIST-NEW-PAGE.md`
- **Process Guide**: `/Users/vishen/Documents/Github/workspace/PROCESS-GUIDE-MINDVALLEY-COMPONENTS.md`
- **Agent Guide**: `/Users/vishen/Documents/Github/workspace/HOW-TO-USE-AGENT.md`

---

## Quick Reference Card

**REDESIGN MODE AUTO-TRIGGERS WHEN:**
- User provides a URL
- User says "redesign", "optimize", "improve", "analyze"
- User mentions converting/rebuilding existing page

**5-PHASE WORKFLOW:**
1. **Scrape** → Firecrawl extracts content
2. **Analyze** → Identifies conversion weaknesses
3. **Question** → Asks strategic clarifications
4. **Rebuild** → Maps to Mindvalley components
5. **Deliver** → Page + optimization documentation

**KEY CAPABILITIES:**
- ✅ URL analysis & content extraction
- ✅ Conversion optimization diagnosis
- ✅ Strategic question framework
- ✅ Component mapping intelligence
- ✅ Evidence-based improvement predictions
- ✅ Full Mindvalley design system application

**ALWAYS INCLUDED:**
- Design Tokens (CSS variables)
- Typography System (Gilroy/Inter)
- Official Mindvalley components
- WCAG 2.2 AA compliance
- Mobile-first responsive
- Core Web Vitals optimization
- Conversion best practices
