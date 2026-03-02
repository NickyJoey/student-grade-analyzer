#!/usr/bin/env python3
"""
Class Percentile & Letter-Grade Estimator
- Uses grade tiers (A+, A, A-, ..., F) + tier score ranges + tier headcounts
- Estimates your percentile and tier based on your estimated score
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

# Default score ranges (editable at runtime)
# Format: tier -> (low_inclusive, high_inclusive)
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

    # 1) Confirm tiers (editable by user)
    tiers = DEFAULT_TIERS.copy()
    print("Default grade tiers (from highest to lowest):")
    print("  " + ", ".join(tiers))
    if ask_yes_no("Do you want to modify the tier list?"):
        print("Enter tiers in order from highest to lowest, separated by commas.")
        print("Example: A+,A,A-,B+,B,B-,C+,C,C-,D,F")
        while True:
            raw = input("Tiers: ").strip()
            new_tiers = [x.strip() for x in raw.split(",") if x.strip()]
            if len(new_tiers) < 2:
                print("  -> Please provide at least 2 tiers.")
                continue
            tiers = new_tiers
            break

    # 2) Confirm score ranges (editable)
    ranges = {t: DEFAULT_RANGES.get(t, (0, 0)) for t in tiers}

    print("\nDefault score ranges (you can edit):")
    pretty_ranges(ranges, tiers)

    if ask_yes_no("Do you want to edit score ranges for tiers?"):
        print("Enter low/high for each tier. (Example: low=85 high=89)")
        for t in tiers:
            lo = ask_float(f"  {t} low: ", min_val=0, max_val=100)
            hi = ask_float(f"  {t} high: ", min_val=0, max_val=100)
            ranges[t] = (lo, hi)

    if not validate_ranges(ranges, tiers):
        print("Ranges are invalid. Please re-run and fix them.")
        return

    # 3) Class size
    print("\nNow enter class size and headcounts for each tier.")
    N = ask_int("Class size (N): ", min_val=1)

    # 4) Counts per tier
    counts: Dict[str, int] = {}
    total = 0
    for t in tiers:
        c = ask_int(f"Count in {t}: ", min_val=0)
        counts[t] = c
        total += c

    if total != N:
        print(f"\n⚠️ Heads up: counts sum to {total}, but class size N is {N}.")
        if not ask_yes_no("Continue anyway? (It will still estimate using N for percentages)"):
            print("Okay — re-run and fix the counts so they sum to N.")
            return

    # 5) Your estimated score
    score = ask_float("\nYour estimated score (0–100): ", min_val=0, max_val=100)

    compute_estimate(N=N, score=score, tiers=tiers, ranges=ranges, counts=counts)

    print("Tip: If you want more accuracy, make tier ranges match your syllabus/grade cutoffs.\n")


if __name__ == "__main__":
    main()
