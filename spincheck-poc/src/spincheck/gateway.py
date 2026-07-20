"""Provider-agnostic model gateway.

Every layer (tier1 / tier2 / explainer) is configurable in config/models.yaml.
Switching vendors = a control-plane config edit + a regression pass, never a
code change. SDKs are imported lazily so only the configured providers are
required at runtime. The `mock` provider makes the entire POC runnable offline
and is the deterministic fixture for unit tests and CI.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any

# indicative published prices (USD per MTok in/out) for cost telemetry only —
# override in config or verify against vendor pricing pages before budgeting.
_PRICES = {
    "claude-haiku-4-5": (1.0, 5.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "gpt-5.4-mini": (0.6, 2.4),
    "gpt-5.4": (2.5, 14.0),
    "gemini-3-flash": (0.5, 3.0),
    "gemini-3.1-pro": (2.0, 12.0),
}


@dataclass
class LLMResult:
    text: str
    input_tokens: int
    output_tokens: int
    latency_s: float
    provider: str
    model: str

    @property
    def cost_usd(self) -> float:
        pi, po = _PRICES.get(self.model, (0.0, 0.0))
        return (self.input_tokens * pi + self.output_tokens * po) / 1_000_000


class Gateway:
    def __init__(self, models_cfg: dict):
        self.cfg = models_cfg

    def complete(self, layer: str, prompt: str, mock_payload: Any = None) -> LLMResult:
        lc = self.cfg["layers"][layer]
        provider, model = lc["provider"], lc["model"]
        t0 = time.time()
        if provider == "mock":
            text = json.dumps(mock_payload) if not isinstance(mock_payload, str) else mock_payload
            return LLMResult(text, len(prompt) // 4, len(text) // 4, time.time() - t0, provider, model)
        if provider == "anthropic":
            text, ti, to = self._anthropic(model, prompt, lc)
        elif provider == "openai":
            text, ti, to = self._openai(model, prompt, lc)
        elif provider == "gemini":
            text, ti, to = self._gemini(model, prompt, lc)
        else:
            raise ValueError(f"unknown provider {provider}")
        return LLMResult(text, ti, to, time.time() - t0, provider, model)

    # ------------------------------------------------------------ providers
    def _anthropic(self, model: str, prompt: str, lc: dict):
        import anthropic  # lazy

        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"],
                                     timeout=self.cfg["gateway"]["timeout_s"],
                                     max_retries=self.cfg["gateway"]["max_retries"])
        r = client.messages.create(
            model=model, max_tokens=lc.get("max_tokens", 4000),
            temperature=lc.get("temperature", 0.0),
            messages=[{"role": "user", "content": prompt}])
        return r.content[0].text, r.usage.input_tokens, r.usage.output_tokens

    def _openai(self, model: str, prompt: str, lc: dict):
        from openai import OpenAI  # lazy

        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"],
                        timeout=self.cfg["gateway"]["timeout_s"],
                        max_retries=self.cfg["gateway"]["max_retries"])
        r = client.chat.completions.create(
            model=model, temperature=lc.get("temperature", 0.0),
            max_tokens=lc.get("max_tokens", 4000),
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}])
        u = r.usage
        return r.choices[0].message.content, u.prompt_tokens, u.completion_tokens

    def _gemini(self, model: str, prompt: str, lc: dict):
        # Gemini via its OpenAI-compatible endpoint keeps the gateway to one code path.
        from openai import OpenAI  # lazy

        client = OpenAI(api_key=os.environ["GOOGLE_API_KEY"],
                        base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        r = client.chat.completions.create(
            model=model, temperature=lc.get("temperature", 0.0),
            max_tokens=lc.get("max_tokens", 4000),
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}])
        u = r.usage
        return r.choices[0].message.content, u.prompt_tokens, u.completion_tokens
