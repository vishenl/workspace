#!/usr/bin/env python3
"""
Script to analyze Airtable Outcomes table and find duplicates.
"""

import json
from collections import defaultdict

# Store outcomes as we fetch them
outcomes_data = []

# Manually collected outcomes from API calls
outcomes_data.append({
    "id": "rec02WtS4NCFbg2Em",
    "Outcome": "Improving Endurance",
    "Definition": "I cultivate the ability to sustain prolonged physical exertion, and increase my stamina to achieve new levels of endurance."
})

outcomes_data.append({
    "id": "rec07h3OkHA7APWQ1",
    "Outcome": "Surrender/Acceptance to a Higher Power",
    "Definition": "I surrender and accept the guidance and wisdom of a higher power, finding solace and trust in the unfolding of life's journey."
})

outcomes_data.append({
    "id": "rec0jXiD2Im3YYiDW",
    "Outcome": "Improving Athletic Performance",
    "Definition": "I optimise my athletic abilities in my chosen sport or activity through targeted training and conditioning, "
})

def find_duplicates(outcomes):
    """Find duplicate or very similar outcomes."""
    duplicates = []

    # Normalize outcomes for comparison
    normalized = {}
    for outcome in outcomes:
        # Create normalized version (lowercase, remove special chars)
        name_norm = outcome['Outcome'].lower().strip()
        normalized[outcome['id']] = {
            'original': outcome['Outcome'],
            'normalized': name_norm,
            'definition': outcome.get('Definition', ''),
            'id': outcome['id']
        }

    # Compare all pairs
    checked = set()
    for id1, data1 in normalized.items():
        for id2, data2 in normalized.items():
            if id1 >= id2:  # Skip self and already checked pairs
                continue

            pair_key = tuple(sorted([id1, id2]))
            if pair_key in checked:
                continue
            checked.add(pair_key)

            # Check for similarity
            name1 = data1['normalized']
            name2 = data2['normalized']

            # Look for various patterns of duplication
            similar = False
            reason = ""

            # Exact match after normalization
            if name1 == name2:
                similar = True
                reason = f"Exact match (normalized)"

            # One is substring of other
            elif name1 in name2 or name2 in name1:
                similar = True
                reason = f"One name contains the other"

            # Word order variation (e.g., "Building Confidence" vs "Confidence Building")
            words1 = set(name1.split())
            words2 = set(name2.split())
            if len(words1) == len(words2) and words1 == words2:
                similar = True
                reason = f"Same words, different order"

            if similar:
                duplicates.append({
                    'id1': id1,
                    'name1': data1['original'],
                    'id2': id2,
                    'name2': data2['original'],
                    'reason': reason
                })

    return duplicates

# Print current data
print("Current outcomes collected:")
for outcome in outcomes_data:
    print(f"- {outcome['id']}: {outcome['Outcome']}")

print("\n\nNeed to collect more outcomes to find patterns...")
print("Next batch targets:")
print("- Records with 'stress' in name")
print("- Records with 'confidence' in name")
print("- Records with 'improve/improving' in name")
print("- Records with 'reduce/reducing' in name")
print("- Records with 'build/building' in name")
