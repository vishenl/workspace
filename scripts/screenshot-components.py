#!/usr/bin/env python3

"""
Automated Component Screenshot Generator

This script uses Playwright to take screenshots of all component preview files
and saves them to the screenshots/ directory.

Usage:
    1. Make sure your local server is running on port 8000
    2. Install Playwright: pip install playwright && playwright install chromium
    3. Run: python3 scripts/screenshot-components.py
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

components = [
    {
        'name': 'hero-dark-with-image',
        'url': 'http://localhost:8000/components/hero-dark-with-image.html',
        'viewport': {'width': 1920, 'height': 1080}
    },
    {
        'name': 'curriculum-module',
        'url': 'http://localhost:8000/components/curriculum-module.html',
        'viewport': {'width': 1200, 'height': 800}
    },
    {
        'name': 'teacher-cards',
        'url': 'http://localhost:8000/components/teacher-cards.html',
        'viewport': {'width': 1400, 'height': 900}
    },
    {
        'name': 'typography-system',
        'url': 'http://localhost:8000/components/typography-system.html',
        'viewport': {'width': 1200, 'height': 1800}
    },
    {
        'name': 'trust-signals',
        'url': 'http://localhost:8000/components/trust-signals.html',
        'viewport': {'width': 1200, 'height': 600}
    },
    {
        'name': 'section-header',
        'url': 'http://localhost:8000/components/section-header.html',
        'viewport': {'width': 1200, 'height': 500}
    },
    {
        'name': 'faq-item',
        'url': 'http://localhost:8000/components/faq-item.html',
        'viewport': {'width': 1200, 'height': 1000}
    },
    {
        'name': 'investment-section',
        'url': 'http://localhost:8000/components/investment-section.html',
        'viewport': {'width': 1200, 'height': 1200}
    },
    {
        'name': 'design-tokens',
        'url': 'http://localhost:8000/components/design-tokens.html',
        'viewport': {'width': 1400, 'height': 2000}
    }
]

async def take_screenshots():
    # Create screenshots directory
    screenshots_dir = Path(__file__).parent.parent / 'screenshots'
    screenshots_dir.mkdir(exist_ok=True)

    print('🚀 Starting screenshot capture...\n')

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)

        try:
            for component in components:
                print(f"📸 Capturing: {component['name']}...")

                # Create new page
                page = await browser.new_page(
                    viewport=component['viewport']
                )

                # Navigate to component
                await page.goto(component['url'], wait_until='networkidle')

                # Wait for fonts to load
                await page.wait_for_timeout(500)

                # Take screenshot
                screenshot_path = screenshots_dir / f"{component['name']}.png"
                await page.screenshot(path=screenshot_path, full_page=True)

                print(f"   ✅ Saved to: screenshots/{component['name']}.png")

                await page.close()

            print('\n🎉 All screenshots captured successfully!')
            print(f'📁 Location: {screenshots_dir}')
            print('\n📝 Next steps:')
            print('   1. Open the screenshots/ folder')
            print('   2. Upload each screenshot to the corresponding Airtable record')

        except Exception as error:
            print(f'❌ Error capturing screenshots: {error}')
            raise
        finally:
            await browser.close()

if __name__ == '__main__':
    asyncio.run(take_screenshots())
