from __future__ import annotations

import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from northstar_compliance.harness.context import ContextSource
from northstar_compliance.harness.factory import build_harness
from northstar_compliance.harness.runtime import HarnessRequest


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    now = datetime(2026, 7, 31, 20, 0, tzinfo=timezone.utc)
    with tempfile.TemporaryDirectory(prefix="northstar-stage4c-") as temp:
        harness = build_harness(repository_root=repo, runtime_root=temp, approval_secret=b"stage4c-demo-secret-material-32-bytes-minimum", approval_ttl_seconds=60)
        request = HarnessRequest(
            initiator_id="maya.chen",
            context_sources=[
                ContextSource("PUB-DEMO", "publication", "PUBLIC", "regulatory_analysis", True, 1, lambda: "Urgent synthetic regulatory publication."),
                ContextSource("EVID-DEMO", "evidence", "INTERNAL", "regulatory_analysis", True, 2, lambda: "Authorized policy and control evidence."),
            ],
        )
        waiting = harness.start(request, now=now)
        harness.submit_decision(session_id=waiting.session_id, token=waiting.approval_token, reviewer_id="daniel.brooks", reviewer_roles=["compliance_approver"], decision="approved", reason="Evidence package is sufficient", now=now+timedelta(seconds=10))
        final = harness.resume(session_id=waiting.session_id, run_id=waiting.run_id, worker_id="demo-resumer", now=now+timedelta(seconds=11))
        session = harness.graph.store.load_session(waiting.session_id)
        trace_lines = sum(1 for _ in (Path(session["workspace_path"]) / "trace.jsonl").open(encoding="utf-8"))
        print(f"session_id={waiting.session_id}")
        print(f"run_id={waiting.run_id}")
        print(f"waiting_status={waiting.status}")
        print(f"context_digest={waiting.context_digest}")
        print(f"instruction_digest={waiting.instruction_digest}")
        print(f"manifest_digest={waiting.manifest_digest}")
        print(f"final_status={final.status}")
        print(f"review_outcome={final.review_outcome}")
        print(f"final_disposition={final.disposition}")
        print(f"tool006_effects={harness.graph.store.count_tool_effects('TOOL-006')}")
        print(f"trace_events={trace_lines}")
        print("memory_enabled=false")
        print("agent_count=1")


if __name__ == "__main__":
    main()
