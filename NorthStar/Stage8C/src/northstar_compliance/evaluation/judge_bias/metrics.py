from __future__ import annotations

import math
import random
from collections import Counter
from statistics import mean
from typing import Iterable, Sequence

POSITIVE = {"pass"}


def _check_prob(x: float) -> None:
    if not (0.0 <= x <= 1.0):
        raise ValueError("probability outside [0,1]")


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total <= 0 or successes < 0 or successes > total:
        raise ValueError("invalid binomial counts")
    p = successes / total
    denom = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denom
    radius = z * math.sqrt((p * (1 - p) + z * z / (4 * total)) / total) / denom
    return max(0.0, centre - radius), min(1.0, centre + radius)


def bootstrap_mean_ci(values: Sequence[float], seed: int = 1701, iterations: int = 2000, alpha: float = 0.05) -> tuple[float, float]:
    if not values:
        raise ValueError("values required")
    if iterations < 100:
        raise ValueError("iterations must be >= 100")
    rng = random.Random(seed)
    n = len(values)
    sims = sorted(mean(values[rng.randrange(n)] for _ in range(n)) for _ in range(iterations))
    lo = sims[int((alpha / 2) * iterations)]
    hi = sims[min(iterations - 1, int((1 - alpha / 2) * iterations))]
    return lo, hi


def exact_mcnemar_p(b: int, c: int) -> float:
    """Two-sided exact McNemar/sign-test p-value for discordant matched pairs."""
    if b < 0 or c < 0:
        raise ValueError("counts must be non-negative")
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def _majority(labels: Sequence[str]) -> str:
    if not labels:
        return "abstain"
    counts = Counter(labels)
    best = counts.most_common()
    if len(best) > 1 and best[0][1] == best[1][1]:
        return "abstain"
    return best[0][0]


def binary_pair_metrics(rows: Sequence[dict]) -> dict[str, float | int]:
    grouped: dict[str, dict[str, list[dict]]] = {}
    for row in rows:
        grouped.setdefault(row["pair_id"], {}).setdefault(row["variant"], []).append(row)
    pairs = []
    score_deltas = []
    for pair_id, variants in grouped.items():
        if set(variants) != {"control", "treatment"}:
            continue
        c = _majority([r["observed_label"] for r in variants["control"]])
        t = _majority([r["observed_label"] for r in variants["treatment"]])
        c_scores = [r["score"] for r in variants["control"] if r.get("score") is not None]
        t_scores = [r["score"] for r in variants["treatment"] if r.get("score") is not None]
        if c_scores and t_scores:
            score_deltas.append(mean(t_scores) - mean(c_scores))
        pairs.append((c, t))
    if not pairs:
        raise ValueError("no complete pairs")
    n = len(pairs)
    c_pos = sum(c in POSITIVE for c, _ in pairs) / n
    t_pos = sum(t in POSITIVE for _, t in pairs) / n
    flips = sum(c != t for c, t in pairs)
    b = sum(c in POSITIVE and t not in POSITIVE for c, t in pairs)
    c_count = sum(c not in POSITIVE and t in POSITIVE for c, t in pairs)
    deltas = [int(t in POSITIVE) - int(c in POSITIVE) for c, t in pairs]
    ci_low, ci_high = bootstrap_mean_ci(deltas, iterations=1000)
    return {
        "n_pairs": n,
        "control_positive_rate": c_pos,
        "treatment_positive_rate": t_pos,
        "paired_delta": t_pos - c_pos,
        "flip_rate": flips / n,
        "directional_flip_rate": (c_count - b) / n,
        "score_delta": mean(score_deltas) if score_deltas else 0.0,
        "score_abs_delta": mean(abs(v) for v in score_deltas) if score_deltas else 0.0,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "mcnemar_p": exact_mcnemar_p(b, c_count),
    }


def central_tendency_metrics(scores: Sequence[int], expected_scores: Sequence[int], middle: set[int] = {3}) -> dict[str, float]:
    if not scores or len(scores) != len(expected_scores):
        raise ValueError("aligned scores required")
    n = len(scores)
    middle_rate = sum(s in middle for s in scores) / n
    expected_extreme = [i for i, e in enumerate(expected_scores) if e in {1, 5}]
    tail_recall = (
        sum(scores[i] == expected_scores[i] for i in expected_extreme) / len(expected_extreme)
        if expected_extreme else 1.0
    )
    obs_range = max(scores) - min(scores)
    exp_range = max(expected_scores) - min(expected_scores)
    compression = 1.0 - (obs_range / exp_range if exp_range else 1.0)
    mae = mean(abs(a - b) for a, b in zip(scores, expected_scores))
    return {"middle_score_rate": middle_rate, "tail_recall": tail_recall, "scale_compression": compression, "mae": mae}


def position_metrics(rows: Sequence[dict]) -> dict[str, float]:
    by_pair: dict[str, dict[int, list[str]]] = {}
    for r in rows:
        by_pair.setdefault(r["pair_id"], {}).setdefault(int(r["order"]), []).append(r["observed_label"])
    complete = []
    for pair, orders in by_pair.items():
        if 0 in orders and 1 in orders:
            complete.append((_majority(orders[0]), _majority(orders[1])))
    if not complete:
        raise ValueError("no order-swapped pairs")
    n = len(complete)
    consistency = sum(a == b for a, b in complete) / n
    first_pref = sum(a == "pass" for a, _ in complete) / n
    second_pref = sum(b == "pass" for _, b in complete) / n
    fairness = 1.0 - abs(first_pref - second_pref)
    return {"position_consistency": consistency, "preference_fairness": fairness, "order_flip_rate": 1.0 - consistency}


def holm_bonferroni(p_values: dict[str, float], alpha: float = 0.05) -> dict[str, dict[str, float | bool]]:
    if not p_values:
        return {}
    for p in p_values.values():
        _check_prob(p)
    ordered = sorted(p_values.items(), key=lambda kv: kv[1])
    m = len(ordered)
    out: dict[str, dict[str, float | bool]] = {}
    running = 0.0
    still_rejecting = True
    for i, (name, p) in enumerate(ordered):
        adjusted = min(1.0, (m - i) * p)
        running = max(running, adjusted)
        threshold = alpha / (m - i)
        reject = still_rejecting and p <= threshold
        if not reject:
            still_rejecting = False
        out[name] = {"raw_p": p, "adjusted_p": running, "reject": reject}
    return out
