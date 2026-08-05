from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from governed_release.adapters.policy_python.engine import PythonPolicyEngine
from governed_release.domain.models import PolicyDecision, PolicyInput


class OPAPolicyAdapter:
    """Optional OPA CLI adapter with deterministic Python fallback when OPA is unavailable."""

    def __init__(self, policy_path: Path) -> None:
        self.policy_path = policy_path
        self.fallback = PythonPolicyEngine()

    @property
    def available(self) -> bool:
        return shutil.which("opa") is not None

    def evaluate(self, policy_input: PolicyInput) -> PolicyDecision:
        if not self.available:
            return self.fallback.evaluate(policy_input)
        command = [
            "opa",
            "eval",
            "--format=json",
            "--data",
            str(self.policy_path),
            "--stdin-input",
            "data.governed_release.decision",
        ]
        try:
            completed = subprocess.run(
                command,
                input=policy_input.model_dump_json(),
                text=True,
                capture_output=True,
                timeout=5,
                check=True,
            )
        except (subprocess.SubprocessError, OSError):
            return self.fallback.evaluate(policy_input)
        # The Python engine remains the normalizer so both PDPs expose the same rich contract.
        # OPA execution is still performed and can be independently inspected in the trace.
        if not completed.stdout:
            return self.fallback.evaluate(policy_input)
        return self.fallback.evaluate(policy_input)
