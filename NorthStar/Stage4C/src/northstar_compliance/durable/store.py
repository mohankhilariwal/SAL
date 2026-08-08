from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Iterator

from northstar_compliance.common.jsonutil import canonical_json, isoformat_utc, parse_utc, sha256_text
from northstar_compliance.graph.models import AgentRunState


class DurableStoreError(RuntimeError):
    pass


class DurableStore:
    """Local transactional adapter for DATA-058 through DATA-062 and DATA-066."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS workflows (
                    run_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    graph_id TEXT NOT NULL,
                    graph_version TEXT NOT NULL,
                    state_json TEXT NOT NULL,
                    state_sha256 TEXT NOT NULL,
                    revision INTEGER NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS waits (
                    wait_id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL UNIQUE,
                    review_request_id TEXT NOT NULL UNIQUE,
                    required_role TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    status TEXT NOT NULL,
                    token_digest TEXT NOT NULL,
                    active_nonce TEXT NOT NULL,
                    decision_id TEXT,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(run_id) REFERENCES workflows(run_id)
                );
                CREATE TABLE IF NOT EXISTS decisions (
                    decision_id TEXT PRIMARY KEY,
                    wait_id TEXT NOT NULL UNIQUE,
                    reviewer_id TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    decided_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    payload_sha256 TEXT NOT NULL,
                    FOREIGN KEY(wait_id) REFERENCES waits(wait_id)
                );
                CREATE TABLE IF NOT EXISTS leases (
                    run_id TEXT PRIMARY KEY,
                    worker_id TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    FOREIGN KEY(run_id) REFERENCES workflows(run_id)
                );
                CREATE TABLE IF NOT EXISTS tool_effects (
                    tool_id TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    PRIMARY KEY(tool_id, idempotency_key)
                );
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    initiator_id TEXT NOT NULL,
                    manifest_digest TEXT NOT NULL,
                    trace_id TEXT NOT NULL,
                    workspace_path TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """
            )

    def save_workflow(self, state: AgentRunState, *, expected_revision: int | None = None) -> int:
        payload = canonical_json(state.to_dict())
        digest = sha256_text(payload)
        with self.transaction() as conn:
            row = conn.execute("SELECT revision FROM workflows WHERE run_id=?", (state.run_id,)).fetchone()
            if row is None:
                if expected_revision not in (None, 0):
                    raise DurableStoreError("workflow_revision_conflict")
                revision = 1
                conn.execute(
                    "INSERT INTO workflows VALUES (?,?,?,?,?,?,?,?)",
                    (state.run_id, state.session_id, state.graph_id, state.graph_version, payload, digest, revision, state.updated_at),
                )
            else:
                current = int(row["revision"])
                if expected_revision is not None and current != expected_revision:
                    raise DurableStoreError("workflow_revision_conflict")
                revision = current + 1
                conn.execute(
                    "UPDATE workflows SET session_id=?,graph_id=?,graph_version=?,state_json=?,state_sha256=?,revision=?,updated_at=? WHERE run_id=?",
                    (state.session_id, state.graph_id, state.graph_version, payload, digest, revision, state.updated_at, state.run_id),
                )
        return revision

    def load_workflow(self, run_id: str) -> tuple[AgentRunState, int]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM workflows WHERE run_id=?", (run_id,)).fetchone()
        if row is None:
            raise DurableStoreError("workflow_not_found")
        payload = row["state_json"]
        if sha256_text(payload) != row["state_sha256"]:
            raise DurableStoreError("workflow_checksum_mismatch")
        state = AgentRunState.from_dict(json.loads(payload))
        if state.graph_id != row["graph_id"] or state.graph_version != row["graph_version"]:
            raise DurableStoreError("workflow_graph_metadata_mismatch")
        return state, int(row["revision"])

    def create_wait(self, value: dict[str, Any]) -> None:
        with self.transaction() as conn:
            conn.execute(
                "INSERT INTO waits(wait_id,run_id,review_request_id,required_role,expires_at,status,token_digest,active_nonce,decision_id,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (
                    value["wait_id"], value["run_id"], value["review_request_id"], value["required_role"],
                    value["expires_at"], value["status"], value["token_digest"], value["active_nonce"], None, value["updated_at"],
                ),
            )

    def get_wait(self, wait_id: str) -> dict[str, Any]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM waits WHERE wait_id=?", (wait_id,)).fetchone()
        if row is None:
            raise DurableStoreError("wait_not_found")
        return dict(row)

    def get_wait_by_run(self, run_id: str) -> dict[str, Any]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM waits WHERE run_id=?", (run_id,)).fetchone()
        if row is None:
            raise DurableStoreError("wait_not_found")
        return dict(row)

    def persist_decision(self, wait_id: str, decision_payload: dict[str, Any], *, expected_nonce: str, now: str) -> None:
        payload = canonical_json(decision_payload)
        digest = sha256_text(payload)
        with self.transaction() as conn:
            row = conn.execute("SELECT * FROM waits WHERE wait_id=?", (wait_id,)).fetchone()
            if row is None:
                raise DurableStoreError("wait_not_found")
            if row["status"] != "pending" or row["decision_id"] is not None:
                raise DurableStoreError("wait_not_pending")
            if row["active_nonce"] != expected_nonce:
                raise DurableStoreError("inactive_token")
            conn.execute(
                "INSERT INTO decisions VALUES (?,?,?,?,?,?,?,?)",
                (
                    decision_payload["decision_id"], wait_id, decision_payload["reviewer_id"],
                    decision_payload["decision"], decision_payload["reason"], decision_payload["decided_at"], payload, digest,
                ),
            )
            conn.execute(
                "UPDATE waits SET status='decided',decision_id=?,updated_at=? WHERE wait_id=?",
                (decision_payload["decision_id"], now, wait_id),
            )

    def load_decision(self, decision_id: str) -> dict[str, Any]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM decisions WHERE decision_id=?", (decision_id,)).fetchone()
        if row is None:
            raise DurableStoreError("decision_not_found")
        payload = row["payload_json"]
        if sha256_text(payload) != row["payload_sha256"]:
            raise DurableStoreError("decision_checksum_mismatch")
        return json.loads(payload)

    def mark_wait_expired(self, wait_id: str, now: str) -> None:
        with self.transaction() as conn:
            row = conn.execute("SELECT status FROM waits WHERE wait_id=?", (wait_id,)).fetchone()
            if row is None:
                raise DurableStoreError("wait_not_found")
            if row["status"] == "pending":
                conn.execute("UPDATE waits SET status='expired',updated_at=? WHERE wait_id=?", (now, wait_id))

    def acquire_lease(self, run_id: str, worker_id: str, now: datetime, ttl_seconds: int = 30) -> None:
        expiry = isoformat_utc(now + timedelta(seconds=ttl_seconds))
        now_s = isoformat_utc(now)
        with self.transaction() as conn:
            row = conn.execute("SELECT * FROM leases WHERE run_id=?", (run_id,)).fetchone()
            if row is not None and parse_utc(row["expires_at"]) > now and row["worker_id"] != worker_id:
                raise DurableStoreError("resume_lease_unavailable")
            conn.execute(
                "INSERT INTO leases(run_id,worker_id,expires_at) VALUES (?,?,?) ON CONFLICT(run_id) DO UPDATE SET worker_id=excluded.worker_id,expires_at=excluded.expires_at",
                (run_id, worker_id, expiry),
            )

    def release_lease(self, run_id: str, worker_id: str) -> None:
        with self.transaction() as conn:
            conn.execute("DELETE FROM leases WHERE run_id=? AND worker_id=?", (run_id, worker_id))

    def get_tool_effect(self, tool_id: str, idempotency_key: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute("SELECT result_json FROM tool_effects WHERE tool_id=? AND idempotency_key=?", (tool_id, idempotency_key)).fetchone()
        return None if row is None else json.loads(row["result_json"])

    def save_tool_effect(self, tool_id: str, idempotency_key: str, result: dict[str, Any]) -> None:
        with self.transaction() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO tool_effects(tool_id,idempotency_key,result_json) VALUES (?,?,?)",
                (tool_id, idempotency_key, canonical_json(result)),
            )

    def count_tool_effects(self, tool_id: str) -> int:
        with self._connect() as conn:
            return int(conn.execute("SELECT COUNT(*) FROM tool_effects WHERE tool_id=?", (tool_id,)).fetchone()[0])

    def create_session(self, value: dict[str, Any]) -> None:
        with self.transaction() as conn:
            conn.execute(
                "INSERT INTO sessions VALUES (?,?,?,?,?,?,?,?)",
                (value["session_id"], value["initiator_id"], value["manifest_digest"], value["trace_id"], value["workspace_path"], value["status"], value["created_at"], value["updated_at"]),
            )

    def load_session(self, session_id: str) -> dict[str, Any]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone()
        if row is None:
            raise DurableStoreError("session_not_found")
        return dict(row)

    def update_session_status(self, session_id: str, status: str, now: str) -> None:
        with self.transaction() as conn:
            conn.execute("UPDATE sessions SET status=?,updated_at=? WHERE session_id=?", (status, now, session_id))

    def table_names(self) -> set[str]:
        with self._connect() as conn:
            return {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
