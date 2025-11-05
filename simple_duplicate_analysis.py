#!/usr/bin/env python3
"""
Simple analysis focused on close duplicates - straightforward comparison
"""

import os
import requests
import time
from difflib import SequenceMatcher

BASE_ID = 'app4ulN4GnBRvcfAL'
TABLE_ID = 'tblLA13fGO7KM1JHA'

api_key = os.environ.get('AIRTABLE_API_KEY')

def fetch_all_outcomes():
    """Fetch all current outcomes"""
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

    print("Fetching current outcomes...")

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

        time.sleep(0.2)

    print(f"Total outcomes: {len(all_records)}")
    return all_records

def normalize(text):
    """Simple normalization"""
    return text.lower().strip() if text else ""

def similarity_ratio(text1, text2):
    """Calculate similarity between two texts"""
    return SequenceMatcher(None, normalize(text1), normalize(text2)).ratio()

def find_close_duplicates(outcomes):
    """
    Find close duplicates using simple, clear criteria:
    - Very similar names OR
    - Very similar definitions OR
    - Names that are substrings of each other with similar meanings
    """
    duplicates = {}

    print("\nAnalyzing for close duplicates...")
    print("Criteria: Similar names + similar definitions\n")

    for i in range(len(outcomes)):
        for j in range(i + 1, len(outcomes)):
            o1 = outcomes[i]
            o2 = outcomes[j]

            name_sim = similarity_ratio(o1['name'], o2['name'])
            def_sim = similarity_ratio(o1['definition'], o2['definition'])

            # Check if one name contains the other
            name1_norm = normalize(o1['name'])
            name2_norm = normalize(o2['name'])
            name_contains = (name1_norm in name2_norm or name2_norm in name1_norm) and name1_norm != name2_norm

            # Determine confidence and whether it's a duplicate
            confidence = 0
            reason = ""

            # CONFIDENCE 5: Very high similarity
            if def_sim >= 0.90:
                confidence = 5
                reason = f"Definitions are {def_sim:.0%} identical"
            elif name_sim >= 0.85 and def_sim >= 0.70:
                confidence = 5
                reason = f"Names {name_sim:.0%} similar, definitions {def_sim:.0%} similar"
            elif name_contains and def_sim >= 0.70:
                confidence = 5
                reason = f"One name contains the other, definitions {def_sim:.0%} similar"

            # CONFIDENCE 4: High similarity
            elif def_sim >= 0.75:
                confidence = 4
                reason = f"Definitions are {def_sim:.0%} similar"
            elif name_sim >= 0.75 and def_sim >= 0.60:
                confidence = 4
                reason = f"Names {name_sim:.0%} similar, definitions {def_sim:.0%} similar"
            elif name_contains and def_sim >= 0.55:
                confidence = 4
                reason = f"One name contains the other, definitions {def_sim:.0%} similar"

            # CONFIDENCE 3: Moderate similarity
            elif def_sim >= 0.60:
                confidence = 3
                reason = f"Definitions are {def_sim:.0%} similar"
            elif name_sim >= 0.65 and def_sim >= 0.50:
                confidence = 3
                reason = f"Names {name_sim:.0%} similar, definitions {def_sim:.0%} similar"

            if confidence >= 3:
                # Determine which to keep (higher program count wins)
                if o1['program_count'] > o2['program_count']:
                    keep, merge = o1, o2
                elif o2['program_count'] > o1['program_count']:
                    keep, merge = o2, o1
                else:
                    # Same program count - keep longer/more descriptive name
                    keep, merge = (o1, o2) if len(o1['name']) >= len(o2['name']) else (o2, o1)

                merge_id = merge['id']

                # Only keep highest confidence for each outcome
                if merge_id not in duplicates or confidence > duplicates[merge_id]['confidence']:
                    duplicates[merge_id] = {
                        'merge_name': merge['name'],
                        'merge_programs': merge['program_count'],
                        'keep_name': keep['name'],
                        'keep_programs': keep['program_count'],
                        'confidence': confidence,
                        'reason': reason,
                        'name_similarity': name_sim,
                        'def_similarity': def_sim
                    }

    return duplicates

def generate_recommendations(outcomes, duplicates):
    """Generate simple, clear recommendations"""
    recommendations = {}

    # Default: Keep everything
    for outcome in outcomes:
        pc = outcome['program_count']

        if pc == 0:
            recommendations[outcome['id']] = {
                'action': 'Keep',
                'explanation': f"No programs currently use this outcome. Review if still needed.",
                'confidence': None
            }
        else:
            recommendations[outcome['id']] = {
                'action': 'Keep',
                'explanation': f"Unique outcome used by {pc} program(s).",
                'confidence': None
            }

    # Update with merges
    for merge_id, dup in duplicates.items():
        explanation = f"{dup['reason']}. "
        explanation += f"Merge '{dup['merge_name']}' ({dup['merge_programs']} programs) "
        explanation += f"into '{dup['keep_name']}' ({dup['keep_programs']} programs)."

        recommendations[merge_id] = {
            'action': 'Merge',
            'explanation': explanation,
            'confidence': str(dup['confidence'])
        }

    return recommendations

def update_airtable(recommendations):
    """Update Airtable with recommendations"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print("\nUpdating Airtable...")

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

    # Update in batches of 10
    for i in range(0, len(updates), 10):
        batch = updates[i:i+10]
        payload = {"records": batch}

        response = requests.patch(url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"Error in batch {i//10 + 1}: {response.status_code}")
            print(response.text)
            return False

        print(f"  Batch {i//10 + 1}/{(len(updates)-1)//10 + 1} updated")
        time.sleep(0.2)

    return True

def main():
    print("=" * 80)
    print("SIMPLE CLOSE DUPLICATE ANALYSIS")
    print("=" * 80)

    outcomes = fetch_all_outcomes()

    if not outcomes:
        print("No outcomes found!")
        return

    duplicates = find_close_duplicates(outcomes)

    print(f"\nFound {len(duplicates)} close duplicates")

    # Show confidence distribution
    conf_counts = {}
    for dup in duplicates.values():
        conf = dup['confidence']
        conf_counts[conf] = conf_counts.get(conf, 0) + 1

    print("\nConfidence Distribution:")
    for conf in sorted(conf_counts.keys(), reverse=True):
        print(f"  Confidence {conf}: {conf_counts[conf]} outcomes")

    # Show examples of confidence 5
    conf5 = {k: v for k, v in duplicates.items() if v['confidence'] == 5}
    if conf5:
        print(f"\n{'='*80}")
        print(f"CONFIDENCE 5 DUPLICATES: {len(conf5)} found")
        print(f"{'='*80}")

        for i, (merge_id, dup) in enumerate(list(conf5.items())[:15]):
            print(f"\n{i+1}. MERGE: '{dup['merge_name']}' ({dup['merge_programs']} programs)")
            print(f"   INTO:  '{dup['keep_name']}' ({dup['keep_programs']} programs)")
            print(f"   WHY:   {dup['reason']}")

        if len(conf5) > 15:
            print(f"\n   ... and {len(conf5) - 15} more")

    # Generate and apply
    recommendations = generate_recommendations(outcomes, duplicates)

    if update_airtable(recommendations):
        print(f"\n{'='*80}")
        print(f"✓ Successfully analyzed {len(outcomes)} outcomes")
        print(f"{'='*80}")

        action_counts = {}
        for rec in recommendations.values():
            action_counts[rec['action']] = action_counts.get(rec['action'], 0) + 1

        print("\nAction Summary:")
        for action, count in sorted(action_counts.items()):
            print(f"  {action}: {count}")

        print("\nRecommendation:")
        print("  → Filter by 'Claude Confidence = 5' to see immediate merge candidates")
        print(f"  → You can delete these {len(conf5)} duplicates right away")

if __name__ == '__main__':
    main()
