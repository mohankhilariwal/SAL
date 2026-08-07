from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .artifact_store import LocalArtifactStore
from .intake import Publication
from .model_gateway import SummaryModel
from .schemas import ModelInvocationRecord, PreliminaryRegulatorySummary
from .validation import build_validated_summary


@dataclass(frozen=True)
class SummaryRunResult:
    summary: PreliminaryRegulatorySummary
    invocation: ModelInvocationRecord
    artifact_path: Path


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _invocation_id(publication: Publication, started_at: str) -> str:
    seed = f"{publication.metadata.publication_id}|{started_at}".encode("utf-8")
    return f"INV-{hashlib.sha256(seed).hexdigest()[:16].upper()}"


def run_summary(
    publication: Publication,
    *,
    model: SummaryModel,
    store: LocalArtifactStore,
) -> SummaryRunResult:
    started = _now()
    invocation_id = _invocation_id(publication, started)
    try:
        result = model.summarize(publication)
        summary = build_validated_summary(publication, result.payload)
        completed = _now()
        invocation = ModelInvocationRecord(
            invocation_id=invocation_id,
            provider=result.provider,
            model=result.model,
            prompt_version=summary.prompt_version,
            schema_version=summary.schema_version,
            started_at=started,
            completed_at=completed,
            input_sha256=publication.metadata.sha256,
            success=True,
            usage=result.usage,
        )
    except Exception as exc:
        completed = _now()
        failure = ModelInvocationRecord(
            invocation_id=invocation_id,
            provider=getattr(model, "provider", "unknown"),
            model=getattr(model, "model", "unknown"),
            prompt_version="stage1-summary-v1",
            schema_version="1.0.0",
            started_at=started,
            completed_at=completed,
            input_sha256=publication.metadata.sha256,
            success=False,
            error_type=type(exc).__name__,
            error_message=str(exc)[:1000],
        )
        # Failed invocations are intentionally surfaced. Stage 1 does not implement retries/fallback.
        raise RuntimeError(json.dumps(failure.to_dict(), sort_keys=True)) from exc
    artifact_path = store.persist(publication, summary, invocation)
    return SummaryRunResult(summary=summary, invocation=invocation, artifact_path=artifact_path)
