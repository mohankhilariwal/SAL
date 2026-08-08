from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class RegistryError(RuntimeError):
    pass


class VersionedRegistry:
    def __init__(self, name: str):
        self.name = name
        self._entries: dict[str, Any] = {}
        self._frozen = False

    def register(self, key: str, value: Any) -> None:
        if self._frozen:
            raise RegistryError(f"registry_frozen:{self.name}")
        if key in self._entries:
            raise RegistryError(f"duplicate_registration:{key}")
        self._entries[key] = value

    def freeze(self) -> None:
        self._frozen = True

    def resolve(self, key: str) -> Any:
        try:
            return self._entries[key]
        except KeyError as exc:
            raise RegistryError(f"unregistered:{key}") from exc

    def keys(self) -> tuple[str, ...]:
        return tuple(sorted(self._entries))

    @property
    def frozen(self) -> bool:
        return self._frozen


@dataclass(frozen=True)
class AgentRegistration:
    agent_id: str
    version: str
    authority: str


@dataclass(frozen=True)
class GraphRegistration:
    graph_id: str
    version: str
