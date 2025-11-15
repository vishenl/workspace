#!/usr/bin/env python3
"""
Direct Airtable Outcomes Analyzer

This script processes outcomes directly using smaller queries.
"""

import subprocess
import json
import sys
from collections import defaultdict

BASE_ID = "app4ulN4GnBRvcfAL"
TABLE_ID = "tblLA13fGO7KM1JHA"

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


def run_mcp_command(command_args):
    """Run an MCP command and return the result"""
    try:
        # This is a placeholder - in practice we'd use the MCP SDK
        # For now, we'll just print what we would do
        print(f"Would run MCP command: {command_args}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error running MCP command: {e}", file=sys.stderr)
        return None


def normalize_text(text):
    """Normalize text for comparison"""
    if not text:
        return ""
    return text.lower().strip()


def get_usage_counts(fields):
    """Extract usage counts from outcome fields"""
    program_count = fields.get('Program Count', 0) or 0
    meditation_count = fields.get('Meditation Count', 0) or 0
    audio_count = fields.get('Audio Count', 0) or 0
    return program_count, meditation_count, audio_count, program_count + meditation_count + audio_count


def find_semantic_matches(outcome_name, all_outcomes):
    """Find outcomes that match in semantic groups"""
    name_lower = normalize_text(outcome_name)
    matches = []
    my_group = None

    # Find which group(s) this outcome belongs to
    for group in SEMANTIC_GROUPS:
        for term in group:
            if term in name_lower:
                my_group = group
                break
        if my_group:
            break

    if not my_group:
        return matches

    # Find other outcomes in the same group
    for other in all_outcomes:
        other_name = normalize_text(other.get('fields', {}).get('Outcome', ''))
        if other_name == name_lower:
            continue

        for term in my_group:
            if term in other_name:
                matches.append(other)
                break

    return matches


def analyze_outcomes_batch(outcomes):
    """Analyze a batch of outcomes"""
    results = {
        'deletions': [],
        'merges': [],
        'kept': [],
        'semantic_groups': defaultdict(list)
    }

    # First pass: identify deletions
    for outcome in outcomes:
        fields = outcome.get('fields', {})
        outcome_id = outcome.get('id')
        outcome_name = fields.get('Outcome', '')

        # Skip if already processed
        if fields.get('UPDATE TYPE'):
            continue

        p, m, a, total = get_usage_counts(fields)

        # Check deletion criteria
        if total == 0:
            results['deletions'].append({
                'id': outcome_id,
                'name': outcome_name,
                'note': 'No usage: Program Count=0, Meditation Count=0, Audio Count=0',
                'usage': 0
            })
        elif total <= 2:
            results['deletions'].append({
                'id': outcome_id,
                'name': outcome_name,
                'note': f'Low usage: Total={total} (Program={p}, Meditation={m}, Audio={a})',
                'usage': total
            })

    # Second pass: identify merges (exclude deletions)
    deletion_ids = {d['id'] for d in results['deletions']}
    active_outcomes = [o for o in outcomes if o['id'] not in deletion_ids and not o.get('fields', {}).get('UPDATE TYPE')]

    for outcome in active_outcomes:
        fields = outcome.get('fields', {})
        outcome_id = outcome.get('id')
        outcome_name = fields.get('Outcome', '')
        p, m, a, total = get_usage_counts(fields)

        # Find semantic matches
        matches = find_semantic_matches(outcome_name, active_outcomes)

        if matches:
            # Find the highest usage outcome in this group
            group_outcomes = [{'id': outcome_id, 'name': outcome_name, 'usage': total}]
            for match in matches:
                match_fields = match.get('fields', {})
                mp, mm, ma, mtotal = get_usage_counts(match_fields)
                group_outcomes.append({
                    'id': match['id'],
                    'name': match_fields.get('Outcome', ''),
                    'usage': mtotal
                })

            # Sort by usage
            group_outcomes.sort(key=lambda x: x['usage'], reverse=True)
            primary = group_outcomes[0]

            # Track for reporting
            group_key = primary['name']
            results['semantic_groups'][group_key].extend(group_outcomes)

            # If not the primary, recommend merge
            if primary['id'] != outcome_id:
                results['merges'].append({
                    'id': outcome_id,
                    'name': outcome_name,
                    'note': f'Merge into "{primary["name"]}" (usage={primary["usage"]}). Current usage={total}.',
                    'usage': total,
                    'primary': primary['name']
                })
            else:
                results['kept'].append({
                    'id': outcome_id,
                    'name': outcome_name,
                    'usage': total,
                    'reason': 'Primary in semantic group'
                })
        else:
            results['kept'].append({
                'id': outcome_id,
                'name': outcome_name,
                'usage': total,
                'reason': 'Unique outcome'
            })

    return results


def print_report(results, total_analyzed):
    """Print analysis report"""
    print("\n" + "=" * 80)
    print("MINDVALLEY OUTCOMES ANALYSIS REPORT")
    print("=" * 80)

    deletions = results['deletions']
    merges = results['merges']
    kept = results['kept']

    print(f"\nTotal outcomes analyzed: {total_analyzed}")
    print(f"Recommended for DELETION: {len(deletions)}")
    print(f"Recommended for MERGE: {len(merges)}")
    print(f"To KEEP: {len(kept)}")
    print(f"\nEstimated final count: {len(kept)}")
    print(f"Reduction: {len(deletions) + len(merges)} outcomes ({(len(deletions) + len(merges)) / total_analyzed * 100:.1f}%)")

    # Deletions
    print("\n" + "-" * 80)
    print("DELETION RECOMMENDATIONS")
    print("-" * 80)
    print(f"Total: {len(deletions)}\n")

    # Group by reason
    no_usage = [d for d in deletions if d['usage'] == 0]
    low_usage = [d for d in deletions if d['usage'] > 0]

    print(f"** No Usage ({len(no_usage)}) **")
    for item in sorted(no_usage, key=lambda x: x['name'])[:20]:
        print(f"  • {item['name']}")
    if len(no_usage) > 20:
        print(f"  ... and {len(no_usage) - 20} more")

    print(f"\n** Low Usage (≤2) ({len(low_usage)}) **")
    for item in sorted(low_usage, key=lambda x: x['usage'])[:20]:
        print(f"  • {item['name']} (usage: {item['usage']})")
    if len(low_usage) > 20:
        print(f"  ... and {len(low_usage) - 20} more")

    # Merges
    print("\n" + "-" * 80)
    print("MERGE RECOMMENDATIONS")
    print("-" * 80)
    print(f"Total: {len(merges)}\n")

    # Group by primary
    merge_groups = defaultdict(list)
    for m in merges:
        merge_groups[m['primary']].append(m)

    for primary, items in sorted(merge_groups.items(), key=lambda x: len(x[1]), reverse=True)[:15]:
        print(f"\n** Merge into: {primary} **")
        for item in sorted(items, key=lambda x: x['usage'], reverse=True):
            print(f"  • {item['name']} (usage: {item['usage']})")

    # Semantic groups
    print("\n" + "-" * 80)
    print("SEMANTIC GROUPS SUMMARY")
    print("-" * 80)

    for group_name, outcomes in sorted(results['semantic_groups'].items(), key=lambda x: len(x[1]), reverse=True)[:20]:
        unique_outcomes = {o['name']: o for o in outcomes}
        if len(unique_outcomes) > 1:
            print(f"\n** {group_name} ** ({len(unique_outcomes)} outcomes)")
            for outcome in sorted(unique_outcomes.values(), key=lambda x: x['usage'], reverse=True)[:5]:
                print(f"  • {outcome['name']} (usage: {outcome['usage']})")


def generate_update_json(results):
    """Generate JSON for batch updates"""
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

    return updates


def main():
    """Main analysis function"""
    print("=" * 80, file=sys.stderr)
    print("STARTING OUTCOMES ANALYSIS", file=sys.stderr)
    print("=" * 80, file=sys.stderr)

    # For this to work, we need outcome data
    # Since MCP returns too much data, we'll need to get creative

    # Sample data structure for testing
    sample_outcomes = []

    # If we have sample data, analyze it
    if sample_outcomes:
        results = analyze_outcomes_batch(sample_outcomes)
        print_report(results, len(sample_outcomes))

        # Output JSON for updates
        updates = generate_update_json(results)
        print("\n" + "=" * 80)
        print("BATCH UPDATE DATA")
        print("=" * 80)

        # Output in batches of 10
        for i in range(0, len(updates), 10):
            batch = updates[i:i+10]
            print(f"\n# Batch {i//10 + 1} ({len(batch)} records)")
            print(json.dumps(batch, indent=2))
    else:
        print("\nNo data to analyze. This script needs to be integrated with MCP tools.", file=sys.stderr)
        print("See the analysis logic above for the algorithm.", file=sys.stderr)


if __name__ == '__main__':
    main()
