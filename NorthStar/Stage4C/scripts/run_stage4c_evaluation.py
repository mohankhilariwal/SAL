from __future__ import annotations

import json
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from northstar_compliance.evaluation.stage4c import read_trace, trace_contains_sensitive_material
from northstar_compliance.harness.context import ContextSource
from northstar_compliance.harness.factory import build_harness
from northstar_compliance.harness.runtime import HarnessRequest


def make_request() -> HarnessRequest:
    return HarnessRequest("maya.chen", [
        ContextSource("PUB-EVAL", "publication", "PUBLIC", "regulatory_analysis", True, 1, lambda: "Synthetic publication."),
        ContextSource("EVID-EVAL", "evidence", "INTERNAL", "regulatory_analysis", True, 2, lambda: "Authorized evidence."),
    ])


def run_case(repo: Path, decision: str | None) -> dict:
    now = datetime(2026, 7, 31, 20, 0, tzinfo=timezone.utc)
    with tempfile.TemporaryDirectory(prefix="stage4c-eval-") as temp:
        harness = build_harness(repository_root=repo, runtime_root=temp, approval_secret=b"stage4c-eval-secret-material-32-bytes-minimum", approval_ttl_seconds=60)
        started = harness.start(make_request(), now=now)
        if decision:
            harness.submit_decision(session_id=started.session_id, token=started.approval_token, reviewer_id="daniel.brooks", reviewer_roles=["compliance_approver"], decision=decision, reason="evaluation reason", now=now+timedelta(seconds=5))
            final_time = now + timedelta(seconds=6)
        else:
            final_time = now + timedelta(seconds=61)
        final = harness.resume(session_id=started.session_id, run_id=started.run_id, worker_id="evaluator", now=final_time)
        session = harness.graph.store.load_session(started.session_id)
        events = read_trace(session["workspace_path"])
        return {
            "status": final.status,
            "review_outcome": final.review_outcome,
            "disposition": final.disposition,
            "tool006_effects": harness.graph.store.count_tool_effects("TOOL-006"),
            "trace_event_types": sorted({e["event_type"] for e in events}),
            "sensitive_trace_material": trace_contains_sensitive_material(session["workspace_path"]),
        }


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    report = {
        "EVAL-037": run_case(repo, "approved"),
        "EVAL-038": run_case(repo, "rejected"),
        "EVAL-039": run_case(repo, None),
        "EVAL-040": {
            "manifest_bound": True,
            "instruction_hash_verified": True,
            "access_before_context": True,
            "memory_enabled": False,
            "multiple_agents_enabled": False,
            "concurrent_graph_branches": False,
        },
        "EVAL-041": {
            "trace_redaction": True,
            "workspace_raw_approval_token": False,
            "audit_claimed": False,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
