"""Offline calibration fitting (control plane).

Fits the bucket->displayed-bucket map from human-graded outcomes and writes it
as a versioned artifact (config/calibration_map.json). The data plane applies
it as a pure lookup — never fits online.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

BUCKET_P = {"low": 0.55, "medium": 0.75, "high": 0.92}  # target displayed meaning


def fit(graded: list[dict]) -> dict:
    """graded: [{"confidence": "high", "correct": true}, ...] from human review."""
    out = {}
    order = ["low", "medium", "high"]
    for b in order:
        xs = [g for g in graded if g["confidence"] == b]
        if not xs:
            out[b] = b; continue
        acc = sum(g["correct"] for g in xs) / len(xs)
        i = order.index(b)
        while i > 0 and acc < BUCKET_P[order[i]] - 0.05:
            i -= 1
        out[b] = order[i]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graded", type=Path, default=Path("logs/graded.jsonl"))
    ap.add_argument("--out", type=Path, default=Path("config/calibration_map.json"))
    args = ap.parse_args()
    if not args.graded.exists():
        print("no graded log yet — writing identity map")
        args.out.write_text(json.dumps({"low": "low", "medium": "medium", "high": "high"}, indent=2))
        return
    graded = [json.loads(l) for l in args.graded.read_text().splitlines() if l.strip()]
    cmap = fit(graded)
    args.out.write_text(json.dumps(cmap, indent=2))
    print("calibration map written:", cmap)


if __name__ == "__main__":
    main()
