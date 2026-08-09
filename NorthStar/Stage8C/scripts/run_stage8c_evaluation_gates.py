from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
report = json.loads((ROOT / "reports/stage8c-bias-lab.json").read_text())
checks = {
    "EVAL-151-probe-catalogue": report["probe_count"] == 23,
    "EVAL-152-repeated-pairs": report["observation_count"] == 3312,
    "EVAL-153-no-live-model": report["live_model_called"] is False,
    "EVAL-154-no-route": report["model_route_activated"] is False,
    "EVAL-155-advisory-only": report["authority_effect"] == "none",
    "EVAL-156-production-thresholds-absent": report["production_thresholds"] is False,
    "EVAL-157-control-not-production": any(r["judge_id"]=="JUDGE-CONTROL" and not r["production_eligible"] for r in report["recommendations"]),
    "EVAL-158-biased-quarantined": any(r["judge_id"]=="JUDGE-BIASED" and r["status"]=="quarantine" for r in report["recommendations"]),
    "EVAL-159-critical-probes": any(e["critical_failures"]>0 for e in report["estimates"]),
    "EVAL-160-hard-gates-not-averaged": all(r["production_eligible"] is False for r in report["recommendations"]),
    "EVAL-161-paired-ci": all(e["ci_low"] <= e["paired_delta"] <= e["ci_high"] for e in report["estimates"]),
    "EVAL-162-multiple-testing": all("corrected_p" in e for e in report["estimates"]),
    "EVAL-163-sealed-excluded": "sealed_stage8a_case" not in json.dumps(report),
    "EVAL-164-language-slices": any(e["probe_id"]=="BIAS-LANGUAGE" for e in report["estimates"]),
    "EVAL-165-self-preference": any(e["probe_id"]=="BIAS-SELF-PREFERENCE" for e in report["estimates"]),
    "EVAL-166-injection": any(e["probe_id"]=="BIAS-PROMPT-INJECTION" for e in report["estimates"]),
    "EVAL-167-score-last": any(e["probe_id"]=="BIAS-PREMATURE-COMMITMENT" for e in report["estimates"]),
    "EVAL-168-deterministic-replay": report["evidence_kind"] == "synthetic_replay",
}
failed = [name for name, ok in checks.items() if not ok]
out = {"checks": checks, "passed": len(checks)-len(failed), "total": len(checks), "failed": failed}
(ROOT / "reports/stage8c-evaluation-gates.json").write_text(json.dumps(out, indent=2, sort_keys=True)+"\n", encoding="utf-8")
if failed:
    raise SystemExit("FAILED: " + ", ".join(failed))
print(f"PASSED: {len(checks)}/{len(checks)} Stage 8C evaluation gates")
