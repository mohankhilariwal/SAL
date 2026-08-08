from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from northstar_compliance.common.jsonutil import canonical_json
from northstar_compliance.harness.models import WorkspaceManifest


class WorkspaceError(RuntimeError):
    pass


_SAFE_ID = re.compile(r"^[A-Z0-9_-]{4,80}$")
_FORBIDDEN_KEY_PARTS = ("approval_token", "secret", "password", "authorization", "cookie", "chain_of_thought", "hidden_reasoning")


def _contains_forbidden_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            if any(part in lowered for part in _FORBIDDEN_KEY_PARTS):
                if child != "[REDACTED]":
                    return True
                continue
            if _contains_forbidden_key(child):
                return True
    elif isinstance(value, list):
        return any(_contains_forbidden_key(item) for item in value)
    return False


class SessionWorkspace:
    def __init__(self, root: Path, manifest: WorkspaceManifest):
        self.root = root
        self.manifest = manifest

    def _resolve(self, relative_path: str) -> Path:
        candidate = (self.root / relative_path).resolve()
        if self.root.resolve() not in candidate.parents and candidate != self.root.resolve():
            raise WorkspaceError("workspace_path_escape")
        if candidate.suffix not in self.manifest.allowed_suffixes:
            raise WorkspaceError("workspace_suffix_not_allowed")
        return candidate

    def _workspace_size(self) -> int:
        return sum(p.stat().st_size for p in self.root.rglob("*") if p.is_file())

    def write_json(self, relative_path: str, value: Any) -> Path:
        if _contains_forbidden_key(value):
            raise WorkspaceError("forbidden_sensitive_field")
        payload = canonical_json(value) + "\n"
        if len(payload.encode("utf-8")) > self.manifest.max_file_bytes:
            raise WorkspaceError("workspace_file_too_large")
        if self._workspace_size() + len(payload.encode("utf-8")) > self.manifest.max_workspace_bytes:
            raise WorkspaceError("workspace_quota_exceeded")
        path = self._resolve(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
        return path

    def append_jsonl(self, relative_path: str, value: Any) -> Path:
        if _contains_forbidden_key(value):
            raise WorkspaceError("forbidden_sensitive_field")
        payload = canonical_json(value) + "\n"
        if len(payload.encode("utf-8")) > self.manifest.max_file_bytes:
            raise WorkspaceError("workspace_file_too_large")
        if self._workspace_size() + len(payload.encode("utf-8")) > self.manifest.max_workspace_bytes:
            raise WorkspaceError("workspace_quota_exceeded")
        path = self._resolve(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(payload)
        return path


class WorkspaceManager:
    def __init__(self, root: str | Path, *, max_file_bytes: int = 64_000, max_workspace_bytes: int = 1_000_000):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.max_file_bytes = max_file_bytes
        self.max_workspace_bytes = max_workspace_bytes

    def create(self, session_id: str, created_at: str) -> SessionWorkspace:
        if not _SAFE_ID.fullmatch(session_id):
            raise WorkspaceError("invalid_session_id")
        path = (self.root / "sessions" / session_id).resolve()
        if self.root not in path.parents:
            raise WorkspaceError("workspace_path_escape")
        path.mkdir(parents=True, exist_ok=False)
        manifest = WorkspaceManifest(
            schema_version="1.0.0",
            session_id=session_id,
            root_relative_path=str(path.relative_to(self.root)),
            allowed_suffixes=(".json", ".jsonl"),
            max_file_bytes=self.max_file_bytes,
            max_workspace_bytes=self.max_workspace_bytes,
            created_at=created_at,
        )
        workspace = SessionWorkspace(path, manifest)
        workspace.write_json("workspace-manifest.json", manifest.to_dict())
        return workspace

    def open(self, session_id: str, created_at: str = "") -> SessionWorkspace:
        if not _SAFE_ID.fullmatch(session_id):
            raise WorkspaceError("invalid_session_id")
        path = (self.root / "sessions" / session_id).resolve()
        if not path.is_dir():
            raise WorkspaceError("workspace_not_found")
        manifest_data = json.loads((path / "workspace-manifest.json").read_text(encoding="utf-8"))
        manifest_data["allowed_suffixes"] = tuple(manifest_data["allowed_suffixes"])
        return SessionWorkspace(path, WorkspaceManifest(**manifest_data))
