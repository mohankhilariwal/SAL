"""POC comparison runner: score the configured pipeline on the eval set.

Compare pipelines by editing config/models.yaml between runs (that IS the
control-plane workflow) or by pointing --config-root at variant config dirs.
"""
from __future__ import annotations
import argparse, json, statistics, sys
from pathlib import Path

sys.path.insert(0, "src")
from spincheck.config import ControlPlane          # noqa: E402
from spincheck.orchestrator import Orchestrator    # noqa: E402
from metrics import span_prf, type_accuracy        # noqa: E402

BUCKET_P = {"low": 0.55, "medium": 0.75, "high": 0.92}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", type=Path, required=True)
    ap.add_argument("--runs", type=int, default=1)
    args = ap.parse_args()
    cp = ControlPlane.load()
    orch = Orchestrator(cp)
    items = [json.loads(l) for l in args.dataset.read_text().splitlines() if l.strip()]

    all_f1 = []
    for run in range(args.runs):
        preds, esc, absn, lat, cost = [], 0, 0, [], 0.0
        for it in items:
            r = orch.analyze(it["text"])
            esc += int(r.escalated); absn += int(r.status == "abstained")
            lat.append(r.latency_s); cost += r.cost_usd
            preds.append((it, r.analysis or {"claims": [], "rhetoric": []}))
        p, rc, f1 = span_prf(preds); acc = type_accuracy(preds)
        all_f1.append(f1)
        print(json.dumps({
            "run": run + 1, "n": len(items),
            "span_precision": p, "span_recall": rc, "span_f1": f1,
            "claim_type_accuracy": acc,
            "escalation_rate": round(esc / len(items), 3),
            "abstention_rate": round(absn / len(items), 3),
            "latency_p50_s": round(statistics.median(lat), 4),
            "cost_total_usd": round(cost, 5),
            "tier1_pin": cp.version_vector()["tier1_pin"],
        }, indent=2))
    if args.runs > 1:
        print(f"span_f1 across runs: mean={statistics.mean(all_f1):.3f} "
              f"spread={max(all_f1)-min(all_f1):.3f}  (label-flip stability check)")


if __name__ == "__main__":
    main()
