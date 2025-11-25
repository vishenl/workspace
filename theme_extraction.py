#!/usr/bin/env python3
import csv
import re
from collections import Counter

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

COL_HIGHLIGHT = 11

# Extract all highlights
highlights = []
reader = csv.reader(open(csv_file, 'r', encoding='utf-8-sig'))
for i, row in enumerate(reader):
    if i <= data_start:
        continue
    if len(row) < 19:
        continue
    if row[0] == '#':
        continue

    if len(row) > COL_HIGHLIGHT and row[COL_HIGHLIGHT]:
        highlights.append(row[COL_HIGHLIGHT])

print("=" * 80)
print("THEME EXTRACTION - WHAT RESONATED MOST")
print("=" * 80)

# Define themes to track
themes = {
    'quantum_jumping': ['quantum jump', 'quantum travel', 'quantum experience', 'future self', 'spaceship meditation'],
    'activation': ['activation', 'truth frequency', 'energetic', 'frequency'],
    'qi_gong': ['qi gong', 'qigong', 'chi gong', 'energy hands', 'lee holden', 'lee'],
    'shaolin': ['shaolin', 'shi heng yi', 'shi', 'monk', 'inner power'],
    'feng_shui': ['feng shui', 'marie diamond', 'marie', 'space', 'vortex'],
    'practice': ['practice', 'exercise', 'meditation', 'breathing'],
    'transformation': ['transform', 'breakthrough', 'shift', 'change'],
    'energy': ['energy', 'vibration', 'power', 'force'],
    'authenticity': ['authentic', 'true self', 'truth', 'real'],
    'wisdom': ['wisdom', 'insight', 'learning', 'knowledge'],
    'connection': ['connect', 'connection', 'community'],
    'gratitude': ['grateful', 'thank', 'appreciate', 'gratitude'],
}

# Count theme mentions
theme_counts = {theme: 0 for theme in themes}
for highlight in highlights:
    h_lower = highlight.lower()
    for theme, keywords in themes.items():
        if any(keyword in h_lower for keyword in keywords):
            theme_counts[theme] += 1

print("\nTop Themes Mentioned in Highlights:")
for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{theme:20s}: {count:4d} mentions ({count/len(highlights)*100:.1f}%)")

# Extract specific concept mentions
print("\n" + "=" * 80)
print("SPECIFIC CONCEPTS THAT RESONATED")
print("=" * 80)

concepts = {
    'Quantum Jumping Experience': 0,
    'Future Self Visualization': 0,
    'Truth Frequency Activation': 0,
    'Regan\'s Activation': 0,
    'Energy in Hands': 0,
    'Feng Shui Compass': 0,
    'Inner Power/Discipline': 0,
    'Coming Home to Self': 0,
    'Sacred Spaces': 0,
    'Silva Method': 0,
}

for highlight in highlights:
    h_lower = highlight.lower()

    if 'quantum jump' in h_lower or 'quantum travel' in h_lower:
        concepts['Quantum Jumping Experience'] += 1
    if 'future self' in h_lower or 'future me' in h_lower:
        concepts['Future Self Visualization'] += 1
    if 'truth frequency' in h_lower or "regan's activation" in h_lower or 'activation' in h_lower:
        concepts['Truth Frequency Activation'] += 1
    if 'energy' in h_lower and ('hands' in h_lower or 'palm' in h_lower):
        concepts['Energy in Hands'] += 1
    if 'compass' in h_lower:
        concepts['Feng Shui Compass'] += 1
    if 'discipline' in h_lower or 'inner power' in h_lower or 'consistency' in h_lower:
        concepts['Inner Power/Discipline'] += 1
    if 'home to' in h_lower or 'authentic self' in h_lower:
        concepts['Coming Home to Self'] += 1
    if 'sacred' in h_lower or 'vortex' in h_lower:
        concepts['Sacred Spaces'] += 1
    if 'silva' in h_lower:
        concepts['Silva Method'] += 1

print("\nSpecific Teaching Concepts Mentioned:")
for concept, count in sorted(concepts.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f"{concept:30s}: {count:3d} mentions")

# Extract teaching style preferences
print("\n" + "=" * 80)
print("TEACHING STYLE PREFERENCES")
print("=" * 80)

teaching_styles = {
    'Interactive/Experiential': ['practice', 'exercise', 'experience', 'doing', 'movement', 'activity'],
    'Storytelling': ['story', 'stories', 'shared', 'real life'],
    'Wisdom/Philosophy': ['wisdom', 'philosophy', 'insight', 'teaching'],
    'Energy Work': ['activation', 'energy', 'frequency', 'vibration'],
    'Practical/Actionable': ['practical', 'actionable', 'tools', 'techniques', 'how to'],
}

style_counts = {style: 0 for style in teaching_styles}
for highlight in highlights:
    h_lower = highlight.lower()
    for style, keywords in teaching_styles.items():
        if any(keyword in h_lower for keyword in keywords):
            style_counts[style] += 1

print("\nPreferred Teaching Approaches:")
for style, count in sorted(style_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{style:25s}: {count:4d} mentions ({count/len(highlights)*100:.1f}%)")

# Find the most passionate/detailed responses
print("\n" + "=" * 80)
print("MOST DETAILED/PASSIONATE RESPONSES (150+ characters)")
print("=" * 80)

detailed_responses = [h for h in highlights if len(h) > 150]
print(f"\nTotal detailed responses: {len(detailed_responses)} ({len(detailed_responses)/len(highlights)*100:.1f}%)")
print("\nSample detailed responses (first 20):")
for i, h in enumerate(detailed_responses[:20], 1):
    print(f"{i}. {h}\n")

# Look for specific pain points or desires mentioned
print("=" * 80)
print("DESIRED OUTCOMES MENTIONED")
print("=" * 80)

outcomes = {
    'Spiritual Growth': ['spiritual', 'spirituality', 'enlighten', 'awaken'],
    'Self-Discovery': ['discover', 'find myself', 'who i am', 'authentic'],
    'Healing': ['heal', 'healing', 'relief', 'release'],
    'Energy Management': ['energy', 'balance', 'flow', 'alignment'],
    'Purpose/Clarity': ['purpose', 'clarity', 'direction', 'path'],
    'Manifestation': ['manifest', 'create', 'attract'],
    'Peace/Calm': ['peace', 'calm', 'relaxed', 'serenity'],
}

outcome_counts = {outcome: 0 for outcome in outcomes}
for highlight in highlights:
    h_lower = highlight.lower()
    for outcome, keywords in outcomes.items():
        if any(keyword in h_lower for keyword in keywords):
            outcome_counts[outcome] += 1

print("\nDesired Outcomes/Benefits Mentioned:")
for outcome, count in sorted(outcome_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{outcome:25s}: {count:4d} mentions")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
