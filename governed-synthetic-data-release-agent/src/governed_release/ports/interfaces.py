from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

import pandas as pd

from governed_release.domain.models import (
    AuditEvent,
    PolicyDecision,
    PolicyInput,
    WorkflowState,
)


class PolicyDecisionPoint(Protocol):
    def evaluate(self, policy_input: PolicyInput) -> PolicyDecision: ...


class ModelGateway(Protocol):
    def interpret(self, text: str, *, trace_id: str) -> dict[str, Any]: ...
    def explain(self, facts: dict[str, Any], *, trace_id: str) -> str: ...


class SyntheticDataGenerator(Protocol):
    name: str

    def generate(
        self, source: pd.DataFrame, rows: int, seed: int, *, unsafe_mode: bool = False
    ) -> pd.DataFrame: ...


class WorkflowStore(Protocol):
    def save(self, state: WorkflowState) -> None: ...
    def get(self, workflow_id: str) -> WorkflowState: ...
    def list(self) -> list[WorkflowState]: ...


class AuditStore(Protocol):
    def append(self, event: AuditEvent) -> None: ...
    def last_hash(self) -> str: ...
    def events_for_workflow(self, workflow_id: str) -> list[AuditEvent]: ...
    def all_records(self) -> list[Any]: ...


class ExportGateway(Protocol):
    def release(self, state: WorkflowState, candidate_path: Path, evidence_dir: Path) -> Any: ...
