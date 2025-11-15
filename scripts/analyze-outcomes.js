/**
 * Mindvalley Outcomes Analysis Script
 *
 * This script analyzes outcomes in the Airtable and recommends:
 * - Deletions (low/no usage)
 * - Merges (semantic similarity)
 *
 * Usage: node analyze-outcomes.js
 */

const baseId = 'app4ulN4GnBRvcfAL';
const tableId = 'tblLA13fGO7KM1JHA';
const apiKey = process.env.AIRTABLE_API_KEY;

// Semantic groups for merge detection
const semanticGroups = [
  ['Stress', 'Anxiety', 'Worry', 'Tension'],
  ['Happiness', 'Joy', 'Bliss', 'Contentment'],
  ['Focus', 'Concentration', 'Attention'],
  ['Energy', 'Vitality', 'Vigor'],
  ['Calm', 'Peace', 'Tranquility', 'Serenity'],
  ['Confidence', 'Self-esteem', 'Self-worth'],
  ['Creativity', 'Innovation', 'Imagination'],
  ['Motivation', 'Drive', 'Ambition'],
  ['Relaxation', 'Rest', 'Recovery'],
  ['Clarity', 'Clear-thinking', 'Mental clarity'],
  ['Gratitude', 'Thankfulness', 'Appreciation'],
  ['Compassion', 'Empathy', 'Kindness'],
  ['Resilience', 'Strength', 'Fortitude'],
  ['Mindfulness', 'Presence', 'Awareness'],
  ['Sleep', 'Rest', 'Sleep quality'],
  ['Abundance', 'Prosperity', 'Wealth'],
  ['Healing', 'Recovery', 'Restoration'],
  ['Balance', 'Harmony', 'Equilibrium'],
  ['Forgiveness', 'Letting go', 'Release'],
  ['Intuition', 'Inner wisdom', 'Gut feeling']
];

async function fetchAllOutcomes() {
  const outcomes = [];
  let offset = null;

  do {
    const url = new URL(`https://api.airtable.com/v0/${baseId}/${tableId}`);
    url.searchParams.append('filterByFormula', 'NOT({UPDATE TYPE})');
    url.searchParams.append('fields[]', 'Outcome');
    url.searchParams.append('fields[]', 'Program Count');
    url.searchParams.append('fields[]', 'Meditation Count');
    url.searchParams.append('fields[]', 'Audio Count');
    url.searchParams.append('fields[]', 'Description');
    url.searchParams.append('fields[]', 'UPDATE TYPE');
    url.searchParams.append('pageSize', '100');

    if (offset) {
      url.searchParams.append('offset', offset);
    }

    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();
    outcomes.push(...data.records);
    offset = data.offset;

    console.log(`Fetched ${outcomes.length} outcomes so far...`);
  } while (offset);

  return outcomes;
}

function analyzeOutcome(outcome, allOutcomes) {
  const fields = outcome.fields;
  const programCount = fields['Program Count'] || 0;
  const meditationCount = fields['Meditation Count'] || 0;
  const audioCount = fields['Audio Count'] || 0;
  const totalUsage = programCount + meditationCount + audioCount;
  const outcomeName = fields['Outcome'] || '';
  const description = fields['Description'] || '';

  // Check deletion criteria
  if (totalUsage === 0) {
    return {
      type: 'Deleted',
      note: `No usage: Program Count=0, Meditation Count=0, Audio Count=0`
    };
  }

  if (totalUsage <= 2) {
    return {
      type: 'Deleted',
      note: `Low usage: Total usage=${totalUsage} (Program=${programCount}, Meditation=${meditationCount}, Audio=${audioCount})`
    };
  }

  // Check merge criteria - find semantically similar outcomes
  const similarOutcomes = findSimilarOutcomes(outcome, allOutcomes);
  if (similarOutcomes.length > 0) {
    // Find the outcome with highest usage
    const allRelated = [outcome, ...similarOutcomes];
    const sorted = allRelated.sort((a, b) => {
      const aUsage = (a.fields['Program Count'] || 0) + (a.fields['Meditation Count'] || 0) + (a.fields['Audio Count'] || 0);
      const bUsage = (b.fields['Program Count'] || 0) + (b.fields['Meditation Count'] || 0) + (b.fields['Audio Count'] || 0);
      return bUsage - aUsage;
    });

    const primary = sorted[0];
    const isPrimary = primary.id === outcome.id;

    if (!isPrimary) {
      const primaryUsage = (primary.fields['Program Count'] || 0) + (primary.fields['Meditation Count'] || 0) + (primary.fields['Audio Count'] || 0);
      return {
        type: 'Merged',
        note: `Similar to "${primary.fields['Outcome']}" (usage=${primaryUsage}). Current usage=${totalUsage}. Merge into primary outcome.`
      };
    }
  }

  return null; // Keep as-is
}

function findSimilarOutcomes(outcome, allOutcomes) {
  const outcomeName = (outcome.fields['Outcome'] || '').toLowerCase();
  const similar = [];

  // Check if this outcome is in any semantic group
  for (const group of semanticGroups) {
    const matchesGroup = group.some(term =>
      outcomeName.includes(term.toLowerCase()) ||
      term.toLowerCase().includes(outcomeName)
    );

    if (matchesGroup) {
      // Find other outcomes in the same group
      for (const other of allOutcomes) {
        if (other.id === outcome.id) continue;
        if (other.fields['UPDATE TYPE']) continue; // Skip already processed

        const otherName = (other.fields['Outcome'] || '').toLowerCase();
        const otherMatchesGroup = group.some(term =>
          otherName.includes(term.toLowerCase()) ||
          term.toLowerCase().includes(otherName)
        );

        if (otherMatchesGroup) {
          similar.push(other);
        }
      }
    }
  }

  // Also check for very similar descriptions
  const description = (outcome.fields['Description'] || '').toLowerCase();
  if (description) {
    for (const other of allOutcomes) {
      if (other.id === outcome.id) continue;
      if (other.fields['UPDATE TYPE']) continue;
      if (similar.includes(other)) continue; // Already found

      const otherDesc = (other.fields['Description'] || '').toLowerCase();
      if (otherDesc && description === otherDesc) {
        similar.push(other);
      }
    }
  }

  return similar;
}

async function updateOutcome(recordId, updateType, updateNote) {
  const url = `https://api.airtable.com/v0/${baseId}/${tableId}/${recordId}`;

  const response = await fetch(url, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      fields: {
        'UPDATE TYPE': updateType,
        'UPDATE NOTE': updateNote
      }
    })
  });

  return response.json();
}

async function main() {
  console.log('Fetching outcomes from Airtable...');
  const outcomes = await fetchAllOutcomes();
  console.log(`Total outcomes to analyze: ${outcomes.length}`);

  const deletions = [];
  const merges = [];
  const kept = [];

  console.log('\nAnalyzing outcomes...');

  for (const outcome of outcomes) {
    const analysis = analyzeOutcome(outcome, outcomes);

    if (!analysis) {
      kept.push(outcome);
      continue;
    }

    if (analysis.type === 'Deleted') {
      deletions.push({ outcome, ...analysis });
    } else if (analysis.type === 'Merged') {
      merges.push({ outcome, ...analysis });
    }
  }

  // Generate report
  console.log('\n' + '='.repeat(80));
  console.log('ANALYSIS REPORT');
  console.log('='.repeat(80));
  console.log(`\nTotal outcomes analyzed: ${outcomes.length}`);
  console.log(`Recommended for deletion: ${deletions.length}`);
  console.log(`Recommended for merging: ${merges.length}`);
  console.log(`To keep: ${kept.length}`);
  console.log(`Estimated final count: ${kept.length + Math.ceil(merges.length / 2)}`);

  console.log('\n' + '-'.repeat(80));
  console.log('DELETION RECOMMENDATIONS (First 20):');
  console.log('-'.repeat(80));

  deletions.slice(0, 20).forEach((item, idx) => {
    console.log(`\n${idx + 1}. ${item.outcome.fields['Outcome']}`);
    console.log(`   Reason: ${item.note}`);
  });

  console.log('\n' + '-'.repeat(80));
  console.log('MERGE RECOMMENDATIONS (First 20):');
  console.log('-'.repeat(80));

  merges.slice(0, 20).forEach((item, idx) => {
    console.log(`\n${idx + 1}. ${item.outcome.fields['Outcome']}`);
    console.log(`   ${item.note}`);
  });

  // Ask for confirmation before updating
  console.log('\n' + '='.repeat(80));
  console.log('Would you like to update Airtable with these recommendations?');
  console.log('Set environment variable UPDATE_AIRTABLE=true to proceed');
  console.log('='.repeat(80));

  if (process.env.UPDATE_AIRTABLE === 'true') {
    console.log('\nUpdating Airtable...');

    // Update in batches of 10
    const allUpdates = [...deletions, ...merges];
    for (let i = 0; i < allUpdates.length; i += 10) {
      const batch = allUpdates.slice(i, i + 10);
      await Promise.all(
        batch.map(item =>
          updateOutcome(item.outcome.id, item.type, item.note)
        )
      );
      console.log(`Updated ${Math.min(i + 10, allUpdates.length)} / ${allUpdates.length}`);
    }

    console.log('\nUpdate complete!');
  }
}

main().catch(console.error);
