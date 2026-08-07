from __future__ import annotations

from typing import Any

from .intake import Publication
from .schemas import DeadlineCandidate, EvidenceReference, PreliminaryRegulatorySummary, SummaryClaim


class SummaryValidationError(ValueError):
    pass


def _int(value: Any, field: str) -> int:
    if not isinstance(value, int):
        raise SummaryValidationError(f"{field} must be an integer")
    return value


def _str(value: Any, field: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise SummaryValidationError(f"{field} must be a non-empty string")
    return value.strip()


def validate_evidence(publication: Publication, *, line_start: int, line_end: int, excerpt: str) -> EvidenceReference:
    if line_start < 1 or line_end < line_start or line_end > len(publication.lines):
        raise SummaryValidationError(f"Invalid evidence line range: {line_start}-{line_end}")
    selected = "\n".join(publication.lines[line_start - 1:line_end])
    if excerpt not in selected:
        raise SummaryValidationError("Evidence excerpt is not present in the cited line range")
    return EvidenceReference(
        publication_id=publication.metadata.publication_id,
        source_sha256=publication.metadata.sha256,
        line_start=line_start,
        line_end=line_end,
        excerpt=excerpt,
    )


def build_validated_summary(publication: Publication, payload: dict[str, Any]) -> PreliminaryRegulatorySummary:
    expected = {"executive_summary", "source_facts", "candidate_affected_areas", "deadline_candidates", "missing_information", "uncertainties"}
    missing = expected - set(payload)
    if missing:
        raise SummaryValidationError(f"Missing model fields: {sorted(missing)}")

    claims: list[SummaryClaim] = []
    for i, item in enumerate(payload["source_facts"]):
        statement = _str(item.get("statement"), f"source_facts[{i}].statement")
        line_start = _int(item.get("line_start"), f"source_facts[{i}].line_start")
        line_end = _int(item.get("line_end"), f"source_facts[{i}].line_end")
        excerpt = _str(item.get("excerpt"), f"source_facts[{i}].excerpt")
        evidence = validate_evidence(publication, line_start=line_start, line_end=line_end, excerpt=excerpt)
        claims.append(SummaryClaim(
            statement=statement,
            kind="source_fact",
            evidence=[evidence],
            uncertainty=_str(item.get("uncertainty", ""), f"source_facts[{i}].uncertainty", allow_empty=True),
        ))

    deadlines: list[DeadlineCandidate] = []
    for i, item in enumerate(payload["deadline_candidates"]):
        line_start = _int(item.get("line_start"), f"deadline_candidates[{i}].line_start")
        line_end = _int(item.get("line_end"), f"deadline_candidates[{i}].line_end")
        excerpt = _str(item.get("excerpt"), f"deadline_candidates[{i}].excerpt")
        evidence = validate_evidence(publication, line_start=line_start, line_end=line_end, excerpt=excerpt)
        normalized = item.get("normalized_date")
        if normalized is not None and not isinstance(normalized, str):
            raise SummaryValidationError("normalized_date must be a string or null")
        deadlines.append(DeadlineCandidate(
            text=_str(item.get("text"), f"deadline_candidates[{i}].text"),
            evidence=evidence,
            normalized_date=normalized,
        ))

    def string_list(name: str) -> list[str]:
        value = payload[name]
        if not isinstance(value, list) or not all(isinstance(x, str) and x.strip() for x in value):
            raise SummaryValidationError(f"{name} must be a list of non-empty strings")
        return [x.strip() for x in value]

    # Critical disposition fields are application-owned and cannot be widened by model payload.
    return PreliminaryRegulatorySummary(
        publication_id=publication.metadata.publication_id,
        title=publication.metadata.title,
        executive_summary=_str(payload["executive_summary"], "executive_summary"),
        source_facts=claims,
        candidate_affected_areas=string_list("candidate_affected_areas"),
        deadline_candidates=deadlines,
        missing_information=string_list("missing_information"),
        uncertainties=string_list("uncertainties"),
    )
