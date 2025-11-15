#!/usr/bin/env python3
"""
Batch process Mindvalley Outcomes analysis with MCP-compatible approach.
This script works around token limits by processing records systematically.
"""

import json
import time
from datetime import datetime

# Configuration
BASE_ID = "app4ulN4GnBRvcfAL"
TABLE_ID = "tblLA13fGO7KM1JHA"

# Field IDs from the table description
FIELDS = {
    'outcome': 'fldCP33pFkB25Ynee',
    'program_count': 'fldE9oQRoudmUiZ2I',
    'meditation_count': 'fldkVIkUgZcbBwkaD',
    'audio_count': 'fldTmPvCIb4e2Bm98',
    'description': 'fldpAfFrmwipYiYAw',
    'update_type': 'flddtQoH4JfAU0uTv',
    'update_note': 'fldo4SmxBXYHqOu4R'
}

# Common semantic patterns for merging
SEMANTIC_PATTERNS = {
    'stress_anxiety': ['stress', 'anxiety', 'worry', 'tension', 'anxious', 'stressed', 'worrying'],
    'happiness_joy': ['happiness', 'joy', 'bliss', 'contentment', 'happy', 'joyful', 'blissful'],
    'focus_concentration': ['focus', 'concentration', 'attention', 'focused', 'concentrate', 'attentive'],
    'energy_vitality': ['energy', 'vitality', 'vigor', 'energetic', 'vital', 'vigorous'],
    'calm_peace': ['calm', 'peace', 'tranquility', 'serenity', 'peaceful', 'tranquil', 'serene'],
    'confidence': ['confidence', 'self-esteem', 'self-worth', 'self-confidence', 'confident'],
    'creativity': ['creativity', 'innovation', 'imagination', 'creative', 'innovative', 'imaginative'],
    'motivation': ['motivation', 'drive', 'ambition', 'motivated', 'driven', 'ambitious'],
    'relaxation': ['relaxation', 'rest', 'recovery', 'relaxed', 'resting', 'recovering'],
    'clarity': ['clarity', 'clear-thinking', 'mental clarity', 'clear', 'clearheaded'],
    'gratitude': ['gratitude', 'thankfulness', 'appreciation', 'grateful', 'thankful', 'appreciative'],
    'compassion': ['compassion', 'empathy', 'kindness', 'compassionate', 'empathetic', 'kind'],
    'resilience': ['resilience', 'strength', 'fortitude', 'resilient', 'strong'],
    'mindfulness': ['mindfulness', 'presence', 'awareness', 'mindful', 'present', 'aware'],
    'sleep': ['sleep', 'rest', 'sleep quality', 'sleeping', 'restful'],
    'abundance': ['abundance', 'prosperity', 'wealth', 'abundant', 'prosperous', 'wealthy'],
    'healing': ['healing', 'recovery', 'restoration', 'heal', 'recover', 'restore'],
    'balance': ['balance', 'harmony', 'equilibrium', 'balanced', 'harmonious'],
    'forgiveness': ['forgiveness', 'letting go', 'release', 'forgive', 'let go'],
    'intuition': ['intuition', 'inner wisdom', 'gut feeling', 'intuitive', 'instinct']
}

def find_semantic_group(outcome_name):
    """Find which semantic group this outcome belongs to."""
    outcome_lower = outcome_name.lower()
    for group, keywords in SEMANTIC_PATTERNS.items():
        for keyword in keywords:
            if keyword in outcome_lower:
                return group, keywords
    return None, None

def analyze_for_deletion(program_count, meditation_count, audio_count):
    """Determine if outcome should be deleted based on usage."""
    total_usage = program_count + meditation_count + audio_count

    if total_usage == 0:
        return True, f"Zero usage across all content types (Programs: {program_count}, Meditations: {meditation_count}, Audios: {audio_count}). Not utilized."

    if total_usage <= 2:
        return True, f"Very low usage: {total_usage} total (Programs: {program_count}, Meditations: {meditation_count}, Audios: {audio_count}). Consider removing."

    return False, None

def generate_merge_note(outcome_name, similar_outcomes, primary_outcome):
    """Generate a merge recommendation note."""
    if similar_outcomes:
        similar_list = ', '.join([f"'{o['name']}' (usage: {o['usage']})" for o in similar_outcomes])
        return f"Similar to {similar_list}. Recommend merging into '{primary_outcome}' as the primary outcome."
    return None

def create_analysis_report():
    """Create a structured analysis report."""
    print("\n" + "="*80)
    print("MINDVALLEY OUTCOMES SIMPLIFICATION ANALYSIS")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

    print("\n📋 ANALYSIS APPROACH:")
    print("""
This analysis will:
1. Identify outcomes with zero or very low usage (≤2 total uses)
2. Find semantically similar outcomes that could be merged
3. Recommend keeping the most-used outcome in each semantic group
4. Provide UPDATE TYPE and UPDATE NOTE for each recommendation
    """)

    print("\n🎯 SEMANTIC GROUPS TO CHECK:")
    for i, (group, keywords) in enumerate(SEMANTIC_PATTERNS.items(), 1):
        print(f"  {i:2d}. {group:20s}: {', '.join(keywords[:5])}")
        if len(keywords) > 5:
            print(f"      {' '*20}  {', '.join(keywords[5:])}")

    print("\n📊 UPDATE TYPES:")
    print("  • Deleted - For outcomes with zero or very low usage")
    print("  • Merged  - For outcomes that should be combined with similar outcomes")

    print("\n" + "="*80)

def create_update_template():
    """Create a template for updating Airtable records."""
    template = {
        "instructions": "Use this structure to update outcomes in Airtable",
        "example_updates": [
            {
                "record_id": "rec123456789",
                "fields": {
                    "UPDATE TYPE": "Deleted",
                    "UPDATE NOTE": "Zero usage across programs (0), meditations (0), and audios (0). Not utilized in content."
                }
            },
            {
                "record_id": "rec987654321",
                "fields": {
                    "UPDATE TYPE": "Merged",
                    "UPDATE NOTE": "Similar to 'Stress Relief' (usage: 25). Recommend merging into 'Stress Relief' as the primary outcome."
                }
            }
        ],
        "batch_update_format": {
            "baseId": BASE_ID,
            "tableId": TABLE_ID,
            "records": []
        }
    }

    with open('update_template.json', 'w') as f:
        json.dump(template, f, indent=2)

    print("✅ Created update_template.json")

def main():
    """Main analysis function."""
    print("🚀 Starting Mindvalley Outcomes Analysis...")

    create_analysis_report()
    create_update_template()

    print("\n" + "="*80)
    print("READY FOR MCP-BASED PROCESSING")
    print("="*80)
    print("""
Next Steps:
1. Use Airtable MCP to fetch outcomes in batches
2. Apply analysis logic for each outcome
3. Generate UPDATE TYPE and UPDATE NOTE recommendations
4. Batch update records in Airtable

To proceed, we'll need to:
- Query outcomes sorted by Program Count (ascending)
- Analyze each batch for deletion/merge candidates
- Group by semantic similarity
- Generate update records
    """)

if __name__ == "__main__":
    main()
