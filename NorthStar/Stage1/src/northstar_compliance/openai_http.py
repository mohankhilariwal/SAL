from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from .intake import Publication
from .model_gateway import ModelResult
from .prompts import SYSTEM_INSTRUCTIONS, build_user_prompt
from .schemas import SUMMARY_JSON_SCHEMA


class OpenAIHTTPError(RuntimeError):
    pass


class OpenAIResponsesSummaryModel:
    """Optional Responses API adapter using only Python's standard library.

    The automated Stage 1 acceptance tests do not make a network call.
    """

    provider = "openai"

    def __init__(self, *, api_key: str | None = None, model: str | None = None, timeout: float = 60.0) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model or os.getenv("OPENAI_MODEL", "")
        self.timeout = timeout
        if not self.api_key:
            raise OpenAIHTTPError("OPENAI_API_KEY is required for provider=openai")
        if not self.model:
            raise OpenAIHTTPError("OPENAI_MODEL is required for provider=openai")

    def summarize(self, publication: Publication) -> ModelResult:
        body: dict[str, Any] = {
            "model": self.model,
            "instructions": SYSTEM_INSTRUCTIONS,
            "input": build_user_prompt(publication),
            "store": False,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "northstar_stage1_summary",
                    "schema": SUMMARY_JSON_SCHEMA,
                    "strict": True,
                }
            },
        }
        request = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise OpenAIHTTPError(f"OpenAI HTTP {exc.code}: {detail[:1000]}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise OpenAIHTTPError(f"OpenAI request failed: {exc}") from exc

        output_text = raw.get("output_text")
        if not output_text:
            for item in raw.get("output", []):
                for content in item.get("content", []):
                    if content.get("type") == "output_text" and content.get("text"):
                        output_text = content["text"]
                        break
        if not output_text:
            raise OpenAIHTTPError("Response contained no output_text")
        try:
            payload = json.loads(output_text)
        except json.JSONDecodeError as exc:
            raise OpenAIHTTPError("Structured response was not valid JSON") from exc
        usage = raw.get("usage") or {}
        clean_usage = {str(k): int(v) for k, v in usage.items() if isinstance(v, int)}
        return ModelResult(provider=self.provider, model=self.model, payload=payload, usage=clean_usage)
