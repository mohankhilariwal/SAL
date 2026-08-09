from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ChaosResult:
    experiment_id: str
    injected: bool
    invariant_passed: bool
    safe_summary: str
    authority_effect: str = "none"


class ChaosHarness:
    """Runs deterministic local fault injections; never targets production."""

    def run(self, experiment_id: str, inject: Callable[[], None], verify: Callable[[], bool]) -> ChaosResult:
        inject()
        passed = bool(verify())
        return ChaosResult(experiment_id, True, passed, "local fault injection completed")
