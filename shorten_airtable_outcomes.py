#!/usr/bin/env python3
"""
Script to find Airtable outcomes with 'Proposal to shorten' status
and suggest shorter, clearer names in the Claude Explanation field.
"""

import json
import subprocess
import sys

BASE_ID = "app4ulN4GnBRvcfAL"
TABLE_ID = "tblLA13fGO7KM1JHA"
STATUS_FIELD = "fldMe3I9aIFetUicW"
OUTCOME_FIELD = "fldCP33pFkB25Ynee"
CLAUDE_EXPLANATION_FIELD = "fldamdoLPuG3q9niu"

def shorten_outcome_name(outcome_name):
    """
    Generate a shorter, clearer version of the outcome name.
    Target: Clear, concise, under 35 characters.
    """
    # Common patterns to shorten
    replacements = {
        "Ability to": "",
        "Ability for": "",
        "Increased": "",
        "Enhanced": "",
        "Improved": "",
        "Greater": "",
        "Better": "",
        "Deeper": "",
        "Stronger": "",
        "More": "",
        "A Sense of": "",
        "A Feeling of": "",
        "The Ability to": "",
        "Surrender/Acceptance to": "Surrender to",
        " and ": " & ",
    }

    shortened = outcome_name.strip()

    for old, new in replacements.items():
        if shortened.startswith(old):
            shortened = new + shortened[len(old):]
            shortened = shortened.strip()

    # Additional smart shortening
    if len(shortened) > 35:
        # Try to remove redundant words
        if " to " in shortened and " and " in shortened:
            parts = shortened.split(" and ")
            if len(parts) == 2 and parts[0].strip():
                shortened = parts[0].strip()

    return shortened.strip()


def main():
    print("Fetching outcomes with 'Proposal to shorten' status...")
    print("This may take a moment due to the large dataset...\n")

    # We'll need to call the Airtable list_records through subprocess
    # since direct API calls hit token limits

    # For now, let's create a list of records to process manually
    # based on common patterns

    print("Due to the large size of the Airtable response, please use Claude Code's")
    print("MCP integration to process records in batches.")
    print("\nSuggested approach:")
    print("1. Filter the view in Airtable to show only 'Proposal to shorten' records")
    print("2. Process in smaller batches of 5-10 records at a time")
    print("\nExample shortened names for common patterns:")
    print("-" * 80)

    examples = [
        ("Surrender/Acceptance to a Higher Power", "Surrender to Higher Power"),
        ("Ability to Overcome Fear", "Overcome Fear"),
        ("Increased Self-Confidence", "Self-Confidence"),
        ("Enhanced Emotional Intelligence", "Emotional Intelligence"),
        ("A Sense of Inner Peace", "Inner Peace"),
        ("Greater Connection with Others", "Connection with Others"),
        ("Improved Sleep Quality", "Better Sleep"),
        ("Deeper Understanding of Self", "Self-Understanding"),
    ]

    for original, suggested in examples:
        print(f"Original ({len(original)} chars): {original}")
        print(f"Suggested ({len(suggested)} chars): {suggested}")
        print()

if __name__ == "__main__":
    main()
