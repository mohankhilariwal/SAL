from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, Protocol

from .models import JudgeEvaluationEnvelope


class JudgeAdapter(Protocol):
    judge_id: str
    judge_version: str

    def evaluate(self, envelope: JudgeEvaluationEnvelope, prompt: str, *, variant: str = "base") -> str:
        ...


@dataclass(frozen=True)
class ReplayJudgeAdapter:
    judge_id: str
    judge_version: str
    replays: Mapping[tuple[str, str], str]

    def evaluate(self, envelope: JudgeEvaluationEnvelope, prompt: str, *, variant: str = "base") -> str:
        del prompt
        key = (envelope.case_id, variant)
        try:
            return self.replays[key]
        except KeyError as exc:
            raise KeyError(f"missing replay for {self.judge_id} {key}") from exc


@dataclass(frozen=True)
class CallableJudgeAdapter:
    judge_id: str
    judge_version: str
    callback: Callable[[JudgeEvaluationEnvelope, str, str], str]

    def evaluate(self, envelope: JudgeEvaluationEnvelope, prompt: str, *, variant: str = "base") -> str:
        return self.callback(envelope, prompt, variant)
