from __future__ import annotations

from pathlib import Path

from northstar_compliance.common.jsonutil import sha256_text
from northstar_compliance.harness.models import InstructionBundle


class InstructionError(RuntimeError):
    pass


class InstructionStore:
    """Versioned instruction text. It shapes model behavior but grants no authority."""

    def __init__(self, path: str | Path, *, name: str, version: str, expected_sha256: str | None = None):
        self.path = Path(path)
        self.name = name
        self.version = version
        self.expected_sha256 = expected_sha256

    def load(self) -> InstructionBundle:
        content = self.path.read_text(encoding="utf-8")
        digest = sha256_text(content)
        if self.expected_sha256 is not None and digest != self.expected_sha256:
            raise InstructionError("instruction_hash_mismatch")
        return InstructionBundle(
            schema_version="1.0.0",
            instruction_name=self.name,
            instruction_version=self.version,
            content=content,
            content_sha256=digest,
            critical_controls_external=True,
        )
