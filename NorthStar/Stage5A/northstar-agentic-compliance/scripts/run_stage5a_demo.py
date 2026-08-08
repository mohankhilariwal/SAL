from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from northstar_compliance.specification.assertions import RuntimeAssertionEngine
from northstar_compliance.specification.gates import DeploymentGateEvaluator
from northstar_compliance.specification.integration import build_specification_runtime

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    manifest = json.loads((ROOT / "config/harness/harness-manifest.json").read_text(encoding="utf-8"))
    runtime = build_specification_runtime(ROOT / "config/agents/AGT-001.spec.json", manifest)
    context = {
        "envelope_id": "CTX-DEMO-001",
        "items": [
            {
                "source_id": "PUB-DEMO-001",
                "kind": "publication",
                "authorized": True,
                "content": "Synthetic regulatory publication requiring evidence-backed review.",
                "content_sha256": "a" * 64,
            },
            {
                "source_id": "EVID-DEMO-001",
                "kind": "evidence",
                "authorized": True,
                "content": "Synthetic authorized internal policy evidence.",
                "content_sha256": "b" * 64,
            },
        ],
    }
    pre = RuntimeAssertionEngine().pre_start(runtime.specification, manifest=manifest, context_envelope=context)
    result = {
        "status": "completed",
        "review_outcome": "approved",
        "final_disposition": "preliminary_grounded_human_approved",
        "tool006_effects": 1,
        "final_legal_or_compliance_closure": False,
    }
    persisted = {
        "status": result["status"],
        "final_disposition": result["final_disposition"],
        "specification_digest": runtime.specification.digest,
    }
    post = RuntimeAssertionEngine().post_result(runtime.specification, result=result, persisted_result=persisted)
    evidence = {
        "specification_digest": runtime.specification.digest,
        "tests": {f"TEST-{i:03d}": True for i in range(183, 213)},
        "evaluations": {f"EVAL-{i:03d}": True for i in range(42, 48)},
        "blocking_security_findings": 0,
        "future_stage_flags": {
            "memory_enabled": False,
            "concurrent_graph_branches": False,
            "multiple_agents_enabled": False,
        },
        "human_approval_semantics": True,
        "final_legal_or_compliance_closure": False,
    }
    gate = DeploymentGateEvaluator().evaluate(runtime.specification, runtime.validation, evidence)
    output = {
        "specification_id": runtime.specification.specification_id,
        "specification_version": runtime.specification.version,
        "specification_digest": runtime.specification.digest,
        "agent_id": runtime.specification.agent_id,
        "graph": manifest["graph"],
        "allowed_tools": list(runtime.specification.allowed_tool_ids),
        "context_profile": runtime.specification.raw["context_policy"]["profile_id"],
        "memory_enabled": runtime.specification.raw["context_policy"]["memory_enabled"],
        "pre_start_assertions_passed": pre.passed,
        "post_result_assertions_passed": post.passed,
        "deployment_gate_allowed": gate.allowed,
        "final_disposition": result["final_disposition"],
        "final_legal_or_compliance_closure": result["final_legal_or_compliance_closure"],
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
