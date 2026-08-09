from .canonical import sha256_hex
from .models import TaskProfileBinding


def bind_task_profile(*, run_id, profile, agent_spec_version="1.1.0"):
    if not run_id or any(ch in run_id for ch in ("\\", "/")) or "\x00" in run_id:
        raise ValueError("invalid run_id")
    if profile.agent_id != "AGT-001":
        raise ValueError("only AGT-001")
    if (profile.graph_id, profile.graph_version) != ("GRAPH-001", "1.1.0"):
        raise ValueError("graph")
    if agent_spec_version != "1.1.0":
        raise ValueError("spec")
    base = {
        "binding_id": f"BIND-{run_id}-{profile.profile_id}",
        "run_id": run_id,
        "agent_id": profile.agent_id,
        "agent_spec_version": agent_spec_version,
        "graph_id": profile.graph_id,
        "graph_version": profile.graph_version,
        "node_key": profile.node_key,
        "profile_id": profile.profile_id,
        "profile_version": profile.profile_version,
        "profile_sha256": profile.profile_sha256,
        "authority_owner": "CMP-005/CMP-007/CMP-006",
        "state_owner": "CMP-003",
        "route_owner": "GRAPH-001/CMP-003",
        "memory_owner": "CMP-003 harness memory lifecycle",
    }
    return TaskProfileBinding(**base, binding_sha256=sha256_hex(base))
