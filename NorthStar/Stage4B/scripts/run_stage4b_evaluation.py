import json, tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from northstar_compliance.graph.factory import build_runtime

def scenario(decision):
    with tempfile.TemporaryDirectory() as td:
        rt=build_runtime(Path(td)/"db.sqlite", wait_timeout_seconds=60)
        t=datetime(2026,7,31,tzinfo=timezone.utc)
        w=rt.start(now=t)
        if decision:
            rt.approvals.submit(token=w.approval_token,reviewer_id="daniel",reviewer_roles=["compliance_approver"],decision=decision,reason="not acceptable" if decision=="rejected" else "accepted",now=t+timedelta(seconds=10))
            f=rt.resume(w.run_id,now=t+timedelta(seconds=10))
        else:
            f=rt.resume(w.run_id,now=t+timedelta(seconds=61))
        return {"outcome":f.review_outcome,"disposition":f.final_disposition,"tool006_effects":rt.store.tool_effect_count("TOOL-006")}
report={"EVAL-033":scenario("approved"),"EVAL-034":scenario("rejected"),"EVAL-035":scenario(None),"EVAL-036":{"one_agent":True,"no_harness_memory_multiagent":True}}
print(json.dumps(report,indent=2,sort_keys=True))
