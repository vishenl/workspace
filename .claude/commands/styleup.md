# StyleUp: Transform HTML into Visually Stunning Pages

You are an elite visual designer specializing in creating magazine-quality, high-impact web pages. When this command is invoked, dramatically enhance the visual design of the specified HTML file using Mindvalley brand standards.

## Your Mission

Transform basic HTML documents into visually stunning, magazine-quality pages that rival the best of Apple, Stripe, and Mindvalley design.

## Design System Foundation

Always link to the Mindvalley base CSS:
```html
<link rel="stylesheet" href="../../mv-selfreset-base.css">
```

Use Mindvalley typography classes:
- `mv-type--headline1` through `mv-type--headline6`
- `mv-container` for layout containers

## Visual Enhancement Checklist

### 1. Hero Section (Full Impact)
- [ ] Full viewport height (`min-height: 100vh`)
- [ ] Background image with overlay gradient
- [ ] Animated floating particles or subtle motion
- [ ] Glowing/pulsing badge or label
- [ ] Gradient text for key numbers/stats
- [ ] Scroll indicator at bottom
- [ ] Stats row with large numbers

### 2. Section Design Patterns
- [ ] Alternating light/dark backgrounds
- [ ] Magazine-style split layouts (image | content)
- [ ] Giant decorative numbers or quotes
- [ ] Color-coded elements with gradients
- [ ] Generous whitespace (100px+ padding)

### 3. Interactive Elements
- [ ] Hover lift effects (`transform: translateY(-10px)`)
- [ ] Scale on hover for cards
- [ ] Glowing borders/shadows on focus
- [ ] Smooth transitions (0.3s ease)

### 4. Visual Hierarchy
- [ ] Giant headline numbers (3-8rem)
- [ ] Color-coded categories/phases
- [ ] Progress indicators or funnels
- [ ] Timeline with gradient lines
- [ ] Dashboard-style metrics

### 5. Animations (CSS Only)
```css
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-20px); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 20px rgba(122, 18, 212, 0.3); }
    50% { box-shadow: 0 0 40px rgba(122, 18, 212, 0.6); }
}
```

### 6. Color System
```css
:root {
    /* Mindvalley Core */
    --mv-purple: #7a12d4;
    --mv-purple-light: #9a3de8;

    /* Neutrals */
    --ink-black: #0a0a0a;
    --mist: #f5f5f5;

    /* Accent (customize per project) */
    --accent-gold: #c9a959;

    /* Phase/Category Colors */
    --phase-1: #4a90d9;
    --phase-2: #7a12d4;
    --phase-3: #c9a959;
    --phase-4: #d94a4a;
}
```

### 7. Card Patterns
```css
/* Glass Card */
.glass-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    backdrop-filter: blur(10px);
}

/* Elevated Card */
.elevated-card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.elevated-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 30px 80px rgba(0,0,0,0.15);
}
```

### 8. Typography Enhancements
```css
/* Gradient Text */
.gradient-text {
    background: linear-gradient(135deg, var(--accent), #fff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Giant Numbers */
.giant-number {
    font-family: Grotesk-Bold, sans-serif;
    font-size: 8rem;
    line-height: 1;
}

/* Decorative Quote */
.giant-quote::before {
    content: '"';
    font-size: 8rem;
    position: absolute;
    opacity: 0.1;
}
```

### 9. Layout Patterns

**Split Screen (Magazine Style)**
```css
.split-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    min-height: 100vh;
}

.split-section:nth-child(even) {
    direction: rtl;
}

.split-section:nth-child(even) > * {
    direction: ltr;
}
```

**Funnel Visualization**
```css
.funnel-stage:nth-child(1) .bar { width: 100%; }
.funnel-stage:nth-child(2) .bar { width: 65%; margin-left: 17.5%; }
.funnel-stage:nth-child(3) .bar { width: 35%; margin-left: 32.5%; }
.funnel-stage:nth-child(4) .bar { width: 20%; margin-left: 40%; }
```

**Timeline with Gradient**
```css
.timeline-line {
    position: absolute;
    left: 50%;
    width: 4px;
    background: linear-gradient(to bottom, var(--phase-1), var(--phase-2), var(--phase-3), var(--phase-4));
}
```

### 10. Responsive Breakpoints
```css
@media (max-width: 1000px) {
    .split-section { grid-template-columns: 1fr; }
    .giant-number { font-size: 5rem; }
}

@media (max-width: 768px) {
    .giant-number { font-size: 3.5rem; }
    .timeline-line { left: 20px; }
}
```

## Process

1. **Read the current HTML file** to understand its structure and content
2. **Identify the content type** (proposal, launch plan, sales page, etc.)
3. **Plan the visual sections** based on content hierarchy
4. **Apply the design patterns** from this checklist
5. **Add animations and interactivity** for engagement
6. **Ensure responsive design** works on all devices
7. **Test hover states and transitions** mentally
8. **Commit and push** the changes

## Quality Standards

- Every section should have visual interest
- No plain white boxes - add gradients, borders, or shadows
- Numbers should be BIG and prominent
- Use icons/emojis strategically for visual anchors
- Maintain generous whitespace
- Ensure all text is readable (contrast ratios)
- Mobile-first responsive design

## Example Transformation

**Before:** Plain `<h2>Revenue: $2.5M</h2>`

**After:**
```html
<div class="revenue-hero">
    <div class="revenue-total">$2.5M+</div>
    <div class="revenue-subtitle">Year 1 Potential Revenue</div>
</div>
```
```css
.revenue-total {
    font-family: Grotesk-Bold, sans-serif;
    font-size: 8rem;
    background: linear-gradient(135deg, var(--accent-gold), #fff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: countUp 1.5s ease-out;
}
```

---

Now read the specified file and transform it into a visually stunning page!
