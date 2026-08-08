from pathlib import Path
import json, tempfile
from northstar_compliance.graph.factory import build_runtime, build_state

ROOT = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
    runtime, gateway = build_runtime(ROOT, checkpoint_dir=Path(td))
    state = runtime.run(build_state(run_id="RUN-STAGE4A-DEMO"))
    output = {
        "status": state.run_state.status,
        "termination_reason": state.run_state.termination_reason,
        "graph_id": state.graph_id,
        "graph_version": state.graph_version,
        "transitions": len(state.transitions),
        "model_calls": state.run_state.ledger.model_calls,
        "tool_calls": state.run_state.ledger.tool_calls,
        "milestones": state.run_state.milestones,
        "artifacts": sorted(state.run_state.artifacts),
        "final_disposition": state.run_state.final_disposition,
        "human_review_required": state.run_state.human_review_required,
        "gateway_calls": gateway.calls,
    }
    print(json.dumps(output, indent=2))
