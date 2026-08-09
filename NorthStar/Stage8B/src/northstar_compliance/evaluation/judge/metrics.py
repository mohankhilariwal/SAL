from __future__ import annotations

from dataclasses import dataclass
from math import fsum
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class BinaryAgreement:
    accuracy: float
    precision: float
    recall: float
    f1: float
    kappa: float
    tp: int
    tn: int
    fp: int
    fn: int


def safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def binary_agreement(expected: Sequence[bool], observed: Sequence[bool]) -> BinaryAgreement:
    if len(expected) != len(observed) or not expected:
        raise ValueError("expected and observed must be non-empty and equal length")
    tp = sum(e and o for e, o in zip(expected, observed))
    tn = sum((not e) and (not o) for e, o in zip(expected, observed))
    fp = sum((not e) and o for e, o in zip(expected, observed))
    fn = sum(e and (not o) for e, o in zip(expected, observed))
    n = len(expected)
    accuracy = safe_div(tp + tn, n)
    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    f1 = safe_div(2 * precision * recall, precision + recall)
    p_yes_e = safe_div(tp + fn, n)
    p_yes_o = safe_div(tp + fp, n)
    p_no_e = 1 - p_yes_e
    p_no_o = 1 - p_yes_o
    expected_agreement = p_yes_e * p_yes_o + p_no_e * p_no_o
    kappa = safe_div(accuracy - expected_agreement, 1 - expected_agreement)
    return BinaryAgreement(accuracy, precision, recall, f1, kappa, tp, tn, fp, fn)


def coverage(values: Sequence[object | None]) -> float:
    if not values:
        return 0.0
    return sum(value is not None for value in values) / len(values)


def exact_score_agreement(expected: Sequence[int], observed: Sequence[int]) -> float:
    if len(expected) != len(observed) or not expected:
        raise ValueError("invalid score sequences")
    return sum(e == o for e, o in zip(expected, observed)) / len(expected)


def mean_absolute_error(expected: Sequence[int], observed: Sequence[int]) -> float:
    if len(expected) != len(observed) or not expected:
        raise ValueError("invalid score sequences")
    return fsum(abs(e - o) for e, o in zip(expected, observed)) / len(expected)


def flip_rate(base: Mapping[str, str], variant: Mapping[str, str]) -> float:
    keys = sorted(set(base) & set(variant))
    if not keys:
        return 0.0
    return sum(base[k] != variant[k] for k in keys) / len(keys)


def middle_score_rate(scores: Iterable[int], *, low: int = 1, high: int = 3) -> float:
    values = list(scores)
    if not values:
        return 0.0
    return sum(low <= score <= high for score in values) / len(values)


def tail_recall(expected: Sequence[int], observed: Sequence[int]) -> float:
    pairs = [(e, o) for e, o in zip(expected, observed) if e in {0, 4}]
    if not pairs:
        return 0.0
    return sum(e == o for e, o in pairs) / len(pairs)


def attack_success_rate(attacked_expected_fail: Sequence[bool], observed_pass: Sequence[bool]) -> float:
    if len(attacked_expected_fail) != len(observed_pass) or not observed_pass:
        raise ValueError("invalid attack sequences")
    attacked = [o for expected_fail, o in zip(attacked_expected_fail, observed_pass) if expected_fail]
    return safe_div(sum(attacked), len(attacked))


def group_accuracy_gap(expected: Sequence[bool], observed: Sequence[bool], groups: Sequence[str]) -> float:
    if not (len(expected) == len(observed) == len(groups)):
        raise ValueError("group inputs must align")
    by_group: dict[str, list[bool]] = {}
    for e, o, group in zip(expected, observed, groups):
        by_group.setdefault(group, []).append(e == o)
    if len(by_group) < 2:
        return 0.0
    accuracies = [sum(values) / len(values) for values in by_group.values()]
    return max(accuracies) - min(accuracies)
