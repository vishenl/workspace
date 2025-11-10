#!/usr/bin/env python3
"""
Fetch outcomes with 'Proposal to shorten' status and update Claude Explanation field
with shortening suggestions.
"""

import os
import requests
import json
from typing import List, Dict, Any

# Airtable configuration
BASE_ID = "app4ulN4GnBRvcfAL"
TABLE_ID = "tblLA13fGO7KM1JHA"

# Field IDs
OUTCOME_FIELD = "fldCP33pFkB25Ynee"
STATUS_FIELD = "fldMe3I9aIFetUicW"
CLAUDE_EXPLANATION_FIELD = "fldamdoLPuG3q9niu"
CHAR_LENGTH_FIELD = "fldRxLVPcccr4USS3"
NEW_PROPOSED_NAME_FIELD = "fldXrxQhs1fam7BDy"


def shorten_outcome_name(outcome_name: str) -> str:
    """Generate a shorter, clearer version keeping the core meaning."""

    prefixes_to_remove = [
        "Ability to ",
        "Ability for ",
        "The Ability to ",
        "Increased ",
        "Enhanced ",
        "Improved ",
        "Greater ",
        "Better ",
        "Deeper ",
        "Stronger ",
        "More ",
        "A Sense of ",
        "A Feeling of ",
        "A State of ",
        "The Feeling of ",
        "An Increased ",
        "An Enhanced ",
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

    # If still too long, try more aggressive shortening
    if len(shortened) > 35:
        # Remove trailing descriptors
        if " and " in shortened:
            parts = shortened.split(" & ")
            # Take the first part if it's substantial
            if len(parts[0].strip()) > 10:
                shortened = parts[0].strip()

    return shortened.strip()


def create_explanation(original: str, shortened: str) -> str:
    """Create explanation for the Claude Explanation field."""
    return f"""**Suggested Shorter Name:** {shortened}

**Analysis:**
- Original: "{original}" ({len(original)} characters)
- Suggested: "{shortened}" ({len(shortened)} characters)
- Saved: {len(original) - len(shortened)} characters

**Reasoning:** This shorter version maintains the core meaning while being more concise, easier to scan, and fits better in UI elements. The essence of the outcome is preserved while removing redundant qualifiers."""


def get_api_key() -> str:
    """Get Airtable API key from environment."""
    api_key = os.getenv('AIRTABLE_PERSONAL_ACCESS_TOKEN') or os.getenv('AIRTABLE_API_KEY')
    if not api_key:
        raise ValueError("AIRTABLE_PERSONAL_ACCESS_TOKEN or AIRTABLE_API_KEY environment variable not set")
    return api_key


def fetch_records_to_shorten(api_key: str) -> List[Dict[str, Any]]:
    """Fetch records with 'Proposal to shorten' status."""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    params = {
        "filterByFormula": "{Status} = 'Proposal to shorten'",
        "fields[]": [OUTCOME_FIELD, STATUS_FIELD, CLAUDE_EXPLANATION_FIELD, CHAR_LENGTH_FIELD, NEW_PROPOSED_NAME_FIELD]
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

    return records


def update_record(api_key: str, record_id: str, explanation: str) -> None:
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


def main():
    """Main execution function."""
    print("=" * 80)
    print("AIRTABLE OUTCOME SHORTENING TOOL")
    print("=" * 80)
    print()

    try:
        api_key = get_api_key()
        print("✓ API key found")
        print()

        print("Fetching records with 'Proposal to shorten' status...")
        records = fetch_records_to_shorten(api_key)
        print(f"✓ Found {len(records)} records to process")
        print()

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
