#!/usr/bin/env python3
"""
Migrate outcomes from original Outcomes table to Outcomes2 table
with Claude's consolidation recommendations
"""

import os
import json
import requests
import time

BASE_ID = 'app4ulN4GnBRvcfAL'
SOURCE_TABLE_ID = 'tblLA13fGO7KM1JHA'  # Original Outcomes table
TARGET_TABLE_ID = 'tblQf8UE2NoQtu5U4'  # New Outcomes2 table

# Get API key from environment (set by MCP)
api_key = os.environ.get('AIRTABLE_API_KEY')

def fetch_all_outcomes():
    """Fetch all outcomes from source table with minimal fields"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{SOURCE_TABLE_ID}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    params = {
        "fields[]": ["Outcome", "Definition", "Status", "Program Count"],
        "pageSize": 100
    }

    all_outcomes = []
    offset = None

    print("Fetching outcomes from source table...")

    while True:
        if offset:
            params['offset'] = offset

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            break

        data = response.json()
        records = data.get('records', [])

        for record in records:
            fields = record.get('fields', {})
            all_outcomes.append({
                'source_id': record['id'],
                'name': fields.get('Outcome', ''),
                'definition': fields.get('Definition', ''),
                'status': fields.get('Status', ''),
                'program_count': fields.get('Program Count', 0)
            })

        offset = data.get('offset')
        if not offset:
            break

        print(f"Fetched {len(all_outcomes)} outcomes so far...")
        time.sleep(0.2)  # Rate limiting

    print(f"\nTotal outcomes fetched: {len(all_outcomes)}")
    return all_outcomes

def determine_claude_update(outcome):
    """Determine the Claude Update status based on analysis"""
    name = outcome['name'].lower()
    status = outcome['status']
    program_count = outcome['program_count']

    # Rejected outcomes -> Delete
    if status == 'Rejected':
        return 'Delete', None

    # Zero program count -> Delete
    if program_count == 0:
        return 'Delete', None

    # Semantic duplicates -> Merge (we'll need to identify these)
    # For now, return Review for potential duplicates

    # Check for common duplicate patterns
    merge_candidates = {
        'better sleep': 'Deeper Sleep',
        'quality sleep': 'Deeper Sleep',
        'improved concentration': 'Enhanced Focus',
        'better focus': 'Enhanced Focus',
        'building confidence': 'Self-Confidence',
        'self-esteem': 'Self-Confidence',
        'stress relief': 'Stress Management',
        'stress reduction': 'Stress Management',
        'higher energy levels': 'Increased Energy',
        'vitality': 'Increased Energy',
        'improved relationships': 'Better Relationships',
        'stronger connections': 'Better Relationships',
        'creative thinking': 'Enhanced Creativity',
        'creative expression': 'Enhanced Creativity',
        'better performance': 'Increased Productivity',
        'peak performance': 'Increased Productivity',
        'more joy': 'Greater Happiness',
        'increased happiness': 'Greater Happiness',
    }

    for pattern, target in merge_candidates.items():
        if pattern in name and outcome['name'] != target:
            return 'Merge', target

    # Low program count (1-2) -> Review
    if program_count <= 2:
        return 'Review', None

    # Everything else -> Keep
    return 'Keep', None

def create_records_batch(outcomes_batch):
    """Create records in Outcomes2 table in batches of 10"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TARGET_TABLE_ID}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    records = []
    for outcome in outcomes_batch:
        claude_update, merge_target = determine_claude_update(outcome)

        record = {
            "fields": {
                "Outcome": outcome['name'],
                "Definition": outcome['definition'] or '',
                "Status": outcome['status'] or '',
                "Program Count": outcome['program_count'],
                "Claude Update": claude_update
            }
        }
        records.append(record)

    payload = {"records": records}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"Error creating records: {response.status_code}")
        print(response.text)
        return []

    return response.json().get('records', [])

def main():
    print("=" * 60)
    print("OUTCOMES MIGRATION TO OUTCOMES2 TABLE")
    print("=" * 60)

    # Fetch all outcomes
    outcomes = fetch_all_outcomes()

    if not outcomes:
        print("No outcomes found!")
        return

    # Create records in batches of 10 (Airtable limit)
    print("\nCreating records in Outcomes2 table...")
    created_records = []

    for i in range(0, len(outcomes), 10):
        batch = outcomes[i:i+10]
        print(f"Processing batch {i//10 + 1} ({len(batch)} records)...")

        batch_records = create_records_batch(batch)
        created_records.extend(batch_records)

        time.sleep(0.2)  # Rate limiting

    print(f"\n✓ Successfully created {len(created_records)} records in Outcomes2 table")

    # Generate summary
    statuses = {}
    for outcome in outcomes:
        claude_update, _ = determine_claude_update(outcome)
        statuses[claude_update] = statuses.get(claude_update, 0) + 1

    print("\nClaude Update Distribution:")
    for status, count in sorted(statuses.items()):
        print(f"  {status}: {count}")

    print("\n" + "=" * 60)
    print("Migration complete!")
    print("Next step: Add merge links for 'Merge' status outcomes")
    print("=" * 60)

if __name__ == '__main__':
    main()
