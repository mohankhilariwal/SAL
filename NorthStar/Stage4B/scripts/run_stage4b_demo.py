from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
from northstar_compliance.graph.factory import build_runtime

with tempfile.TemporaryDirectory() as td:
    db = Path(td) / "stage4b.db"
    rt = build_runtime(db, wait_timeout_seconds=600)
    t0 = datetime(2026, 7, 31, 18, 0, tzinfo=timezone.utc)
    waiting = rt.start(now=t0)
    print(f"status={waiting.status}")
    print(f"run_id={waiting.run_id}")
    print(f"wait_id={waiting.wait_id}")
    print(f"tool006_effects={rt.store.tool_effect_count('TOOL-006')}")
    rt.approvals.submit(token=waiting.approval_token, reviewer_id="daniel.brooks",
                        reviewer_roles=["compliance_approver"], decision="approved",
                        reason="Evidence package is sufficient for controlled continuation", now=t0+timedelta(minutes=5))
    final = rt.resume(waiting.run_id, now=t0+timedelta(minutes=5), worker_id="demo-resumer")
    print(f"final_status={final.status}")
    print(f"review_outcome={final.review_outcome}")
    print(f"final_disposition={final.final_disposition}")
    print(f"tool006_effects_after_resume={rt.store.tool_effect_count('TOOL-006')}")
