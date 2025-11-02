#!/usr/bin/env python3
"""
Add merge links to Outcomes2 table for records with Claude Update = 'Merge'
"""

import os
import requests
import time

BASE_ID = 'app4ulN4GnBRvcfAL'
TABLE_ID = 'tblQf8UE2NoQtu5U4'  # Outcomes2 table

api_key = os.environ.get('AIRTABLE_API_KEY')

def fetch_all_outcomes2():
    """Fetch all records from Outcomes2 table"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    params = {
        "pageSize": 100
    }

    all_records = []
    offset = None

    print("Fetching all records from Outcomes2...")

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
        all_records.extend(records)

        offset = data.get('offset')
        if not offset:
            break

        print(f"Fetched {len(all_records)} records so far...")
        time.sleep(0.2)

    print(f"\nTotal records: {len(all_records)}")
    return all_records

def find_merge_target_id(target_name, all_records):
    """Find the record ID for a given outcome name"""
    for record in all_records:
        if record['fields'].get('Outcome') == target_name:
            return record['id']
    return None

def update_merge_links(records_to_update):
    """Update merge links in batches of 10"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    for i in range(0, len(records_to_update), 10):
        batch = records_to_update[i:i+10]
        print(f"Updating batch {i//10 + 1} ({len(batch)} records)...")

        payload = {
            "records": batch
        }

        response = requests.patch(url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"Error updating records: {response.status_code}")
            print(response.text)
        else:
            print(f"  ✓ Updated {len(batch)} records")

        time.sleep(0.2)

def main():
    print("=" * 60)
    print("ADDING MERGE LINKS TO OUTCOMES2")
    print("=" * 60)

    # Fetch all records
    all_records = fetch_all_outcomes2()

    # Create a map of outcome names to record IDs
    name_to_id = {
        record['fields'].get('Outcome'): record['id']
        for record in all_records
        if record['fields'].get('Outcome')
    }

    # Define merge mappings from analysis
    merge_mappings = {
        'Better Sleep': 'Deeper Sleep',
        'Quality Sleep': 'Deeper Sleep',
        'Improved Concentration': 'Enhanced Focus',
        'Better Focus': 'Enhanced Focus',
        'Building Confidence': 'Self-Confidence',
        'Self-Esteem': 'Self-Confidence',
        'Stress Relief': 'Stress Management',
        'Stress Reduction': 'Stress Management',
        'Higher Energy Levels': 'Increased Energy',
        'Vitality': 'Increased Energy',
        'Improved Relationships': 'Better Relationships',
        'Stronger Connections': 'Better Relationships',
        'Creative Thinking': 'Enhanced Creativity',
        'Creative Expression': 'Enhanced Creativity',
        'Better Performance': 'Increased Productivity',
        'Peak Performance': 'Increased Productivity',
        'More Joy': 'Greater Happiness',
        'Increased Happiness': 'Greater Happiness',
    }

    # Find records that need merge links
    records_to_update = []
    merge_count = 0

    print("\nIdentifying merge candidates...")

    for record in all_records:
        outcome_name = record['fields'].get('Outcome')
        claude_update = record['fields'].get('Claude Update')

        if claude_update == 'Merge' and outcome_name in merge_mappings:
            target_name = merge_mappings[outcome_name]
            target_id = name_to_id.get(target_name)

            if target_id:
                records_to_update.append({
                    "id": record['id'],
                    "fields": {
                        "Merge Into": [target_id]
                    }
                })
                merge_count += 1
                print(f"  {outcome_name} → {target_name}")

    print(f"\nFound {merge_count} merge links to create")

    if records_to_update:
        print("\nUpdating records...")
        update_merge_links(records_to_update)

    print("\n" + "=" * 60)
    print(f"✓ Successfully added {merge_count} merge links!")
    print("=" * 60)

if __name__ == '__main__':
    main()
