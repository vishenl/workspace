#!/usr/bin/env python3
"""
Enhanced semantic duplicate analysis using Definition field and program count
"""

import os
import requests
import time
from difflib import SequenceMatcher
import re

BASE_ID = 'app4ulN4GnBRvcfAL'
TABLE_ID = 'tblLA13fGO7KM1JHA'

api_key = os.environ.get('AIRTABLE_API_KEY')

def fetch_all_outcomes():
    """Fetch all outcomes including the Definition field"""
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

    print("Fetching all outcomes with definitions...")

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
                'program_count': fields.get('Program Count', 0) or 0
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

def extract_root_words(text):
    """Extract meaningful words, removing common modifiers"""
    if not text:
        return set()

    # Remove common modifiers
    modifiers = ['better', 'improved', 'enhanced', 'greater', 'increased', 'deeper',
                 'higher', 'more', 'improved', 'learning', 'developing', 'building',
                 'cultivating', 'achieving', 'mastering', 'understanding', 'gaining']

    words = re.findall(r'\w+', text.lower())
    root_words = [w for w in words if w not in modifiers and len(w) > 3]
    return set(root_words)

def calculate_similarity(text1, text2):
    """Calculate similarity ratio between two texts"""
    return SequenceMatcher(None, normalize_text(text1), normalize_text(text2)).ratio()

def analyze_duplicate(outcome1, outcome2):
    """
    Enhanced duplicate detection using definitions
    Returns: (is_duplicate, confidence_level, explanation)
    """
    name1 = normalize_text(outcome1['name'])
    name2 = normalize_text(outcome2['name'])
    def1 = normalize_text(outcome1['definition'])
    def2 = normalize_text(outcome2['definition'])

    # Skip if same outcome
    if name1 == name2 or outcome1['id'] == outcome2['id']:
        return False, 0, "", None

    # Extract root words from names and definitions
    name1_roots = extract_root_words(outcome1['name'])
    name2_roots = extract_root_words(outcome2['name'])
    def1_roots = extract_root_words(outcome1['definition'])
    def2_roots = extract_root_words(outcome2['definition'])

    # Calculate various similarities
    name_similarity = calculate_similarity(name1, name2)
    def_similarity = calculate_similarity(def1, def2)

    # Root word overlap
    name_root_overlap = len(name1_roots & name2_roots) / max(len(name1_roots | name2_roots), 1)
    def_root_overlap = len(def1_roots & def2_roots) / max(len(def1_roots | def2_roots), 1)

    # Check if one name contains the other
    name_contains = name1 in name2 or name2 in name1

    # Determine which to keep (prefer higher program count, then longer name)
    if outcome1['program_count'] > outcome2['program_count']:
        keep, merge = outcome1, outcome2
    elif outcome1['program_count'] < outcome2['program_count']:
        keep, merge = outcome2, outcome1
    else:
        # Same program count - prefer longer/more descriptive name
        if len(outcome1['name']) >= len(outcome2['name']):
            keep, merge = outcome1, outcome2
        else:
            keep, merge = outcome2, outcome1

    # CONFIDENCE 5: Strict semantic duplicates
    # Very high definition similarity OR names nearly identical with high def similarity
    if def_similarity > 0.85:
        explanation = f"Definitions are {def_similarity:.0%} identical. "
        explanation += f"'{merge['name']}' ({merge['program_count']} programs) should merge into '{keep['name']}' ({keep['program_count']} programs)."
        return True, 5, explanation, keep['name']

    if name_similarity > 0.85 and def_similarity > 0.70:
        explanation = f"Names are {name_similarity:.0%} similar and definitions are {def_similarity:.0%} similar. "
        explanation += f"'{merge['name']}' ({merge['program_count']} programs) should merge into '{keep['name']}' ({keep['program_count']} programs)."
        return True, 5, explanation, keep['name']

    # High root word overlap in definitions (same core concept)
    if def_root_overlap > 0.7 and name_root_overlap > 0.5:
        explanation = f"Core concepts overlap significantly (definition: {def_root_overlap:.0%}, name: {name_root_overlap:.0%}). "
        explanation += f"'{merge['name']}' ({merge['program_count']} programs) should merge into '{keep['name']}' ({keep['program_count']} programs)."
        return True, 5, explanation, keep['name']

    # CONFIDENCE 4: Very likely duplicates
    if (name_contains and def_similarity > 0.60) or \
       (name_similarity > 0.75 and def_similarity > 0.60) or \
       (def_root_overlap > 0.6 and name_root_overlap > 0.4):
        explanation = f"Very likely duplicate - definitions {def_similarity:.0%} similar, names {name_similarity:.0%} similar. "
        explanation += f"'{merge['name']}' ({merge['program_count']} programs) likely merges into '{keep['name']}' ({keep['program_count']} programs)."
        return True, 4, explanation, keep['name']

    # CONFIDENCE 3: Probable overlap
    if (def_similarity > 0.50 and name_root_overlap > 0.4) or \
       (def_root_overlap > 0.5 and name_similarity > 0.50):
        explanation = f"Probable overlap - definitions {def_similarity:.0%} similar, core concepts {def_root_overlap:.0%} overlapping. "
        explanation += f"Consider merging '{merge['name']}' ({merge['program_count']} programs) into '{keep['name']}' ({keep['program_count']} programs)."
        return True, 3, explanation, keep['name']

    # CONFIDENCE 2: Possible consolidation
    if (def_similarity > 0.40 and name_similarity > 0.40):
        explanation = f"Possible consolidation - definitions {def_similarity:.0%} similar, names {name_similarity:.0%} similar. "
        explanation += f"Review if '{merge['name']}' ({merge['program_count']} programs) can merge into '{keep['name']}' ({keep['program_count']} programs)."
        return True, 2, explanation, keep['name']

    return False, 0, "", None

def find_all_duplicates(outcomes):
    """Find all duplicate pairs with enhanced analysis"""
    duplicates = {}  # Use dict to track best match per outcome

    print("\nRunning enhanced semantic analysis...")

    total_comparisons = len(outcomes) * (len(outcomes) - 1) // 2
    comparison_count = 0

    for i in range(len(outcomes)):
        outcome1 = outcomes[i]

        for j in range(i + 1, len(outcomes)):
            outcome2 = outcomes[j]
            comparison_count += 1

            if comparison_count % 5000 == 0:
                print(f"  Analyzed {comparison_count}/{total_comparisons} pairs...")

            is_dup, confidence, explanation, merge_target = analyze_duplicate(outcome1, outcome2)

            if is_dup:
                # Determine which is the merge candidate
                if merge_target == outcome1['name']:
                    merge_id = outcome2['id']
                    merge_outcome = outcome2
                else:
                    merge_id = outcome1['id']
                    merge_outcome = outcome1

                # Keep highest confidence recommendation for each outcome
                if merge_id not in duplicates or confidence > duplicates[merge_id]['confidence']:
                    duplicates[merge_id] = {
                        'outcome': merge_outcome,
                        'confidence': confidence,
                        'explanation': explanation,
                        'merge_target': merge_target
                    }

    print(f"  Completed {comparison_count} comparisons")
    return duplicates

def generate_recommendations(outcomes, duplicates):
    """Generate final recommendations"""
    recommendations = {}

    # Initialize all as Keep
    for outcome in outcomes:
        # Check for zero program count
        if outcome['program_count'] == 0:
            recommendations[outcome['id']] = {
                'action': 'Keep',
                'explanation': f"Zero programs currently use this outcome. Consider if this outcome is still needed for future programs.",
                'confidence': '2'
            }
        else:
            recommendations[outcome['id']] = {
                'action': 'Keep',
                'explanation': f"Unique outcome with {outcome['program_count']} program(s) using it.",
                'confidence': None
            }

    # Update with merge recommendations
    for outcome_id, dup_info in duplicates.items():
        recommendations[outcome_id] = {
            'action': 'Merge',
            'explanation': dup_info['explanation'],
            'confidence': str(dup_info['confidence'])
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
        print(f"Error: {response.status_code}")
        print(response.text)
        return False

    return True

def apply_recommendations(recommendations):
    """Apply recommendations to Airtable"""
    print("\nUpdating Airtable with recommendations...")

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

    # Process in batches
    for i in range(0, len(updates), 10):
        batch = updates[i:i+10]
        print(f"  Updating batch {i//10 + 1}/{(len(updates)-1)//10 + 1}...")

        if not update_records_batch(batch):
            return False

        time.sleep(0.2)

    return True

def main():
    print("=" * 80)
    print("ENHANCED SEMANTIC DUPLICATE ANALYSIS")
    print("=" * 80)

    outcomes = fetch_all_outcomes()

    if not outcomes:
        print("No outcomes found!")
        return

    duplicates = find_all_duplicates(outcomes)

    print(f"\nFound {len(duplicates)} outcomes to merge")

    # Show confidence distribution
    confidence_dist = {}
    for dup_info in duplicates.values():
        conf = dup_info['confidence']
        confidence_dist[conf] = confidence_dist.get(conf, 0) + 1

    print("\nConfidence Distribution:")
    for conf in sorted(confidence_dist.keys(), reverse=True):
        count = confidence_dist[conf]
        print(f"  Confidence {conf}: {count} outcomes")

    # Show high confidence duplicates
    high_conf = {k: v for k, v in duplicates.items() if v['confidence'] == 5}
    if high_conf:
        print(f"\n{'='*80}")
        print(f"HIGH CONFIDENCE DUPLICATES (Confidence = 5): {len(high_conf)} found")
        print(f"{'='*80}")
        for dup_id, dup_info in list(high_conf.items())[:10]:  # Show first 10
            print(f"\n  MERGE: '{dup_info['outcome']['name']}' ({dup_info['outcome']['program_count']} programs)")
            print(f"  INTO:  '{dup_info['merge_target']}'")
            print(f"  Reason: {dup_info['explanation'][:120]}...")

        if len(high_conf) > 10:
            print(f"\n  ... and {len(high_conf) - 10} more confidence=5 duplicates")

    # Generate and apply recommendations
    recommendations = generate_recommendations(outcomes, duplicates)

    if apply_recommendations(recommendations):
        print(f"\n{'='*80}")
        print(f"✓ Successfully updated all {len(outcomes)} outcomes!")
        print(f"{'='*80}")

        # Summary
        action_counts = {}
        for rec in recommendations.values():
            action = rec['action']
            action_counts[action] = action_counts.get(action, 0) + 1

        print("\nFinal Action Summary:")
        for action, count in sorted(action_counts.items()):
            print(f"  {action}: {count}")

        print("\nNext Steps:")
        print("1. Filter by 'Claude Confidence = 5' - IMMEDIATE DELETE candidates")
        print("2. Filter by 'Claude Confidence = 4' - Review and likely delete")
        print("3. Filter by 'Claude Confidence = 3' - Manual review for consolidation")
        print("4. Filter by 'Claude Action = Keep' and 'Program Count = 0' - Consider removal")

if __name__ == '__main__':
    main()
