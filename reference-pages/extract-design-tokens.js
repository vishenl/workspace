const fs = require('fs');

// Read the CSS file
const css = fs.readFileSync('academy-full.css', 'utf-8');

// Initialize tokens object
const tokens = {
  colors: {},
  typography: {
    fontFamily: {},
    fontSize: {},
    fontWeight: {},
    lineHeight: {},
    letterSpacing: {}
  },
  spacing: {},
  borders: {
    width: {},
    radius: {}
  },
  shadows: {},
  breakpoints: {},
  buttons: {},
  gradients: {}
};

const stats = {
  colorsFound: 0,
  fontsFound: 0,
  spacingFound: 0,
  breakpointsFound: 0,
  shadowsFound: 0,
  gradientsFound: 0
};

// Extract colors (hex, rgb, rgba)
const colorMatches = css.match(/(#[0-9A-Fa-f]{3,8}|rgba?\([^)]+\))/g);
const colorSet = new Set(colorMatches || []);

// Extract font families from @font-face and declarations
const fontFaceMatches = css.matchAll(/@font-face\s*{[^}]*font-family:\s*([^;]+);/g);
const fontFamilies = new Set();
for (const match of fontFaceMatches) {
  fontFamilies.add(match[1].trim());
}

// Extract font sizes
const fontSizeMatches = css.matchAll(/font-size:\s*([^;]+);/g);
const fontSizes = new Set();
for (const match of fontSizeMatches) {
  const size = match[1].trim();
  if (size.match(/^\d+(\.\d+)?(px|rem|em)$/)) {
    fontSizes.add(size);
  }
}

// Extract font weights
const fontWeightMatches = css.matchAll(/font-weight:\s*([^;]+);/g);
const fontWeights = new Set();
for (const match of fontWeightMatches) {
  fontWeights.add(match[1].trim());
}

// Extract line heights
const lineHeightMatches = css.matchAll(/line-height:\s*([^;]+);/g);
const lineHeights = new Set();
for (const match of lineHeightMatches) {
  lineHeights.add(match[1].trim());
}

// Extract letter spacing
const letterSpacingMatches = css.matchAll(/letter-spacing:\s*([^;]+);/g);
const letterSpacings = new Set();
for (const match of letterSpacingMatches) {
  letterSpacings.add(match[1].trim());
}

// Extract spacing values (padding, margin, gap)
const spacingMatches = css.matchAll(/(?:padding|margin|gap)(?:-(?:top|bottom|left|right))?:\s*([^;]+);/g);
const spacingValues = new Set();
for (const match of spacingMatches) {
  const values = match[1].trim().split(/\s+/);
  values.forEach(val => {
    if (val.match(/^\d+(\.\d+)?(px|rem|em)$/)) {
      spacingValues.add(val);
    }
  });
}

// Extract border radius
const radiusMatches = css.matchAll(/border-radius:\s*([^;]+);/g);
const radiusValues = new Set();
for (const match of radiusMatches) {
  radiusValues.add(match[1].trim());
}

// Extract box shadows
const shadowMatches = css.matchAll(/box-shadow:\s*([^;]+);/g);
const shadows = new Set();
for (const match of shadowMatches) {
  shadows.add(match[1].trim());
}

// Extract media queries (breakpoints)
const mediaMatches = css.matchAll(/@media[^{]*\((?:min|max)-width:\s*(\d+px)\)/g);
const breakpoints = new Set();
for (const match of mediaMatches) {
  breakpoints.add(match[1]);
}

// Extract gradients
const gradientMatches = css.matchAll(/background(?:-image)?:\s*((?:linear|radial)-gradient\([^)]+\))/g);
const gradients = new Set();
for (const match of gradientMatches) {
  gradients.add(match[1].trim());
}

// Build color tokens from unique colors
const colorArray = Array.from(colorSet).sort();
colorArray.forEach((color, idx) => {
  // Try to categorize colors
  if (color.includes('255, 255, 255') || color === '#fff' || color === '#ffffff') {
    tokens.colors['white'] = color;
  } else if (color.includes('0, 0, 0') || color === '#000' || color === '#000000') {
    tokens.colors['black'] = color;
  } else {
    tokens.colors[`color-${idx + 1}`] = color;
  }
});

// Build typography tokens
Array.from(fontFamilies).forEach((family, idx) => {
  const key = family.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  tokens.typography.fontFamily[key] = family;
});

Array.from(fontSizes).sort((a, b) => {
  const aNum = parseFloat(a);
  const bNum = parseFloat(b);
  return aNum - bNum;
}).forEach((size, idx) => {
  tokens.typography.fontSize[`size-${idx + 1}`] = size;
});

Array.from(fontWeights).forEach(weight => {
  tokens.typography.fontWeight[`weight-${weight}`] = weight;
});

Array.from(lineHeights).forEach((height, idx) => {
  tokens.typography.lineHeight[`lh-${idx + 1}`] = height;
});

Array.from(letterSpacings).forEach((spacing, idx) => {
  tokens.typography.letterSpacing[`ls-${idx + 1}`] = spacing;
});

// Build spacing scale from actual values
const spacingArray = Array.from(spacingValues).sort((a, b) => {
  const aNum = parseFloat(a);
  const bNum = parseFloat(b);
  return aNum - bNum;
});

spacingArray.forEach((value, idx) => {
  tokens.spacing[`${idx}`] = value;
});

// Build border tokens
Array.from(radiusValues).forEach((radius, idx) => {
  tokens.borders.radius[`radius-${idx + 1}`] = radius;
});

// Build shadow tokens
Array.from(shadows).forEach((shadow, idx) => {
  tokens.shadows[`shadow-${idx + 1}`] = shadow;
});

// Build breakpoint tokens
const bpArray = Array.from(breakpoints).sort((a, b) => parseInt(a) - parseInt(b));
const bpNames = ['sm', 'md', 'lg', 'xl', '2xl', '3xl'];
bpArray.forEach((bp, idx) => {
  const name = bpNames[idx] || `bp-${idx + 1}`;
  tokens.breakpoints[name] = bp;
});

// Build gradient tokens
Array.from(gradients).forEach((gradient, idx) => {
  tokens.gradients[`gradient-${idx + 1}`] = gradient;
});

// Update stats
stats.colorsFound = colorSet.size;
stats.fontsFound = fontFamilies.size;
stats.spacingFound = spacingValues.size;
stats.breakpointsFound = breakpoints.size;
stats.shadowsFound = shadows.size;
stats.gradientsFound = gradients.size;

// Write tokens file
fs.writeFileSync('design-system/mindvalley-tokens.json', JSON.stringify(tokens, null, 2));

console.log('✅ Tokens extracted successfully!');
console.log('');
console.log('📊 Statistics:');
console.log(`   Colors: ${stats.colorsFound}`);
console.log(`   Font families: ${stats.fontsFound}`);
console.log(`   Font sizes: ${fontSizes.size}`);
console.log(`   Spacing values: ${stats.spacingFound}`);
console.log(`   Border radii: ${radiusValues.size}`);
console.log(`   Shadows: ${stats.shadowsFound}`);
console.log(`   Breakpoints: ${stats.breakpointsFound}`);
console.log(`   Gradients: ${stats.gradientsFound}`);
console.log('');
console.log('📄 File created: design-system/mindvalley-tokens.json');
