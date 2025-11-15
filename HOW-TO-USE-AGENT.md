# How to Use the Mindvalley Page Builder Agent

## 🚀 Quick Start (30 seconds)

### Step 1: Invoke the Agent
Type this in Claude:
```
/agent mindvalley-page-builder
```

### Step 2: Tell It What You Want
Be specific about the page type:
```
Build me a sales page for a manifestation course
```

### Step 3: Wait for the Magic
The agent will:
1. ✅ Fetch components from Airtable
2. ✅ Use Design Tokens + Typography System
3. ✅ Build the page with official components only
4. ✅ Give you the complete HTML file

That's it! 🎉

---

## 📋 Usage Examples

### Example 1: Landing Page
```
/agent mindvalley-page-builder

Build a landing page for our new AI Mastery program.
Include:
- Hero section with dark background
- Trust signals showing 19,000+ students
- 3 program cards for related courses
- FAQ section with 5 questions
```

### Example 2: Sales Page
```
/agent mindvalley-page-builder

Create a sales page for the Spiritual Mastery certification.
I need:
- Compelling hero section
- Social proof stats
- Comparison table for 2 pricing tiers
- FAQ section
- Price clarification box
```

### Example 3: Course Page
```
/agent mindvalley-page-builder

Build a course overview page for Social Media Mastery.
Include:
- Hero section
- 6 curriculum modules with images
- Trust signals
- FAQ section
```

### Example 4: Simple Request
```
/agent mindvalley-page-builder

Build a landing page for a meditation course
```

*The agent will ask follow-up questions if needed*

---

## 💡 Pro Tips

### Tip 1: Be Specific (But Not Too Specific)
**Good:**
```
Build a sales page for a manifestation course with pricing comparison
```

**Too Vague:**
```
Build me a page
```

**Too Specific (let the agent decide components):**
```
Build a sales page using hero component, 3 technique cards,
comparison table with exactly 4 rows, FAQ with purple borders...
```

### Tip 2: Mention Key Content
```
Build a landing page for AI Mastery with:
- 3 key benefits
- Stats: 5,000+ students, 95% satisfaction
- 4 FAQ questions about pricing and access
```

### Tip 3: Reference Existing Pages
```
Build a page similar to the Spiritual Summit page,
but for a business coaching program
```

---

## 🎯 What the Agent Does Automatically

You don't need to mention these - the agent handles them:

✅ Fetches components from Airtable
✅ Includes Design Tokens (CSS variables)
✅ Includes Typography System
✅ Uses exact component CSS and HTML
✅ Adds proper HTML5 structure
✅ Makes it responsive
✅ Uses CSS variables (no hardcoded colors)
✅ Adds component comments in HTML

---

## 🔍 What to Tell the Agent

### Always Mention:
- **Page type** (landing, sales, course, etc.)
- **Topic/product** (AI Mastery, Manifestation, etc.)
- **Key sections needed** (hero, FAQs, pricing, etc.)

### Optionally Mention:
- Specific stats/numbers to include
- How many items (e.g., "5 FAQs", "3 program cards")
- Pricing tiers or comparison needs
- Special requirements (e.g., "needs a price clarification")

### Don't Mention:
- Which specific components to use (agent knows best)
- CSS details (agent handles this)
- Responsive breakpoints (automatic)
- Colors/fonts (uses design tokens)

---

## 📊 Common Page Types & What You Get

### Landing Page
**You say:**
```
Build a landing page for [topic]
```

**Agent uses:**
- Design Tokens
- Typography System
- Hero - Dark Background
- Trust Signals
- Program Cards (grid)
- FAQ Items

### Sales Page
**You say:**
```
Build a sales page for [product]
```

**Agent uses:**
- Design Tokens
- Typography System
- Hero - Dark Background
- Trust Signals
- Technique Cards (features)
- Comparison Table
- Price Clarification Box
- FAQ Items

### Course Page
**You say:**
```
Build a course page for [course name]
```

**Agent uses:**
- Design Tokens
- Typography System
- Hero section
- Curriculum Modules
- Program Cards (related)
- FAQ Items

---

## 🔧 Troubleshooting

### "The agent isn't using Airtable components"
**Check:** Did you invoke with `/agent mindvalley-page-builder`?
**Fix:** Make sure you start with the exact command

### "I want to modify a component"
**Remember:** The agent uses components exactly as-is
**If you need changes:** After the page is built, ask for content customization only

### "The agent is taking too long"
**Normal:** Fetching from Airtable takes a moment
**Wait:** Usually 30-60 seconds for a complete page

### "I want to add just one component to an existing page"
**Better approach:** Use the slash command instead
```
/mindvalley-components

Add an FAQ section with 5 questions about pricing
```

---

## 🎓 Learning Progression

### First Time (Do This Now!)
```
/agent mindvalley-page-builder

Build me a simple landing page for a test product.
Include hero, stats, and 3 FAQs.
```

See what it does and how the components look.

### Second Time
```
/agent mindvalley-page-builder

Build a sales page for [your actual project]
```

Use it for real work.

### After That
You'll know exactly how to request pages quickly!

---

## ✅ Checklist for Using the Agent

Before invoking:
- [ ] Know what type of page you need
- [ ] Know the topic/product
- [ ] Have a rough idea of sections needed

After agent delivers:
- [ ] Check that Design Tokens are included
- [ ] Verify Typography System is included
- [ ] Confirm components match your request
- [ ] Test responsive (375px, 768px, 1024px)
- [ ] Customize content (text, images) as needed
- [ ] Use `/Users/vishen/Documents/Github/workspace/CHECKLIST-NEW-PAGE.md` for final QA

---

## 🚀 Ready to Try?

**Copy and paste this right now:**

```
/agent mindvalley-page-builder

Build me a simple landing page for a meditation course.
Include a hero section, trust signals showing student count,
and 3 FAQ items about the course format and access.
```

Then watch the magic happen! ✨

---

## 📞 Need Help?

**Agent not working?**
- Check you typed `/agent mindvalley-page-builder` exactly
- Make sure Airtable MCP connection is active

**Want different components?**
- Just ask the agent: "Use curriculum modules instead of program cards"

**Want to see what's possible?**
- Look at: `/Users/vishen/Documents/Github/workspace/reference-pages/EXAMPLE-USING-COMPONENTS.html`

---

**Last Updated:** November 2025
**Agent File:** `.claude/agents/mindvalley-page-builder.md`
