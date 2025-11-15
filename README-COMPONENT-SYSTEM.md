# Mindvalley Component System - Complete Guide

Welcome! This guide ensures you always use the official Mindvalley components when building new pages.

---

## 📚 What You Have

### 1. **Component Library (Airtable)**
Your source of truth for all official components.

**URL:** https://airtable.com/appeEKr8u6nsrOaAu/tblPZpDvwBqbmqYg7/viwADLg2DQAeoCIL5

**Contains:**
- 10 official components (as of Nov 2025)
- Visual previews (Attachments field)
- CSS code (CSS field)
- Usage notes (Notes field)
- Live preview URLs (Component URL field)

### 2. **Local Stylesheet Reference**
Complete HTML example with all components integrated.

**Location:** `/Users/vishen/Downloads/MVA Stylesheet.txt`

**Use for:**
- Quick reference without opening Airtable
- Copy-paste HTML structures
- See components in context
- Offline access

### 3. **Documentation You Now Have**

I've created 4 essential documents for you:

#### A. **Full Process Guide** (Start here!)
`PROCESS-GUIDE-MINDVALLEY-COMPONENTS.md`
- Complete workflow from start to finish
- When to use which component
- How to ask Claude for help
- Quality checklist
- Common mistakes to avoid

#### B. **Quick Start Guide** (Daily reference)
`QUICK-START-COMPONENTS.md`
- 3-step method for using components
- Quick reference table
- How to ask Claude (with examples)
- Page templates
- Common issues & fixes

#### C. **Working Example Page** (Learn by doing)
`reference-pages/EXAMPLE-USING-COMPONENTS.html`
- Live example using 3 components
- Shows exact implementation
- Includes Design Tokens + Typography System
- Notes on each component
- Working interactive elements

#### D. **Printable Checklist** (Keep at your desk)
`CHECKLIST-NEW-PAGE.md`
- Print and check off as you build
- Every step from start to publish
- Common components list
- Troubleshooting quick reference

---

## 🚀 Getting Started (5 Minutes)

### Step 1: Bookmark These Resources (1 min)

Bookmark in your browser:
1. Airtable Component Library: https://airtable.com/appeEKr8u6nsrOaAu/tblPZpDvwBqbmqYg7/viwADLg2DQAeoCIL5
2. Local Stylesheet: `/Users/vishen/Downloads/MVA Stylesheet.txt`

### Step 2: Read the Quick Start (2 min)

Open `QUICK-START-COMPONENTS.md` and read the 3-step method.

### Step 3: View the Example (2 min)

Open `reference-pages/EXAMPLE-USING-COMPONENTS.html` in your browser.
See how components work in practice.

**That's it!** You're ready to start building pages with official components.

---

## 💡 The Simple Workflow

### Every New Page:

1. **Check the library** → Find components you need
2. **Copy CSS** → From Airtable "CSS" field
3. **Copy HTML** → From Airtable "Notes" field or example
4. **Customize content** → Only text and images
5. **Test responsive** → Mobile, tablet, desktop
6. **Publish** → You're done!

---

## 🎯 The Golden Rules

### ✅ DO:
- Always include Design Tokens (CSS variables)
- Always include Typography System
- Copy component CSS exactly
- Copy component HTML structure exactly
- Customize content (text, images)
- Use CSS variables for colors (var(--mv-purple))
- Test responsive design

### ❌ DON'T:
- Change class names
- Change HTML structure
- Hardcode colors (#8A2BE2 instead of var(--mv-purple))
- Change font families
- Skip responsive testing
- Build from scratch if a component exists

---

## 📖 Document Quick Reference

### When to Use Each:

| Document | When to Use |
|----------|-------------|
| **PROCESS-GUIDE** | First time setup, learning the system, understanding workflows |
| **QUICK-START** | Daily use, quick reference, asking Claude for help |
| **EXAMPLE-PAGE** | Learning by example, understanding implementation |
| **CHECKLIST** | Building any new page (every time!) |

---

## 🎨 Available Components (as of Nov 2025)

### Required on Every Page:
1. **Design Tokens** - CSS variables for colors, spacing, etc.
2. **Typography System** - All text styling (h1-h6, p, etc.)

### Layout & Hero:
3. **Hero - Dark Background with Image Overlay** - Landing page heroes

### Content Components:
4. **Program Card - 16:9 Image Box** - Course/program listings
5. **Curriculum Module - Two Column with Image** - Course content breakdown
6. **Technique Card - White Glass** - Feature/method listings

### Interactive:
7. **FAQ Item - Left Border Accent** - Accordion Q&A sections

### Social Proof:
8. **Trust Signals - 4 Column Stats Grid** - Statistics showcase

### Comparison & Pricing:
9. **Comparison Table - Details Column** - Feature/pricing comparison
10. **Price Clarification Box - White Glass** - Important notes/alerts

---

## 🔧 How to Ask Claude for Help

### Template 1: Building a New Page
```
"Build me a [page type] using official components from MVA Stylesheet.txt:
- [Component 1] for [section]
- [Component 2] for [section]
- [Component 3] for [section]"
```

### Template 2: Adding a Component
```
"Add the [Component Name] component to this page.
Get it from /Users/vishen/Downloads/MVA Stylesheet.txt
or the Airtable library."
```

### Template 3: Fixing Issues
```
"This [component] looks wrong. Check if I'm using the exact
structure from the MVA Stylesheet.txt file."
```

---

## 🎓 Learning Path

### Week 1: Familiarize
- [ ] Browse all 10 components in Airtable
- [ ] Read component Notes fields
- [ ] View Component URLs (live previews)
- [ ] Open EXAMPLE-USING-COMPONENTS.html
- [ ] Read QUICK-START-COMPONENTS.md

### Week 2: Practice
- [ ] Build a simple landing page with 3 components
- [ ] Use the checklist for each step
- [ ] Test responsive design
- [ ] Ask Claude for help using the templates

### Week 3: Master
- [ ] Build complex pages with 5+ components
- [ ] Mix and match components for different page types
- [ ] Create your own templates using official components
- [ ] Help others use the system

---

## 🆘 Troubleshooting

### Component looks broken
→ Check if you included Design Tokens and Typography System

### Colors are wrong
→ Use CSS variables: `var(--mv-purple)` not `#8A2BE2`

### Not responsive
→ Keep exact HTML structure from component

### Hover effects don't work
→ Don't change class names

### Fonts look wrong
→ Include Typography System, use `var(--font-heading)`

### Still stuck?
→ Open EXAMPLE-USING-COMPONENTS.html and compare your code

---

## 📞 Quick Links

**Component Library (Airtable):**
https://airtable.com/appeEKr8u6nsrOaAu/tblPZpDvwBqbmqYg7/viwADLg2DQAeoCIL5

**Local Files:**
- Stylesheet: `/Users/vishen/Downloads/MVA Stylesheet.txt`
- Process Guide: `PROCESS-GUIDE-MINDVALLEY-COMPONENTS.md`
- Quick Start: `QUICK-START-COMPONENTS.md`
- Example Page: `reference-pages/EXAMPLE-USING-COMPONENTS.html`
- Checklist: `CHECKLIST-NEW-PAGE.md`

---

## 🔄 System Maintenance

### Monthly:
- [ ] Review new components added to Airtable
- [ ] Update documentation if components change
- [ ] Share learnings with team

### When Adding New Components:
1. Add to Airtable with all fields filled
2. Update QUICK-START-COMPONENTS.md list
3. Update this README's component list
4. Add usage example if complex

---

## 🎯 Success Metrics

You'll know the system is working when:
- ✅ All pages use official components
- ✅ Brand consistency across all pages
- ✅ Faster page development
- ✅ Less custom CSS written
- ✅ Easier maintenance
- ✅ Better responsive design

---

## 🎉 You're Ready!

You now have everything you need to build beautiful, consistent Mindvalley pages using official components.

**Remember the Golden Rules:**
1. Check the library first
2. Copy exactly
3. Customize content only
4. Test responsive
5. Use the checklist

**Start with:**
Open `QUICK-START-COMPONENTS.md` and try building your first page using the 3-step method!

---

**Questions?** Ask Claude using the templates in the Quick Start guide.

**Last Updated:** November 2025
**System Version:** 1.0
**Components Count:** 10
