#!/usr/bin/env python3
import csv
import re
from collections import Counter, defaultdict

# Initialize data structures
ratings_intro_spiritual = []
satisfaction_scores = []
nps_scores = []
highlights = []
all_session_ratings = {
    'Quantum Jumping': [],
    'Feng Shui (Marie)': [],
    'Shaolin (Shi Heng Yi)': [],
    'Intro to Spiritual Mastery': [],
    'Q&A': [],
    'Truth Frequency (Regan)': [],
    'Qi Gong (Lee)': []
}

# Read CSV file
csv_file = '/Users/vishen/Downloads/Spiritual Summit 2025_Day1_ Survey.csv'

# Find the data start line
with open(csv_file, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

data_start = 0
for i, line in enumerate(lines):
    if 'User ID,User Name,Email Address' in line:
        data_start = i
        break

# Column indices based on the header
# 9: NPS, 10: Satisfaction, 11: Highlight, 12-18: Session ratings
COL_NPS = 9
COL_SATISFACTION = 10
COL_HIGHLIGHT = 11
COL_QUANTUM = 12
COL_MARIE = 13
COL_SHI = 14
COL_INTRO_SPIRITUAL = 15
COL_QA = 16
COL_REGAN = 17
COL_LEE = 18

# Parse the data
reader = csv.reader(open(csv_file, 'r', encoding='utf-8-sig'))
for i, row in enumerate(reader):
    if i <= data_start:
        continue

    if len(row) < 19:
        continue

    # Skip header row in data section
    if row[0] == '#':
        continue

    # Extract ratings
    try:
        if row[COL_INTRO_SPIRITUAL]:
            ratings_intro_spiritual.append(int(row[COL_INTRO_SPIRITUAL]))
        if row[COL_SATISFACTION]:
            satisfaction_scores.append(int(row[COL_SATISFACTION]))
        if row[COL_NPS]:
            nps_scores.append(int(row[COL_NPS]))
        if row[COL_QUANTUM]:
            all_session_ratings['Quantum Jumping'].append(int(row[COL_QUANTUM]))
        if row[COL_MARIE]:
            all_session_ratings['Feng Shui (Marie)'].append(int(row[COL_MARIE]))
        if row[COL_SHI]:
            all_session_ratings['Shaolin (Shi Heng Yi)'].append(int(row[COL_SHI]))
        if row[COL_QA]:
            all_session_ratings['Q&A'].append(int(row[COL_QA]))
        if row[COL_REGAN]:
            all_session_ratings['Truth Frequency (Regan)'].append(int(row[COL_REGAN]))
        if row[COL_LEE]:
            all_session_ratings['Qi Gong (Lee)'].append(int(row[COL_LEE]))
    except (ValueError, IndexError):
        pass

    # Extract highlights
    if len(row) > COL_HIGHLIGHT and row[COL_HIGHLIGHT]:
        highlights.append(row[COL_HIGHLIGHT])

# Calculate statistics
def avg(lst):
    return sum(lst) / len(lst) if lst else 0

def rating_distribution(ratings):
    dist = Counter(ratings)
    total = len(ratings)
    return {k: (v, v/total*100) for k, v in sorted(dist.items())}

# Print Analysis
print("=" * 80)
print("SPIRITUAL SUMMIT DAY 1 SURVEY ANALYSIS")
print("=" * 80)
print(f"\nTotal Responses: {len(highlights)}")

print("\n" + "=" * 80)
print("1. SESSION RATING ANALYSIS - INTRO TO SPIRITUAL MASTERY")
print("=" * 80)
print(f"Total Ratings: {len(ratings_intro_spiritual)}")
print(f"Average Rating: {avg(ratings_intro_spiritual):.2f} / 5.00")
print("\nRating Distribution:")
dist = rating_distribution(ratings_intro_spiritual)
for rating, (count, pct) in dist.items():
    print(f"  {rating} stars: {count:4d} responses ({pct:5.1f}%)")

low_ratings = [r for r in ratings_intro_spiritual if r <= 2]
print(f"\nLow Ratings (1-2 stars): {len(low_ratings)} ({len(low_ratings)/len(ratings_intro_spiritual)*100:.1f}%)")

print("\n" + "=" * 80)
print("2. COMPARATIVE SESSION RATINGS")
print("=" * 80)
for session, ratings in all_session_ratings.items():
    if ratings:
        print(f"{session:30s}: {avg(ratings):.2f} ({len(ratings)} ratings)")

print("\n" + "=" * 80)
print("3. OVERALL SATISFACTION")
print("=" * 80)
print(f"Average Satisfaction: {avg(satisfaction_scores):.2f} / 5.00")
print(f"Average NPS Score: {avg(nps_scores):.2f} / 10.00")

print("\n" + "=" * 80)
print("4. HIGHLIGHT MENTIONS - SPEAKER/SESSION ANALYSIS")
print("=" * 80)

# Count mentions
vishen_mentions = 0
vishen_quantum = 0
vishen_qa = 0
vishen_spiritual_mastery = 0
regan_mentions = 0
lee_mentions = 0
shi_mentions = 0
marie_mentions = 0

vishen_positive = []
vishen_negative = []

for highlight in highlights:
    h_lower = highlight.lower()

    # Vishen mentions
    if 'vishen' in h_lower:
        vishen_mentions += 1
        if 'quantum' in h_lower:
            vishen_quantum += 1
        if 'q&a' in h_lower or 'question' in h_lower:
            vishen_qa += 1
        if 'spiritual mastery' in h_lower or 'intro to spiritual' in h_lower:
            vishen_spiritual_mastery += 1

    # Other speakers
    if 'regan' in h_lower or 'hillyer' in h_lower:
        regan_mentions += 1
    if 'lee' in h_lower or 'holden' in h_lower or 'qi gong' in h_lower or 'qigong' in h_lower:
        lee_mentions += 1
    if 'shi' in h_lower or 'heng yi' in h_lower or 'shaolin' in h_lower:
        shi_mentions += 1
    if 'marie' in h_lower or 'diamond' in h_lower or 'feng shui' in h_lower:
        marie_mentions += 1

print(f"Vishen (Total): {vishen_mentions}")
print(f"  - Quantum Jumping: {vishen_quantum}")
print(f"  - Q&A Session: {vishen_qa}")
print(f"  - Spiritual Mastery: {vishen_spiritual_mastery}")
print(f"Regan Hillyer: {regan_mentions}")
print(f"Lee Holden (Qi Gong): {lee_mentions}")
print(f"Shi Heng Yi (Shaolin): {shi_mentions}")
print(f"Marie Diamond (Feng Shui): {marie_mentions}")

print("\n" + "=" * 80)
print("5. DETAILED HIGHLIGHT SAMPLES - VISHEN MENTIONS")
print("=" * 80)
vishen_highlights = [h for h in highlights if 'vishen' in h.lower()]
print(f"\nTotal mentions of Vishen in highlights: {len(vishen_highlights)}")
print("\nSample highlights mentioning Vishen (first 30):")
for i, h in enumerate(vishen_highlights[:30], 1):
    print(f"{i}. {h}")

print("\n" + "=" * 80)
print("6. SPIRITUAL MASTERY SPECIFIC MENTIONS")
print("=" * 80)
spiritual_mastery_mentions = [h for h in highlights if 'spiritual mastery' in h.lower() or 'intro to spiritual' in h.lower()]
print(f"Total mentions: {len(spiritual_mastery_mentions)}")
for i, h in enumerate(spiritual_mastery_mentions, 1):
    print(f"{i}. {h}")

print("\n" + "=" * 80)
print("7. NEGATIVE/CRITICAL FEEDBACK PATTERNS")
print("=" * 80)
negative_keywords = ['disappointed', 'confused', 'too much', 'too long', 'boring', 'sales', 'pitch', 'pushy', 'expensive', 'price', 'problem', 'issue', 'technical', 'couldn\'t', 'didn\'t work']
negative_feedback = []
for highlight in highlights:
    h_lower = highlight.lower()
    for keyword in negative_keywords:
        if keyword in h_lower:
            negative_feedback.append(highlight)
            break

print(f"Potentially negative feedback: {len(negative_feedback)}")
for i, h in enumerate(negative_feedback[:50], 1):
    print(f"{i}. {h}")

print("\n" + "=" * 80)
print("8. MOST COMMON POSITIVE THEMES")
print("=" * 80)
positive_keywords = ['love', 'amazing', 'powerful', 'transformative', 'enlightening', 'inspiring', 'grateful', 'beautiful', 'excellent', 'wonderful', 'fantastic', 'incredible', 'breakthrough', 'emotional', 'cried', 'touched', 'resonated']
theme_counts = defaultdict(int)
for highlight in highlights:
    h_lower = highlight.lower()
    for keyword in positive_keywords:
        if keyword in h_lower:
            theme_counts[keyword] += 1

print("Emotion word frequency:")
for word, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {word:20s}: {count}")

print("\n" + "=" * 80)
print("9. TOP MENTIONED SESSIONS IN HIGHLIGHTS")
print("=" * 80)
quantum_in_highlights = sum(1 for h in highlights if 'quantum' in h.lower())
regan_in_highlights = sum(1 for h in highlights if 'regan' in h.lower() or 'truth frequency' in h.lower())
lee_in_highlights = sum(1 for h in highlights if 'lee' in h.lower() or 'qi gong' in h.lower() or 'qigong' in h.lower())
shi_in_highlights = sum(1 for h in highlights if 'shi' in h.lower() or 'shaolin' in h.lower())
marie_in_highlights = sum(1 for h in highlights if 'marie' in h.lower() or 'feng shui' in h.lower())

print(f"Quantum Jumping: {quantum_in_highlights}")
print(f"Regan's Session: {regan_in_highlights}")
print(f"Lee's Qi Gong: {lee_in_highlights}")
print(f"Shi Heng Yi's Shaolin: {shi_in_highlights}")
print(f"Marie's Feng Shui: {marie_in_highlights}")

print("\n" + "=" * 80)
print("10. REGAN HILLYER HIGHLIGHT SAMPLES (Top Performer)")
print("=" * 80)
regan_highlights = [h for h in highlights if 'regan' in h.lower()][:20]
for i, h in enumerate(regan_highlights, 1):
    print(f"{i}. {h}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
