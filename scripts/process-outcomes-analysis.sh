#!/bin/bash

# Mindvalley Outcomes Analysis - Data Fetcher
# This script fetches outcomes data from Airtable with minimal fields

BASE_ID="app4ulN4GnBRvcfAL"
TABLE_ID="tblLA13fGO7KM1JHA"

# Check for API key
if [ -z "$AIRTABLE_API_KEY" ]; then
    echo "Error: AIRTABLE_API_KEY environment variable not set"
    exit 1
fi

# Fetch outcomes with only the fields we need
echo "Fetching outcomes from Airtable..." >&2

# Build the URL with field filters
FIELDS="fields%5B%5D=Outcome&fields%5B%5D=Program+Count&fields%5B%5D=Meditation+Count&fields%5B%5D=Audio+Count&fields%5B%5D=Description&fields%5B%5D=UPDATE+TYPE&fields%5B%5D=UPDATE+NOTE"
FILTER="filterByFormula=NOT(%7BUPDATE%20TYPE%7D)"  # NOT({UPDATE TYPE})

curl -s "https://api.airtable.com/v0/${BASE_ID}/${TABLE_ID}?${FIELDS}&${FILTER}&pageSize=100" \
    -H "Authorization: Bearer ${AIRTABLE_API_KEY}" | \
    python3 scripts/analyze-outcomes.py
