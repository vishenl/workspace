/**
 * Script to analyze Mindvalley Outcomes for consolidation opportunities
 * This script retrieves outcomes and identifies duplicates/semantic overlaps
 */

const Airtable = require('airtable');

// Configuration
const BASE_ID = 'app4ulN4GnBRvcfAL';
const TABLE_ID = 'tblLA13fGO7KM1JHA';

// Initialize Airtable
const base = new Airtable({ apiKey: process.env.AIRTABLE_API_KEY }).base(BASE_ID);

async function getAllOutcomes() {
  const outcomes = [];

  await base(TABLE_ID)
    .select({
      fields: ['Outcome', 'Definition', 'Status', 'Program Count', 'Character length'],
      view: 'Grid view' // Using default view
    })
    .eachPage((records, fetchNextPage) => {
      records.forEach(record => {
        outcomes.push({
          id: record.id,
          name: record.get('Outcome'),
          definition: record.get('Definition'),
          status: record.get('Status'),
          programCount: record.get('Program Count') || 0,
          characterLength: record.get('Character length') || 0
        });
      });
      fetchNextPage();
    });

  return outcomes;
}

async function analyzeOutcomes() {
  console.log('Retrieving all outcomes from Airtable...');
  const outcomes = await getAllOutcomes();

  console.log(`\nTotal outcomes retrieved: ${outcomes.length}`);
  console.log('\n=== OUTCOME ANALYSIS ===\n');

  // Sort by name for easier reading
  outcomes.sort((a, b) => (a.name || '').localeCompare(b.name || ''));

  // Output as JSON for further processing
  console.log(JSON.stringify({
    total: outcomes.length,
    outcomes: outcomes.map(o => ({
      name: o.name,
      definition: o.definition,
      status: o.status,
      programCount: o.programCount
    }))
  }, null, 2));
}

analyzeOutcomes().catch(console.error);
