from __future__ import annotations

import json
import statistics
import time
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from northstar_compliance.specification.assertions import RuntimeAssertionEngine
from northstar_compliance.specification.gates import DeploymentGateEvaluator
from northstar_compliance.specification.loader import AgentSpecificationStore
from northstar_compliance.specification.validator import AgentSpecificationValidator

ROOT = Path(__file__).resolve().parents[1]
ITERATIONS = 1000


def measure(callable_):
    samples = []
    for _ in range(ITERATIONS):
        start = time.perf_counter_ns()
        callable_()
        samples.append((time.perf_counter_ns() - start) / 1_000_000)
    ordered = sorted(samples)
    return {
        "iterations": ITERATIONS,
        "p50_ms": statistics.median(ordered),
        "p95_ms": ordered[int(ITERATIONS * 0.95) - 1],
        "p99_ms": ordered[int(ITERATIONS * 0.99) - 1],
        "max_ms": max(ordered),
    }


def main() -> None:
    manifest = json.loads((ROOT / "config/harness/harness-manifest.json").read_text(encoding="utf-8"))
    specification = AgentSpecificationStore(ROOT / "config/agents/AGT-001.spec.json").load()
    validator = AgentSpecificationValidator()
    validation = validator.validate(specification, manifest=manifest)
    context = {"items": [{"source_id": "PUB-001", "kind": "publication", "authorized": True, "content": "x", "content_sha256": "a" * 64}]}
    assertion_engine = RuntimeAssertionEngine()
    evidence = {
        "specification_digest": specification.digest,
        "tests": {f"TEST-{i:03d}": True for i in range(183, 213)},
        "evaluations": {f"EVAL-{i:03d}": True for i in range(42, 48)},
        "blocking_security_findings": 0,
        "future_stage_flags": {"memory_enabled": False, "concurrent_graph_branches": False, "multiple_agents_enabled": False},
        "human_approval_semantics": True,
        "final_legal_or_compliance_closure": False,
    }
    output = {
        "scope": "local standard-library control-path microbenchmark; not a production SLO benchmark",
        "python_operations_only": True,
        "specification_validation": measure(lambda: validator.validate(specification, manifest=manifest)),
        "pre_start_assertions": measure(lambda: assertion_engine.pre_start(specification, manifest=manifest, context_envelope=context)),
        "deployment_gate": measure(lambda: DeploymentGateEvaluator().evaluate(specification, validation, evidence)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
