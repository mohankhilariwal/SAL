from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from pathlib import Path

from northstar_compliance.handoff.artifacts import InMemoryArtifactStore
from northstar_compliance.handoff.fixtures import build_signed_fixture
from northstar_compliance.handoff.lifecycle import HandoffCoordinator
from northstar_compliance.handoff.simulator import SequentialHandoffSandbox


def encode(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    raise TypeError(type(value).__name__)


def main() -> int:
    f = build_signed_fixture()
    coordinator = HandoffCoordinator()
    sandbox = SequentialHandoffSandbox(
        sender=f["sender"],
        recipient=f["recipient"],
        authority=f["authority"],
        envelopes=f["envelopes"],
        coordinator=coordinator,
        artifacts=InMemoryArtifactStore(),
    )
    receipt, output = sandbox.execute_verification(
        envelope=f["envelope"], grant=f["child"], input_content=f["content"], now=f["now"]
    )
    report = {
        "architecture_version": "1.4.0",
        "runtime_mode": f["policy"].current_runtime_mode,
        "active_agents": list(f["policy"].active_agent_ids),
        "candidate_endpoint": f["recipient"].endpoint_id,
        "envelope_digest": f["envelope"].digest_sha256,
        "grant_digest": f["child"].digest_sha256,
        "receipt": asdict(receipt),
        "output_artifact": asdict(output),
        "status_events": [asdict(event) for event in coordinator.events(f["envelope"].envelope_id)],
        "system_termination_ready": coordinator.system_termination_ready((f["envelope"].envelope_id,)),
        "limitations": [
            "candidate endpoint is sandbox-only",
            "no second active agent",
            "no concurrency",
            "no MCP or A2A protocol selected",
            "local HMAC is a tutorial reference, not production OAuth/DPoP",
        ],
    }
    target = Path("reports/Stage-6B-Demo-Report.json")
    target.write_text(json.dumps(report, indent=2, default=encode) + "\n")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
