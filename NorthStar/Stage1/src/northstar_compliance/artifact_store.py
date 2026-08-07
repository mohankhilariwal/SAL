from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .intake import Publication
from .schemas import ModelInvocationRecord, PreliminaryRegulatorySummary


class ArtifactStoreError(RuntimeError):
    pass


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


class LocalArtifactStore:
    """Tutorial persistence only; not an enterprise records or audit ledger."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def persist(
        self,
        publication: Publication,
        summary: PreliminaryRegulatorySummary,
        invocation: ModelInvocationRecord,
    ) -> Path:
        target = self.root / publication.metadata.publication_id
        try:
            _atomic_write(target / "source.txt", publication.text.encode("utf-8"))
            _atomic_write(target / "metadata.json", json.dumps(asdict(publication.metadata), indent=2, sort_keys=True).encode("utf-8"))
            _atomic_write(target / "summary.json", json.dumps(summary.to_dict(), indent=2, sort_keys=True).encode("utf-8"))
            _atomic_write(target / "model-invocation.json", json.dumps(invocation.to_dict(), indent=2, sort_keys=True).encode("utf-8"))
        except OSError as exc:
            raise ArtifactStoreError(f"Could not persist Stage 1 artifacts: {exc}") from exc
        return target
