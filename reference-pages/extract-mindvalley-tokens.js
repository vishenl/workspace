const fs = require('fs');

// Read the CSS file
const css = fs.readFileSync('academy-full.css', 'utf-8');

// Initialize refined tokens object with Mindvalley semantic structure
const tokens = {
  colors: {
    brand: {
      mastery: {}
    },
    text: {},
    background: {},
    border: {},
    accent: {},
    button: {}
  },
  gradients: {
    mastery: {}
  },
  typography: {
    fontFamily: {},
    scale: {
      display: {},
      title: {},
      body: {},
      caption: {}
    },
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
  breakpoints: {}
};

const stats = {
  colorsFound: 0,
  gradientsMapped: 0,
  typographyClassesFound: 0,
  spacingValuesFound: 0,
  breakpointsFound: 0
};

// Helper function to extract CSS rules for a specific class
function extractClassRules(className) {
  const classPattern = new RegExp(`\\.${className.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\s*{([^}]+)}`, 'g');
  const matches = [...css.matchAll(classPattern)];
  return matches.map(m => m[1].trim());
}

// Helper function to parse CSS properties from rule block
function parseProperties(ruleBlock) {
  const props = {};
  const propertyMatches = ruleBlock.matchAll(/([a-z-]+):\s*([^;]+);/g);
  for (const match of propertyMatches) {
    props[match[1]] = match[2].trim();
  }
  return props;
}

// 1. Extract Mastery Brand Colors (mastery-50 through mastery-950)
console.log('🎨 Extracting Mastery brand colors...');
const masteryScales = ['50', '100', '200', '300', '400', '500', '600', '650', '700', '800', '850', '900', '950'];
masteryScales.forEach(scale => {
  const rules = extractClassRules(`bg-mastery-${scale}`);
  if (rules.length > 0) {
    const props = parseProperties(rules[0]);
    if (props['background-color']) {
      tokens.colors.brand.mastery[scale] = props['background-color'];
      stats.colorsFound++;
    }
  }
});

// 2. Extract Mastery Gradients
console.log('🌈 Extracting Mastery gradients...');
const gradientVariants = [
  'gradient',
  'gradient-aurora',
  'gradient-fog',
  'gradient-mist',
  'gradient-soft-bordered',
  'gradient-spring',
  'gradient-surface-fog',
  'gradient-teal-deep',
  'gradient-vertical'
];

gradientVariants.forEach(variant => {
  const rules = extractClassRules(`bg-mastery-${variant}`);
  if (rules.length > 0) {
    const props = parseProperties(rules[0]);
    if (props['background'] || props['background-image']) {
      tokens.gradients.mastery[variant] = props['background'] || props['background-image'];
      stats.gradientsMapped++;
    }
  }
});

// 3. Extract Typography Scale from .mv-type-- classes
console.log('📝 Extracting typography classes...');
const typeClasses = [
  'display1', 'display2', 'display3',
  'title1', 'title2', 'title3', 'title4', 'title5', 'title6',
  'body', 'body-large', 'body-small',
  'caption1', 'caption2',
  'overline'
];

typeClasses.forEach(typeClass => {
  const className = `mv-type--${typeClass}`;
  const rules = extractClassRules(className);

  if (rules.length > 0) {
    const props = parseProperties(rules[0]);
    const typeKey = typeClass.replace(/\d+/, match => `-${match}`);

    // Categorize into display/title/body/caption
    if (typeClass.startsWith('display')) {
      tokens.typography.scale.display[typeClass] = props;
    } else if (typeClass.startsWith('title')) {
      tokens.typography.scale.title[typeClass] = props;
    } else if (typeClass.includes('body')) {
      tokens.typography.scale.body[typeClass] = props;
    } else if (typeClass.startsWith('caption') || typeClass === 'overline') {
      tokens.typography.scale.caption[typeClass] = props;
    }

    stats.typographyClassesFound++;
  }
});

// 4. Extract Font Families from @font-face
console.log('🔤 Extracting font families...');
const fontFaceMatches = css.matchAll(/@font-face\s*{[^}]*font-family:\s*["']?([^"';]+)["']?[^}]*}/g);
const fontFamilies = new Set();
for (const match of fontFaceMatches) {
  const family = match[1].trim();
  fontFamilies.add(family);
}

Array.from(fontFamilies).forEach((family, idx) => {
  const key = family.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  tokens.typography.fontFamily[key] = family;
});

// 5. Extract Font Weights
const fontWeightMatches = css.matchAll(/font-weight:\s*(\d{3}|normal|bold|bolder|lighter);/g);
const fontWeights = new Set();
for (const match of fontWeightMatches) {
  fontWeights.add(match[1]);
}

Array.from(fontWeights).sort((a, b) => {
  const aNum = parseInt(a) || 0;
  const bNum = parseInt(b) || 0;
  return aNum - bNum;
}).forEach(weight => {
  const key = weight === 'normal' ? '400' : weight === 'bold' ? '700' : weight;
  tokens.typography.fontWeight[`weight-${key}`] = weight;
});

// 6. Extract Line Heights
const lineHeightMatches = css.matchAll(/line-height:\s*([^;]+);/g);
const lineHeights = new Set();
for (const match of lineHeightMatches) {
  const lh = match[1].trim();
  // Only capture numeric or unit-based values
  if (lh.match(/^[\d.]+(%|px|rem|em)?$/)) {
    lineHeights.add(lh);
  }
}

Array.from(lineHeights).forEach((lh, idx) => {
  tokens.typography.lineHeight[`lh-${idx + 1}`] = lh;
});

// 7. Extract Letter Spacing
const letterSpacingMatches = css.matchAll(/letter-spacing:\s*([^;]+);/g);
const letterSpacings = new Set();
for (const match of letterSpacingMatches) {
  letterSpacings.add(match[1].trim());
}

Array.from(letterSpacings).forEach((ls, idx) => {
  tokens.typography.letterSpacing[`ls-${idx + 1}`] = ls;
});

// 8. Extract Spacing Scale from actual padding/margin/gap values
console.log('📏 Extracting spacing scale...');
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

// Sort spacing values numerically
const spacingArray = Array.from(spacingValues).sort((a, b) => {
  const aNum = parseFloat(a);
  const bNum = parseFloat(b);
  return aNum - bNum;
});

spacingArray.forEach((value, idx) => {
  tokens.spacing[`${idx}`] = value;
  stats.spacingValuesFound++;
});

// 9. Extract Border Radii
const radiusMatches = css.matchAll(/border-radius:\s*([^;]+);/g);
const radiusValues = new Set();
for (const match of radiusMatches) {
  radiusValues.add(match[1].trim());
}

Array.from(radiusValues).forEach((radius, idx) => {
  tokens.borders.radius[`radius-${idx + 1}`] = radius;
});

// 10. Extract Shadows
const shadowMatches = css.matchAll(/box-shadow:\s*([^;]+);/g);
const shadows = new Set();
for (const match of shadowMatches) {
  shadows.add(match[1].trim());
}

Array.from(shadows).forEach((shadow, idx) => {
  tokens.shadows[`shadow-${idx + 1}`] = shadow;
});

// 11. Extract Breakpoints from media queries
console.log('📱 Extracting breakpoints...');
const mediaMatches = css.matchAll(/@media[^{]*\((?:min|max)-width:\s*(\d+)px\)/g);
const breakpoints = new Set();
for (const match of mediaMatches) {
  breakpoints.add(match[1]);
}

const bpArray = Array.from(breakpoints).sort((a, b) => parseInt(a) - parseInt(b));
const bpNames = ['xs', 'sm', 'md', 'lg', 'xl', '2xl', '3xl', '4xl', '5xl'];
bpArray.forEach((bp, idx) => {
  const name = bpNames[idx] || `bp-${idx + 1}`;
  tokens.breakpoints[name] = `${bp}px`;
  stats.breakpointsFound++;
});

// 12. Extract Text Colors
console.log('🎨 Extracting text colors...');
const textColorPrefixes = ['mastery', 'aqua', 'cool-grey', 'white', 'black'];
textColorPrefixes.forEach(prefix => {
  tokens.colors.text[prefix] = {};

  if (prefix === 'white' || prefix === 'black') {
    const rules = extractClassRules(`text-${prefix}`);
    if (rules.length > 0) {
      const props = parseProperties(rules[0]);
      if (props.color) {
        tokens.colors.text[prefix] = props.color;
      }
    }
  } else {
    // Extract color scales for mastery, aqua, cool-grey
    ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'].forEach(scale => {
      const rules = extractClassRules(`text-${prefix}-${scale}`);
      if (rules.length > 0) {
        const props = parseProperties(rules[0]);
        if (props.color) {
          tokens.colors.text[prefix][scale] = props.color;
        }
      }
    });
  }
});

// 13. Extract Button Colors
console.log('🔘 Extracting button colors...');
const buttonVariants = [
  'mv-btn--mastery',
  'mv-btn--primary',
  'mv-btn--secondary',
  'mv-btn--tertiary',
  'mv-btn--mastery-white',
  'mv-btn--mastery-secondary'
];

buttonVariants.forEach(variant => {
  const rules = extractClassRules(variant);
  if (rules.length > 0) {
    const props = parseProperties(rules[0]);
    const variantKey = variant.replace('mv-btn--', '');
    tokens.colors.button[variantKey] = {
      background: props['background-color'] || props.background,
      color: props.color,
      border: props.border || props['border-color']
    };
  }
});

// Write refined tokens file
fs.writeFileSync('design-system/mindvalley-tokens.json', JSON.stringify(tokens, null, 2));

console.log('');
console.log('✅ Mindvalley Design Tokens extracted successfully!');
console.log('');
console.log('📊 Statistics:');
console.log(`   Mastery brand colors: ${Object.keys(tokens.colors.brand.mastery).length}`);
console.log(`   Mastery gradients: ${stats.gradientsMapped}`);
console.log(`   Typography classes: ${stats.typographyClassesFound}`);
console.log(`   Font families: ${Object.keys(tokens.typography.fontFamily).length}`);
console.log(`   Spacing values: ${stats.spacingValuesFound}`);
console.log(`   Border radii: ${Object.keys(tokens.borders.radius).length}`);
console.log(`   Shadows: ${Object.keys(tokens.shadows).length}`);
console.log(`   Breakpoints: ${stats.breakpointsFound}`);
console.log(`   Button variants: ${Object.keys(tokens.colors.button).length}`);
console.log('');
console.log('📄 File created: design-system/mindvalley-tokens.json');
