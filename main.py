#!/usr/bin/env python3
"""
Class Percentile & Letter-Grade Estimator
- Uses grade tiers (A+, A, A-, ..., F) + tier score ranges + tier headcounts
- Estimates your percentile and tier based on your estimated score
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


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


def ask_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
    while True:
        s = input(prompt).strip()
        try:
            val = int(s)
            if min_val is not None and val < min_val:
                print(f"  -> Must be >= {min_val}. Try again.")
                continue
            if max_val is not None and val > max_val:
                print(f"  -> Must be <= {max_val}. Try again.")
                continue
            return val
        except ValueError:
            print("  -> Please enter an integer. Try again.")


def ask_float(prompt: str, min_val: float = None, max_val: float = None) -> float:
    while True:
        s = input(prompt).strip()
        try:
            val = float(s)
            if min_val is not None and val < min_val:
                print(f"  -> Must be >= {min_val}. Try again.")
                continue
            if max_val is not None and val > max_val:
                print(f"  -> Must be <= {max_val}. Try again.")
                continue
            return val
        except ValueError:
            print("  -> Please enter a number. Try again.")


def ask_yes_no(prompt: str) -> bool:
    while True:
        s = input(prompt + " (y/n): ").strip().lower()
        if s in ("y", "yes"):
            return True
        if s in ("n", "no"):
            return False
        print("  -> Please type y or n.")


def pretty_ranges(ranges: Dict[str, Tuple[float, float]], tiers: List[str]) -> None:
    for t in tiers:
        lo, hi = ranges[t]
        print(f"  {t:>2}: {lo:g}–{hi:g}")


def validate_ranges(ranges: Dict[str, Tuple[float, float]], tiers: List[str]) -> bool:
    # Basic sanity checks: each lo <= hi, and cover 0..100 (not strictly required but recommended)
    for t in tiers:
        lo, hi = ranges[t]
        if lo > hi:
            print(f"  -> Range invalid for {t}: low > high.")
            return False
    return True


def score_to_tier(score: float, ranges: Dict[str, Tuple[float, float]], tiers: List[str]) -> str:
    # Prefer highest tier if overlapping exists
    for t in tiers:
        lo, hi = ranges[t]
        if lo <= score <= hi:
            return t
    # If not in any tier, find closest by boundary
    # But usually shouldn't happen if ranges cover 0..100
    return "Unknown"


def tier_position_ratio(score: float, tier: str, ranges: Dict[str, Tuple[float, float]]) -> float:
    """
    Return position inside the tier from 0 to 1:
      0 = at the bottom of tier, 1 = at the top of tier
    """
    lo, hi = ranges[tier]
    if hi == lo:
        return 0.5
    # clamp score into [lo, hi] so it doesn't break
    s = min(max(score, lo), hi)
    return (s - lo) / (hi - lo)


def compute_estimate(
    N: int,
    score: float,
    tiers: List[str],
    ranges: Dict[str, Tuple[float, float]],
    counts: Dict[str, int],
) -> None:
    tier = score_to_tier(score, ranges, tiers)
    if tier == "Unknown":
        print("\nCould not map your score to any tier based on current ranges.")
        return

    # Count strictly higher tiers (tiers list is ordered from best to worst)
    higher_count = 0
    for t in tiers:
        if t == tier:
            break
        higher_count += counts.get(t, 0)

    tier_count = counts.get(tier, 0)
    pos = tier_position_ratio(score, tier, ranges)  # 0..1 inside tier
    # People ahead inside same tier: those closer to top. Approx (1 - pos) * tier_count
    ahead_in_tier = (1.0 - pos) * tier_count

    estimated_ahead = higher_count + ahead_in_tier
    estimated_rank = int(round(estimated_ahead + 1))

    # clamp rank to [1, N]
    if estimated_rank < 1:
        estimated_rank = 1
    if estimated_rank > N:
        estimated_rank = N

    # "Top X%" where smaller is better
    top_percent = (estimated_rank / N) * 100.0

    # Also show percentile (0..100 where higher is better): 100 - top%
    percentile = 100.0 - top_percent

    print("\n===== ESTIMATE =====")
    print(f"Estimated tier: {tier}")
    print(f"Estimated rank: ~{estimated_rank} / {N}")
    print(f"Estimated position: Top {top_percent:.1f}%  (higher is better -> ~{percentile:.1f}th percentile)")
    print("\nBreakdown:")
    print(f"  People in higher tiers: {higher_count}")
    print(f"  People ahead within {tier}: ~{ahead_in_tier:.1f} (based on your score within the tier range)")
    print("====================\n")


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
