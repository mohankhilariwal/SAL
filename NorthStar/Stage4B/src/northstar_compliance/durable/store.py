from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from northstar_compliance.graph.models import GraphExecutionState, ReviewDecision


class DurableStoreError(RuntimeError):
    pass


class StateIntegrityError(DurableStoreError):
    pass


class RevisionConflict(DurableStoreError):
    pass


class LeaseUnavailable(DurableStoreError):
    pass


def utc_iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def canonical(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(data: Any) -> str:
    return hashlib.sha256(canonical(data).encode("utf-8")).hexdigest()


class DurableStore:
    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=5, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=FULL")
        return conn

    @contextmanager
    def tx(self) -> Iterator[sqlite3.Connection]:
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            yield conn
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    def _init(self) -> None:
        with self._connect() as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS workflow_runs(
              run_id TEXT PRIMARY KEY,
              graph_id TEXT NOT NULL,
              graph_version TEXT NOT NULL,
              current_node TEXT NOT NULL,
              status TEXT NOT NULL,
              state_json TEXT NOT NULL,
              state_sha256 TEXT NOT NULL,
              revision INTEGER NOT NULL DEFAULT 0,
              lease_owner TEXT,
              lease_expires_at TEXT,
              updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS approval_waits(
              wait_id TEXT PRIMARY KEY,
              run_id TEXT NOT NULL UNIQUE REFERENCES workflow_runs(run_id),
              review_request_id TEXT NOT NULL UNIQUE,
              initiated_by TEXT NOT NULL,
              required_role TEXT NOT NULL,
              status TEXT NOT NULL,
              expires_at TEXT NOT NULL,
              token_nonce TEXT NOT NULL,
              token_digest TEXT NOT NULL,
              decision_id TEXT UNIQUE,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS approval_decisions(
              decision_id TEXT PRIMARY KEY,
              wait_id TEXT NOT NULL UNIQUE REFERENCES approval_waits(wait_id),
              run_id TEXT NOT NULL,
              decision TEXT NOT NULL CHECK(decision IN ('approved','rejected')),
              reviewer_id TEXT NOT NULL,
              reviewer_roles_json TEXT NOT NULL,
              reason TEXT,
              issued_at TEXT NOT NULL,
              token_nonce TEXT NOT NULL UNIQUE,
              payload_json TEXT NOT NULL,
              payload_sha256 TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS tool_effects(
              idempotency_key TEXT PRIMARY KEY,
              tool_id TEXT NOT NULL,
              result_json TEXT NOT NULL,
              created_at TEXT NOT NULL
            );
            """)

    def create_run(self, state: GraphExecutionState, now: datetime) -> None:
        payload = state.to_dict()
        with self.tx() as conn:
            conn.execute(
                "INSERT INTO workflow_runs(run_id,graph_id,graph_version,current_node,status,state_json,state_sha256,updated_at) VALUES(?,?,?,?,?,?,?,?)",
                (state.run_state.run_id, state.graph_id, state.graph_version, state.current_node,
                 state.graph_status, canonical(payload), digest(payload), utc_iso(now)),
            )

    def load_run(self, run_id: str) -> tuple[GraphExecutionState, int]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM workflow_runs WHERE run_id=?", (run_id,)).fetchone()
        if row is None:
            raise DurableStoreError("run_not_found")
        raw = json.loads(row["state_json"])
        if digest(raw) != row["state_sha256"]:
            raise StateIntegrityError("state_checksum_mismatch")
        return GraphExecutionState.from_dict(raw), int(row["revision"])

    def save_run(self, state: GraphExecutionState, expected_revision: int, now: datetime) -> int:
        payload = state.to_dict()
        with self.tx() as conn:
            cur = conn.execute(
                """UPDATE workflow_runs SET graph_id=?,graph_version=?,current_node=?,status=?,state_json=?,state_sha256=?,revision=revision+1,updated_at=?
                   WHERE run_id=? AND revision=?""",
                (state.graph_id, state.graph_version, state.current_node, state.graph_status,
                 canonical(payload), digest(payload), utc_iso(now), state.run_state.run_id, expected_revision),
            )
            if cur.rowcount != 1:
                raise RevisionConflict("run_revision_conflict")
            return expected_revision + 1

    def acquire_lease(self, run_id: str, owner: str, now: datetime, lease_seconds: int) -> None:
        expires = datetime.fromtimestamp(now.timestamp() + lease_seconds, tz=timezone.utc)
        with self.tx() as conn:
            cur = conn.execute(
                """UPDATE workflow_runs SET lease_owner=?,lease_expires_at=?
                   WHERE run_id=? AND (lease_owner IS NULL OR lease_expires_at<=? OR lease_owner=?)""",
                (owner, utc_iso(expires), run_id, utc_iso(now), owner),
            )
            if cur.rowcount != 1:
                raise LeaseUnavailable("resume_lease_unavailable")

    def release_lease(self, run_id: str, owner: str) -> None:
        with self.tx() as conn:
            conn.execute("UPDATE workflow_runs SET lease_owner=NULL,lease_expires_at=NULL WHERE run_id=? AND lease_owner=?", (run_id, owner))

    def ensure_tool_effect(self, key: str, tool_id: str, result: dict[str, Any], now: datetime) -> tuple[dict[str, Any], bool]:
        with self.tx() as conn:
            existing = conn.execute("SELECT result_json FROM tool_effects WHERE idempotency_key=?", (key,)).fetchone()
            if existing:
                return json.loads(existing["result_json"]), False
            conn.execute("INSERT INTO tool_effects VALUES(?,?,?,?)", (key, tool_id, canonical(result), utc_iso(now)))
            return result, True

    def tool_effect_count(self, tool_id: str) -> int:
        with self._connect() as conn:
            return int(conn.execute("SELECT count(*) FROM tool_effects WHERE tool_id=?", (tool_id,)).fetchone()[0])

    def ensure_wait(self, *, wait_id: str, run_id: str, review_request_id: str, initiated_by: str,
                    required_role: str, expires_at: datetime, token_nonce: str, token_digest: str,
                    now: datetime) -> dict[str, Any]:
        with self.tx() as conn:
            row = conn.execute("SELECT * FROM approval_waits WHERE run_id=?", (run_id,)).fetchone()
            if row:
                return dict(row)
            conn.execute(
                """INSERT INTO approval_waits(wait_id,run_id,review_request_id,initiated_by,required_role,status,expires_at,
                   token_nonce,token_digest,created_at,updated_at) VALUES(?,?,?,?,?,'pending',?,?,?,?,?)""",
                (wait_id, run_id, review_request_id, initiated_by, required_role, utc_iso(expires_at),
                 token_nonce, token_digest, utc_iso(now), utc_iso(now)),
            )
            return dict(conn.execute("SELECT * FROM approval_waits WHERE wait_id=?", (wait_id,)).fetchone())

    def rotate_wait_token(self, wait_id: str, nonce: str, token_digest: str, now: datetime) -> None:
        with self.tx() as conn:
            cur = conn.execute(
                "UPDATE approval_waits SET token_nonce=?,token_digest=?,updated_at=? WHERE wait_id=? AND status='pending'",
                (nonce, token_digest, utc_iso(now), wait_id),
            )
            if cur.rowcount != 1:
                raise DurableStoreError("wait_not_pending")

    def load_wait(self, wait_id: str | None = None, run_id: str | None = None) -> dict[str, Any]:
        if not wait_id and not run_id:
            raise ValueError("wait_id_or_run_id_required")
        sql, value = ("SELECT * FROM approval_waits WHERE wait_id=?", wait_id) if wait_id else ("SELECT * FROM approval_waits WHERE run_id=?", run_id)
        with self._connect() as conn:
            row = conn.execute(sql, (value,)).fetchone()
        if not row:
            raise DurableStoreError("wait_not_found")
        return dict(row)

    def record_decision(self, decision: ReviewDecision, *, expected_token_digest: str, now: datetime) -> ReviewDecision:
        with self.tx() as conn:
            wait = conn.execute("SELECT * FROM approval_waits WHERE wait_id=?", (decision.wait_id,)).fetchone()
            if not wait:
                raise DurableStoreError("wait_not_found")
            if wait["run_id"] != decision.run_id:
                raise DurableStoreError("run_wait_mismatch")
            existing = conn.execute("SELECT * FROM approval_decisions WHERE wait_id=?", (decision.wait_id,)).fetchone()
            if existing:
                raise DurableStoreError("decision_already_recorded")
            if wait["status"] != "pending":
                raise DurableStoreError("wait_not_pending")
            if parse_utc(wait["expires_at"]) <= now:
                raise DurableStoreError("wait_expired")
            if wait["token_nonce"] != decision.token_nonce or wait["token_digest"] != expected_token_digest:
                raise DurableStoreError("token_not_active")
            if decision.reviewer_id == wait["initiated_by"]:
                raise DurableStoreError("separation_of_duties_violation")
            if wait["required_role"] not in decision.reviewer_roles:
                raise DurableStoreError("reviewer_role_missing")
            if decision.decision not in {"approved", "rejected"}:
                raise DurableStoreError("invalid_decision")
            if decision.decision == "rejected" and not (decision.reason or "").strip():
                raise DurableStoreError("rejection_reason_required")
            payload = asdict(decision)
            conn.execute(
                """INSERT INTO approval_decisions(decision_id,wait_id,run_id,decision,reviewer_id,reviewer_roles_json,reason,issued_at,
                   token_nonce,payload_json,payload_sha256) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                (decision.decision_id, decision.wait_id, decision.run_id, decision.decision, decision.reviewer_id,
                 canonical(decision.reviewer_roles), decision.reason, decision.issued_at, decision.token_nonce,
                 canonical(payload), digest(payload)),
            )
            conn.execute("UPDATE approval_waits SET status='decided',decision_id=?,updated_at=? WHERE wait_id=?",
                         (decision.decision_id, utc_iso(now), decision.wait_id))
            return decision

    def load_decision(self, wait_id: str) -> ReviewDecision:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM approval_decisions WHERE wait_id=?", (wait_id,)).fetchone()
        if not row:
            raise DurableStoreError("decision_not_found")
        payload = json.loads(row["payload_json"])
        if digest(payload) != row["payload_sha256"]:
            raise StateIntegrityError("decision_checksum_mismatch")
        return ReviewDecision(**payload)

    def expire_wait(self, wait_id: str, now: datetime) -> bool:
        with self.tx() as conn:
            cur = conn.execute(
                "UPDATE approval_waits SET status='expired',updated_at=? WHERE wait_id=? AND status='pending' AND expires_at<=?",
                (utc_iso(now), wait_id, utc_iso(now)),
            )
            return cur.rowcount == 1
