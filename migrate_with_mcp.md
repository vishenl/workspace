# Outcomes Migration Plan

Since the Airtable API key is not available in the Python environment, I'll use the MCP Airtable tools to migrate the data in batches.

## Strategy:

1. Fetch outcomes in small batches using filters
2. Create records in Outcomes2 using mcp__airtable__create_record
3. Track progress and handle the ~300 outcomes systematically

## Challenge:

The original Outcomes table has ~300 records with lots of linked data (images, etc.), making bulk fetches fail due to token limits.

## Solution Options:

### Option A: Manual Filter-Based Migration
- Use filters to get subsets (by Status, by Program Count ranges)
- Process each subset separately
- Time-consuming but guaranteed to work

### Option B: Ask User for API Key
- User provides their Airtable Personal Access Token
- Run the Python script which handles everything automatically
- Fastest and most reliable

### Option C: Use Airtable UI
- User could duplicate the table in Airtable UI
- Then I add the new fields manually
- I provide a CSV with the Claude Update recommendations
- User imports the CSV to update the fields

## Recommendation:

**Option B** is best - ask the user for their Airtable API key to run the automated migration script.
