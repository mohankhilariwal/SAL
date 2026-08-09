from __future__ import annotations

import json
from dataclasses import asdict

from northstar_compliance.interoperability.adapters.a2a import A2AMappingAdapter
from northstar_compliance.interoperability.adapters.direct import DirectAdapter
from northstar_compliance.interoperability.adapters.mcp import McpMappingAdapter
from northstar_compliance.interoperability.fixtures import build_fixture
from northstar_compliance.interoperability.registry import PROFILES


def main() -> None:
    fixture = build_fixture()
    direct = DirectAdapter().deliver(fixture)
    mcp = McpMappingAdapter().build_server_document(
        tool_ids=("TOOL-001", "TOOL-002", "TOOL-003", "TOOL-004", "TOOL-005", "TOOL-006"),
        artifacts=(fixture["manifest"],),
    )
    a2a = A2AMappingAdapter()
    output = {
        "architectureVersion": "1.5.0",
        "activeAgent": fixture["sender"].endpoint_id,
        "candidateEndpoint": fixture["recipient"].endpoint_id,
        "directReferenceReceipt": asdict(direct),
        "mcpMapping": mcp,
        "a2aAgentCard": a2a.build_agent_card(fixture["recipient"], endpoint_url="https://candidate.invalid/a2a/v1"),
        "a2aTaskMessage": a2a.map_task_message(fixture["envelope"]),
        "protocolProfiles": [asdict(profile) for profile in PROFILES],
        "claims": {
            "secondAgentActivated": False,
            "concurrencyEnabled": False,
            "mcpServerActivated": False,
            "a2aEndpointActivated": False,
            "httpReferenceBoundaryImplemented": True,
        },
    }
    print(json.dumps(output, indent=2, default=str, sort_keys=True))


if __name__ == "__main__":
    main()
