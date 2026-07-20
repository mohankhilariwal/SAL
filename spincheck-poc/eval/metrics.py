"""POC metrics: relaxed span P/R/F1, claim-type accuracy, ECE/Brier helpers."""
from __future__ import annotations


def _overlap(a, b):
    s = max(a[0], b[0]); e = min(a[1], b[1])
    inter = max(0, e - s)
    return inter / max(1, min(a[1] - a[0], b[1] - b[0]))


def span_prf(preds, thr: float = 0.5):
    tp = fp = fn = 0
    for gold_item, doc in preds:
        gold = [(c["start"], c["end"]) for c in gold_item.get("gold_claims", [])]
        pred = [(c["start"], c["end"]) for c in doc.get("claims", [])]
        used = set()
        for p in pred:
            hit = next((i for i, g in enumerate(gold)
                        if i not in used and _overlap(p, g) >= thr), None)
            if hit is None:
                fp += 1
            else:
                tp += 1; used.add(hit)
        fn += len(gold) - len(used)
    prec = tp / max(1, tp + fp); rec = tp / max(1, tp + fn)
    f1 = 2 * prec * rec / max(1e-9, prec + rec)
    return round(prec, 3), round(rec, 3), round(f1, 3)


def type_accuracy(preds, thr: float = 0.5):
    ok = tot = 0
    for gold_item, doc in preds:
        for g in gold_item.get("gold_claims", []):
            tot += 1
            for c in doc.get("claims", []):
                if _overlap((c["start"], c["end"]), (g["start"], g["end"])) >= thr:
                    ok += int(c["claim_type"] == g["claim_type"]); break
    return round(ok / max(1, tot), 3)


def ece(confs: list[float], correct: list[int], bins: int = 5) -> float:
    n = len(confs)
    if not n:
        return 0.0
    total = 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        idx = [i for i, c in enumerate(confs) if lo <= c < hi or (b == bins - 1 and c == hi)]
        if not idx:
            continue
        acc = sum(correct[i] for i in idx) / len(idx)
        conf = sum(confs[i] for i in idx) / len(idx)
        total += len(idx) / n * abs(acc - conf)
    return round(total, 4)


def brier(confs: list[float], correct: list[int]) -> float:
    if not confs:
        return 0.0
    return round(sum((c - y) ** 2 for c, y in zip(confs, correct)) / len(confs), 4)
