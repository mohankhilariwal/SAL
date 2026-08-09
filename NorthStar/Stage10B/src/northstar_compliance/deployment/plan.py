from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeploymentPlan:
    environment: str
    strategy: str
    route_activation_allowed: bool
    rollback_required: bool
    notes: tuple[str, ...]
    authority_effect: str = "none"


class DeploymentPlanner:
    ALLOWED = {"local", "shared-dev", "test", "pre-production"}

    def prepare(self, environment: str) -> DeploymentPlan:
        if environment not in self.ALLOWED:
            return DeploymentPlan(
                environment,
                "none",
                False,
                True,
                ("production and multi-region routes are outside the accepted Stage 10B baseline",),
            )
        strategy = "local-compose" if environment == "local" else "rolling-reference"
        return DeploymentPlan(
            environment,
            strategy,
            False,
            True,
            ("reference plan only", "route activation requires later accepted control-plane and evaluation gates"),
        )
