from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


@dataclass(frozen=True)
class ToolDescriptor:
    raw: dict[str, Any]
    descriptor_hash: str

    @property
    def tool_id(self) -> str:
        return str(self.raw["tool_id"])

    @property
    def version(self) -> str:
        return str(self.raw["version"])

    @property
    def impact_class(self) -> str:
        return str(self.raw["impact_class"])

    @property
    def input_schema(self) -> dict[str, Any]:
        return dict(self.raw["input_schema"])

    @property
    def output_schema(self) -> dict[str, Any]:
        return dict(self.raw["output_schema"])


class ToolRegistry:
    def __init__(self, descriptors: dict[tuple[str, str], ToolDescriptor]):
        self._descriptors = descriptors

    @classmethod
    def load(cls, directory: Path) -> "ToolRegistry":
        meta = json.loads((directory / "tool-descriptor.schema.json").read_text())
        validator = Draft202012Validator(meta)
        descriptors: dict[tuple[str, str], ToolDescriptor] = {}
        for path in sorted(directory.glob("TOOL-*.json")):
            raw = json.loads(path.read_text())
            validator.validate(raw)
            if raw["impact_class"] not in {"read_only", "reversible_write"}:
                raise ValueError(f"Unsupported impact class for {raw['tool_id']}")
            canonical = json.dumps(raw, sort_keys=True, separators=(",", ":")).encode()
            descriptor = ToolDescriptor(raw=raw, descriptor_hash=hashlib.sha256(canonical).hexdigest())
            key = (descriptor.tool_id, descriptor.version)
            if key in descriptors:
                raise ValueError(f"Duplicate descriptor {key}")
            descriptors[key] = descriptor
        if len(descriptors) != 6:
            raise ValueError(f"Expected six descriptors, found {len(descriptors)}")
        return cls(descriptors)

    def resolve(self, tool_id: str, version: str) -> ToolDescriptor:
        exact = self._descriptors.get((tool_id, version))
        if exact:
            return exact
        versions = [v for (tid, v) in self._descriptors if tid == tool_id]
        if versions:
            raise LookupError(f"version_mismatch:{tool_id}:{version}")
        raise KeyError(f"not_found:{tool_id}")

    def list_descriptors(self) -> list[ToolDescriptor]:
        return [self._descriptors[key] for key in sorted(self._descriptors)]

    def model_view(self) -> list[dict[str, Any]]:
        return [
            {
                "tool_id": d.tool_id,
                "version": d.version,
                "name": d.raw["name"],
                "description": d.raw["description"],
                "impact_class": d.impact_class,
                "input_schema": d.input_schema,
            }
            for d in self.list_descriptors()
        ]
