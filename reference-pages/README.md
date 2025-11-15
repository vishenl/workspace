# Mindvalley Academy - Full Page Scrape ✅

**Date:** November 14, 2025
**Source URL:** https://www.mindvalley.com/academy
**Extraction Method:** Node.js with Brotli decompression

## Files Extracted

### 1. `academy.html` (1.2MB)
Complete raw HTML from the Mindvalley Academy homepage, including:
- Full DOM structure
- All embedded JavaScript
- All data attributes and component configurations
- Server-rendered Nuxt.js application markup

### 2. `academy-full.css` (740KB - COMPLETE ✅)
**Complete CSS extraction with all styles successfully decompressed!**

**Successfully Extracted:**
- ✅ All 10 external CSS files (Brotli-decompressed)
- ✅ Vue-select component styles
- ✅ Main app CSS (585KB decompressed)
- ✅ Page component CSS
- ✅ Column component CSS
- ✅ Navbar component CSS
- ✅ Lazy image component CSS
- ✅ Ellipse number component CSS
- ✅ Double media scroll CSS
- ✅ RSVP component CSS
- ✅ Phone number form CSS
- ✅ All inline `<style>` blocks from HTML

## Extraction Details

### Brotli Decompression Success ✅
The Mindvalley CDN serves CSS files with Brotli compression (`content-encoding: br`). Successfully decompressed using Node.js's built-in `zlib.brotliDecompressSync()` function.

**Decompression Results:**
- External CSS #1 (vue-select): 53 bytes (no compression)
- External CSS #2 (app.css): 585,267 bytes decompressed
- External CSS #3 (page.css): 8,750 bytes decompressed
- External CSS #4 (column.css): 10,356 bytes decompressed
- External CSS #5 (navbar.css): 1,624 bytes decompressed
- External CSS #6 (lazy-image.css): 204 bytes decompressed
- External CSS #7 (ellipse-number.css): 11,085 bytes decompressed
- External CSS #8 (double-media-scroll.css): 11,368 bytes decompressed
- External CSS #9 (rsvp-now.css): 11,525 bytes decompressed
- External CSS #10 (phone-number-form.css): 111,668 bytes decompressed

**Total:** 751,900 bytes → 740KB in final file (includes headers and inline styles)

## Page Structure Analysis

The Mindvalley Academy page is a **Nuxt.js/Vue.js** application with:
- Server-side rendering (SSR)
- Component-based CSS architecture
- Storyblok CMS integration
- Google Cloud Storage for static assets (storyblok-assets.mindvalley.com)
- Fastly CDN (via Varnish cache headers)

## Components Identified

Based on CSS file names:
- Page wrapper/layout component
- Multi-column grid system
- Popup navigation bar
- Lazy-loaded images
- Ellipse number displays (probably for stats like "19,000+ students")
- Double media scroll (image/video carousel)
- RSVP/CTA buttons
- Phone number input forms

## Usage

To use these files:

```bash
# View the HTML
open academy.html

# Check CSS (partial)
cat academy.css
```

For full CSS reconstruction, manual browser extraction is recommended.
