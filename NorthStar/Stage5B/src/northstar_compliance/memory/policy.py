from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class MemoryPolicy:
    enabled: bool
    allowed_memory_kinds: tuple[str, ...]
    requires_opt_in: bool
    default_ttl_days: int
    max_ttl_days: int
    max_records_per_case: int
    max_facts_per_record: int
    max_value_chars: int
    context_target_items: int
    context_target_chars: int
    hard_max_items: int
    hard_max_chars: int
    allow_cross_case_recall: bool
    allow_user_profile_memory: bool
    allow_semantic_memory: bool
    allow_episodic_memory: bool
    allow_organizational_memory: bool
    allow_shared_agent_memory: bool
    allowed_fact_origins: tuple[str, ...]

    @classmethod
    def from_file(cls, path: str | Path) -> "MemoryPolicy":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            enabled=bool(raw["enabled"]),
            allowed_memory_kinds=tuple(raw["allowed_memory_kinds"]),
            requires_opt_in=bool(raw["requires_opt_in"]),
            default_ttl_days=int(raw["default_ttl_days"]),
            max_ttl_days=int(raw["max_ttl_days"]),
            max_records_per_case=int(raw["max_records_per_case"]),
            max_facts_per_record=int(raw["max_facts_per_record"]),
            max_value_chars=int(raw["max_value_chars"]),
            context_target_items=int(raw["context_target_items"]),
            context_target_chars=int(raw["context_target_chars"]),
            hard_max_items=int(raw["hard_max_items"]),
            hard_max_chars=int(raw["hard_max_chars"]),
            allow_cross_case_recall=bool(raw["allow_cross_case_recall"]),
            allow_user_profile_memory=bool(raw["allow_user_profile_memory"]),
            allow_semantic_memory=bool(raw["allow_semantic_memory"]),
            allow_episodic_memory=bool(raw["allow_episodic_memory"]),
            allow_organizational_memory=bool(raw["allow_organizational_memory"]),
            allow_shared_agent_memory=bool(raw["allow_shared_agent_memory"]),
            allowed_fact_origins=tuple(raw["allowed_fact_origins"]),
        )

    def validate_boundary(self) -> None:
        if not self.enabled:
            raise ValueError("memory_policy_disabled")
        if self.allowed_memory_kinds != ("case_working",):
            raise ValueError("only_case_working_memory_permitted")
        forbidden_flags = {
            "cross_case": self.allow_cross_case_recall,
            "user_profile": self.allow_user_profile_memory,
            "semantic": self.allow_semantic_memory,
            "episodic": self.allow_episodic_memory,
            "organizational": self.allow_organizational_memory,
            "shared_agent": self.allow_shared_agent_memory,
        }
        enabled = sorted(name for name, value in forbidden_flags.items() if value)
        if enabled:
            raise ValueError(f"future_memory_capability_enabled:{','.join(enabled)}")
        if self.default_ttl_days <= 0 or self.default_ttl_days > self.max_ttl_days:
            raise ValueError("invalid_default_ttl")
        if self.hard_max_items > 8 or self.hard_max_chars > 12_000:
            raise ValueError("stage5a_context_budget_expanded")
