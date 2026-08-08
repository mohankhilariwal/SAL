from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from .models import ImpactClass, RetryPolicy, ToolDescriptor
from .utils import sha256_json


class ToolRegistryError(ValueError):
    pass


class ToolRegistry:
    def __init__(self, descriptors: Iterable[ToolDescriptor]):
        self._by_key: dict[tuple[str, str], ToolDescriptor] = {}
        self._latest: dict[str, ToolDescriptor] = {}
        for descriptor in descriptors:
            key = (descriptor.tool_id, descriptor.version)
            if key in self._by_key:
                raise ToolRegistryError(f"duplicate tool descriptor: {key}")
            if descriptor.impact_class in {
                ImpactClass.IRREVERSIBLE_WRITE,
                ImpactClass.PRIVILEGED_REGULATED,
            }:
                raise ToolRegistryError(
                    f"Stage 3A refuses high-impact tool registration: {descriptor.tool_id}"
                )
            self._by_key[key] = descriptor
            current = self._latest.get(descriptor.tool_id)
            if current is None or descriptor.version > current.version:
                self._latest[descriptor.tool_id] = descriptor

    @classmethod
    def load(cls, directory: Path) -> "ToolRegistry":
        meta_path = directory / "tool-descriptor.schema.json"
        meta_schema = json.loads(meta_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(meta_schema)
        validator = Draft202012Validator(meta_schema)
        descriptors: list[ToolDescriptor] = []
        for path in sorted(directory.glob("TOOL-*.json")):
            raw = json.loads(path.read_text(encoding="utf-8"))
            try:
                validator.validate(raw)
            except ValidationError as exc:
                raise ToolRegistryError(f"invalid descriptor {path.name}: {exc.message}") from exc
            descriptor_hash = sha256_json(raw)
            retry = raw["retry_policy"]
            descriptors.append(
                ToolDescriptor(
                    schema_version=raw["schema_version"],
                    tool_id=raw["tool_id"],
                    name=raw["name"],
                    version=raw["version"],
                    description=raw["description"],
                    impact_class=ImpactClass(raw["impact_class"]),
                    input_schema=raw["input_schema"],
                    output_schema=raw["output_schema"],
                    allowed_groups=tuple(raw["allowed_groups"]),
                    allowed_purposes=tuple(raw["allowed_purposes"]),
                    allowed_residencies=tuple(raw["allowed_residencies"]),
                    timeout_ms=int(raw["timeout_ms"]),
                    max_result_bytes=int(raw["max_result_bytes"]),
                    idempotency_required=bool(raw["idempotency_required"]),
                    approval_required=bool(raw["approval_required"]),
                    retry_policy=RetryPolicy(
                        max_attempts=int(retry["max_attempts"]),
                        retryable_errors=tuple(retry["retryable_errors"]),
                    ),
                    sensitive_input_fields=tuple(raw.get("sensitive_input_fields", [])),
                    descriptor_hash=descriptor_hash,
                )
            )
        if not descriptors:
            raise ToolRegistryError(f"no TOOL-*.json descriptors found in {directory}")
        return cls(descriptors)

    def resolve(self, tool_id: str, version: str) -> ToolDescriptor:
        try:
            return self._by_key[(tool_id, version)]
        except KeyError as exc:
            if tool_id in self._latest:
                raise ToolRegistryError(
                    f"tool version mismatch for {tool_id}: requested {version}, "
                    f"available {self._latest[tool_id].version}"
                ) from exc
            raise ToolRegistryError(f"unknown tool: {tool_id}") from exc

    def all(self) -> tuple[ToolDescriptor, ...]:
        return tuple(self._by_key[key] for key in sorted(self._by_key))
