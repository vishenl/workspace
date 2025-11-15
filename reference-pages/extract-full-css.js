const https = require('https');
const zlib = require('zlib');
const fs = require('fs');

// List of CSS URLs from the HTML
const cssUrls = [
  'https://unpkg.com/vue-select@latest/dist/vue-select.css',
  'https://storyblok-assets.mindvalley.com/css/app.90db21c78a12d2d27b1d.css',
  'https://storyblok-assets.mindvalley.com/css/components/page.5367e9336782c7c050b7.css',
  'https://storyblok-assets.mindvalley.com/css/components/column.1bdf5d4ea2f744a5bf80.css',
  'https://storyblok-assets.mindvalley.com/css/components/mindvalley-navbar-pop-up-version.9b2fde17f63eb345934d.css',
  'https://storyblok-assets.mindvalley.com/css/components/lazy-image.17ebd3997972e7a35e49.css',
  'https://storyblok-assets.mindvalley.com/css/components/ellipse-number.aa335b596f1941fec487.css',
  'https://storyblok-assets.mindvalley.com/css/components/double-media-scroll.2262fa0a7257ed07e009.css',
  'https://storyblok-assets.mindvalley.com/css/components/rsvp-now.af88bd0e75d3d0ed95d3.css',
  'https://storyblok-assets.mindvalley.com/css/vendors/components/phone-number-form/components/registration/components/registration-one-step/compon/42223800.fd6cf5e288fb332a56b8.css'
];

let output = `/* =============================================
   MINDVALLEY ACADEMY - COMPLETE CSS EXTRACTION
   Generated: ${new Date().toISOString()}
   Source: https://www.mindvalley.com/academy

   This file contains all external CSS files
   decompressed from Brotli/Gzip encoding
   ============================================= */

`;

let count = 0;

function fetchCSS(url) {
  return new Promise((resolve, reject) => {
    console.log(`Fetching ${count + 1}/${cssUrls.length}: ${url}`);

    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'text/css,*/*;q=0.1',
        'Accept-Encoding': 'br, gzip, deflate'
      }
    };

    https.get(url, options, (res) => {
      const chunks = [];

      res.on('data', chunk => chunks.push(chunk));

      res.on('end', () => {
        const buffer = Buffer.concat(chunks);
        const encoding = res.headers['content-encoding'];

        let decompressed;
        try {
          if (encoding === 'br') {
            decompressed = zlib.brotliDecompressSync(buffer);
          } else if (encoding === 'gzip') {
            decompressed = zlib.gunzipSync(buffer);
          } else if (encoding === 'deflate') {
            decompressed = zlib.inflateSync(buffer);
          } else {
            decompressed = buffer;
          }

          const css = decompressed.toString('utf-8');
          console.log(`  ✓ Downloaded and decompressed (${encoding || 'none'}) - ${css.length} bytes`);
          resolve(css);
        } catch (err) {
          console.log(`  ✗ Decompression failed: ${err.message}`);
          reject(err);
        }
      });
    }).on('error', reject);
  });
}

async function extractAllCSS() {
  for (const url of cssUrls) {
    count++;
    output += `\n\n/* =============================================
   EXTERNAL STYLESHEET #${count}
   Source: ${url}
   ============================================= */\n\n`;

    try {
      const css = await fetchCSS(url);
      output += css;
    } catch (err) {
      output += `/* Failed to fetch: ${err.message} */`;
      console.error(`Failed to fetch ${url}:`, err.message);
    }
  }

  fs.writeFileSync('academy-full.css', output);
  console.log('\n=== Extraction Complete ===');
  console.log(`Written to: academy-full.css`);
  console.log(`Total size: ${(output.length / 1024).toFixed(2)} KB`);
  console.log(`Lines: ${output.split('\n').length}`);
}

extractAllCSS().catch(console.error);
