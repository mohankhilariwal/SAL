from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from northstar_compliance.specification.integration import build_specification_runtime


class SpecificationGuardedHarness:
    """Thin S05A composition wrapper around an existing S04C harness adapter.

    The wrapped harness still owns graph, tool, approval and persistence behavior.
    This guard performs specification validation/assertions before and after calls.
    """

    def __init__(self, specification_path: Path, manifest: Mapping[str, Any], harness: Any):
        self.runtime = build_specification_runtime(specification_path, manifest)
        self.manifest = manifest
        self.harness = harness

    def start(self, request: Mapping[str, Any], context_envelope: Mapping[str, Any]) -> Any:
        pre = self.runtime.assertions.pre_start(
            self.runtime.specification,
            manifest=self.manifest,
            context_envelope=context_envelope,
        )
        if not pre.passed:
            raise RuntimeError(f"specification_pre_start_failed:{','.join(pre.failures)}")
        result = self.harness.start(request)
        persisted = result.get("persisted_result") if isinstance(result, Mapping) else None
        post = self.runtime.assertions.post_result(
            self.runtime.specification,
            result=result,
            persisted_result=persisted,
        )
        if not post.passed:
            raise RuntimeError(f"specification_post_result_failed:{','.join(post.failures)}")
        return result
