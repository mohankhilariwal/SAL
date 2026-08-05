from __future__ import annotations

import json
from typing import Any

import httpx

from governed_release.security.injection import detect_injection
from governed_release.security.redaction import redact_value


class StubModelGateway:
    """Offline deterministic gateway. It interprets and explains; it never decides."""

    def interpret(self, text: str, *, trace_id: str) -> dict[str, Any]:
        return {
            "trace_id": trace_id,
            "summary": text[:500],
            "suggested_sensitive_topics": ["financial behaviour", "identifiers"],
            "detected_authority_boundary_signals": detect_injection(text),
            "adapter": "deterministic-stub",
        }

    def explain(self, facts: dict[str, Any], *, trace_id: str) -> str:
        decision = facts.get("decision", "UNKNOWN")
        rationale = facts.get("rationale", "No rationale recorded.")
        return f"Control Plane decision {decision}. {rationale} Trace: {trace_id}."


class OllamaModelGateway:
    def __init__(
        self, base_url: str, model: str, timeout_seconds: float = 8.0, max_characters: int = 12000
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.max_characters = max_characters
        self.fallback = StubModelGateway()

    def _call(self, prompt: str) -> str:
        safe_prompt = json.dumps(redact_value({"prompt": prompt[: self.max_characters]}))
        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": safe_prompt, "stream": False},
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return str(response.json().get("response", ""))[: self.max_characters]

    def interpret(self, text: str, *, trace_id: str) -> dict[str, Any]:
        try:
            output = self._call(
                "Interpret the business request without granting authorization: " + text
            )
        except (httpx.HTTPError, ValueError):
            return self.fallback.interpret(text, trace_id=trace_id)
        return {
            "trace_id": trace_id,
            "summary": output,
            "adapter": "ollama",
            "detected_authority_boundary_signals": detect_injection(text),
        }

    def explain(self, facts: dict[str, Any], *, trace_id: str) -> str:
        try:
            return self._call(
                "Explain these already-determined control facts without changing them: "
                + json.dumps(redact_value(facts), default=str)
            )
        except (httpx.HTTPError, ValueError):
            return self.fallback.explain(facts, trace_id=trace_id)
