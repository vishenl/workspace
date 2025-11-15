#!/usr/bin/env python3
"""
Mindvalley Outcomes Analysis Script

This script analyzes outcomes in the Airtable and provides recommendations for:
- Deletions (low/no usage)
- Merges (semantic similarity)

The script will output a detailed report and optionally update Airtable.
"""

import json
import sys
from collections import defaultdict

# Semantic groups for merge detection
SEMANTIC_GROUPS = [
    ['stress', 'anxiety', 'worry', 'tension'],
    ['happiness', 'joy', 'bliss', 'contentment'],
    ['focus', 'concentration', 'attention'],
    ['energy', 'vitality', 'vigor'],
    ['calm', 'peace', 'tranquility', 'serenity'],
    ['confidence', 'self-esteem', 'self-worth'],
    ['creativity', 'innovation', 'imagination'],
    ['motivation', 'drive', 'ambition'],
    ['relaxation', 'rest', 'recovery'],
    ['clarity', 'clear-thinking', 'mental clarity'],
    ['gratitude', 'thankfulness', 'appreciation'],
    ['compassion', 'empathy', 'kindness'],
    ['resilience', 'strength', 'fortitude'],
    ['mindfulness', 'presence', 'awareness'],
    ['sleep', 'rest', 'sleep quality'],
    ['abundance', 'prosperity', 'wealth'],
    ['healing', 'recovery', 'restoration'],
    ['balance', 'harmony', 'equilibrium'],
    ['forgiveness', 'letting go', 'release'],
    ['intuition', 'inner wisdom', 'gut feeling']
]


def load_outcomes_from_stdin():
    """Load outcomes data from stdin (piped from MCP tool)"""
    try:
        data = json.load(sys.stdin)
        return data.get('records', [])
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        return []


def get_usage_counts(fields):
    """Extract usage counts from outcome fields"""
    program_count = fields.get('Program Count', 0) or 0
    meditation_count = fields.get('Meditation Count', 0) or 0
    audio_count = fields.get('Audio Count', 0) or 0
    return program_count, meditation_count, audio_count


def find_semantic_group(outcome_name):
    """Find which semantic group this outcome belongs to"""
    name_lower = outcome_name.lower()
    for group_idx, group in enumerate(SEMANTIC_GROUPS):
        for term in group:
            if term in name_lower or name_lower in term:
                return group_idx, group
    return None, None


def analyze_outcome(outcome, all_outcomes, outcomes_by_group):
    """Analyze a single outcome and determine action"""
    fields = outcome.get('fields', {})
    outcome_id = outcome.get('id')
    outcome_name = fields.get('Outcome', '')
    description = fields.get('Description', '')

    # Skip if already has UPDATE TYPE
    if fields.get('UPDATE TYPE'):
        return None

    # Get usage counts
    program_count, meditation_count, audio_count = get_usage_counts(fields)
    total_usage = program_count + meditation_count + audio_count

    # DELETION CRITERIA
    if total_usage == 0:
        return {
            'id': outcome_id,
            'name': outcome_name,
            'type': 'Deleted',
            'note': f'No usage: Program Count=0, Meditation Count=0, Audio Count=0'
        }

    if total_usage <= 2:
        return {
            'id': outcome_id,
            'name': outcome_name,
            'type': 'Deleted',
            'note': f'Low usage: Total={total_usage} (Program={program_count}, Meditation={meditation_count}, Audio={audio_count})'
        }

    # MERGE CRITERIA
    group_idx, group = find_semantic_group(outcome_name)
    if group_idx is not None:
        # Find other outcomes in the same semantic group
        similar_outcomes = outcomes_by_group.get(group_idx, [])
        similar_outcomes = [o for o in similar_outcomes if o['id'] != outcome_id]

        if similar_outcomes:
            # Find the outcome with highest usage in the group
            all_related = [{'id': outcome_id, 'name': outcome_name, 'usage': total_usage}]
            for sim in similar_outcomes:
                sim_fields = sim.get('fields', {})
                p, m, a = get_usage_counts(sim_fields)
                all_related.append({
                    'id': sim['id'],
                    'name': sim_fields.get('Outcome', ''),
                    'usage': p + m + a
                })

            # Sort by usage (highest first)
            all_related.sort(key=lambda x: x['usage'], reverse=True)
            primary = all_related[0]

            # If current outcome is not the primary, recommend merge
            if primary['id'] != outcome_id:
                return {
                    'id': outcome_id,
                    'name': outcome_name,
                    'type': 'Merged',
                    'note': f'Similar to "{primary["name"]}" (usage={primary["usage"]}). Current usage={total_usage}. Semantic group: {", ".join(group[:3])}...'
                }

    # Check for identical descriptions
    if description:
        for other in all_outcomes:
            if other['id'] == outcome_id:
                continue
            if other.get('fields', {}).get('UPDATE TYPE'):
                continue

            other_desc = other.get('fields', {}).get('Description', '')
            if other_desc and description.lower() == other_desc.lower():
                other_fields = other.get('fields', {})
                p, m, a = get_usage_counts(other_fields)
                other_usage = p + m + a

                if other_usage > total_usage:
                    return {
                        'id': outcome_id,
                        'name': outcome_name,
                        'type': 'Merged',
                        'note': f'Identical description to "{other_fields.get("Outcome", "")}" (usage={other_usage}). Current usage={total_usage}.'
                    }

    return None


def main():
    print("Loading outcomes data from stdin...", file=sys.stderr)
    outcomes = load_outcomes_from_stdin()

    if not outcomes:
        print("No outcomes loaded. Please pipe data from MCP tool.", file=sys.stderr)
        return

    print(f"Loaded {len(outcomes)} outcomes", file=sys.stderr)

    # Skip outcomes that already have UPDATE TYPE
    outcomes_to_analyze = [o for o in outcomes if not o.get('fields', {}).get('UPDATE TYPE')]
    print(f"Analyzing {len(outcomes_to_analyze)} outcomes (skipping {len(outcomes) - len(outcomes_to_analyze)} already processed)", file=sys.stderr)

    # Group outcomes by semantic group for faster lookup
    outcomes_by_group = defaultdict(list)
    for outcome in outcomes_to_analyze:
        outcome_name = outcome.get('fields', {}).get('Outcome', '')
        group_idx, _ = find_semantic_group(outcome_name)
        if group_idx is not None:
            outcomes_by_group[group_idx].append(outcome)

    # Analyze each outcome
    deletions = []
    merges = []

    for outcome in outcomes_to_analyze:
        result = analyze_outcome(outcome, outcomes_to_analyze, outcomes_by_group)
        if result:
            if result['type'] == 'Deleted':
                deletions.append(result)
            elif result['type'] == 'Merged':
                merges.append(result)

    # Generate report
    print("\n" + "=" * 80)
    print("MINDVALLEY OUTCOMES ANALYSIS REPORT")
    print("=" * 80)
    print(f"\nTotal outcomes in table: {len(outcomes)}")
    print(f"Already processed: {len(outcomes) - len(outcomes_to_analyze)}")
    print(f"Analyzed in this run: {len(outcomes_to_analyze)}")
    print(f"\nRecommended for DELETION: {len(deletions)}")
    print(f"Recommended for MERGE: {len(merges)}")
    print(f"To KEEP as-is: {len(outcomes_to_analyze) - len(deletions) - len(merges)}")
    print(f"\nEstimated reduction: {len(deletions) + len(merges)} outcomes")

    # Deletion details
    print("\n" + "-" * 80)
    print("DELETION RECOMMENDATIONS")
    print("-" * 80)
    print(f"Total: {len(deletions)}\n")

    for i, item in enumerate(deletions[:30], 1):
        print(f"{i}. {item['name']}")
        print(f"   → {item['note']}\n")

    if len(deletions) > 30:
        print(f"... and {len(deletions) - 30} more\n")

    # Merge details
    print("\n" + "-" * 80)
    print("MERGE RECOMMENDATIONS")
    print("-" * 80)
    print(f"Total: {len(merges)}\n")

    # Group merges by semantic group
    merge_groups = defaultdict(list)
    for item in merges:
        # Extract semantic group from note
        if 'Semantic group:' in item['note']:
            group = item['note'].split('Semantic group:')[1].split('...')[0].strip()
            merge_groups[group].append(item)
        else:
            merge_groups['Identical Description'].append(item)

    for group_name, items in sorted(merge_groups.items()):
        print(f"\n** {group_name.upper()} **")
        for item in items[:10]:
            print(f"  • {item['name']}")
            print(f"    → {item['note']}\n")

    # Semantic group summary
    print("\n" + "-" * 80)
    print("SEMANTIC GROUPS WITH MULTIPLE OUTCOMES")
    print("-" * 80)

    for group_idx, outcomes_in_group in sorted(outcomes_by_group.items(), key=lambda x: len(x[1]), reverse=True):
        if len(outcomes_in_group) > 1:
            group_terms = SEMANTIC_GROUPS[group_idx]
            print(f"\n{', '.join(group_terms[:3])}... ({len(outcomes_in_group)} outcomes)")
            for outcome in outcomes_in_group[:5]:
                fields = outcome.get('fields', {})
                p, m, a = get_usage_counts(fields)
                total = p + m + a
                print(f"  • {fields.get('Outcome', '')} (usage: {total})")

    # Output update data as JSON for batch processing
    print("\n" + "=" * 80)
    print("UPDATE DATA (JSON)")
    print("=" * 80)

    updates = []
    for item in deletions + merges:
        updates.append({
            'id': item['id'],
            'fields': {
                'UPDATE TYPE': item['type'],
                'UPDATE NOTE': item['note']
            }
        })

    # Output in batches of 10 for Airtable batch update
    for i in range(0, len(updates), 10):
        batch = updates[i:i+10]
        print(f"\n# Batch {i//10 + 1}")
        print(json.dumps(batch, indent=2))


if __name__ == '__main__':
    main()
