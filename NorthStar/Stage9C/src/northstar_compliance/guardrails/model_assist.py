from __future__ import annotations

import re

from .models import GuardrailRequest, Outcome


INJECTION_PATTERNS = (
    r"ignore (all|any|the) (previous|prior|system|developer) instructions",
    r"reveal (the )?(system prompt|hidden instructions|secret)",
    r"bypass (policy|authorization|guardrail|approval)",
    r"treat .* as trusted instructions",
)

APPROVAL_PATTERNS = (
    r"\b(case|assessment|change) (is|has been) approved\b",
    r"\bfinal approval\b",
    r"\bno human review (is )?required\b",
)


def advisory_classifier(request: GuardrailRequest, *, mode: str) -> tuple[bool, str, str, Outcome]:
    """Deterministic teaching substitute for a model-assisted classifier.

    A production adapter may call a classifier/LLM, but it must preserve the contract:
    it may flag/quarantine/request review and can never issue authority or approval.
    """
    text = str(request.payload.get("text", ""))
    patterns = INJECTION_PATTERNS if mode == "injection" else APPROVAL_PATTERNS
    for pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
            outcome = Outcome.QUARANTINE if mode == "injection" else Outcome.REQUIRE_HUMAN_REVIEW
            return False, f"MODEL_ASSISTED_{mode.upper()}_FLAG", f"Potential {mode} signal detected", outcome
    return True, f"MODEL_ASSISTED_{mode.upper()}_CLEAR", f"No {mode} signal detected", Outcome.ALLOW
