from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class AgentSpecification:
    raw: Mapping[str, Any]
    digest: str

    @property
    def specification_id(self) -> str:
        return str(self.raw["specification_id"])

    @property
    def version(self) -> str:
        return str(self.raw["version"])

    @property
    def agent_id(self) -> str:
        return str(self.raw["agent"]["id"])

    @property
    def status(self) -> str:
        return str(self.raw["lifecycle"]["status"])

    @property
    def allowed_tool_ids(self) -> tuple[str, ...]:
        return tuple(item["id"] for item in self.raw["authority"]["allowed_tools"])


@dataclass(frozen=True)
class SpecificationBinding:
    specification_id: str
    specification_version: str
    specification_digest: str
    agent_id: str
    graph_id: str
    graph_version: str
    instruction_id: str
    instruction_digest: str
    manifest_digest: str


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str
    path: str = "$"


@dataclass(frozen=True)
class SpecificationValidationReport:
    valid: bool
    specification_id: str | None
    specification_version: str | None
    digest: str | None
    findings: tuple[Finding, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "specification_id": self.specification_id,
            "specification_version": self.specification_version,
            "digest": self.digest,
            "findings": [finding.__dict__ for finding in self.findings],
        }


@dataclass(frozen=True)
class RuntimeAssertionResult:
    passed: bool
    phase: str
    checks: Mapping[str, bool]
    failures: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "phase": self.phase,
            "checks": dict(self.checks),
            "failures": list(self.failures),
        }


@dataclass(frozen=True)
class DeploymentGateResult:
    allowed: bool
    gate_profile: str
    checks: Mapping[str, bool]
    blocking_reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "gate_profile": self.gate_profile,
            "checks": dict(self.checks),
            "blocking_reasons": list(self.blocking_reasons),
        }
