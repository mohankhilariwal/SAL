from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from northstar_compliance.handoff.authority import AuthorityError
from northstar_compliance.handoff.fixtures import build_signed_fixture


def main() -> int:
    results = []
    f = build_signed_fixture()
    checks = {
        "EVAL-062": f["policy"].active_agent_ids == ("AGT-001",),
        "EVAL-063": f["child"].delegation_depth_remaining == 0 and not f["child"].allowed_tools,
        "EVAL-064": f["envelope"].authority_grant_digest == f["child"].digest_sha256,
        "EVAL-065": all(a.immutable for a in f["envelope"].input_artifacts),
        "EVAL-066": f["recipient"].allowed_tools == () and not f["recipient"].may_write_memory,
        "EVAL-067": f["policy"].max_hops == 1 and f["policy"].max_attempts == 1,
        "EVAL-068": f["policy"].current_runtime_mode == "contract_sandbox_only",
        "EVAL-069": all(x is False for x in (f["recipient"].may_route, f["recipient"].may_approve, f["recipient"].may_finalize, f["recipient"].may_run_concurrently)),
    }
    for eval_id, passed in checks.items():
        results.append({"evaluation_id": eval_id, "passed": bool(passed)})
    report = {
        "architecture_version": "1.4.0",
        "results": results,
        "passed": all(r["passed"] for r in results),
        "scope": "deterministic local contract evaluation; no model-quality or production identity claim",
    }
    target = Path("reports/Stage-6B-Evaluation-Report.json")
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(target)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
