#!/usr/bin/env python3
"""
Analyze Mindvalley Outcomes for consolidation opportunities
Uses Airtable API to fetch outcomes with minimal data
"""

import os
import json
from typing import List, Dict
import requests

BASE_ID = 'app4ulN4GnBRvcfAL'
TABLE_ID = 'tblLA13fGO7KM1JHA'

# Get API key from environment
api_key = os.environ.get('AIRTABLE_API_KEY')
if not api_key:
    # Try to get from Airtable MCP configuration
    print("Warning: AIRTABLE_API_KEY not found in environment")

def fetch_outcomes_minimal():
    """Fetch outcomes with only essential fields to minimize data transfer"""

    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Request only specific fields to reduce payload
    params = {
        "fields[]": ["Outcome", "Definition", "Status", "Program Count"],
        "pageSize": 100  # Maximum allowed by Airtable
    }

    all_outcomes = []
    offset = None

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
            all_outcomes.append({
                'id': record['id'],
                'name': fields.get('Outcome', ''),
                'definition': fields.get('Definition', ''),
                'status': fields.get('Status', ''),
                'program_count': fields.get('Program Count', 0)
            })

        # Check if there are more pages
        offset = data.get('offset')
        if not offset:
            break

        print(f"Fetched {len(all_outcomes)} outcomes so far...")

    return all_outcomes

def find_semantic_overlaps(outcomes: List[Dict]) -> List[Dict]:
    """Identify outcomes with semantic similarities"""

    recommendations = []

    # Group outcomes by keywords for initial analysis
    keyword_groups = {}

    for outcome in outcomes:
        name = outcome['name'].lower()
        definition = (outcome['definition'] or '').lower()

        # Extract key concepts
        keywords = []

        # Common concepts to group by
        concepts = {
            'sleep': ['sleep', 'rest', 'insomnia'],
            'confidence': ['confidence', 'self-esteem', 'self-worth'],
            'focus': ['focus', 'concentration', 'attention'],
            'stress': ['stress', 'anxiety', 'calm', 'relax'],
            'energy': ['energy', 'vitality', 'vigor'],
            'relationship': ['relationship', 'connection', 'intimacy'],
            'creativity': ['creative', 'creativity', 'innovation'],
            'productivity': ['productivity', 'efficiency', 'performance'],
            'health': ['health', 'wellness', 'wellbeing'],
            'wealth': ['wealth', 'money', 'financial', 'abundance'],
            'spiritual': ['spiritual', 'spirit', 'soul', 'divine'],
            'body': ['body', 'physical', 'fitness'],
            'mind': ['mind', 'mental', 'cognitive'],
            'learning': ['learn', 'education', 'knowledge'],
            'leadership': ['leader', 'leadership', 'influence'],
        }

        for concept, terms in concepts.items():
            if any(term in name or term in definition for term in terms):
                keywords.append(concept)

        for keyword in keywords:
            if keyword not in keyword_groups:
                keyword_groups[keyword] = []
            keyword_groups[keyword].append(outcome)

    # Analyze groups with multiple outcomes
    for concept, group in keyword_groups.items():
        if len(group) >= 2:
            # Sort by program count (ascending) to prioritize merging low-usage outcomes
            group.sort(key=lambda x: x['program_count'])

            # Look for very similar outcomes
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    outcome1 = group[i]
                    outcome2 = group[j]

                    name1 = outcome1['name'].lower()
                    name2 = outcome2['name'].lower()

                    # Check for high similarity
                    similarity_score = calculate_similarity(name1, name2)

                    if similarity_score > 0.6:  # High similarity threshold
                        recommendations.append({
                            'merge_group': [outcome1['name'], outcome2['name']],
                            'primary_outcome': outcome2['name'] if outcome2['program_count'] >= outcome1['program_count'] else outcome1['name'],
                            'rationale': f"High semantic similarity in {concept} domain (score: {similarity_score:.2f})",
                            'confidence': 'high' if similarity_score > 0.8 else 'medium',
                            'program_impact': f"{outcome1['program_count'] + outcome2['program_count']} programs total",
                            'estimated_impact': f"Consolidating '{outcome1['name']}' into '{outcome2['name']}'"
                        })

    return recommendations

def calculate_similarity(str1: str, str2: str) -> float:
    """Simple word overlap similarity score"""
    words1 = set(str1.split())
    words2 = set(str2.split())

    if not words1 or not words2:
        return 0.0

    intersection = words1.intersection(words2)
    union = words1.union(words2)

    return len(intersection) / len(union)

def main():
    print("Fetching outcomes from Airtable...")
    outcomes = fetch_outcomes_minimal()

    print(f"\nTotal outcomes: {len(outcomes)}\n")

    # Output all outcomes for review
    print("=== ALL OUTCOMES ===")
    for i, outcome in enumerate(sorted(outcomes, key=lambda x: x['name']), 1):
        print(f"{i}. {outcome['name']} (Programs: {outcome['program_count']}, Status: {outcome['status']})")

    print("\n\n=== FINDING DUPLICATES ===\n")
    recommendations = find_semantic_overlaps(outcomes)

    # Output analysis
    result = {
        "total_outcomes_analyzed": len(outcomes),
        "consolidation_recommendations": recommendations[:60],  # Limit to target ~60
        "total_outcomes_to_remove": min(len(recommendations), 60),
        "reduction_percentage": (min(len(recommendations), 60) / len(outcomes)) * 100 if outcomes else 0,
        "summary": f"Identified {len(recommendations)} potential consolidation opportunities based on semantic similarity analysis"
    }

    # Save to file
    with open('outcomes_analysis.json', 'w') as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
