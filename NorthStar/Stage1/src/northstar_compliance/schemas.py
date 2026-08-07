from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Disposition = Literal["preliminary_unapproved"]
ClaimKind = Literal["source_fact", "candidate_interpretation"]


@dataclass(frozen=True)
class PublicationMetadata:
    publication_id: str
    title: str
    source_uri: str
    jurisdiction: str
    received_at: str
    file_name: str
    sha256: str
    line_count: int
    byte_count: int
    schema_version: str = "1.0.0"


@dataclass(frozen=True)
class EvidenceReference:
    publication_id: str
    source_sha256: str
    line_start: int
    line_end: int
    excerpt: str


@dataclass(frozen=True)
class SummaryClaim:
    statement: str
    kind: ClaimKind
    evidence: list[EvidenceReference]
    uncertainty: str = ""


@dataclass(frozen=True)
class DeadlineCandidate:
    text: str
    evidence: EvidenceReference
    normalized_date: str | None = None


@dataclass(frozen=True)
class PreliminaryRegulatorySummary:
    publication_id: str
    title: str
    executive_summary: str
    source_facts: list[SummaryClaim]
    candidate_affected_areas: list[str]
    deadline_candidates: list[DeadlineCandidate]
    missing_information: list[str]
    uncertainties: list[str]
    disposition: Disposition = "preliminary_unapproved"
    human_review_required: bool = True
    approval_status: str = "not_requested"
    legal_conclusion: str = "not_provided"
    schema_version: str = "1.0.0"
    prompt_version: str = "stage1-summary-v1"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ModelInvocationRecord:
    invocation_id: str
    provider: str
    model: str
    prompt_version: str
    schema_version: str
    started_at: str
    completed_at: str
    input_sha256: str
    success: bool
    error_type: str | None = None
    error_message: str | None = None
    usage: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


SUMMARY_JSON_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "executive_summary", "source_facts", "candidate_affected_areas",
        "deadline_candidates", "missing_information", "uncertainties"
    ],
    "properties": {
        "executive_summary": {"type": "string", "minLength": 1},
        "source_facts": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["statement", "line_start", "line_end", "excerpt", "uncertainty"],
                "properties": {
                    "statement": {"type": "string", "minLength": 1},
                    "line_start": {"type": "integer", "minimum": 1},
                    "line_end": {"type": "integer", "minimum": 1},
                    "excerpt": {"type": "string", "minLength": 1},
                    "uncertainty": {"type": "string"}
                }
            }
        },
        "candidate_affected_areas": {"type": "array", "items": {"type": "string"}},
        "deadline_candidates": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["text", "line_start", "line_end", "excerpt", "normalized_date"],
                "properties": {
                    "text": {"type": "string"},
                    "line_start": {"type": "integer", "minimum": 1},
                    "line_end": {"type": "integer", "minimum": 1},
                    "excerpt": {"type": "string"},
                    "normalized_date": {"type": ["string", "null"]}
                }
            }
        },
        "missing_information": {"type": "array", "items": {"type": "string"}},
        "uncertainties": {"type": "array", "items": {"type": "string"}}
    }
}
