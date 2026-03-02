from typing import Dict, List, Tuple

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
    for t in tiers:
        lo, hi = ranges[t]
        if lo > hi:
            print(f"  -> Range invalid for {t}: low > high.")
            return False
    return True

def score_to_tier(score: float, ranges: Dict[str, Tuple[float, float]], tiers: List[str]) -> str:
    for t in tiers:
        lo, hi = ranges[t]
        if lo <= score <= hi:
            return t
    return "Unknown"

def tier_position_ratio(score: float, tier: str, ranges: Dict[str, Tuple[float, float]]) -> float:
    lo, hi = ranges[tier]
    if hi == lo:
        return 0.5
    s = min(max(score, lo), hi)
    return (s - lo) / (hi - lo)

import json

def compute_estimate(
    N: int,
    score: float,
    tiers: List[str],
    ranges: Dict[str, Tuple[float, float]],
    counts: Dict[str, int],
    json_mode: bool = False,
) -> None:
    tier = score_to_tier(score, ranges, tiers)
    if tier == "Unknown":
        print("\nCould not map your score to any tier based on current ranges.")
        return

    higher_count = 0
    for t in tiers:
        if t == tier:
            break
        higher_count += counts.get(t, 0)

    tier_count = counts.get(tier, 0)
    pos = tier_position_ratio(score, tier, ranges)
    ahead_in_tier = (1.0 - pos) * tier_count

    estimated_ahead = higher_count + ahead_in_tier
    estimated_rank = int(round(estimated_ahead + 1))

    if estimated_rank < 1:
        estimated_rank = 1
    if estimated_rank > N:
        estimated_rank = N

    top_percent = (estimated_rank / N) * 100.0
    percentile = 100.0 - top_percent

    if json_mode:
        result = {
            "tier": tier,
            "rank": estimated_rank,
            "class_size": N,
            "top_percent": round(top_percent, 1),
            "percentile": round(percentile, 1),
        }
        print(json.dumps(result, indent=4))
        return

    print("\n===== ESTIMATE =====")
    print(f"Estimated tier: {tier}")
    print(f"Estimated rank: ~{estimated_rank} / {N}")
    print(f"Estimated position: Top {top_percent:.1f}%  (higher is better -> ~{percentile:.1f}th percentile)")
    print("\nBreakdown:")
    print(f"  People in higher tiers: {higher_count}")
    print(f"  People ahead within {tier}: ~{ahead_in_tier:.1f}")
    print("====================\n")
