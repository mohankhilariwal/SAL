from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check(condition: bool, detail: str) -> dict[str, object]:
    return {"passed": bool(condition), "detail": detail}


def main() -> None:
    demo = json.loads((ROOT / "reports/stage10a-demo.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "reports/stage10a-validation.json").read_text(encoding="utf-8"))
    performance = json.loads((ROOT / "reports/stage10a-performance.json").read_text(encoding="utf-8"))
    status = demo["status"]
    checks = {
        "EVAL-229": check(demo["stage"] == "S10A", "scope is Stage 10A only"),
        "EVAL-230": check(status["telemetry_events"] >= 1, "structured operational telemetry exists"),
        "EVAL-231": check(status["audit_events"] >= 1, "material audit evidence exists"),
        "EVAL-232": check(status["audit_valid"], "hash chain verifies"),
        "EVAL-233": check(demo["authority_effect"] == "none", "telemetry/audit do not grant authority"),
        "EVAL-234": check(status["worm_storage_implemented"] is False, "no false WORM claim"),
        "EVAL-235": check(status["kms_hsm_signing_implemented"] is False, "local HMAC is not KMS/HSM signing"),
        "EVAL-236": check(status["full_control_plane_implemented"] is False, "S09D remains unresolved"),
        "EVAL-237": check(status["stage8d_resolved"] is False, "S08D remains unresolved"),
        "EVAL-238": check(status["stage9d_resolved"] is False, "sequence divergence is explicit"),
        "EVAL-239": check(validation["schemas_checked"] == 20, "DATA-217..236 schemas validated"),
        "EVAL-240": check(validation["valid"], "structural validation passed"),
        "EVAL-241": check(performance["local_guard_passed"], "local performance guards passed"),
        "EVAL-242": check(performance["production_benchmark"] is False, "performance result not represented as production benchmark"),
        "EVAL-243": check(demo["evidence_package_digest"], "evidence package is digest-bound"),
        "EVAL-244": check(demo["telemetry_exported"] >= 1, "telemetry export path exercised"),
        "EVAL-245": check(status["telemetry_dropped"] == 0, "demo did not drop telemetry"),
        "EVAL-246": check(status["telemetry_export_error"] is None, "demo exporter healthy"),
        "EVAL-247": check(status["production_ready"] is False, "production promotion remains denied"),
        "EVAL-248": check(demo["observability_model"] == "OBS-001/1.0.0", "observability model version pinned"),
        "EVAL-249": check(demo["audit_model"] == "AUD-001/1.0.0", "audit model version pinned"),
        "EVAL-250": check(demo["graph_version"] == "GRAPH-001/1.11.0", "graph version advanced exactly once"),
        "EVAL-251": check(all(r["authority_effect"] == "none" for r in demo["results"]), "all stage decisions remain non-authorizing"),
        "EVAL-252": check("TOOL-007" not in json.dumps(demo) and "AGT-002" not in json.dumps(demo), "no new tool or agent activated"),
    }
    result = {
        "stage": "S10A",
        "passed": all(value["passed"] for value in checks.values()),
        "checks": checks,
    }
    (ROOT / "reports/stage10a-evaluation.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
