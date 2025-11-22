# Mindvalley Self Reset Design System – Claude Code Guide

This document tells Claude how to build pages that match the Self Reset event style.

All pages in this project must:

- Use `mv-selfreset-base.css`
- Use Mindvalley Grotesk font faces defined there
- Use the typography utility classes from that file
- Use `mv-container` for main layout

---

## 1. Layout

### 1.1 Page wrapper

- Always wrap main content in `.mv-container`.
- Keep vertical page spacing using inline padding on sections, for example:

  ```html
  <section class="mv-container" style="padding: 6rem 0 5rem 0;">
    ...
  </section>
  ```

Claude is allowed to factor these paddings into reusable classes later, for example `.mv-section--hero`, but must update the CSS in `mv-selfreset-base.css` at the same time.

### 1.2 Sections

Typical patterns:

* Hero section at the top
* One or more content sections below using `mv-container`
* Footer is also an `mv-container` with smaller type

Do not invent new layout frameworks or utility class systems. Stick to what is already here.

---

## 2. Typography

### 2.1 Fonts

Use the Grotesk families defined in `mv-selfreset-base.css`:

* Body text: `Grotesk-Regular, sans-serif`
* Headings: `Grotesk-Bold` or `Grotesk-Bold-16` as provided by the utility classes

Never override the font family in inline styles unless absolutely required.

### 2.2 Headline utilities

Use these utilities on headings or wrappers instead of hardcoding font sizes:

* `mv-type--headline1` – main hero heading
* `mv-type--headline2` – large section headings
* `mv-type--headline3` and `mv-type--headline4` – subheadings or important section labels
* `mv-type--headline5` to `mv-type--headline9` – smaller subheads and labels

Examples:

```html
<h1 class="mv-type--headline1">Reset how you speak to yourself.</h1>

<h2 class="mv-type--headline3">What you will experience</h2>

<h3 class="mv-type--headline6">Clarity</h3>
```

Paragraphs should use plain `<p>` with no extra font overrides. The base CSS already applies Grotesk Regular.

### 2.3 Eyebrow text

For small eyebrow or kicker text above the hero:

* Uppercase
* Slight letter spacing
* Grotesk Medium

Use inline styles copied from existing pages or move them into a reusable class if needed, for example `.mv-kicker`, but keep the same visual style.

---

## 3. Color

Primary brand color:

* Purple `#7a12d4`

Rules:

* Links in body copy should use the default purple link style from `mv-selfreset-base.css`
* Primary CTAs should be purple background with white text
* Secondary CTAs can be outlined purple or neutral

Do not introduce new brand colors without explicit instruction.

---

## 4. Buttons

Use these patterns when creating CTAs.

### 4.1 Primary CTA

* Background `#7a12d4`
* White text
* Grotesk Bold
* Fully rounded pill

Example:

```html
<a
  href="#"
  style="
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 1rem 2rem;
    background-color: #7a12d4;
    color: white;
    font-family: Grotesk-Bold, sans-serif;
    font-size: 1rem;
    border-radius: 999px;
    text-decoration: none;
  "
>
  Primary CTA
</a>
```

Claude may refactor this into a class like `.mv-btn-primary` inside `mv-selfreset-base.css`, but must update all affected HTML when it does.

### 4.2 Secondary CTA

* Transparent background
* Purple border
* Purple text
* Grotesk Medium
* Same pill radius

Example:

```html
<a
  href="#"
  style="
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 1rem 2rem;
    background-color: transparent;
    color: #7a12d4;
    border: 2px solid #7a12d4;
    font-family: Grotesk-Medium, sans-serif;
    border-radius: 999px;
    text-decoration: none;
  "
>
  Secondary CTA
</a>
```

---

## 5. Content patterns

### 5.1 Hero

* `mv-container` section
* Eyebrow text
* `mv-type--headline1` H1
* Supporting paragraph at slightly larger size and softer color
* CTA row with primary and secondary buttons

### 5.2 Three column feature grid

* `mv-container` section
* A heading using `mv-type--headline3`
* A responsive grid using CSS grid:

  ```html
  <div
    style="
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 2rem;
    "
  >
    <!-- card blocks -->
  </div>
  ```

Each card:

* Small heading using `mv-type--headline6`
* Short paragraph

---

## 6. Rules for Claude Code

When Claude is editing or generating pages in this project:

1. **Read the theme**

   * Always read `mv-selfreset-base.css`
   * Always read this `docs/mindvalley-design-system.md` before making layout or typography changes

2. **Reuse patterns**

   * Copy structure from existing pages like `spiritual-mastery-quiz.html` for new landing pages
   * Reuse hero layout, CTAs and grid patterns instead of inventing new ones

3. **Do not**

   * Do not replace the font stack
   * Do not introduce a new design system or utility framework
   * Do not touch `<head>` unless specifically asked
   * Do not remove the link to `mv-selfreset-base.css`

4. **When in doubt**

   * Prefer copying patterns from existing sections in this repo
   * Ask for new sections to follow an existing pattern unless told otherwise

---

## 7. Quick Reference

### File Structure
```
workspace/
  mv-selfreset-base.css          ← Core design system CSS
  docs/
    mindvalley-design-system.md  ← This file
  .claude/
    commands/
      newpage.md                 ← /newpage command
```

### HTML Template Starter

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
    <link rel="stylesheet" href="mv-selfreset-base.css">
    <style>
        /* Only page-specific styles here */
        /* NO font-face declarations */
        /* NO typography overrides */
    </style>
</head>
<body>
    <section class="mv-container" style="padding: 6rem 0 5rem 0;">
        <h1 class="mv-type--headline1">Hero Heading</h1>
        <p>Supporting text</p>
    </section>
</body>
</html>
```

### Typography Classes Quick Reference
- `mv-type--headline1` - Hero (3rem mobile / 4.5rem desktop)
- `mv-type--headline2` - Major sections (2.25rem mobile / 3.75rem desktop)
- `mv-type--headline3` - Subheadings (1.875rem mobile / 3rem desktop)
- `mv-type--headline4` - Section labels (1.75rem mobile / 2.25rem desktop)
- `mv-type--headline5` - Card titles (1.5rem mobile / 1.75rem desktop)
- `mv-type--headline6` - Small headings (1.375rem mobile / 1.5rem desktop)
- `mv-type--headline7-9` - Smallest labels

### Color Palette
- Primary Purple: `#7a12d4`
- Dark Text: `#0f131a` (from base CSS)
- Links: `#7a12d4` (from base CSS)
