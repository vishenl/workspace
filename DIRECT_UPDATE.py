#!/usr/bin/env python3
"""
Direct update script for Airtable outcomes.
Run this with: python3 DIRECT_UPDATE.py YOUR_TOKEN_HERE
"""

import sys
import requests
import time

BASE_ID = "app4ulN4GnBRvcfAL"
TABLE_ID = "tblLA13fGO7KM1JHA"
OUTCOME_FIELD = "fldCP33pFkB25Ynee"
STATUS_FIELD = "fldMe3I9aIFetUicW"
CLAUDE_EXPLANATION_FIELD = "fldamdoLPuG3q9niu"


def shorten_outcome_name(outcome_name: str) -> str:
    """Generate a shorter, clearer version."""
    prefixes_to_remove = [
        "Ability to ", "Ability for ", "The Ability to ",
        "Increased ", "Enhanced ", "Improved ", "Greater ",
        "Better ", "Deeper ", "Stronger ", "More ",
        "A Sense of ", "A Feeling of ", "A State of ",
        "The Feeling of ", "An Increased ", "An Enhanced ",
    ]

    shortened = outcome_name.strip()

    for prefix in prefixes_to_remove:
        if shortened.startswith(prefix):
            shortened = shortened[len(prefix):]
            break

    replacements = {
        "Surrender/Acceptance to a": "Surrender to",
        "Surrender/Acceptance to": "Surrender to",
        "Understanding of": "Understanding",
        "Connection with": "Connection to",
        "Awareness of": "Awareness",
        " and ": " & ",
    }

    for old, new in replacements.items():
        shortened = shortened.replace(old, new)

    if len(shortened) > 35 and " & " in shortened:
        parts = shortened.split(" & ")
        if len(parts[0].strip()) > 10:
            shortened = parts[0].strip()

    return shortened.strip()


def create_explanation(original: str, shortened: str) -> str:
    """Create explanation for the Claude Explanation field."""
    char_saved = len(original) - len(shortened)
    return f"""**Suggested Shorter Name:** {shortened}

**Analysis:**
- Original: "{original}" ({len(original)} characters)
- Suggested: "{shortened}" ({len(shortened)} characters)
- Saved: {char_saved} characters

**Reasoning:** This shorter version maintains the core meaning while being more concise and easier to scan. Redundant words have been removed or simplified, making the outcome name punchier and more memorable while preserving its transformational essence."""


def fetch_records(api_key: str):
    """Fetch records with 'Proposal to shorten' status."""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Only request the fields we need
    params = {
        "filterByFormula": "{Status} = 'Proposal to shorten'",
        "fields": ["fldCP33pFkB25Ynee", "fldMe3I9aIFetUicW"]  # Outcome and Status
    }

    records = []
    offset = None

    while True:
        if offset:
            params['offset'] = offset

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        records.extend(data.get('records', []))

        offset = data.get('offset')
        if not offset:
            break

        time.sleep(0.2)  # Rate limiting

    return records


def update_record(api_key: str, record_id: str, explanation: str):
    """Update a record's Claude Explanation field."""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}/{record_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "fields": {
            CLAUDE_EXPLANATION_FIELD: explanation
        }
    }

    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()
    time.sleep(0.2)  # Rate limiting


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 DIRECT_UPDATE.py YOUR_AIRTABLE_TOKEN")
        print("\nGet a token from: https://airtable.com/create/tokens")
        print("Make sure to give it access to the 'Mindvalley Brain' base")
        sys.exit(1)

    api_key = sys.argv[1]

    print("=" * 80)
    print("AIRTABLE OUTCOME SHORTENING - DIRECT UPDATE")
    print("=" * 80)
    print()

    try:
        print("Fetching records with 'Proposal to shorten' status...")
        records = fetch_records(api_key)
        print(f"✓ Found {len(records)} records to process\n")

        if not records:
            print("No records found. Exiting.")
            return

        print("Processing records...")
        print("-" * 80)

        updated_count = 0
        for i, record in enumerate(records, 1):
            record_id = record['id']
            fields = record.get('fields', {})
            outcome = fields.get(OUTCOME_FIELD, '')

            if not outcome:
                print(f"  {i}. Skipping - no outcome name")
                continue

            shortened = shorten_outcome_name(outcome)
            explanation = create_explanation(outcome, shortened)

            print(f"\n  {i}. {outcome}")
            print(f"      → {shortened} ({len(shortened)} chars)")

            try:
                update_record(api_key, record_id, explanation)
                updated_count += 1
                print(f"      ✓ Updated")
            except Exception as e:
                print(f"      ✗ Error: {e}")

        print()
        print("-" * 80)
        print(f"\n✓ Successfully updated {updated_count} of {len(records)} records")
        print()
        print("=" * 80)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
