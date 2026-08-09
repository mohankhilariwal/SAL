from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .models import ArtifactDescriptor


class ArtifactError(ValueError):
    pass


@dataclass(slots=True)
class InMemoryArtifactStore:
    _contents: dict[str, bytes]

    def __init__(self) -> None:
        self._contents = {}

    def put(self, descriptor: ArtifactDescriptor, content: bytes) -> None:
        if not descriptor.immutable:
            raise ArtifactError("mutable_artifact_prohibited")
        digest = hashlib.sha256(content).hexdigest()
        if digest != descriptor.content_sha256:
            raise ArtifactError("artifact_content_digest_mismatch")
        existing = self._contents.get(descriptor.artifact_id)
        if existing is not None and existing != content:
            raise ArtifactError("immutable_artifact_conflict")
        self._contents[descriptor.artifact_id] = content

    def get(self, descriptor: ArtifactDescriptor, *, subject_id: str, case_id: str) -> bytes:
        if descriptor.case_id != case_id:
            raise ArtifactError("artifact_case_scope_mismatch")
        if subject_id not in descriptor.authorized_subjects:
            raise ArtifactError("artifact_subject_not_authorized")
        try:
            content = self._contents[descriptor.artifact_id]
        except KeyError as exc:
            raise ArtifactError("artifact_not_found") from exc
        if hashlib.sha256(content).hexdigest() != descriptor.content_sha256:
            raise ArtifactError("artifact_tampered")
        return content
