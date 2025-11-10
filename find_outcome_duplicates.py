#!/usr/bin/env python3
"""
Find duplicate outcomes in Airtable that could be merged.
This analyzes semantic similarity and suggests merges.
"""

import sys
import requests
import time
from collections import defaultdict
import re

BASE_ID = "app4ulN4GnBRvcfAL"
TABLE_ID = "tblLA13fGO7KM1JHA"
OUTCOME_FIELD = "fldCP33pFkB25Ynee"
STATUS_FIELD = "fldMe3I9aIFetUicW"
PROGRAM_COUNT_FIELD = "fldE9oQRoudmUiZ2I"


def normalize_outcome(outcome: str) -> str:
    """Normalize outcome for comparison."""
    normalized = outcome.lower()

    prefixes = [
        "ability to ", "ability for ", "the ability to ",
        "increased ", "enhanced ", "improved ", "greater ",
        "better ", "deeper ", "stronger ", "more ",
        "a sense of ", "a feeling of ", "a state of ",
        "the feeling of ", "an increased ", "an enhanced ",
        "the ", "a ", "an "
    ]

    for prefix in prefixes:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]
            break

    normalized = normalized.replace("and", "&")
    normalized = normalized.replace("/", " ")
    normalized = normalized.replace("-", " ")
    normalized = " ".join(normalized.split())

    return normalized


def get_core_concepts(outcome: str) -> set:
    """Extract core concepts from outcome."""
    stop_words = {
        "a", "an", "the", "to", "of", "for", "in", "on", "at", "by",
        "with", "from", "about", "into", "through", "during", "including"
    }

    normalized = normalize_outcome(outcome)
    words = set(normalized.split())
    core = words - stop_words

    return core


def calculate_similarity(outcome1: str, outcome2: str) -> float:
    """Calculate similarity score between two outcomes."""
    core1 = get_core_concepts(outcome1)
    core2 = get_core_concepts(outcome2)

    if not core1 or not core2:
        return 0.0

    intersection = len(core1 & core2)
    union = len(core1 | core2)

    return intersection / union if union > 0 else 0.0


def fetch_all_outcomes(api_key: str):
    """Fetch all outcomes from Airtable."""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    params = {
        "fields": [OUTCOME_FIELD, STATUS_FIELD, PROGRAM_COUNT_FIELD]
    }

    records = []
    offset = None

    print("Fetching outcomes from Airtable...")

    while True:
        if offset:
            params['offset'] = offset

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            batch = data.get('records', [])
            records.extend(batch)
            print(f"  Fetched {len(records)} records so far...")

            offset = data.get('offset')
            if not offset:
                break

            time.sleep(0.2)

        except Exception as e:
            print(f"Error fetching: {e}")
            break

    return records


def find_duplicates(records):
    """Find potential duplicate outcomes."""
    outcomes = []

    for record in records:
        fields = record.get('fields', {})
        outcome = fields.get(OUTCOME_FIELD, '').strip()
        status = fields.get(STATUS_FIELD, '')
        program_count = fields.get(PROGRAM_COUNT_FIELD, 0)

        if outcome:
            outcomes.append({
                'id': record['id'],
                'name': outcome,
                'status': status,
                'program_count': program_count,
                'normalized': normalize_outcome(outcome)
            })

    print(f"\nAnalyzing {len(outcomes)} outcomes for duplicates...")

    duplicates = []
    seen = set()

    for i, outcome1 in enumerate(outcomes):
        for j, outcome2 in enumerate(outcomes):
            if i >= j:
                continue

            pair_key = tuple(sorted([outcome1['id'], outcome2['id']]))
            if pair_key in seen:
                continue

            similarity = calculate_similarity(outcome1['name'], outcome2['name'])

            if similarity >= 0.6:
                seen.add(pair_key)
                duplicates.append({
                    'outcome1': outcome1,
                    'outcome2': outcome2,
                    'similarity': similarity
                })

    duplicates.sort(key=lambda x: x['similarity'], reverse=True)

    return duplicates


def generate_report(duplicates):
    """Generate a markdown report of duplicate outcomes."""
    report = f"""# Outcome Duplicate Analysis

## Summary
Found **{len(duplicates)}** potential duplicate pairs that could be merged.

## Recommendations

"""

    for i, dup in enumerate(duplicates, 1):
        o1 = dup['outcome1']
        o2 = dup['outcome2']
        similarity = dup['similarity']

        report += f"""### {i}. Similarity: {similarity:.0%}

**Outcome A:** {o1['name']}
- Status: {o1['status']}
- Programs using: {o1['program_count']}
- Record ID: `{o1['id']}`

**Outcome B:** {o2['name']}
- Status: {o2['status']}
- Programs using: {o2['program_count']}
- Record ID: `{o2['id']}`

**Recommendation:**
"""

        if o1['program_count'] > o2['program_count']:
            report += f"Keep **Outcome A** (used by {o1['program_count']} programs), merge B into it.\n"
        elif o2['program_count'] > o1['program_count']:
            report += f"Keep **Outcome B** (used by {o2['program_count']} programs), merge A into it.\n"
        elif len(o1['name']) < len(o2['name']):
            report += f"Keep **Outcome A** (shorter name), merge B into it.\n"
        else:
            report += f"Keep **Outcome B** (shorter name), merge A into it.\n"

        report += "\n---\n\n"

    return report


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 find_outcome_duplicates.py YOUR_AIRTABLE_TOKEN")
        sys.exit(1)

    api_key = sys.argv[1]

    print("=" * 80)
    print("AIRTABLE OUTCOME DUPLICATE FINDER")
    print("=" * 80)
    print()

    try:
        records = fetch_all_outcomes(api_key)
        print(f"✓ Fetched {len(records)} total records\n")

        duplicates = find_duplicates(records)
        print(f"✓ Found {len(duplicates)} potential duplicate pairs\n")

        if duplicates:
            report = generate_report(duplicates)

            report_file = "airtable_outcomes_duplicates.md"
            with open(report_file, 'w') as f:
                f.write(report)

            print(f"✓ Report saved to: {report_file}")
            print()
            print("Top 10 duplicates:")
            print("-" * 80)

            for i, dup in enumerate(duplicates[:10], 1):
                o1 = dup['outcome1']
                o2 = dup['outcome2']
                similarity = dup['similarity']
                print(f"\n{i}. {similarity:.0%} similar:")
                print(f"   A: {o1['name']}")
                print(f"   B: {o2['name']}")
        else:
            print("No duplicates found!")

        print()
        print("=" * 80)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
