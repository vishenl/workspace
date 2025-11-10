#!/usr/bin/env python3
"""
Process Airtable outcomes with 'Proposal to shorten' status.
Updates Claude Explanation field with shortening suggestions.
"""

def shorten_outcome_name(outcome_name):
    """Generate a shorter, clearer version keeping the core meaning."""

    # Remove common prefixes that add length without much value
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
        "Understanding of": "Understanding",
        "Connection with": "Connection to",
        "Awareness of": "Awareness",
        " and ": " & ",
        "Communication": "Comm.",
    }

    for old, new in replacements.items():
        shortened = shortened.replace(old, new)

    return shortened.strip()


def create_explanation(original, shortened):
    """Create explanation for the Claude Explanation field."""
    return f"**Suggested shorter name:** {shortened}\n\n**Original:** {original} ({len(original)} chars)\n**Shortened:** {shortened} ({len(shortened)} chars)\n\nThis shorter version maintains the core meaning while being more concise and easier to scan."


# Test with the example we saw
if __name__ == "__main__":
    test_cases = [
        "Surrender/Acceptance to a Higher Power",
        "Ability to Overcome Fear and Anxiety",
        "Increased Self-Confidence and Self-Esteem",
        "Enhanced Emotional Intelligence",
        "A Sense of Inner Peace and Calm",
        "Greater Connection with Nature",
        "Improved Sleep Quality and Duration",
        "Deeper Understanding of Self and Purpose",
        "The Ability to Forgive and Let Go",
        "An Enhanced Sense of Gratitude",
    ]

    print("Example shortenings:\n")
    print("=" * 80)

    for original in test_cases:
        shortened = shorten_outcome_name(original)
        if len(shortened) <= 35:
            status = "✓"
        else:
            status = "⚠"

        print(f"\n{status} Original ({len(original):2d}): {original}")
        print(f"  Shortened ({len(shortened):2d}): {shortened}")

    print("\n" + "=" * 80)
    print(f"\n✓ = Under 35 characters")
    print(f"⚠ = Still over 35 characters (needs manual review)")
