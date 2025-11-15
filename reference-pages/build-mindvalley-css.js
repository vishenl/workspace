const fs = require('fs');

// Read tokens and source CSS
const tokens = JSON.parse(fs.readFileSync('design-system/mindvalley-tokens.json', 'utf-8'));
const css = fs.readFileSync('academy-full.css', 'utf-8');

let output = [];
let stats = {
  cssVariablesCreated: 0,
  typographyClassesExtracted: 0,
  buttonClassesExtracted: 0,
  utilityClassesExtracted: 0,
  componentClassesExtracted: 0
};

// Helper function to extract complete CSS rule
function extractFullRule(className) {
  const pattern = new RegExp(`\\.${className.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\s*{[^}]+}`, 'g');
  const matches = [...css.matchAll(pattern)];
  return matches.map(m => m[0]);
}

// Helper function to extract media query rules
function extractMediaRules(className) {
  const pattern = new RegExp(`@media[^{]+{[^}]*\\.${className.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[^}]+}[^}]*}`, 'g');
  const matches = [...css.matchAll(pattern)];
  return matches.map(m => m[0]);
}

output.push('/**');
output.push(' * Mindvalley Design System');
output.push(' * Canonical stylesheet extracted from academy-full.css');
output.push(' * Do not modify manually - regenerate from source');
output.push(' */');
output.push('');

// ========================================
// 1. CSS VARIABLES FROM TOKENS
// ========================================
output.push('/* ========================================');
output.push(' * DESIGN TOKENS - CSS VARIABLES');
output.push(' * ======================================== */');
output.push('');
output.push(':root {');

// Brand Colors - Mastery
output.push('  /* Brand Colors - Mastery */');
Object.entries(tokens.colors.brand.mastery).forEach(([scale, value]) => {
  output.push(`  --mastery-${scale}: ${value};`);
  stats.cssVariablesCreated++;
});
output.push('');

// Text Colors
output.push('  /* Text Colors - Mastery */');
Object.entries(tokens.colors.text.mastery).forEach(([scale, value]) => {
  output.push(`  --text-mastery-${scale}: ${value};`);
  stats.cssVariablesCreated++;
});
output.push('');

output.push('  /* Text Colors - Aqua */');
Object.entries(tokens.colors.text.aqua).forEach(([scale, value]) => {
  output.push(`  --text-aqua-${scale}: ${value};`);
  stats.cssVariablesCreated++;
});
output.push('');

output.push('  /* Text Colors - Cool Grey */');
Object.entries(tokens.colors.text['cool-grey']).forEach(([scale, value]) => {
  output.push(`  --text-cool-grey-${scale}: ${value};`);
  stats.cssVariablesCreated++;
});
output.push('');

output.push(`  /* Text Colors - Base */`);
output.push(`  --text-white: ${tokens.colors.text.white};`);
output.push(`  --text-black: ${tokens.colors.text.black};`);
stats.cssVariablesCreated += 2;
output.push('');

// Gradients
output.push('  /* Gradients - Mastery */');
Object.entries(tokens.gradients.mastery).forEach(([name, value]) => {
  output.push(`  --mastery-${name}: ${value};`);
  stats.cssVariablesCreated++;
});
output.push('');

// Typography
output.push('  /* Font Families */');
Object.entries(tokens.typography.fontFamily).forEach(([key, value]) => {
  output.push(`  --font-${key}: ${value};`);
  stats.cssVariablesCreated++;
});
output.push('');

output.push('  /* Font Weights */');
Object.entries(tokens.typography.fontWeight).forEach(([key, value]) => {
  output.push(`  --font-${key}: ${value};`);
  stats.cssVariablesCreated++;
});
output.push('');

// Spacing
output.push('  /* Spacing Scale */');
Object.entries(tokens.spacing).forEach(([key, value]) => {
  output.push(`  --spacing-${key}: ${value};`);
  stats.cssVariablesCreated++;
});
output.push('');

// Borders
output.push('  /* Border Radius */');
Object.entries(tokens.borders.radius).forEach(([key, value]) => {
  output.push(`  --${key}: ${value};`);
  stats.cssVariablesCreated++;
});
output.push('');

// Shadows
output.push('  /* Shadows */');
Object.entries(tokens.shadows).forEach(([key, value]) => {
  output.push(`  --${key}: ${value};`);
  stats.cssVariablesCreated++;
});
output.push('');

// Breakpoints
output.push('  /* Breakpoints */');
Object.entries(tokens.breakpoints).forEach(([key, value]) => {
  output.push(`  --breakpoint-${key}: ${value};`);
  stats.cssVariablesCreated++;
});

output.push('}');
output.push('');

// ========================================
// 2. TYPOGRAPHY CLASSES
// ========================================
output.push('/* ========================================');
output.push(' * TYPOGRAPHY');
output.push(' * ======================================== */');
output.push('');

// Extract .mv-type-- classes
const typeClasses = [
  'display1', 'display2', 'display3',
  'title1', 'title2', 'title3', 'title4', 'title5', 'title6',
  'body', 'body-large', 'body-small',
  'caption1', 'caption2',
  'overline'
];

typeClasses.forEach(typeClass => {
  const className = `mv-type--${typeClass}`;
  const rules = extractFullRule(className);

  if (rules.length > 0) {
    rules.forEach(rule => {
      output.push(rule);
      stats.typographyClassesExtracted++;
    });
    output.push('');
  }
});

// ========================================
// 3. LAYOUT & GRID UTILITIES
// ========================================
output.push('/* ========================================');
output.push(' * LAYOUT & GRID UTILITIES');
output.push(' * ======================================== */');
output.push('');

// Extract .mv-container and grid classes
const layoutClasses = [
  'mv-container',
  'mv-grid',
  'mv-grid-cols-1',
  'mv-grid-cols-2',
  'mv-grid-cols-3',
  'mv-grid-cols-4',
  'mv-grid-cols-6',
  'mv-grid-cols-12',
  'pb-Container'
];

layoutClasses.forEach(className => {
  const rules = extractFullRule(className);

  if (rules.length > 0) {
    rules.forEach(rule => {
      output.push(rule);
      stats.utilityClassesExtracted++;
    });
    output.push('');
  }

  // Also extract responsive variants
  const mediaRules = extractMediaRules(className);
  if (mediaRules.length > 0) {
    mediaRules.forEach(rule => {
      output.push(rule);
      stats.utilityClassesExtracted++;
    });
    output.push('');
  }
});

// ========================================
// 4. BUTTONS
// ========================================
output.push('/* ========================================');
output.push(' * BUTTONS');
output.push(' * ======================================== */');
output.push('');

// Extract button base class
const btnBaseRules = extractFullRule('mv-btn');
if (btnBaseRules.length > 0) {
  btnBaseRules.forEach(rule => {
    output.push(rule);
    stats.buttonClassesExtracted++;
  });
  output.push('');
}

// Extract button variants
const buttonVariants = [
  'mv-btn--mastery',
  'mv-btn--mastery--small',
  'mv-btn--mastery-white',
  'mv-btn--mastery-secondary',
  'mv-btn--primary',
  'mv-btn--secondary',
  'mv-btn--tertiary',
  'mv-btn--webinar',
  'mv-btn--ordermenu-primary'
];

buttonVariants.forEach(className => {
  const rules = extractFullRule(className);

  if (rules.length > 0) {
    rules.forEach(rule => {
      output.push(rule);
      stats.buttonClassesExtracted++;
    });
    output.push('');
  }

  // Extract hover states
  const hoverRules = extractFullRule(`${className}:hover`);
  if (hoverRules.length > 0) {
    hoverRules.forEach(rule => {
      output.push(rule);
      stats.buttonClassesExtracted++;
    });
    output.push('');
  }
});

// ========================================
// 5. COMPONENT SUPPORT CLASSES
// ========================================
output.push('/* ========================================');
output.push(' * COMPONENT SUPPORT CLASSES');
output.push(' * ======================================== */');
output.push('');

// Background utilities
output.push('/* Background Colors - Mastery */');
const masteryBgScales = ['50', '100', '200', '300', '400', '600', '650', '700', '800', '850', '900', '950'];
masteryBgScales.forEach(scale => {
  const rules = extractFullRule(`bg-mastery-${scale}`);
  if (rules.length > 0) {
    rules.forEach(rule => {
      output.push(rule);
      stats.componentClassesExtracted++;
    });
  }
});
output.push('');

// Background gradients
output.push('/* Background Gradients - Mastery */');
const gradientClasses = [
  'bg-mastery-gradient',
  'bg-mastery-gradient-aurora',
  'bg-mastery-gradient-fog',
  'bg-mastery-gradient-mist',
  'bg-mastery-gradient-soft-bordered',
  'bg-mastery-gradient-spring',
  'bg-mastery-gradient-surface-fog',
  'bg-mastery-gradient-teal-deep',
  'bg-mastery-gradient-vertical'
];

gradientClasses.forEach(className => {
  const rules = extractFullRule(className);
  if (rules.length > 0) {
    rules.forEach(rule => {
      output.push(rule);
      stats.componentClassesExtracted++;
    });
  }
});
output.push('');

// Text color utilities
output.push('/* Text Colors */');
const textColorClasses = [
  'text-mastery-50', 'text-mastery-100', 'text-mastery-200', 'text-mastery-300',
  'text-mastery-400', 'text-mastery-500', 'text-mastery-600', 'text-mastery-700',
  'text-mastery-800', 'text-mastery-900',
  'text-white', 'text-black'
];

textColorClasses.forEach(className => {
  const rules = extractFullRule(className);
  if (rules.length > 0) {
    rules.forEach(rule => {
      output.push(rule);
      stats.componentClassesExtracted++;
    });
  }
});
output.push('');

// Common spacing utilities
output.push('/* Spacing Utilities */');
const spacingClasses = [
  'px-4', 'px-6', 'px-8',
  'py-3', 'py-4', 'py-6', 'py-8', 'py-10', 'py-12',
  'pt-8', 'pt-10', 'pt-12', 'pt-16',
  'pb-8', 'pb-10', 'pb-12', 'pb-16',
  'mt-4', 'mt-6', 'mt-8',
  'mb-4', 'mb-6', 'mb-8',
  'gap-4', 'gap-6', 'gap-8'
];

spacingClasses.forEach(className => {
  const rules = extractFullRule(className);
  if (rules.length > 0) {
    rules.forEach(rule => {
      output.push(rule);
      stats.componentClassesExtracted++;
    });
  }
});
output.push('');

// Display & Flexbox utilities
output.push('/* Display & Flexbox */');
const displayClasses = [
  'flex', 'grid', 'block', 'inline-block', 'hidden',
  'items-center', 'items-start', 'items-end',
  'justify-center', 'justify-between', 'justify-around',
  'flex-col', 'flex-row',
  'grid-cols-1', 'grid-cols-2', 'grid-cols-3', 'grid-cols-4', 'grid-cols-6', 'grid-cols-12'
];

displayClasses.forEach(className => {
  const rules = extractFullRule(className);
  if (rules.length > 0) {
    rules.forEach(rule => {
      output.push(rule);
      stats.componentClassesExtracted++;
    });
  }
});
output.push('');

// Write the output file
const cssContent = output.join('\n');
fs.writeFileSync('public/css/mindvalley.css', cssContent);

console.log('');
console.log('✅ Mindvalley canonical stylesheet created successfully!');
console.log('');
console.log('📊 Statistics:');
console.log(`   CSS variables created: ${stats.cssVariablesCreated}`);
console.log(`   Typography classes extracted: ${stats.typographyClassesExtracted}`);
console.log(`   Button classes extracted: ${stats.buttonClassesExtracted}`);
console.log(`   Layout/Grid utilities extracted: ${stats.utilityClassesExtracted}`);
console.log(`   Component support classes extracted: ${stats.componentClassesExtracted}`);
console.log(`   Total classes: ${stats.typographyClassesExtracted + stats.buttonClassesExtracted + stats.utilityClassesExtracted + stats.componentClassesExtracted}`);
console.log('');
console.log('📄 File created: public/css/mindvalley.css');
console.log(`📏 File size: ${(cssContent.length / 1024).toFixed(2)} KB`);
