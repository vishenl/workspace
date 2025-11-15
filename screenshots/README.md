# Component Screenshots

This folder contains automatically generated screenshots of all Mindvalley UI components.

## How to Generate Screenshots

1. Make sure your local server is running:
   ```bash
   python3 -m http.server 8000
   ```

2. Install Puppeteer (if not already installed):
   ```bash
   npm install puppeteer
   ```

3. Run the screenshot script:
   ```bash
   node scripts/screenshot-components.js
   ```

## Screenshots Generated

- `hero-dark-with-image.png` - Hero section with dark background and image overlay
- `curriculum-module.png` - Two-column curriculum module with image
- `teacher-cards.png` - Three-column teacher profile cards
- `typography-system.png` - Complete typography documentation
- `trust-signals.png` - 4-column stats grid
- `section-header.png` - Eyebrow + title + description pattern
- `faq-item.png` - FAQ items with left border accent
- `investment-section.png` - Pricing section with ROI calculator
- `design-tokens.png` - Mindvalley brand design tokens showcase

## Upload to Airtable

After screenshots are generated, upload each one to the corresponding component record in Airtable:
https://airtable.com/appeEKr8u6nsrOaAu/tblPZpDvwBqbmqYg7/viwADLg2DQAeoCIL5
