#!/usr/bin/env python3
"""
Analyze all 317 outcomes for semantic duplicates and provide recommendations
"""

import os
import requests
import time
import json
from difflib import SequenceMatcher

BASE_ID = 'app4ulN4GnBRvcfAL'
TABLE_ID = 'tblLA13fGO7KM1JHA'  # Original Outcomes table

api_key = os.environ.get('AIRTABLE_API_KEY')

def fetch_all_outcomes():
    """Fetch all outcomes from the table"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    params = {
        "fields[]": ["Outcome", "Definition", "Program Count"],
        "pageSize": 100
    }

    all_records = []
    offset = None

    print("Fetching all outcomes...")

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
            all_records.append({
                'id': record['id'],
                'name': fields.get('Outcome', ''),
                'definition': fields.get('Definition', ''),
                'program_count': fields.get('Program Count', 0)
            })

        offset = data.get('offset')
        if not offset:
            break

        print(f"Fetched {len(all_records)} outcomes so far...")
        time.sleep(0.2)

    print(f"\nTotal outcomes fetched: {len(all_records)}")
    return all_records

def normalize_text(text):
    """Normalize text for comparison"""
    if not text:
        return ""
    return text.lower().strip()

def calculate_similarity(text1, text2):
    """Calculate similarity ratio between two texts"""
    return SequenceMatcher(None, normalize_text(text1), normalize_text(text2)).ratio()

def are_semantic_duplicates(outcome1, outcome2):
    """
    Determine if two outcomes are semantic duplicates
    Returns: (is_duplicate, confidence_level, explanation)
    """
    name1 = normalize_text(outcome1['name'])
    name2 = normalize_text(outcome2['name'])
    def1 = normalize_text(outcome1['definition'])
    def2 = normalize_text(outcome2['definition'])

    # Skip if names are identical (same outcome)
    if name1 == name2:
        return False, 0, ""

    # Calculate similarities
    name_similarity = calculate_similarity(name1, name2)
    def_similarity = calculate_similarity(def1, def2)

    # Check for one name being contained in another (e.g., "Forgiveness" in "Learning Forgiveness")
    name_contains = name1 in name2 or name2 in name1

    # Strict semantic duplicates (Confidence 5)
    if (name_similarity > 0.85 and def_similarity > 0.8) or \
       (name_contains and def_similarity > 0.75):
        return True, 5, f"Strict semantic duplicate - names are {name_similarity:.0%} similar and definitions are {def_similarity:.0%} similar"

    # Very likely duplicates (Confidence 4)
    if (name_similarity > 0.75 and def_similarity > 0.7) or \
       (name_contains and def_similarity > 0.6):
        return True, 4, f"Very likely duplicate - names are {name_similarity:.0%} similar and definitions are {def_similarity:.0%} similar"

    # Probable overlap (Confidence 3)
    if (name_similarity > 0.65 and def_similarity > 0.6):
        return True, 3, f"Probable overlap - names are {name_similarity:.0%} similar and definitions are {def_similarity:.0%} similar"

    # Possible consolidation (Confidence 2)
    if (name_similarity > 0.55 and def_similarity > 0.5):
        return True, 2, f"Possible consolidation candidate - names are {name_similarity:.0%} similar and definitions are {def_similarity:.0%} similar"

    return False, 0, ""

def find_duplicates(outcomes):
    """Find all duplicate pairs"""
    duplicates = []

    print("\nAnalyzing for duplicates...")

    for i in range(len(outcomes)):
        for j in range(i + 1, len(outcomes)):
            outcome1 = outcomes[i]
            outcome2 = outcomes[j]

            is_dup, confidence, explanation = are_semantic_duplicates(outcome1, outcome2)

            if is_dup:
                # Determine which to keep (prefer higher program count)
                if outcome1['program_count'] >= outcome2['program_count']:
                    keep = outcome1
                    merge = outcome2
                else:
                    keep = outcome2
                    merge = outcome1

                duplicates.append({
                    'merge_outcome': merge,
                    'keep_outcome': keep,
                    'confidence': confidence,
                    'similarity_explanation': explanation
                })

    return duplicates

def generate_recommendations(outcomes, duplicates):
    """Generate recommendations for each outcome"""
    recommendations = {}

    # Initialize all as "Keep"
    for outcome in outcomes:
        recommendations[outcome['id']] = {
            'action': 'Keep',
            'explanation': f"This outcome appears unique. Program count: {outcome['program_count']}",
            'confidence': None
        }

    # Update with merge recommendations
    for dup in duplicates:
        merge_id = dup['merge_outcome']['id']
        keep_name = dup['keep_outcome']['name']
        confidence = dup['confidence']
        similarity = dup['similarity_explanation']

        merge_pc = dup['merge_outcome']['program_count']
        keep_pc = dup['keep_outcome']['program_count']

        explanation = f"This outcome is a duplicate of '{keep_name}'. {similarity}. "
        explanation += f"'{dup['merge_outcome']['name']}' has {merge_pc} programs, "
        explanation += f"while '{keep_name}' has {keep_pc} programs. "
        explanation += f"Recommend merging into '{keep_name}'."

        if merge_pc == 0:
            explanation += f" Zero program count makes this an easy deletion candidate."

        recommendations[merge_id] = {
            'action': 'Merge',
            'explanation': explanation,
            'confidence': str(confidence)
        }

    return recommendations

def update_records_batch(updates_batch):
    """Update records in batches of 10"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {"records": updates_batch}

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"Error updating records: {response.status_code}")
        print(response.text)
        return False

    return True

def apply_recommendations(recommendations):
    """Apply recommendations to Airtable"""
    print("\nApplying recommendations to Airtable...")

    updates = []
    for record_id, rec in recommendations.items():
        update = {
            "id": record_id,
            "fields": {
                "Claude Action": rec['action'],
                "Claude Explanation": rec['explanation']
            }
        }

        if rec['confidence']:
            update['fields']['Claude Confidence'] = rec['confidence']

        updates.append(update)

    # Process in batches of 10
    for i in range(0, len(updates), 10):
        batch = updates[i:i+10]
        print(f"Updating batch {i//10 + 1} ({len(batch)} records)...")

        if not update_records_batch(batch):
            print(f"Failed to update batch {i//10 + 1}")
            return False

        time.sleep(0.2)

    return True

def main():
    print("=" * 70)
    print("SEMANTIC DUPLICATE ANALYSIS - OUTCOMES TABLE")
    print("=" * 70)

    # Fetch all outcomes
    outcomes = fetch_all_outcomes()

    if not outcomes:
        print("No outcomes found!")
        return

    # Find duplicates
    duplicates = find_duplicates(outcomes)

    print(f"\nFound {len(duplicates)} duplicate pairs")

    # Show confidence distribution
    confidence_dist = {}
    for dup in duplicates:
        conf = dup['confidence']
        confidence_dist[conf] = confidence_dist.get(conf, 0) + 1

    print("\nDuplicate Confidence Distribution:")
    for conf in sorted(confidence_dist.keys(), reverse=True):
        count = confidence_dist[conf]
        print(f"  Confidence {conf}: {count} duplicates")

    # Show high confidence duplicates
    high_conf = [d for d in duplicates if d['confidence'] == 5]
    if high_conf:
        print(f"\n{'='*70}")
        print(f"HIGH CONFIDENCE DUPLICATES (Confidence = 5) - {len(high_conf)} found:")
        print(f"{'='*70}")
        for dup in high_conf:
            print(f"\n  MERGE: '{dup['merge_outcome']['name']}' (Programs: {dup['merge_outcome']['program_count']})")
            print(f"  INTO:  '{dup['keep_outcome']['name']}' (Programs: {dup['keep_outcome']['program_count']})")
            print(f"  Reason: {dup['similarity_explanation']}")

    # Generate recommendations
    recommendations = generate_recommendations(outcomes, duplicates)

    # Apply to Airtable
    if apply_recommendations(recommendations):
        print(f"\n{'='*70}")
        print("✓ Successfully updated all {len(outcomes)} outcomes!")
        print(f"{'='*70}")

        # Summary
        action_counts = {}
        for rec in recommendations.values():
            action = rec['action']
            action_counts[action] = action_counts.get(action, 0) + 1

        print("\nAction Summary:")
        for action, count in sorted(action_counts.items()):
            print(f"  {action}: {count}")

        print("\nNext Steps:")
        print("1. Filter Outcomes table by 'Claude Confidence = 5' to see strict duplicates")
        print("2. Review and immediately delete confidence=5 outcomes")
        print("3. Review confidence 4 outcomes for near-duplicates")
        print("4. Review confidence 3 outcomes for possible consolidation")

if __name__ == '__main__':
    main()
