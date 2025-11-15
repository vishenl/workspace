const fs = require('fs');

// Read the source CSS
const css = fs.readFileSync('academy-full.css', 'utf-8');

// Read the tokens
const tokens = JSON.parse(fs.readFileSync('design-system/mindvalley-tokens.json', 'utf-8'));

let output = [];

// Add header
output.push('/**');
output.push(' * Mindvalley Design System - Clean Build');
output.push(' * Extracted from academy-full.css');
output.push(' */');
output.push('');

// Add CSS variables from tokens
output.push(':root {');

// Mastery colors
Object.entries(tokens.colors.brand.mastery).forEach(([scale, value]) => {
  output.push(`  --mastery-${scale}: ${value};`);
});

// Text colors
Object.entries(tokens.colors.text.mastery).forEach(([scale, value]) => {
  output.push(`  --text-mastery-${scale}: ${value};`);
});

Object.entries(tokens.colors.text.aqua).forEach(([scale, value]) => {
  output.push(`  --text-aqua-${scale}: ${value};`);
});

Object.entries(tokens.colors.text['cool-grey']).forEach(([scale, value]) => {
  output.push(`  --text-cool-grey-${scale}: ${value};`);
});

// Gradients
Object.entries(tokens.gradients.mastery).forEach(([name, value]) => {
  output.push(`  --mastery-${name}: ${value};`);
});

// Spacing
Object.entries(tokens.spacing).forEach(([key, value]) => {
  output.push(`  --spacing-${key}: ${value};`);
});

output.push('}');
output.push('');

// Now extract actual CSS classes from the source
// We'll use regex to extract complete class definitions

function extractClass(className) {
  // Try to find the class definition
  const regex = new RegExp(`\\.${className.replace(/[.*+?^${}()|[\]\\-]/g, '\\$&')}\\s*\\{[^}]+\\}`, 'g');
  const matches = css.match(regex);
  return matches ? matches[0] : null;
}

// List of classes we need
const essentialClasses = [
  // Layout
  'pb-Container', 'mv-container', 'grid', 'flex', 'block', 'inline-block', 'hidden',

  // Grid
  'grid-cols-1', 'grid-cols-2', 'grid-cols-3', 'grid-cols-4', 'grid-cols-6', 'grid-cols-12',
  'col-span-3', 'col-span-6', 'col-span-12', 'col-start-6',

  // Flex
  'items-center', 'items-start', 'justify-between', 'justify-center', 'flex-col',

  // Spacing
  'gap-4', 'gap-6', 'gap-8',
  'px-4', 'px-6', 'py-3', 'py-5', 'py-6', 'py-8', 'py-10',
  'pt-8', 'pt-20', 'pb-16',
  'mt-4', 'mt-6', 'mt-12', 'mb-2', 'mb-3', 'mb-4',
  'p-4', 'p-6',

  // Colors
  'bg-mastery-950', 'bg-mastery-900', 'bg-mastery-850', 'bg-mastery-800',
  'bg-mastery-100', 'bg-mastery-200', 'bg-mastery-300', 'bg-mastery-400',
  'bg-cool-grey-650', 'bg-overview',
  'text-white', 'text-mastery-400', 'text-mastery-800',
  'text-cool-grey-700', 'text-cool-grey-500', 'text-grey-700',

  // Gradients
  'bg-mastery-gradient', 'bg-mastery-gradient-fog', 'bg-mastery-gradient-mist',
  'bg-mastery-gradient-surface-fog',

  // Typography
  'mv-type--title1', 'mv-type--title2', 'mv-type--title4', 'mv-type--title6',
  'mv-type--display1', 'mv-type--display2', 'mv-type--display3',
  'mv-type--body', 'mv-type--overline', 'mv-type--caption1',
  'mv-type--title7',

  // Borders
  'rounded', 'rounded-lg', 'rounded-t-lg',

  // Sizing
  'w-full', 'w-2/6', 'w-4/6', 'w-5/6', 'w-32',
  'min-h-fit', 'min-w-\\[300px\\]',

  // Buttons
  'base-button', 'mv-btn--mastery', 'mv-btn--mastery--small',
  'mv-btn--mastery-white', 'mv-btn--mastery-secondary', 'mv-btn--white',

  // Other
  'navbar-logo', 'navbar-popup', 'is-mastery',
  'mx-auto', 'mx-2',
  'text-center', 'text-left',
  'overflow-hidden', 'overflow-x-auto',
  'space-y-2',
  'border-t', 'border-mastery-800'
];

// Extract each class
output.push('/* Layout & Structure */');
essentialClasses.slice(0, 7).forEach(className => {
  const classDef = extractClass(className);
  if (classDef) output.push(classDef);
});
output.push('');

// Add more classes...
essentialClasses.forEach(className => {
  const classDef = extractClass(className);
  if (classDef) {
    output.push(classDef);
  }
});

// Add responsive variants
output.push('');
output.push('/* Responsive Variants */');
const responsivePrefixes = ['md_', 'lg_'];
const responsiveClasses = [
  'block', 'hidden', 'flex-row', 'flex-col',
  'grid-cols-2', 'grid-cols-3', 'grid-cols-4',
  'w-5/6', 'w-4/6', 'w-auto',
  'py-32', 'py-20', 'py-12', 'py-10',
  'px-10', 'gap-3',
  'text-center', 'text-left', 'text-right',
  'col-span-6', 'items-center'
];

responsivePrefixes.forEach(prefix => {
  responsiveClasses.forEach(className => {
    const fullClass = prefix + className;
    const classDef = extractClass(fullClass);
    if (classDef) output.push(classDef);
  });
});

// Write output
const finalCSS = output.join('\n');
fs.writeFileSync('public/css/mindvalley.css', finalCSS);

console.log('✅ Clean CSS generated');
console.log(`📏 File size: ${(finalCSS.length / 1024).toFixed(2)} KB`);
console.log(`📄 Lines: ${output.length}`);
