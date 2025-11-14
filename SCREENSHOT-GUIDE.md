# Component Screenshot Guide

Since automated screenshot generation is having technical issues, here's the manual process (takes about 5 minutes):

## Quick Steps

1. **Make sure your local server is running**
   ```bash
   python3 -m http.server 8000
   ```

2. **Open each component in your browser and take screenshots:**

   Press **Cmd + Shift + 4** on Mac (or use screenshot tool), then:

   | Component | URL | Airtable Record Name |
   |-----------|-----|---------------------|
   | Hero | http://localhost:8000/components/hero-dark-with-image.html | Hero - Dark Background with Image Overlay |
   | Curriculum | http://localhost:8000/components/curriculum-module.html | Curriculum Module - Two Column with Image |
   | Teachers | http://localhost:8000/components/teacher-cards.html | Teacher Cards - Three Column Grid |
   | Typography | http://localhost:8000/components/typography-system.html | Typography System - Complete Documentation |
   | Trust Signals | http://localhost:8000/components/trust-signals.html | Trust Signals - 4 Column Stats Grid |
   | Section Header | http://localhost:8000/components/section-header.html | Section Header - Eyebrow + Title + Description |
   | FAQ | http://localhost:8000/components/faq-item.html | FAQ Item - Left Border Accent |
   | Investment | http://localhost:8000/components/investment-section.html | Investment Section - ROI Calculator |
   | Design Tokens | http://localhost:8000/components/design-tokens.html | Design Tokens - Mindvalley Brand System |

3. **Upload to Airtable:**
   - Open your Airtable: https://airtable.com/appeEKr8u6nsrOaAu/tblPZpDvwBqbmqYg7
   - Find the matching component record
   - Drag and drop the screenshot into the "Attachments" field

## Tips

- **Browser zoom:** Set to 100% for consistent screenshots
- **Window size:** Maximize browser window for best quality
- **Naming:** Name screenshots the same as component files (e.g., `hero-dark-with-image.png`)
- **Quality:** PNG format recommended for crisp text

## Alternative: Use Browser Extensions

You can also use browser extensions for full-page screenshots:
- **Chrome/Edge:** "GoFullPage - Full Page Screen Capture"
- **Firefox:** "Fireshot"
- **Safari:** Cmd + Shift + 4, then Spacebar to capture window

Total time estimate: **5-7 minutes** for all 9 components
