from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

SCHEMA_VERSION = "1.0.0"


class KnowledgeError(ValueError):
    """Base exception for invalid knowledge-preparation inputs."""


class Classification(StrEnum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


class SourceType(StrEnum):
    POLICY = "POLICY"
    CONTROL = "CONTROL"
    BUSINESS_PROCESS = "BUSINESS_PROCESS"
    TAXONOMY = "TAXONOMY"
    PRIOR_ASSESSMENT = "PRIOR_ASSESSMENT"


@dataclass(frozen=True, slots=True)
class AccessScope:
    classification: Classification
    allowed_groups: tuple[str, ...]
    residency: str = "CA"
    purpose: str = "REGULATORY_CHANGE_ANALYSIS"

    def __post_init__(self) -> None:
        normalized = tuple(sorted({group.strip() for group in self.allowed_groups if group.strip()}))
        object.__setattr__(self, "allowed_groups", normalized)
        if not normalized:
            raise KnowledgeError("allowed_groups must not be empty")
        if self.classification == Classification.PUBLIC and normalized != ("*",):
            raise KnowledgeError("PUBLIC content must use allowed_groups=['*']")
        if self.classification != Classification.PUBLIC and "*" in normalized:
            raise KnowledgeError("non-public content cannot use wildcard access")
        if not self.residency.strip():
            raise KnowledgeError("residency is required")
        if not self.purpose.strip():
            raise KnowledgeError("purpose is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "classification": self.classification.value,
            "allowed_groups": list(self.allowed_groups),
            "residency": self.residency,
            "purpose": self.purpose,
        }


@dataclass(frozen=True, slots=True)
class KnowledgeSourceDescriptor:
    source_id: str
    title: str
    source_type: SourceType
    owner: str
    relative_path: str
    version_label: str
    effective_from: str
    effective_to: str | None
    jurisdictions: tuple[str, ...]
    business_domains: tuple[str, ...]
    access: AccessScope
    retention_class: str
    authoritative: bool = True

    def __post_init__(self) -> None:
        for field_name in (
            "source_id",
            "title",
            "owner",
            "relative_path",
            "version_label",
            "effective_from",
            "retention_class",
        ):
            if not getattr(self, field_name).strip():
                raise KnowledgeError(f"{field_name} is required")
        if not self.source_id.startswith(("POL-", "CTL-", "PROC-", "TAX-", "ASMT-")):
            raise KnowledgeError("source_id must use a reserved knowledge prefix")
        if not self.jurisdictions:
            raise KnowledgeError("at least one jurisdiction is required")
        if not self.business_domains:
            raise KnowledgeError("at least one business domain is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "source_id": self.source_id,
            "title": self.title,
            "source_type": self.source_type.value,
            "owner": self.owner,
            "relative_path": self.relative_path,
            "version_label": self.version_label,
            "effective_from": self.effective_from,
            "effective_to": self.effective_to,
            "jurisdictions": list(self.jurisdictions),
            "business_domains": list(self.business_domains),
            "access": self.access.to_dict(),
            "retention_class": self.retention_class,
            "authoritative": self.authoritative,
        }


@dataclass(frozen=True, slots=True)
class KnowledgeDocumentVersion:
    source_id: str
    source_version_id: str
    version_label: str
    raw_sha256: str
    normalized_sha256: str
    metadata_sha256: str
    byte_count: int
    line_count: int
    parser_version: str
    chunker_version: str
    ingested_at: str
    status: str
    risk_flags: tuple[str, ...] = ()
    supersedes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["schema_version"] = SCHEMA_VERSION
        data["risk_flags"] = list(self.risk_flags)
        return data


@dataclass(frozen=True, slots=True)
class KnowledgeChunk:
    chunk_id: str
    source_id: str
    source_version_id: str
    ordinal: int
    heading_path: tuple[str, ...]
    line_start: int
    line_end: int
    char_count: int
    content_sha256: str
    text: str
    access: AccessScope
    jurisdictions: tuple[str, ...]
    business_domains: tuple[str, ...]
    effective_from: str
    effective_to: str | None
    risk_flags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.line_start < 1 or self.line_end < self.line_start:
            raise KnowledgeError("invalid chunk line coordinates")
        if self.ordinal < 1:
            raise KnowledgeError("chunk ordinal must start at 1")
        if self.char_count != len(self.text):
            raise KnowledgeError("char_count does not match text")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["schema_version"] = SCHEMA_VERSION
        data["heading_path"] = list(self.heading_path)
        data["jurisdictions"] = list(self.jurisdictions)
        data["business_domains"] = list(self.business_domains)
        data["risk_flags"] = list(self.risk_flags)
        data["access"] = self.access.to_dict()
        return data


@dataclass(frozen=True, slots=True)
class IngestionItemResult:
    source_id: str
    source_version_id: str
    action: str
    chunk_count: int
    status: str
    risk_flags: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["risk_flags"] = list(self.risk_flags)
        return data


@dataclass(slots=True)
class IngestionRunRecord:
    run_id: str
    started_at: str
    completed_at: str | None = None
    status: str = "RUNNING"
    manifest_sha256: str = ""
    items: list[IngestionItemResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @classmethod
    def start(cls, run_id: str) -> "IngestionRunRecord":
        return cls(run_id=run_id, started_at=datetime.now(timezone.utc).isoformat())

    def complete(self, *, status: str) -> None:
        self.status = status
        self.completed_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.run_id,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "status": self.status,
            "manifest_sha256": self.manifest_sha256,
            "items": [item.to_dict() for item in self.items],
            "errors": list(self.errors),
        }
