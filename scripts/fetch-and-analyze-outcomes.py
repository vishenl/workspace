#!/usr/bin/env python3
"""
Fetch and Analyze Mindvalley Outcomes

This script fetches outcomes from Airtable in small batches and analyzes them
for deletion and merge recommendations.
"""

import os
import json
import requests
from collections import defaultdict
import time

BASE_ID = "app4ulN4GnBRvcfAL"
TABLE_ID = "tblLA13fGO7KM1JHA"
API_KEY = os.environ.get("AIRTABLE_API_KEY")

if not API_KEY:
    print("ERROR: AIRTABLE_API_KEY environment variable not set")
    print("Please set it with: export AIRTABLE_API_KEY='your_key_here'")
    exit(1)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Semantic groups for merge detection
SEMANTIC_GROUPS = [
    ['stress', 'anxiety', 'worry', 'tension', 'anxious', 'worried', 'tense', 'stressed'],
    ['happiness', 'joy', 'bliss', 'contentment', 'happy', 'joyful', 'blissful', 'content'],
    ['focus', 'concentration', 'attention', 'focused', 'concentrate', 'attentive'],
    ['energy', 'vitality', 'vigor', 'energized', 'energetic', 'vital', 'vigorous'],
    ['calm', 'peace', 'tranquility', 'serenity', 'peaceful', 'tranquil', 'serene', 'calmness'],
    ['confidence', 'self-esteem', 'self-worth', 'self-confidence', 'confident'],
    ['creativity', 'innovation', 'imagination', 'creative', 'innovative', 'imaginative'],
    ['motivation', 'drive', 'ambition', 'motivated', 'driven', 'ambitious'],
    ['relaxation', 'rest', 'recovery', 'relax', 'relaxed', 'rested', 'recover'],
    ['clarity', 'clear-thinking', 'mental clarity', 'clear', 'clearness'],
    ['gratitude', 'thankfulness', 'appreciation', 'grateful', 'thankful', 'appreciative'],
    ['compassion', 'empathy', 'kindness', 'compassionate', 'empathetic', 'kind'],
    ['resilience', 'strength', 'fortitude', 'resilient', 'strong'],
    ['mindfulness', 'presence', 'awareness', 'mindful', 'present', 'aware'],
    ['sleep', 'rest', 'sleep quality', 'sleeping', 'restful'],
    ['abundance', 'prosperity', 'wealth', 'abundant', 'prosperous', 'wealthy'],
    ['healing', 'recovery', 'restoration', 'heal', 'restore', 'recovered'],
    ['balance', 'harmony', 'equilibrium', 'balanced', 'harmonious'],
    ['forgiveness', 'letting go', 'release', 'forgive', 'let go'],
    ['intuition', 'inner wisdom', 'gut feeling', 'intuitive', 'instinct'],
    ['love', 'loving', 'self-love', 'loving-kindness'],
    ['pain', 'pain relief', 'chronic pain', 'back pain'],
    ['anger', 'frustration', 'irritation', 'angry', 'frustrated', 'irritated'],
    ['fear', 'scared', 'frightened', 'afraid', 'fearful'],
    ['sadness', 'depression', 'melancholy', 'sad', 'depressed'],
    ['success', 'achievement', 'accomplishment', 'successful', 'achieve'],
    ['spiritual', 'spirituality', 'spiritual growth', 'spiritual awakening'],
    ['self-awareness', 'self-discovery', 'self-knowledge'],
    ['purpose', 'life purpose', 'meaning', 'meaningful'],
    ['connection', 'social connection', 'belonging', 'connected']
]


def fetch_outcomes():
    """Fetch all outcomes that don't have UPDATE TYPE set"""
    print("Fetching outcomes from Airtable...")

    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"
    params = {
        'filterByFormula': 'NOT({UPDATE TYPE})',
        'fields[]': ['Outcome', 'Program Count', 'Meditation Count', 'Audio Count', 'Description', 'UPDATE TYPE'],
        'pageSize': 100
    }

    all_records = []
    offset = None

    while True:
        if offset:
            params['offset'] = offset

        try:
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()

            records = data.get('records', [])
            all_records.extend(records)
            print(f"  Fetched {len(all_records)} records so far...")

            offset = data.get('offset')
            if not offset:
                break

            time.sleep(0.2)  # Rate limiting

        except Exception as e:
            print(f"Error fetching data: {e}")
            break

    print(f"Total outcomes fetched: {len(all_records)}\n")
    return all_records


def get_usage(fields):
    """Get usage counts from fields"""
    p = fields.get('Program Count', 0) or 0
    m = fields.get('Meditation Count', 0) or 0
    a = fields.get('Audio Count', 0) or 0
    return p, m, a, p + m + a


def find_semantic_group(name):
    """Find which semantic group this outcome belongs to"""
    name_lower = name.lower().strip()
    for idx, group in enumerate(SEMANTIC_GROUPS):
        for term in group:
            if term in name_lower:
                return idx, group
    return None, None


def analyze_outcomes(outcomes):
    """Analyze outcomes and generate recommendations"""
    print("Analyzing outcomes...\n")

    deletions = []
    merges = []
    kept = []

    # Group by semantic similarity
    semantic_map = defaultdict(list)

    for outcome in outcomes:
        fields = outcome.get('fields', {})
        outcome_id = outcome.get('id')
        name = fields.get('Outcome', '')
        p, m, a, total = get_usage(fields)

        # Deletion criteria
        if total == 0:
            deletions.append({
                'id': outcome_id,
                'name': name,
                'note': 'No usage: Program Count=0, Meditation Count=0, Audio Count=0',
                'usage': 0
            })
            continue

        if total <= 2:
            deletions.append({
                'id': outcome_id,
                'name': name,
                'note': f'Low usage: Total={total} (Program={p}, Meditation={m}, Audio={a})',
                'usage': total
            })
            continue

        # Group by semantic similarity
        group_idx, group = find_semantic_group(name)
        if group_idx is not None:
            semantic_map[group_idx].append({
                'id': outcome_id,
                'name': name,
                'usage': total,
                'fields': fields
            })
        else:
            kept.append({
                'id': outcome_id,
                'name': name,
                'usage': total
            })

    # Analyze semantic groups for merges
    for group_idx, outcomes_in_group in semantic_map.items():
        if len(outcomes_in_group) <= 1:
            kept.extend(outcomes_in_group)
            continue

        # Sort by usage (highest first)
        outcomes_in_group.sort(key=lambda x: x['usage'], reverse=True)
        primary = outcomes_in_group[0]

        # Keep the primary, merge the rest
        kept.append(primary)

        for outcome in outcomes_in_group[1:]:
            group_terms = ', '.join(SEMANTIC_GROUPS[group_idx][:3])
            merges.append({
                'id': outcome['id'],
                'name': outcome['name'],
                'note': f'Merge into "{primary["name"]}" (usage={primary["usage"]}). Current usage={outcome["usage"]}. Semantic group: {group_terms}',
                'usage': outcome['usage'],
                'primary': primary['name']
            })

    return {
        'deletions': deletions,
        'merges': merges,
        'kept': kept,
        'semantic_map': semantic_map
    }


def print_report(results, total):
    """Print analysis report"""
    deletions = results['deletions']
    merges = results['merges']
    kept = results['kept']

    print("=" * 80)
    print("MINDVALLEY OUTCOMES ANALYSIS REPORT")
    print("=" * 80)
    print(f"\nTotal outcomes analyzed: {total}")
    print(f"Recommended for DELETION: {len(deletions)}")
    print(f"Recommended for MERGE: {len(merges)}")
    print(f"To KEEP: {len(kept)}")
    print(f"\nEstimated final count: {len(kept)}")
    print(f"Reduction: {len(deletions) + len(merges)} outcomes ({(len(deletions) + len(merges)) / total * 100:.1f}%)")

    # Deletions
    print("\n" + "-" * 80)
    print("DELETION RECOMMENDATIONS")
    print("-" * 80)

    no_usage = [d for d in deletions if d['usage'] == 0]
    low_usage = [d for d in deletions if d['usage'] > 0]

    print(f"\n** No Usage ({len(no_usage)} outcomes) **")
    for item in sorted(no_usage, key=lambda x: x['name'])[:30]:
        print(f"  • {item['name']}")
    if len(no_usage) > 30:
        print(f"  ... and {len(no_usage) - 30} more")

    print(f"\n** Low Usage (≤2) ({len(low_usage)} outcomes) **")
    for item in sorted(low_usage, key=lambda x: x['usage'])[:30]:
        print(f"  • {item['name']} (usage: {item['usage']})")
    if len(low_usage) > 30:
        print(f"  ... and {len(low_usage) - 30} more")

    # Merges
    print("\n" + "-" * 80)
    print("MERGE RECOMMENDATIONS")
    print("-" * 80)

    merge_groups = defaultdict(list)
    for m in merges:
        merge_groups[m['primary']].append(m)

    print(f"\nTotal merge groups: {len(merge_groups)}")
    print(f"Total outcomes to merge: {len(merges)}\n")

    for primary, items in sorted(merge_groups.items(), key=lambda x: len(x[1]), reverse=True)[:20]:
        print(f"\n** Primary: {primary} ({len(items)} to merge) **")
        for item in sorted(items, key=lambda x: x['usage'], reverse=True)[:5]:
            print(f"  • {item['name']} (usage: {item['usage']})")
        if len(items) > 5:
            print(f"  ... and {len(items) - 5} more")

    # Semantic groups summary
    print("\n" + "-" * 80)
    print("SEMANTIC GROUPS SUMMARY")
    print("-" * 80)

    for group_idx, outcomes_list in sorted(results['semantic_map'].items(), key=lambda x: len(x[1]), reverse=True)[:15]:
        if len(outcomes_list) > 1:
            group_terms = ', '.join(SEMANTIC_GROUPS[group_idx][:4])
            print(f"\n** {group_terms} ** ({len(outcomes_list)} outcomes)")
            for outcome in sorted(outcomes_list, key=lambda x: x['usage'], reverse=True)[:5]:
                print(f"  • {outcome['name']} (usage: {outcome['usage']})")


def save_updates_json(results, filename='outcome-updates.json'):
    """Save updates to JSON file for batch processing"""
    updates = []

    for item in results['deletions']:
        updates.append({
            'id': item['id'],
            'fields': {
                'UPDATE TYPE': 'Deleted',
                'UPDATE NOTE': item['note']
            }
        })

    for item in results['merges']:
        updates.append({
            'id': item['id'],
            'fields': {
                'UPDATE TYPE': 'Merged',
                'UPDATE NOTE': item['note']
            }
        })

    # Save in batches of 10
    batches = []
    for i in range(0, len(updates), 10):
        batches.append(updates[i:i+10])

    with open(filename, 'w') as f:
        json.dump({
            'total_updates': len(updates),
            'batches': batches
        }, f, indent=2)

    print(f"\n\nUpdates saved to {filename}")
    print(f"Total updates: {len(updates)}")
    print(f"Total batches: {len(batches)}")


def main():
    outcomes = fetch_outcomes()

    if not outcomes:
        print("No outcomes to analyze")
        return

    results = analyze_outcomes(outcomes)
    print_report(results, len(outcomes))
    save_updates_json(results)

    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("\n1. Review the recommendations above")
    print("2. Check outcome-updates.json for batch update data")
    print("3. Use MCP Airtable update_records tool to apply changes")
    print("\nExample update command:")
    print('  mcp__airtable__update_records(baseId="app4ulN4GnBRvcfAL", tableId="tblLA13fGO7KM1JHA", records=<batch>)')


if __name__ == '__main__':
    main()
