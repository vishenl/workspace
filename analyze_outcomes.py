#!/usr/bin/env python3
"""
Analyze Mindvalley Outcomes and provide recommendations for simplification.
This script analyzes outcomes based on program count, meditation count, and descriptions
to recommend mergers or deletions.
"""

import os
import json
from collections import defaultdict
from pyairtable import Api

# Configuration
BASE_ID = "app4ulN4GnBRvcfAL"
TABLE_ID = "tblLA13fGO7KM1JHA"
API_KEY = os.environ.get("AIRTABLE_API_KEY")

# Field IDs
FIELD_OUTCOME = "fldCP33pFkB25Ynee"
FIELD_PROGRAM_COUNT = "fldE9oQRoudmUiZ2I"
FIELD_MEDITATION_COUNT = "fldkVIkUgZcbBwkaD"
FIELD_DESCRIPTION = "fldpAfFrmwipYiYAw"
FIELD_UPDATE_TYPE = "flddtQoH4JfAU0uTv"
FIELD_UPDATE_NOTE = "fldo4SmxBXYHqOu4R"
FIELD_AUDIO_COUNT = "fldTmPvCIb4e2Bm98"

def get_simple_fields():
    """Return only the essential fields to reduce payload size."""
    return [
        FIELD_OUTCOME,
        FIELD_PROGRAM_COUNT,
        FIELD_MEDITATION_COUNT,
        FIELD_DESCRIPTION,
        FIELD_UPDATE_TYPE,
        FIELD_UPDATE_NOTE,
        FIELD_AUDIO_COUNT
    ]

def fetch_all_outcomes():
    """Fetch all outcomes with only essential fields."""
    api = Api(API_KEY)
    table = api.table(BASE_ID, TABLE_ID)

    print("Fetching outcomes from Airtable...")
    records = []

    # Fetch records using formula to only get essential fields
    for page in table.iterate(
        page_size=100,
        fields=[FIELD_OUTCOME, FIELD_PROGRAM_COUNT, FIELD_MEDITATION_COUNT,
                FIELD_DESCRIPTION, FIELD_UPDATE_TYPE, FIELD_UPDATE_NOTE, FIELD_AUDIO_COUNT]
    ):
        for record in page:
            records.append(record)

    print(f"Fetched {len(records)} outcomes")
    return records

def analyze_outcomes(records):
    """Analyze outcomes and generate recommendations."""
    recommendations = []

    # Group by description similarity
    description_groups = defaultdict(list)

    for record in records:
        fields = record['fields']
        record_id = record['id']

        outcome_name = fields.get(FIELD_OUTCOME, "")
        program_count = fields.get(FIELD_PROGRAM_COUNT, 0)
        meditation_count = fields.get(FIELD_MEDITATION_COUNT, 0)
        audio_count = fields.get(FIELD_AUDIO_COUNT, 0)
        description = fields.get(FIELD_DESCRIPTION, "")
        update_type = fields.get(FIELD_UPDATE_TYPE)

        # Skip if already has an update type
        if update_type:
            continue

        # Calculate total usage
        total_usage = program_count + meditation_count + audio_count

        # Recommendation logic
        recommendation = {
            'id': record_id,
            'outcome': outcome_name,
            'program_count': program_count,
            'meditation_count': meditation_count,
            'audio_count': audio_count,
            'total_usage': total_usage,
            'description': description,
            'update_type': None,
            'update_note': None
        }

        # Rule 1: Very low usage - candidate for deletion
        if total_usage == 0:
            recommendation['update_type'] = 'Deleted'
            recommendation['update_note'] = f"Zero usage across programs ({program_count}), meditations ({meditation_count}), and audios ({audio_count}). Not utilized in content."

        elif total_usage <= 2:
            recommendation['update_type'] = 'Deleted'
            recommendation['update_note'] = f"Very low usage: {total_usage} total (programs: {program_count}, meditations: {meditation_count}, audios: {audio_count}). Consider removing or merging."

        # Rule 2: Group by description for merge candidates
        if description:
            desc_lower = description.lower().strip()
            if desc_lower:
                description_groups[desc_lower].append(recommendation)

        recommendations.append(recommendation)

    # Identify merge candidates based on similar descriptions
    for desc, group in description_groups.items():
        if len(group) > 1:
            # Sort by usage, keep the most used one
            group.sort(key=lambda x: x['total_usage'], reverse=True)
            primary = group[0]

            for i, outcome in enumerate(group[1:], 1):
                # Only suggest merge if not already marked for deletion
                if not outcome['update_type']:
                    outcome['update_type'] = 'Merged'
                    outcome['update_note'] = f"Similar description to '{primary['outcome']}' (usage: {primary['total_usage']}). Suggest merging into the primary outcome."

    return recommendations

def find_semantic_similarities(recommendations):
    """Find outcomes with semantically similar names."""
    merge_suggestions = []

    # Common semantic groups
    similar_terms = [
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

    for terms in similar_terms:
        matches = []
        for rec in recommendations:
            outcome_lower = rec['outcome'].lower()
            if any(term in outcome_lower for term in terms):
                matches.append(rec)

        if len(matches) > 1:
            # Sort by total usage
            matches.sort(key=lambda x: x['total_usage'], reverse=True)
            for match in matches:
                if match not in merge_suggestions:
                    merge_suggestions.append({
                        'outcomes': [m['outcome'] for m in matches],
                        'group': terms,
                        'primary_candidate': matches[0]['outcome']
                    })
                    break

    return merge_suggestions

def generate_report(recommendations):
    """Generate a human-readable report."""
    delete_count = sum(1 for r in recommendations if r['update_type'] == 'Deleted')
    merge_count = sum(1 for r in recommendations if r['update_type'] == 'Merged')

    print("\n" + "="*80)
    print("OUTCOMES SIMPLIFICATION ANALYSIS")
    print("="*80)
    print(f"\nTotal outcomes analyzed: {len(recommendations)}")
    print(f"Recommended for deletion: {delete_count}")
    print(f"Recommended for merging: {merge_count}")
    print(f"Potential reduction: {delete_count + merge_count} outcomes")

    if delete_count > 0:
        print("\n" + "-"*80)
        print("DELETION CANDIDATES (Low/No Usage)")
        print("-"*80)
        deletions = [r for r in recommendations if r['update_type'] == 'Deleted']
        deletions.sort(key=lambda x: x['total_usage'])

        for i, rec in enumerate(deletions[:50], 1):  # Show first 50
            print(f"\n{i}. {rec['outcome']}")
            print(f"   Usage: Programs={rec['program_count']}, Meditations={rec['meditation_count']}, Audios={rec['audio_count']}")
            print(f"   Reason: {rec['update_note']}")

        if len(deletions) > 50:
            print(f"\n... and {len(deletions) - 50} more")

    if merge_count > 0:
        print("\n" + "-"*80)
        print("MERGE CANDIDATES (Similar Descriptions)")
        print("-"*80)
        merges = [r for r in recommendations if r['update_type'] == 'Merged']

        for i, rec in enumerate(merges[:30], 1):  # Show first 30
            print(f"\n{i}. {rec['outcome']}")
            print(f"   Usage: Programs={rec['program_count']}, Meditations={rec['meditation_count']}, Audios={rec['audio_count']}")
            print(f"   Reason: {rec['update_note']}")

        if len(merges) > 30:
            print(f"\n... and {len(merges) - 30} more")

    # Semantic similarity analysis
    print("\n" + "-"*80)
    print("SEMANTIC SIMILARITY ANALYSIS")
    print("-"*80)
    semantic_suggestions = find_semantic_similarities(recommendations)
    if semantic_suggestions:
        for i, suggestion in enumerate(semantic_suggestions[:20], 1):
            print(f"\n{i}. Group: {', '.join(suggestion['group'])}")
            print(f"   Outcomes: {', '.join(suggestion['outcomes'])}")
            print(f"   Primary candidate: {suggestion['primary_candidate']}")

    return recommendations

def save_to_file(recommendations):
    """Save recommendations to JSON file for review."""
    output_file = "outcome_recommendations.json"
    with open(output_file, 'w') as f:
        json.dump(recommendations, f, indent=2)
    print(f"\n\nFull recommendations saved to: {output_file}")

def main():
    if not API_KEY:
        print("Error: AIRTABLE_API_KEY environment variable not set")
        return

    # Fetch outcomes
    records = fetch_all_outcomes()

    # Analyze
    recommendations = analyze_outcomes(records)

    # Generate report
    generate_report(recommendations)

    # Save to file
    save_to_file(recommendations)

    print("\n" + "="*80)
    print("Analysis complete! Review the recommendations above.")
    print("To apply these changes to Airtable, we can create an update script.")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
