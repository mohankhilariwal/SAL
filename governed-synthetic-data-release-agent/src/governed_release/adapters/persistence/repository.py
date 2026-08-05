from __future__ import annotations

import json

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from governed_release.adapters.persistence.models import (
    ApprovalRecord,
    AuditRecord,
    Base,
    KillSwitchRecord,
    WorkflowRecord,
)
from governed_release.domain.models import ApprovalDecision, AuditEvent, WorkflowState, utcnow


class Database:
    def __init__(self, url: str) -> None:
        connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
        self.engine = create_engine(url, connect_args=connect_args)
        self.sessions = sessionmaker(self.engine, expire_on_commit=False)

    def create(self) -> None:
        Base.metadata.create_all(self.engine)

    def drop(self) -> None:
        Base.metadata.drop_all(self.engine)


class SQLAlchemyWorkflowStore:
    def __init__(self, database: Database) -> None:
        self.database = database

    def save(self, state: WorkflowState) -> None:
        payload = state.model_dump_json()
        with self.database.sessions.begin() as session:
            record = session.get(WorkflowRecord, state.workflow_id)
            if record is None:
                record = WorkflowRecord(
                    workflow_id=state.workflow_id,
                    request_id=state.request_id,
                    trace_id=state.trace_id,
                    scenario=state.request.scenario.value,
                    state=state.stage.value,
                    decision=state.decision.value if state.decision else None,
                    payload_json=payload,
                    created_at=state.created_at,
                    updated_at=state.updated_at,
                )
                session.add(record)
            else:
                record.state = state.stage.value
                record.decision = state.decision.value if state.decision else None
                record.payload_json = payload
                record.updated_at = state.updated_at

    def get(self, workflow_id: str) -> WorkflowState:
        with self.database.sessions() as session:
            record = session.get(WorkflowRecord, workflow_id)
            if record is None:
                raise KeyError(f"Unknown workflow: {workflow_id}")
            return WorkflowState.model_validate_json(record.payload_json)

    def list(self) -> list[WorkflowState]:
        with self.database.sessions() as session:
            records = session.scalars(
                select(WorkflowRecord).order_by(WorkflowRecord.created_at.desc())
            )
            return [WorkflowState.model_validate_json(r.payload_json) for r in records]

    def add_approval(self, approval: ApprovalDecision) -> None:
        with self.database.sessions.begin() as session:
            duplicate = session.scalar(
                select(ApprovalRecord).where(
                    ApprovalRecord.workflow_id == approval.workflow_id,
                    ApprovalRecord.role == approval.role.value,
                    ApprovalRecord.candidate_version == approval.candidate_version,
                )
            )
            if duplicate is not None:
                raise ValueError(f"Approval for role {approval.role.value} already exists")
            session.add(
                ApprovalRecord(
                    workflow_id=approval.workflow_id,
                    approval_id=approval.id,
                    role=approval.role.value,
                    approver_id=approval.approver_id,
                    decision=approval.outcome.value,
                    comment=approval.comment,
                    evidence_json=json.dumps(approval.evidence_viewed),
                    request_version=approval.request_version,
                    candidate_version=approval.candidate_version,
                    created_at=approval.created_at,
                )
            )

    def switch_enabled(self, name: str) -> bool:
        with self.database.sessions() as session:
            record = session.get(KillSwitchRecord, name)
            return bool(record.enabled) if record else False

    def set_switch(self, name: str, enabled: bool, reason: str, updated_by: str) -> None:
        with self.database.sessions.begin() as session:
            record = session.get(KillSwitchRecord, name)
            if record is None:
                record = KillSwitchRecord(
                    name=name,
                    enabled=enabled,
                    reason=reason,
                    updated_by=updated_by,
                    updated_at=utcnow(),
                )
                session.add(record)
            else:
                record.enabled = enabled
                record.reason = reason
                record.updated_by = updated_by
                record.updated_at = utcnow()


class SQLAlchemyAuditStore:
    def __init__(self, database: Database) -> None:
        self.database = database

    def append(self, event: AuditEvent) -> None:
        with self.database.sessions.begin() as session:
            session.add(
                AuditRecord(
                    event_id=event.id,
                    workflow_id=event.workflow_id,
                    trace_id=event.trace_id,
                    event_type=event.event_type,
                    payload_json=json.dumps(event.payload, sort_keys=True, default=str),
                    previous_hash=event.previous_hash,
                    event_hash=event.event_hash,
                    created_at=event.created_at,
                )
            )

    def last_hash(self) -> str:
        with self.database.sessions() as session:
            record = session.scalar(select(AuditRecord).order_by(AuditRecord.id.desc()).limit(1))
            return record.event_hash if record else "0" * 64

    def events_for_workflow(self, workflow_id: str) -> list[AuditEvent]:
        with self.database.sessions() as session:
            records = session.scalars(
                select(AuditRecord)
                .where(AuditRecord.workflow_id == workflow_id)
                .order_by(AuditRecord.id)
            )
            return [
                AuditEvent(
                    id=r.event_id,
                    workflow_id=r.workflow_id,
                    trace_id=r.trace_id,
                    event_type=r.event_type,
                    payload=json.loads(r.payload_json),
                    previous_hash=r.previous_hash,
                    event_hash=r.event_hash,
                    created_at=r.created_at,
                    updated_at=r.created_at,
                )
                for r in records
            ]

    def all_records(self) -> list[AuditRecord]:
        with self.database.sessions() as session:
            return list(session.scalars(select(AuditRecord).order_by(AuditRecord.id)))
