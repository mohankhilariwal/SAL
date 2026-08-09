from __future__ import annotations

from hashlib import sha256


def counterbalanced_order(pair_index: int, repetition: int) -> tuple[str, str]:
    """Two-condition Williams/Latin-square equivalent for a paired experiment."""
    if pair_index < 0 or repetition < 0:
        raise ValueError("indices must be non-negative")
    return ("control", "treatment") if (pair_index + repetition) % 2 == 0 else ("treatment", "control")


def stable_trial_id(judge_id: str, probe_id: str, pair_id: str, variant: str, repetition: int) -> str:
    payload = f"{judge_id}|{probe_id}|{pair_id}|{variant}|{repetition}".encode("utf-8")
    return "TRL-" + sha256(payload).hexdigest()[:20].upper()


def canonical_digest(obj: object) -> str:
    import json
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha256(payload).hexdigest()
