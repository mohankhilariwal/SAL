from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from northstar_compliance.common.jsonutil import new_id


class ToolGatewayError(RuntimeError):
    pass


@dataclass(frozen=True)
class ToolSpec:
    tool_id: str
    version: str
    impact: str
    description: str
    allowed_agents: tuple[str, ...] = ("AGT-001",)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ToolResult:
    tool_id: str
    status: str
    data: dict[str, Any]
    idempotency_key: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


DEFAULT_TOOL_SPECS = (
    ToolSpec("TOOL-001", "1.0.0", "read_only", "Search regulatory source catalogue"),
    ToolSpec("TOOL-002", "1.0.0", "read_only", "Query authoritative control catalogue"),
    ToolSpec("TOOL-003", "1.0.0", "read_only", "Retrieve authorized internal evidence"),
    ToolSpec("TOOL-004", "1.0.0", "reversible_write", "Create draft unapproved case"),
    ToolSpec("TOOL-005", "1.0.0", "reversible_write", "Save candidate unapproved mapping"),
    ToolSpec("TOOL-006", "1.0.0", "reversible_write", "Queue human review request"),
)


class ToolGateway:
    """Authoritative INT-017/CMP-005 tool execution boundary."""

    def __init__(self, store: Any, specs: tuple[ToolSpec, ...] = DEFAULT_TOOL_SPECS):
        self._store = store
        self._specs = {spec.tool_id: spec for spec in specs}

    @property
    def specs(self) -> tuple[ToolSpec, ...]:
        return tuple(self._specs[k] for k in sorted(self._specs))

    def invoke(
        self,
        *,
        agent_id: str,
        tool_id: str,
        arguments: dict[str, Any],
        idempotency_key: str,
    ) -> ToolResult:
        spec = self._specs.get(tool_id)
        if spec is None:
            raise ToolGatewayError(f"unregistered_tool:{tool_id}")
        if agent_id not in spec.allowed_agents:
            raise ToolGatewayError("agent_not_authorized")
        if not idempotency_key:
            raise ToolGatewayError("idempotency_key_required")

        existing = self._store.get_tool_effect(tool_id, idempotency_key)
        if existing is not None:
            return ToolResult(**existing)

        if tool_id == "TOOL-006":
            if arguments.get("disposition") != "preliminary_grounded_unapproved":
                raise ToolGatewayError("review_request_requires_unapproved_disposition")
            data = {
                "review_request_id": new_id("REVREQ"),
                "status": "queued_for_human_review",
                "required_role": "compliance_approver",
            }
        elif tool_id == "TOOL-004":
            data = {"case_id": new_id("CASE"), "status": "draft_unapproved"}
        elif tool_id == "TOOL-005":
            data = {"mapping_id": new_id("MAP"), "status": "candidate_unapproved"}
        else:
            data = {"records": [], "status": "ok"}

        result = ToolResult(tool_id=tool_id, status="succeeded", data=data, idempotency_key=idempotency_key)
        self._store.save_tool_effect(tool_id, idempotency_key, result.to_dict())
        return result
