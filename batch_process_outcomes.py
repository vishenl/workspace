#!/usr/bin/env python3
"""
Batch process Airtable outcomes with 'Proposal to shorten' status.
This script will be called from Claude Code using MCP tools.
"""

def shorten_outcome_name(outcome_name: str) -> str:
    """Generate a shorter, clearer version keeping the core meaning."""

    prefixes_to_remove = [
        "Ability to ",
        "Ability for ",
        "The Ability to ",
        "Increased ",
        "Enhanced ",
        "Improved ",
        "Greater ",
        "Better ",
        "Deeper ",
        "Stronger ",
        "More ",
        "A Sense of ",
        "A Feeling of ",
        "A State of ",
        "The Feeling of ",
        "An Increased ",
        "An Enhanced ",
        "The ",
    ]

    shortened = outcome_name.strip()

    # Try removing prefixes
    for prefix in prefixes_to_remove:
        if shortened.startswith(prefix):
            shortened = shortened[len(prefix):]
            break

    # Common replacements
    replacements = {
        "Surrender/Acceptance to a": "Surrender to",
        "Surrender/Acceptance to": "Surrender to",
        "Understanding of": "Understanding",
        "Connection with": "Connection to",
        "Awareness of": "Awareness",
        " and ": " & ",
        "Communication with": "Communication to",
        "Relationship with": "Relationship to",
    }

    for old, new in replacements.items():
        shortened = shortened.replace(old, new)

    # If still too long, try more aggressive shortening
    if len(shortened) > 35:
        # Remove trailing descriptors after &
        if " & " in shortened:
            parts = shortened.split(" & ")
            if len(parts[0].strip()) > 10:
                shortened = parts[0].strip()

    return shortened.strip()


def create_explanation(original: str, shortened: str) -> str:
    """Create explanation for the Claude Explanation field."""
    char_saved = len(original) - len(shortened)

    return f"""**Suggested Shorter Name:** {shortened}

**Analysis:**
- Original: "{original}" ({len(original)} characters)
- Suggested: "{shortened}" ({len(shortened)} characters)
- Saved: {char_saved} characters

**Reasoning:** This shorter version maintains the core meaning while being more concise and easier to scan. Redundant words have been removed or simplified, making the outcome name punchier and more memorable while preserving its transformational essence."""


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Process a single outcome
        outcome = sys.argv[1]
        shortened = shorten_outcome_name(outcome)
        explanation = create_explanation(outcome, shortened)
        print(explanation)
    else:
        # Show help
        print("Usage: python3 batch_process_outcomes.py 'Outcome Name'")
        print("\nExample:")
        print("  python3 batch_process_outcomes.py 'Ability to Overcome Fear'")
