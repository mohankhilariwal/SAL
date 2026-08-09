from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

from .models import EvidenceItem, ReconciliationResult


def reconcile_evidence(
    items: Iterable[EvidenceItem],
    required_ids: Iterable[str],
) -> ReconciliationResult:
    materialized = tuple(items)
    counts = Counter(item.evidence_id for item in materialized)
    by_id = {item.evidence_id: item for item in materialized}
    required = tuple(required_ids)

    duplicates = tuple(sorted(evidence_id for evidence_id, count in counts.items() if count > 1))
    invalid_authority = tuple(
        sorted(item.evidence_id for item in materialized if item.authority_effect != "none")
    )
    present = tuple(sorted(evidence_id for evidence_id in required if evidence_id in by_id))
    missing = tuple(sorted(evidence_id for evidence_id in required if evidence_id not in by_id))

    return ReconciliationResult(
        required_ids=required,
        present_ids=present,
        missing_ids=missing,
        duplicate_ids=duplicates,
        invalid_authority_ids=invalid_authority,
        complete=not missing and not duplicates and not invalid_authority,
    )
