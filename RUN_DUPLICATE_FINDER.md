# How to Find Top 10 Outcome Duplicates

## Quick Start

1. **Set your Airtable API Key:**

```bash
export AIRTABLE_PERSONAL_ACCESS_TOKEN='your_token_here'
```

Or if you're using the legacy API key:

```bash
export AIRTABLE_API_KEY='your_token_here'
```

2. **Run the script:**

```bash
python3 find_top_10_duplicates.py
```

## What It Does

This script will:
- Fetch all outcomes from your Mindvalley Brain Airtable
- Analyze them for duplicates using two strategies:
  1. **Core concept matching** (e.g., "Building Confidence" vs "Developing Confidence")
  2. **High similarity matching** (comparing names and definitions)
- Show you the **top 10 duplicates** to delete
- Prioritize outcomes with 0 programs (safest to delete)
- Give you copy-paste ready record IDs for deletion

## Output

You'll see:
- Each duplicate outcome with its record ID
- Why it's a duplicate
- Which outcome to keep instead
- Confidence score (1-5, where 5 is most confident)
- All record IDs in a comma-separated list for easy deletion

## Example Output

```
TOP 10 OUTCOMES TO DELETE (DUPLICATES)
================================================================================

1. DELETE: rec26tTnU8lixNGKZ
   Outcome: "Improving Strength" (0 programs)
   Reason:  Same core concept: 'strength'
   Keep Instead: "Building Strength" (3 programs)
   Confidence: 5/5

...
```

## Safety Tips

1. Review each duplicate in Airtable before deleting
2. Delete outcomes with **0 programs** first (safest)
3. For outcomes with programs, reassign them to the "keep" outcome first
4. Keep a backup of your Airtable base before mass deletion

## Where to Get Your API Token

1. Go to https://airtable.com/create/tokens
2. Create a new token with `data.records:read` permission
3. Add access to the "Mindvalley Brain" base
4. Copy the token and use it in the export command above
