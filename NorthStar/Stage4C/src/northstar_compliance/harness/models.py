from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from northstar_compliance.common.jsonutil import sha256_json


@dataclass(frozen=True)
class InstructionBundle:
    schema_version: str
    instruction_name: str
    instruction_version: str
    content: str
    content_sha256: str
    critical_controls_external: bool = True

    def to_dict(self, *, include_content: bool = True) -> dict[str, Any]:
        value = asdict(self)
        if not include_content:
            value.pop("content")
        return value


@dataclass(frozen=True)
class ContextItem:
    source_id: str
    kind: str
    classification: str
    purpose: str
    content: str
    content_sha256: str
    truncated: bool = False

    def to_dict(self, *, include_content: bool = True) -> dict[str, Any]:
        value = asdict(self)
        if not include_content:
            value.pop("content")
        return value


@dataclass(frozen=True)
class ContextEnvelope:
    schema_version: str
    envelope_id: str
    agent_id: str
    items: tuple[ContextItem, ...]
    omitted_source_ids: tuple[str, ...]
    total_characters: int
    created_at: str
    content_sha256: str

    def to_dict(self, *, include_content: bool = True) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "envelope_id": self.envelope_id,
            "agent_id": self.agent_id,
            "items": [item.to_dict(include_content=include_content) for item in self.items],
            "omitted_source_ids": list(self.omitted_source_ids),
            "total_characters": self.total_characters,
            "created_at": self.created_at,
            "content_sha256": self.content_sha256,
        }


@dataclass(frozen=True)
class HarnessManifest:
    schema_version: str
    architecture_version: str
    repository_version: str
    agent_id: str
    agent_version: str
    graph_id: str
    graph_version: str
    tool_versions: dict[str, str]
    instruction_name: str
    instruction_version: str
    instruction_sha256: str
    validator_names: tuple[str, ...]
    hook_names: tuple[str, ...]
    memory_enabled: bool = False
    concurrent_graph_branches: bool = False
    multiple_agents_enabled: bool = False
    critical_controls_external: bool = True

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["validator_names"] = list(self.validator_names)
        value["hook_names"] = list(self.hook_names)
        return value

    @property
    def digest(self) -> str:
        return sha256_json(self.to_dict())


@dataclass(frozen=True)
class HarnessSession:
    schema_version: str
    session_id: str
    initiator_id: str
    manifest_digest: str
    trace_id: str
    instruction_digest: str
    context_digest: str
    workspace_path: str
    status: str
    created_at: str
    updated_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WorkspaceManifest:
    schema_version: str
    session_id: str
    root_relative_path: str
    allowed_suffixes: tuple[str, ...]
    max_file_bytes: int
    max_workspace_bytes: int
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["allowed_suffixes"] = list(self.allowed_suffixes)
        return value


@dataclass(frozen=True)
class TraceEvent:
    schema_version: str
    trace_id: str
    span_id: str
    parent_span_id: str | None
    session_id: str
    run_id: str | None
    event_type: str
    timestamp: str
    attributes: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HookResult:
    schema_version: str
    hook_name: str
    lifecycle_event: str
    status: str
    findings: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["findings"] = list(self.findings)
        return value


@dataclass(frozen=True)
class HarnessRunResult:
    schema_version: str
    session_id: str
    run_id: str
    status: str
    current_node: str
    disposition: str
    review_outcome: str | None
    wait_id: str | None
    approval_token: str | None
    manifest_digest: str
    instruction_digest: str
    context_digest: str
    trace_id: str
    hook_results: tuple[HookResult, ...]

    def to_dict(self, *, include_transient: bool = False) -> dict[str, Any]:
        value = asdict(self)
        value["hook_results"] = [h.to_dict() for h in self.hook_results]
        if not include_transient:
            value.pop("approval_token")
        return value
