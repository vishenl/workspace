# Batch Update Process for Airtable Outcomes

## Overview
This document tracks the batch update process for outcomes with "Proposal to shorten" status.

## Process
Since Airtable responses are large, we'll process records in small batches using Claude Code's MCP Airtable integration.

## Script to Use

```python
import subprocess
import json

def shorten_outcome_name(outcome_name: str) -> str:
    """Generate a shorter, clearer version keeping the core meaning."""

    prefixes_to_remove = [
        "Ability to ", "Ability for ", "The Ability to ",
        "Increased ", "Enhanced ", "Improved ", "Greater ",
        "Better ", "Deeper ", "Stronger ", "More ",
        "A Sense of ", "A Feeling of ", "A State of ",
        "The Feeling of ", "An Increased ", "An Enhanced ",
    ]

    shortened = outcome_name.strip()

    for prefix in prefixes_to_remove:
        if shortened.startswith(prefix):
            shortened = shortened[len(prefix):]
            break

    replacements = {
        "Surrender/Acceptance to a": "Surrender to",
        "Surrender/Acceptance to": "Surrender to",
        "Understanding of": "Understanding",
        "Connection with": "Connection to",
        "Awareness of": "Awareness",
        " and ": " & ",
    }

    for old, new in replacements.items():
        shortened = shortened.replace(old, new)

    if len(shortened) > 35 and " & " in shortened:
        parts = shortened.split(" & ")
        if len(parts[0].strip()) > 10:
            shortened = parts[0].strip()

    return shortened.strip()

# Test examples
test_cases = [
    "Surrender/Acceptance to a Higher Power",
    "Ability to Overcome Fear",
    "Increased Self-Confidence",
    "A Sense of Inner Peace",
]

print("Testing shortening logic:\n")
for test in test_cases:
    shortened = shorten_outcome_name(test)
    print(f"Original ({len(test):2d}): {test}")
    print(f"Shortened ({len(shortened):2d}): {shortened}\n")
```

## Next Steps
Claude Code will process records using MCP tools directly.
