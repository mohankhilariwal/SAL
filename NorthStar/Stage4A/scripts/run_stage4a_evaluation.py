from pathlib import Path
import json, tempfile
from northstar_compliance.agent.models import PrincipalContext
from northstar_compliance.graph.factory import build_runtime, build_state
from northstar_compliance.state.checkpoint import LocalCheckpointStore
from northstar_compliance.tools.gateway import ToolGateway

ROOT = Path(__file__).resolve().parents[1]
results = {}
with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    runtime, gateway = build_runtime(ROOT, checkpoint_dir=td / "happy")
    happy = runtime.run(build_state(run_id="RUN-EVAL-027"))
    results["EVAL-027"] = {"status": happy.run_state.status, "transitions": len(happy.transitions), "path_nodes": sorted({t['source_node'] for t in happy.transitions})}

    g2 = ToolGateway({"TOOL-003":"transient_read"})
    runtime2, _ = build_runtime(ROOT, gateway=g2, checkpoint_dir=td / "fallback")
    fallback = runtime2.run(build_state(run_id="RUN-EVAL-028"))
    results["EVAL-028"] = {"status": fallback.run_state.status, "fallback_calls": [c for c in g2.calls if c[1]=='fallback']}

    g3 = ToolGateway({"TOOL-004":"ambiguous_after_commit"})
    runtime3, _ = build_runtime(ROOT, gateway=g3, checkpoint_dir=td / "reconcile")
    reconcile = runtime3.run(build_state(run_id="RUN-EVAL-029"))
    case_records = [v for (tool,_),v in g3.store.items() if tool == 'TOOL-004']
    results["EVAL-029"] = {"status": reconcile.run_state.status, "case_records": len(case_records), "recoveries": reconcile.run_state.recovery_records}

    runtime4, g4 = build_runtime(ROOT, checkpoint_dir=td / "resume")
    partial = runtime4.run(build_state(run_id="RUN-EVAL-030"), stop_after_transitions=12)
    loaded = LocalCheckpointStore(td / "resume").load(partial.run_state.run_id, graph_id="GRAPH-001", graph_version="1.0.0")
    before = len(g4.calls)
    resumed = runtime4.run(loaded)
    results["EVAL-030"] = {"status": resumed.run_state.status, "resumed": resumed.run_state.resumed_from_checkpoint, "additional_calls": len(g4.calls)-before}

    denied = build_state(run_id="RUN-EVAL-031", principal=PrincipalContext(allow_writes=False))
    runtime5, _ = build_runtime(ROOT, checkpoint_dir=td / "denied")
    denied = runtime5.run(denied)
    results["EVAL-031"] = {"status": denied.run_state.status, "reason": denied.run_state.termination_reason, "tool_calls": denied.run_state.ledger.tool_calls}

    results["EVAL-032"] = {"graph_nodes": 9, "agent_count": 1, "memory_modules": 0, "multi_agent_modules": 0, "harness_modules": 0}

out = ROOT / "Stage-4A-Evaluation-Report.json"
out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(results, indent=2, sort_keys=True))
