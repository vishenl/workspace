#!/usr/bin/env python3
import csv

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

# Column indices
COL_NPS = 9
COL_SATISFACTION = 10
COL_HIGHLIGHT = 11
COL_QUANTUM = 12
COL_INTRO_SPIRITUAL = 15

# Parse data to find correlations
low_spiritual_mastery_ratings = []
high_spiritual_mastery_ratings = []

reader = csv.reader(open(csv_file, 'r', encoding='utf-8-sig'))
for i, row in enumerate(reader):
    if i <= data_start:
        continue
    if len(row) < 19:
        continue
    if row[0] == '#':
        continue

    try:
        spiritual_rating = int(row[COL_INTRO_SPIRITUAL]) if row[COL_INTRO_SPIRITUAL] else None
        satisfaction = int(row[COL_SATISFACTION]) if row[COL_SATISFACTION] else None
        nps = int(row[COL_NPS]) if row[COL_NPS] else None
        quantum_rating = int(row[COL_QUANTUM]) if row[COL_QUANTUM] else None
        highlight = row[COL_HIGHLIGHT] if len(row) > COL_HIGHLIGHT else ""

        if spiritual_rating:
            record = {
                'spiritual_rating': spiritual_rating,
                'satisfaction': satisfaction,
                'nps': nps,
                'quantum_rating': quantum_rating,
                'highlight': highlight
            }

            if spiritual_rating <= 2:
                low_spiritual_mastery_ratings.append(record)
            elif spiritual_rating == 5:
                high_spiritual_mastery_ratings.append(record)
    except (ValueError, IndexError):
        pass

print("=" * 80)
print("SPIRITUAL MASTERY PITCH DEEP DIVE")
print("=" * 80)

print("\n" + "=" * 80)
print("1. LOW RATINGS ANALYSIS (1-2 stars for Intro to Spiritual Mastery)")
print("=" * 80)
print(f"Total Low Ratings: {len(low_spiritual_mastery_ratings)}")

if low_spiritual_mastery_ratings:
    avg_satisfaction_low = sum(r['satisfaction'] for r in low_spiritual_mastery_ratings if r['satisfaction']) / len([r for r in low_spiritual_mastery_ratings if r['satisfaction']])
    avg_nps_low = sum(r['nps'] for r in low_spiritual_mastery_ratings if r['nps']) / len([r for r in low_spiritual_mastery_ratings if r['nps']])
    print(f"\nAverage Overall Satisfaction: {avg_satisfaction_low:.2f} / 5.00")
    print(f"Average NPS: {avg_nps_low:.2f} / 10.00")

    print("\nHighlights from people who rated Spiritual Mastery low:")
    for i, record in enumerate(low_spiritual_mastery_ratings, 1):
        if record['highlight']:
            print(f"{i}. [{record['spiritual_rating']}★] {record['highlight']}")

print("\n" + "=" * 80)
print("2. MID-RANGE RATINGS ANALYSIS (3 stars for Intro to Spiritual Mastery)")
print("=" * 80)

mid_ratings = []
reader = csv.reader(open(csv_file, 'r', encoding='utf-8-sig'))
for i, row in enumerate(reader):
    if i <= data_start:
        continue
    if len(row) < 19:
        continue
    if row[0] == '#':
        continue

    try:
        spiritual_rating = int(row[COL_INTRO_SPIRITUAL]) if row[COL_INTRO_SPIRITUAL] else None
        highlight = row[COL_HIGHLIGHT] if len(row) > COL_HIGHLIGHT else ""

        if spiritual_rating == 3 and highlight:
            mid_ratings.append({
                'spiritual_rating': spiritual_rating,
                'highlight': highlight
            })
    except (ValueError, IndexError):
        pass

print(f"Total 3-star Ratings: {len(mid_ratings)}")
print("\nSample highlights from 3-star raters (first 30):")
for i, record in enumerate(mid_ratings[:30], 1):
    print(f"{i}. {record['highlight']}")

print("\n" + "=" * 80)
print("3. SALES PITCH MENTIONS")
print("=" * 80)

sales_mentions = []
reader = csv.reader(open(csv_file, 'r', encoding='utf-8-sig'))
for i, row in enumerate(reader):
    if i <= data_start:
        continue
    if len(row) < 19:
        continue
    if row[0] == '#':
        continue

    try:
        highlight = row[COL_HIGHLIGHT] if len(row) > COL_HIGHLIGHT else ""
        spiritual_rating = int(row[COL_INTRO_SPIRITUAL]) if row[COL_INTRO_SPIRITUAL] else None

        if highlight and ('sales' in highlight.lower() or 'pitch' in highlight.lower() or 'sell' in highlight.lower() or '$' in highlight or 'price' in highlight.lower() or 'expensive' in highlight.lower()):
            sales_mentions.append({
                'spiritual_rating': spiritual_rating,
                'highlight': highlight
            })
    except (ValueError, IndexError):
        pass

print(f"Total mentions of sales/pricing: {len(sales_mentions)}")
for i, record in enumerate(sales_mentions, 1):
    rating_str = f"[{record['spiritual_rating']}★]" if record['spiritual_rating'] else "[No rating]"
    print(f"{i}. {rating_str} {record['highlight']}")

print("\n" + "=" * 80)
print("4. QUANTUM JUMPING VS SPIRITUAL MASTERY COMPARISON")
print("=" * 80)

quantum_better = 0
spiritual_better = 0
tied = 0

reader = csv.reader(open(csv_file, 'r', encoding='utf-8-sig'))
for i, row in enumerate(reader):
    if i <= data_start:
        continue
    if len(row) < 19:
        continue
    if row[0] == '#':
        continue

    try:
        spiritual_rating = int(row[COL_INTRO_SPIRITUAL]) if row[COL_INTRO_SPIRITUAL] else None
        quantum_rating = int(row[COL_QUANTUM]) if row[COL_QUANTUM] else None

        if spiritual_rating and quantum_rating:
            if quantum_rating > spiritual_rating:
                quantum_better += 1
            elif spiritual_rating > quantum_rating:
                spiritual_better += 1
            else:
                tied += 1
    except (ValueError, IndexError):
        pass

total_comparisons = quantum_better + spiritual_better + tied
print(f"Total comparable ratings: {total_comparisons}")
print(f"\nQuantum Jumping rated higher: {quantum_better} ({quantum_better/total_comparisons*100:.1f}%)")
print(f"Spiritual Mastery rated higher: {spiritual_better} ({spiritual_better/total_comparisons*100:.1f}%)")
print(f"Tied: {tied} ({tied/total_comparisons*100:.1f}%)")

print("\n" + "=" * 80)
print("5. HIGH ENGAGEMENT INDICATORS")
print("=" * 80)

emotional_responses = []
reader = csv.reader(open(csv_file, 'r', encoding='utf-8-sig'))
for i, row in enumerate(reader):
    if i <= data_start:
        continue
    if len(row) < 19:
        continue
    if row[0] == '#':
        continue

    try:
        highlight = row[COL_HIGHLIGHT] if len(row) > COL_HIGHLIGHT else ""
        spiritual_rating = int(row[COL_INTRO_SPIRITUAL]) if row[COL_INTRO_SPIRITUAL] else None

        emotional_keywords = ['cried', 'tears', 'emotional', 'touched', 'moved', 'powerful', 'transformative', 'breakthrough', 'profound']

        if highlight and any(keyword in highlight.lower() for keyword in emotional_keywords):
            if 'vishen' in highlight.lower() or 'quantum' in highlight.lower():
                emotional_responses.append({
                    'spiritual_rating': spiritual_rating,
                    'highlight': highlight
                })
    except (ValueError, IndexError):
        pass

print(f"Emotional/transformative responses mentioning Vishen: {len(emotional_responses)}")
print("\nSamples:")
for i, record in enumerate(emotional_responses[:20], 1):
    rating_str = f"[{record['spiritual_rating']}★]" if record['spiritual_rating'] else "[No rating]"
    print(f"{i}. {rating_str} {record['highlight']}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
