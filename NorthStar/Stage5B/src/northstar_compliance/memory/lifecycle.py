from __future__ import annotations

from dataclasses import dataclass

from .compaction import ContextCompactor
from .models import (
    CaseWorkingMemoryRecord,
    ContextSnapshot,
    MemoryConsentGrant,
    MemoryQuery,
    MemoryReadResult,
    Scope,
)
from .regeneration import ContextRegenerator
from .service import CaseWorkingMemoryService


@dataclass(frozen=True)
class ContextLifecycleResult:
    snapshot: ContextSnapshot
    memory_record: CaseWorkingMemoryRecord | None
    memory_read_result: MemoryReadResult | None


class ContextLifecycleEngine:
    """Coordinates regeneration, compaction and optional case-local continuity memory."""

    def __init__(
        self,
        regenerator: ContextRegenerator,
        compactor: ContextCompactor,
        memory_service: CaseWorkingMemoryService,
    ):
        self.regenerator = regenerator
        self.compactor = compactor
        self.memory_service = memory_service

    def start_or_resume(
        self,
        *,
        scope: Scope,
        case_state: dict,
        state_version: str,
        grant: MemoryConsentGrant | None = None,
        write_memory: bool = False,
        read_memory: bool = False,
        write_request_id: str | None = None,
        current_source_versions: dict[str, str] | None = None,
    ) -> ContextLifecycleResult:
        memory_read_result = None
        records = ()
        if read_memory:
            if grant is None:
                raise PermissionError("memory_read_requires_consent")
            query = MemoryQuery(
                query_id=f"MQ-{scope.case_id}-{state_version}",
                schema_version="1.0.0",
                scope=scope,
            )
            memory_read_result = self.memory_service.read(
                query=query,
                grant=grant,
                current_source_versions=current_source_versions or {},
            )
            records = memory_read_result.records

        regenerated = self.regenerator.regenerate(
            scope=scope,
            case_state=case_state,
            state_version=state_version,
            include_memory=read_memory,
            memory_records=records,
        )
        snapshot = self.compactor.compact(regenerated)
        memory_record = None
        if write_memory:
            if grant is None or write_request_id is None:
                raise PermissionError("memory_write_requires_consent_and_request_id")
            memory_record = self.memory_service.write_snapshot(
                snapshot=snapshot,
                grant=grant,
                write_request_id=write_request_id,
            )
        return ContextLifecycleResult(
            snapshot=snapshot,
            memory_record=memory_record,
            memory_read_result=memory_read_result,
        )
