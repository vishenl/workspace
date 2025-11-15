# Quick Start: Building Pages with Official Components

## 🎯 The 3-Step Method

### Step 1: Check the Library
**Airtable:** https://airtable.com/appeEKr8u6nsrOaAu/tblPZpDvwBqbmqYg7/viwADLg2DQAeoCIL5
**OR**
**Local File:** `/Users/vishen/Downloads/MVA Stylesheet.txt`

### Step 2: Copy & Paste
1. Copy CSS from Airtable "CSS" field
2. Copy HTML structure from "Notes" field
3. Include Design Tokens at the top

### Step 3: Customize Content Only
- Change text ✅
- Change images ✅
- Change colors using CSS variables ✅
- Change HTML structure ❌
- Change class names ❌

---

## 📋 Components Quick Reference

| Component Name | Use For | Priority |
|---------------|---------|----------|
| **Design Tokens** | CSS variables - ALWAYS include | 🔴 Required |
| **Typography System** | All text styling - ALWAYS include | 🔴 Required |
| **Hero - Dark Background** | Landing page heroes | 🟠 Common |
| **Trust Signals** | Stats/social proof | 🟠 Common |
| **FAQ Item** | Q&A sections | 🟠 Common |
| **Program Card** | Course/program listings | 🟡 As Needed |
| **Curriculum Module** | Course content breakdown | 🟡 As Needed |
| **Comparison Table** | Pricing/feature comparison | 🟡 As Needed |
| **Price Clarification Box** | Important pricing notes | 🟡 As Needed |
| **Technique Card** | Feature/method listings | 🟡 As Needed |

---

## 💬 How to Ask Claude

### ✅ Good Prompts

```
"Build a sales page using official Mindvalley components from MVA Stylesheet.txt:
- Hero - Dark Background for the top
- Trust Signals for stats
- Comparison Table for pricing
- FAQ Item for FAQs"
```

```
"Add a FAQ section to this page using the 'FAQ Item - Left Border Accent'
component from /Users/vishen/Downloads/MVA Stylesheet.txt"
```

```
"Create a program listing grid using the 'Program Card - 16:9 Image Box'
component. Check the Airtable library for the exact CSS and structure."
```

### ❌ Avoid

```
"Build a FAQ section"
(Too vague - might not use official components)
```

```
"Make it look like Mindvalley"
(Too general - be specific about which components)
```

---

## 🚀 Page Templates

### Landing Page
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Page Title</title>
    <style>
        /* STEP 1: Include Design Tokens - ALWAYS */
        :root {
            --mv-purple: #8A2BE2;
            --mv-purple-light: #DA70D6;
            --mv-gold: #DAA520;
            --font-heading: 'Gilroy', sans-serif;
            --font-body: 'Inter', sans-serif;
        }

        /* STEP 2: Include Typography System - ALWAYS */
        /* [Copy from Airtable "Typography System" component] */

        /* STEP 3: Include component-specific CSS */
        /* [Copy from Airtable for each component you use] */
    </style>
</head>
<body>
    <!-- STEP 4: Add component HTML -->
    <!-- Hero -->
    <!-- Trust Signals -->
    <!-- Main Content -->
    <!-- FAQ -->
</body>
</html>
```

### Sales Page
1. Design Tokens
2. Typography System
3. Hero - Dark Background
4. Trust Signals
5. Technique Card (for features)
6. Comparison Table
7. Price Clarification Box
8. FAQ Item

### Program/Course Page
1. Design Tokens
2. Typography System
3. Hero section
4. Curriculum Module (multiple)
5. Program Card (if showing other programs)
6. FAQ Item

---

## ⚡ Fastest Workflow

### Option 1: Tell Claude Exactly What You Want
```
"Create [page type] using these official components from MVA Stylesheet.txt:
- [Component 1] for [section 1]
- [Component 2] for [section 2]
- etc."
```

### Option 2: Reference Example Page
```
"Build a page similar to /Users/vishen/Downloads/MVA Stylesheet.txt
but for [your topic]. Use the same components."
```

### Option 3: Component by Component
```
"Add the [Component Name] component to this page.
Get it from the Airtable library at
https://airtable.com/appeEKr8u6nsrOaAu/tblPZpDvwBqbmqYg7/viwADLg2DQAeoCIL5"
```

---

## 🎨 Customization Rules

### Safe to Change:
✅ Text content
✅ Images (keep aspect ratios)
✅ Colors using `var(--mv-purple)` syntax
✅ Spacing using `var(--space-lg)` syntax
✅ Number of items (e.g., 5 FAQs instead of 3)

### Don't Change:
❌ Class names (`.faq-item`, `.hero-content`, etc.)
❌ HTML structure (div nesting, semantic tags)
❌ Font families (use Gilroy/Inter as specified)
❌ Animation timings (leave transitions as-is)

---

## 🔧 Common Issues & Fixes

**Issue:** Component looks broken
**Fix:** Check if you included Design Tokens at the top

**Issue:** Fonts look wrong
**Fix:** Include Typography System CSS

**Issue:** Hover effects not working
**Fix:** Don't change class names or HTML structure

**Issue:** Not responsive
**Fix:** Use the exact HTML structure from the component

**Issue:** Colors are off
**Fix:** Use CSS variables like `var(--mv-purple)` instead of hardcoded hex codes

---

## 📖 Daily Checklist

When building any new page:

- [ ] Started with Design Tokens?
- [ ] Included Typography System?
- [ ] Checked Airtable for components I need?
- [ ] Used exact HTML structure?
- [ ] Only customized content (not structure)?
- [ ] Tested at mobile, tablet, desktop sizes?
- [ ] Verified hover/interactive states work?

---

## 🔗 Essential Links

**Airtable Component Library:**
https://airtable.com/appeEKr8u6nsrOaAu/tblPZpDvwBqbmqYg7/viwADLg2DQAeoCIL5

**Local Stylesheet:**
`/Users/vishen/Downloads/MVA Stylesheet.txt`

**Component Preview Files:**
`/Users/vishen/Documents/Github/workspace/reference-pages/components/`

**Full Process Guide:**
`/Users/vishen/Documents/Github/workspace/PROCESS-GUIDE-MINDVALLEY-COMPONENTS.md`

---

**Print this and keep it handy! 🎯**
