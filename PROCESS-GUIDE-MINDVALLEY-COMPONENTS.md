# Process Guide: Using Mindvalley Official Components

## Overview
This guide ensures that all new pages you build use the official Mindvalley components from Airtable when needed, maintaining brand consistency and design quality.

---

## 🎯 When to Use Official Components

Use official components from Airtable when you need:
- **Typography** (headings, body text, text styles)
- **Cards** (program cards, technique cards, curriculum modules)
- **Hero sections** (dark backgrounds, image overlays)
- **Interactive elements** (FAQs, accordions)
- **Comparison tables** (pricing, features)
- **Trust signals** (statistics grids)
- **Alert boxes** (price clarifications, important notes)

---

## 📚 Your Component Library

### Airtable Source
**URL:** https://airtable.com/appeEKr8u6nsrOaAu/tblPZpDvwBqbmqYg7/viwADLg2DQAeoCIL5

### Local Text Reference
**File:** `/Users/vishen/Downloads/MVA Stylesheet.txt`

### Component Preview Directory
**Path:** `/Users/vishen/Documents/Github/workspace/reference-pages/components/`

Available components in Airtable:
1. Design Tokens - Core CSS variables
2. Typography System - Complete text styling
3. Hero - Dark Background with Image Overlay
4. Trust Signals - 4 Column Stats Grid
5. FAQ Item - Left Border Accent
6. Curriculum Module - Two Column with Image
7. Program Card - 16:9 Image Box
8. Comparison Table - Details Column
9. Price Clarification Box - White Glass
10. Technique Card - White Glass

---

## 🔄 The Process

### Step 1: Review Your Design Requirements
Before starting any new page, ask yourself:
- What sections does this page need?
- Do any of these sections match our official components?
- What's the primary goal of each section?

### Step 2: Check the Component Library

**Option A: Browse Airtable (Recommended for Visual Reference)**
1. Open: https://airtable.com/appeEKr8u6nsrOaAu/tblPZpDvwBqbmqYg7/viwADLg2DQAeoCIL5
2. Look through the "Component" column
3. Click on attachments to see visual examples
4. Review the "Notes" field for usage guidelines
5. Copy CSS from the "CSS" field

**Option B: Check Local Stylesheet**
1. Open `/Users/vishen/Downloads/MVA Stylesheet.txt`
2. Search for component names (e.g., "FAQ Item", "Hero", "Program Card")
3. Look at HTML structure comments
4. Review CSS in context

**Option C: Browse Component Files**
```bash
cd /Users/vishen/Documents/Github/workspace/reference-pages/components/
ls -la
```

### Step 3: Implement the Component

#### For Each Component You Use:

1. **Copy the CSS**
   - From Airtable CSS field, or
   - From `/Users/vishen/Downloads/MVA Stylesheet.txt`

2. **Copy the HTML Structure**
   - Look in the "Notes" field for HTML examples
   - Check component preview files in `reference-pages/components/`

3. **Include Design Tokens**
   Always start your page with:
   ```html
   <style>
   :root {
     /* Colors */
     --mv-purple: #8A2BE2;
     --mv-purple-light: #DA70D6;
     --mv-gold: #DAA520;
     --mv-dark: #1A1A1A;
     --mv-gray: #404040;
     --mv-gray-light: #FAFAFA;
     --mv-white: #FFFFFF;

     /* Typography */
     --font-heading: 'Gilroy', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
     --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

     /* Spacing, Shadows, Radius - see Design Tokens component */
   }
   </style>
   ```

4. **Use Component-Specific Classes**
   - Don't rename classes (e.g., keep `.faq-item`, not `.my-faq`)
   - Maintain the exact HTML structure
   - Use CSS variables instead of hardcoded values

### Step 4: Customize Appropriately

**✅ Safe to Customize:**
- Content (text, images)
- Colors using CSS variables
- Spacing using CSS variables
- Grid columns for responsive layouts

**❌ Don't Change:**
- Core class names
- HTML structure (nesting, order)
- Font families (unless you have a good reason)
- Animation timing functions

### Step 5: Test Responsiveness

All official components are responsive. Test at:
- Mobile: 375px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px+

---

## 💡 Quick Reference Guide

### Common Component Combinations

**Landing Page Structure:**
```
1. Hero - Dark Background with Image Overlay
2. Trust Signals - 4 Column Stats Grid
3. Program Card - 16:9 Image Box (in grid)
4. FAQ Item - Left Border Accent (multiple)
5. Price Clarification Box (if needed)
```

**Course/Program Page:**
```
1. Hero section
2. Curriculum Module - Two Column with Image (multiple)
3. Comparison Table - Details Column
4. FAQ Item
5. Trust Signals
```

**Sales Page:**
```
1. Hero - Dark Background
2. Trust Signals
3. Technique Card - White Glass (features)
4. Comparison Table
5. Price Clarification Box
6. FAQ Item
```

---

## 🛠️ Practical Workflow

### When Claude Builds a New Page For You:

**Tell Claude:**
```
"Build me a [page type] using components from our Mindvalley Airtable library.
Check /Users/vishen/Downloads/MVA Stylesheet.txt for official components.
Use [specific components] for [specific sections]."
```

**Example:**
```
"Build me a sales page for a manifestation course using:
- Hero - Dark Background component for the hero
- Trust Signals for social proof
- Comparison Table for pricing options
- FAQ Item components for the FAQ section
Check MVA Stylesheet.txt for the exact CSS."
```

### When You Build Pages Manually:

1. **Start with the template structure:**
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Page Title</title>
       <link rel="stylesheet" href="../reference-pages/public/css/mindvalley-clean.css">
   </head>
   <body>
       <!-- Component HTML here -->
   </body>
   </html>
   ```

2. **Copy component CSS** from Airtable or stylesheet

3. **Copy component HTML** and customize content

4. **Test** in browser

---

## 📋 Component Selection Cheat Sheet

| Need | Use This Component |
|------|-------------------|
| Large headline section | Hero - Dark Background with Image Overlay |
| Stats/numbers showcase | Trust Signals - 4 Column Stats Grid |
| Collapsible Q&A | FAQ Item - Left Border Accent |
| Course curriculum | Curriculum Module - Two Column with Image |
| Program/course listings | Program Card - 16:9 Image Box |
| Feature comparison | Comparison Table - Details Column |
| Important pricing notes | Price Clarification Box - White Glass |
| Meditation techniques | Technique Card - White Glass |
| All text styling | Typography System |
| Consistent styling | Design Tokens (CSS variables) |

---

## 🔍 How to Find Components Quickly

### Search by Purpose:
1. **Airtable:** Use Ctrl+F / Cmd+F to search the "Component" or "Notes" fields
2. **Text file:** Search MVA Stylesheet.txt for keywords like "FAQ", "Hero", "Card"
3. **Component URLs:** Each Airtable record has a "Component URL" for live preview

### Most Used Components:
1. **Design Tokens** - Use in EVERY page
2. **Typography System** - Use in EVERY page
3. **Hero - Dark Background** - Most landing pages
4. **FAQ Item** - Almost all pages need FAQs
5. **Trust Signals** - Social proof sections

---

## ✅ Quality Checklist

Before marking any page as complete, verify:

- [ ] Uses Design Tokens (CSS variables)
- [ ] Uses Typography System for all text
- [ ] All components copied exactly (no structural changes)
- [ ] Only content has been customized (text, images)
- [ ] Responsive at 375px, 768px, 1024px
- [ ] Hover states work correctly
- [ ] Interactive components (FAQs) function properly
- [ ] Brand colors (purple, gold) used correctly
- [ ] Font families (Gilroy for headings, Inter for body) are correct

---

## 🚀 Pro Tips

1. **Always start with Design Tokens**
   Every page should include the CSS variables from the Design Tokens component.

2. **Don't reinvent the wheel**
   If a component exists for your use case, use it. Building from scratch risks inconsistency.

3. **Preview before committing**
   Use the Component URL field in Airtable to see live examples.

4. **Keep the structure intact**
   The HTML structure is designed for accessibility and responsiveness. Don't change it.

5. **Use CSS variables for customization**
   Instead of hardcoding colors, use `var(--mv-purple)`, etc.

6. **Check the Notes field**
   Each component has usage guidelines, best practices, and HTML structure examples.

7. **Combine components thoughtfully**
   Components are designed to work together. Use the "Common Component Combinations" section above.

---

## 🎓 Learning Path

### Week 1: Get Familiar
- Browse all components in Airtable
- Read the Notes for each component
- Click through Component URLs to see live examples

### Week 2: Practice
- Build a simple landing page using 3-4 components
- Experiment with customizing content only
- Test responsiveness

### Week 3: Master
- Build complex pages with 5+ components
- Mix and match components for different page types
- Create your own page templates using official components

---

## 📞 Getting Help

When asking Claude for help:
1. Mention the specific component by name
2. Reference the Airtable URL or stylesheet location
3. Describe what you're trying to achieve
4. Ask for examples using the official components

**Good prompt:**
"I need a FAQ section. Use the 'FAQ Item - Left Border Accent' component from our MVA Stylesheet.txt. Show me how to implement 5 FAQs."

**Bad prompt:**
"Build me a FAQ section" (might not use official components)

---

## 🔄 Updating This Process

As new components are added to Airtable:
1. Update the "Available components in Airtable" list
2. Add to the "Component Selection Cheat Sheet"
3. Include in "Common Component Combinations" if applicable

---

**Last Updated:** November 2025
**Maintained By:** Your team
**Component Library Version:** 1.0
