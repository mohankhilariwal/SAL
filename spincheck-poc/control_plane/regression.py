"""Regression gate — the ONLY door into production for any control-plane change.

Runs the frozen evaluation subset through the current pipeline, computes core
metrics, and compares against the last accepted baseline. Non-zero exit on
regression => CI blocks promotion. Also run weekly (cron/Actions) to catch
silent vendor model updates.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, "src")
from spincheck.config import ControlPlane          # noqa: E402
from spincheck.orchestrator import Orchestrator    # noqa: E402
sys.path.insert(0, "eval")
from metrics import span_prf, type_accuracy        # noqa: E402

BASELINE = Path("control_plane/regression_baseline.json")
TOLERANCE = 0.03  # allowed absolute drop per metric


def run(dataset: Path) -> dict:
    cp = ControlPlane.load()
    orch = Orchestrator(cp)
    items = [json.loads(l) for l in dataset.read_text().splitlines() if l.strip()]
    preds, escalated, abstained, ok_json = [], 0, 0, 0
    for it in items:
        r = orch.analyze(it["text"])
        escalated += int(r.escalated)
        abstained += int(r.status == "abstained")
        ok_json += int(r.analysis is not None or r.status != "ok")
        preds.append((it, r.analysis or {"claims": [], "rhetoric": []}))
    p, r_, f1 = span_prf(preds)
    acc = type_accuracy(preds)
    n = len(items)
    return {"n": n, "span_precision": p, "span_recall": r_, "span_f1": f1,
            "type_accuracy": acc, "escalation_rate": escalated / n,
            "abstention_rate": abstained / n, "json_ok_rate": ok_json / n,
            "version_vector": cp.version_vector()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", type=Path, required=True)
    ap.add_argument("--update-baseline", action="store_true")
    args = ap.parse_args()
    m = run(args.dataset)
    print(json.dumps({k: v for k, v in m.items() if k != "version_vector"}, indent=2))
    if args.update_baseline or not BASELINE.exists():
        BASELINE.write_text(json.dumps(m, indent=2))
        print("baseline written"); return 0
    base = json.loads(BASELINE.read_text())
    fails = [k for k in ("span_f1", "span_recall", "type_accuracy", "json_ok_rate")
             if m[k] < base[k] - TOLERANCE]
    if fails:
        print(f"REGRESSION on {fails} vs baseline — promotion blocked"); return 1
    print("regression gate: PASS"); return 0


if __name__ == "__main__":
    sys.exit(main())
