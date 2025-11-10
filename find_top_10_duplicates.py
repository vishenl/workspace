#!/usr/bin/env python3
"""
Find Top 10 Duplicate Outcomes in Mindvalley Brain Airtable
Optimized to fetch only essential fields and provide clear deletion candidates
"""

import requests
import os
import time
from difflib import SequenceMatcher
from collections import defaultdict

# Configuration
BASE_ID = "app4ulN4GnBRvcfAL"
TABLE_ID = "tblLA13fGO7KM1JHA"
API_KEY = os.environ.get("AIRTABLE_PERSONAL_ACCESS_TOKEN") or os.environ.get("AIRTABLE_API_KEY")

if not API_KEY:
    print("ERROR: Please set AIRTABLE_PERSONAL_ACCESS_TOKEN or AIRTABLE_API_KEY environment variable")
    print("\nTo set it temporarily, run:")
    print("export AIRTABLE_PERSONAL_ACCESS_TOKEN='your_token_here'")
    exit(1)

def fetch_outcomes():
    """Fetch all outcomes with only essential fields"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Only fetch fields we need for duplicate detection
    params = {
        "fields[]": ["Outcome", "Definition", "Program Count", "Status"],
        "pageSize": 100
    }

    all_records = []
    offset = None

    print("Fetching outcomes from Airtable...")

    while True:
        if offset:
            params["offset"] = offset

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            return None

        data = response.json()
        records = data.get("records", [])

        for record in records:
            fields = record.get("fields", {})
            all_records.append({
                "id": record["id"],
                "outcome": fields.get("Outcome", ""),
                "definition": fields.get("Definition", ""),
                "program_count": fields.get("Program Count", 0) or 0,
                "status": fields.get("Status", "")
            })

        print(f"  Fetched {len(all_records)} outcomes...", end="\r")

        offset = data.get("offset")
        if not offset:
            break

        time.sleep(0.2)  # Rate limiting

    print(f"\nTotal outcomes fetched: {len(all_records)}")
    return all_records

def normalize(text):
    """Normalize text for comparison"""
    if not text:
        return ""
    return text.lower().strip()

def similarity(text1, text2):
    """Calculate similarity ratio between two texts"""
    return SequenceMatcher(None, normalize(text1), normalize(text2)).ratio()

def extract_core_concept(outcome_name):
    """Extract the core concept from outcome name by removing common modifiers"""
    name = normalize(outcome_name)

    # Remove common prefixes
    prefixes = [
        "improving ", "building ", "developing ", "enhancing ", "increasing ",
        "reducing ", "decreasing ", "better ", "improved ", "learning ",
        "mastering ", "achieving ", "creating ", "cultivating ", "discovering ",
        "finding ", "gaining ", "growing ", "practicing ", "strengthening "
    ]

    for prefix in prefixes:
        if name.startswith(prefix):
            name = name[len(prefix):]
            break

    return name

def find_duplicates(outcomes):
    """Find duplicate outcomes using multiple strategies"""
    duplicates = []
    processed = set()

    print("\nAnalyzing for duplicates...")

    # Strategy 1: Exact core concept match
    core_concept_map = defaultdict(list)
    for outcome in outcomes:
        core = extract_core_concept(outcome["outcome"])
        if core:
            core_concept_map[core].append(outcome)

    # Find groups with same core concept
    for core, group in core_concept_map.items():
        if len(group) > 1:
            # Sort by program count (descending) to keep the most used one
            group.sort(key=lambda x: x["program_count"], reverse=True)
            keep = group[0]

            for duplicate in group[1:]:
                if duplicate["id"] not in processed:
                    duplicates.append({
                        "delete_id": duplicate["id"],
                        "delete_name": duplicate["outcome"],
                        "delete_programs": duplicate["program_count"],
                        "keep_name": keep["outcome"],
                        "keep_programs": keep["program_count"],
                        "reason": f"Same core concept: '{core}'",
                        "confidence": 5,
                        "name_sim": similarity(duplicate["outcome"], keep["outcome"]),
                        "def_sim": similarity(duplicate["definition"], keep["definition"])
                    })
                    processed.add(duplicate["id"])

    # Strategy 2: High name similarity with definition similarity
    for i in range(len(outcomes)):
        if outcomes[i]["id"] in processed:
            continue

        for j in range(i + 1, len(outcomes)):
            if outcomes[j]["id"] in processed:
                continue

            o1, o2 = outcomes[i], outcomes[j]

            name_sim = similarity(o1["outcome"], o2["outcome"])
            def_sim = similarity(o1["definition"], o2["definition"])

            # High similarity threshold
            if (name_sim >= 0.80 and def_sim >= 0.60) or def_sim >= 0.85:
                # Keep the one with more programs
                if o1["program_count"] >= o2["program_count"]:
                    keep, delete = o1, o2
                else:
                    keep, delete = o2, o1

                confidence = 5 if (name_sim >= 0.85 or def_sim >= 0.90) else 4

                duplicates.append({
                    "delete_id": delete["id"],
                    "delete_name": delete["outcome"],
                    "delete_programs": delete["program_count"],
                    "keep_name": keep["outcome"],
                    "keep_programs": keep["program_count"],
                    "reason": f"Name {name_sim:.0%} similar, Definition {def_sim:.0%} similar",
                    "confidence": confidence,
                    "name_sim": name_sim,
                    "def_sim": def_sim
                })
                processed.add(delete["id"])

    # Sort by confidence and program count (prefer deleting ones with 0 programs)
    duplicates.sort(key=lambda x: (-x["confidence"], x["delete_programs"], -max(x["name_sim"], x["def_sim"])))

    return duplicates

def print_results(duplicates):
    """Print top 10 duplicates for deletion"""
    print("\n" + "="*80)
    print("TOP 10 OUTCOMES TO DELETE (DUPLICATES)")
    print("="*80)

    if not duplicates:
        print("\nNo clear duplicates found!")
        return

    top_10 = duplicates[:10]

    for idx, dup in enumerate(top_10, 1):
        print(f"\n{idx}. DELETE: {dup['delete_id']}")
        print(f"   Outcome: \"{dup['delete_name']}\" ({dup['delete_programs']} programs)")
        print(f"   Reason:  {dup['reason']}")
        print(f"   Keep Instead: \"{dup['keep_name']}\" ({dup['keep_programs']} programs)")
        print(f"   Confidence: {dup['confidence']}/5")

    print("\n" + "="*80)
    print(f"Total duplicates found: {len(duplicates)}")
    print("="*80)

    # Print IDs for easy deletion
    print("\nRecord IDs to delete (copy-paste ready):")
    print(",".join([dup['delete_id'] for dup in top_10]))

    # Summary by confidence
    conf_counts = defaultdict(int)
    for dup in duplicates:
        conf_counts[dup["confidence"]] += 1

    print("\nConfidence Distribution:")
    for conf in sorted(conf_counts.keys(), reverse=True):
        print(f"  Confidence {conf}: {conf_counts[conf]} duplicates")

def main():
    print("="*80)
    print("MINDVALLEY BRAIN OUTCOME DUPLICATE FINDER")
    print("="*80)

    outcomes = fetch_outcomes()

    if not outcomes:
        print("Failed to fetch outcomes!")
        return

    duplicates = find_duplicates(outcomes)
    print_results(duplicates)

    print("\n✓ Analysis complete!")
    print("\nNext steps:")
    print("1. Review the top 10 duplicates above")
    print("2. Verify each one in Airtable before deleting")
    print("3. Delete the outcomes with 0 programs first (safest)")

if __name__ == "__main__":
    main()
