#!/usr/bin/env python3
"""
Class Percentile & Letter-Grade Estimator

A command-line tool that estimates a student's letter grade,
approximate class rank, top percentage, and percentile standing
based on class grade distribution data.
"""

from typing import Dict, List, Tuple

from utils import (
    ask_int,
    ask_float,
    ask_yes_no,
    pretty_ranges,
    validate_ranges,
    compute_estimate,
)


DEFAULT_TIERS: List[str] = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]

DEFAULT_RANGES: Dict[str, Tuple[float, float]] = {
    "A+": (95, 100),
    "A": (90, 94),
    "A-": (85, 89),
    "B+": (80, 84),
    "B": (75, 79),
    "B-": (70, 74),
    "C+": (65, 69),
    "C": (60, 64),
    "C-": (55, 59),
    "D": (50, 54),
    "F": (0, 49),
}


def main() -> None:
    print("Class Percentile & Letter-Grade Estimator\n")

    tiers = DEFAULT_TIERS.copy()

    print("Default grade tiers, from highest to lowest:")
    print("  " + ", ".join(tiers))

    if ask_yes_no("Do you want to modify the tier list?"):
        print("\nEnter tiers from highest to lowest, separated by commas.")
        print("Example: A+,A,A-,B+,B,B-,C+,C,C-,D,F")

        while True:
            raw = input("Tiers: ").strip()
            new_tiers = [tier.strip() for tier in raw.split(",") if tier.strip()]

            if len(new_tiers) < 2:
                print("  -> Please provide at least 2 tiers.")
                continue

            tiers = new_tiers
            break

    ranges = {tier: DEFAULT_RANGES.get(tier, (0, 0)) for tier in tiers}

    print("\nDefault score ranges:")
    pretty_ranges(ranges, tiers)

    if ask_yes_no("Do you want to edit score ranges for tiers?"):
        print("\nEnter a low and high score for each tier.")
        print("Example: low = 85, high = 89")

        for tier in tiers:
            low = ask_float(f"  {tier} low: ", min_val=0, max_val=100)
            high = ask_float(f"  {tier} high: ", min_val=0, max_val=100)
            ranges[tier] = (low, high)

    if not validate_ranges(ranges, tiers):
        print("\nRanges are invalid. Please re-run the program and fix them.")
        return

    print("\nEnter the class size and the number of students in each tier.")
    class_size = ask_int("Class size (N): ", min_val=1)

    counts: Dict[str, int] = {}
    total_count = 0

    for tier in tiers:
        count = ask_int(f"Count in {tier}: ", min_val=0)
        counts[tier] = count
        total_count += count

    if total_count != class_size:
        print(f"\nWarning: tier counts add up to {total_count}, but class size is {class_size}.")
        if not ask_yes_no("Continue anyway?"):
            print("Stopped. Please re-run the program and fix the class size or tier counts.")
            return

    score = ask_float("\nYour estimated score (0-100): ", min_val=0, max_val=100)

    compute_estimate(
        N=class_size,
        score=score,
        tiers=tiers,
        ranges=ranges,
        counts=counts,
    )

    print("Tip: For better accuracy, use the official grade cutoffs from your syllabus.\n")


if __name__ == "__main__":
    main()
