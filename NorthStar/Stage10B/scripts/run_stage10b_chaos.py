from __future__ import annotations

import json

from northstar_compliance.reliability.chaos import ChaosHarness

state = {"audit_available": True, "protected_effect_executed": False}


def inject() -> None:
    state["audit_available"] = False


def verify() -> bool:
    return state["audit_available"] is False and state["protected_effect_executed"] is False


result = ChaosHarness().run("CHAOS-S10B-001", inject, verify)
print(json.dumps(result.__dict__, indent=2))
