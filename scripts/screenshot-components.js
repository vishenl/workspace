#!/usr/bin/env node

/**
 * Automated Component Screenshot Generator
 *
 * This script uses Puppeteer to take screenshots of all component preview files
 * and saves them to the screenshots/ directory.
 *
 * Usage:
 *   1. Make sure your local server is running on port 8000
 *   2. Install Puppeteer: npm install puppeteer
 *   3. Run: node scripts/screenshot-components.js
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const components = [
    {
        name: 'hero-dark-with-image',
        url: 'http://localhost:8000/components/hero-dark-with-image.html',
        viewport: { width: 1920, height: 1080 }
    },
    {
        name: 'curriculum-module',
        url: 'http://localhost:8000/components/curriculum-module.html',
        viewport: { width: 1200, height: 800 }
    },
    {
        name: 'teacher-cards',
        url: 'http://localhost:8000/components/teacher-cards.html',
        viewport: { width: 1400, height: 900 }
    },
    {
        name: 'typography-system',
        url: 'http://localhost:8000/components/typography-system.html',
        viewport: { width: 1200, height: 1800 }
    },
    {
        name: 'trust-signals',
        url: 'http://localhost:8000/components/trust-signals.html',
        viewport: { width: 1200, height: 600 }
    },
    {
        name: 'section-header',
        url: 'http://localhost:8000/components/section-header.html',
        viewport: { width: 1200, height: 500 }
    },
    {
        name: 'faq-item',
        url: 'http://localhost:8000/components/faq-item.html',
        viewport: { width: 1200, height: 1000 }
    },
    {
        name: 'investment-section',
        url: 'http://localhost:8000/components/investment-section.html',
        viewport: { width: 1200, height: 1200 }
    },
    {
        name: 'design-tokens',
        url: 'http://localhost:8000/components/design-tokens.html',
        viewport: { width: 1400, height: 2000 }
    }
];

async function takeScreenshots() {
    // Create screenshots directory if it doesn't exist
    const screenshotsDir = path.join(__dirname, '..', 'screenshots');
    if (!fs.existsSync(screenshotsDir)) {
        fs.mkdirSync(screenshotsDir, { recursive: true });
    }

    console.log('🚀 Starting screenshot capture...\n');

    // Launch browser
    const browser = await puppeteer.launch({
        headless: 'new',
        defaultViewport: null
    });

    try {
        for (const component of components) {
            console.log(`📸 Capturing: ${component.name}...`);

            const page = await browser.newPage();

            // Set viewport
            await page.setViewport(component.viewport);

            // Navigate to component
            await page.goto(component.url, {
                waitUntil: 'networkidle0',
                timeout: 10000
            });

            // Wait a bit for fonts to load
            await page.waitForTimeout(500);

            // Take screenshot
            const screenshotPath = path.join(screenshotsDir, `${component.name}.png`);
            await page.screenshot({
                path: screenshotPath,
                fullPage: true
            });

            console.log(`   ✅ Saved to: screenshots/${component.name}.png`);

            await page.close();
        }

        console.log('\n🎉 All screenshots captured successfully!');
        console.log(`📁 Location: ${screenshotsDir}`);
        console.log('\n📝 Next steps:');
        console.log('   1. Open the screenshots/ folder');
        console.log('   2. Upload each screenshot to the corresponding Airtable record');

    } catch (error) {
        console.error('❌ Error capturing screenshots:', error.message);
        throw error;
    } finally {
        await browser.close();
    }
}

// Run the script
takeScreenshots().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
});
