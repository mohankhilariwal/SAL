from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .assertions import RuntimeAssertionEngine
from .gates import DeploymentGateEvaluator
from .loader import AgentSpecificationStore
from .models import AgentSpecification, SpecificationValidationReport
from .validator import AgentSpecificationValidator


@dataclass(frozen=True)
class SpecificationRuntime:
    specification: AgentSpecification
    validation: SpecificationValidationReport
    assertions: RuntimeAssertionEngine
    gates: DeploymentGateEvaluator


def build_specification_runtime(
    specification_path: Path,
    manifest: Mapping[str, Any],
) -> SpecificationRuntime:
    specification = AgentSpecificationStore(specification_path).load()
    validation = AgentSpecificationValidator().validate(specification, manifest=manifest)
    if not validation.valid:
        codes = ",".join(finding.code for finding in validation.findings)
        raise RuntimeError(f"agent_specification_invalid:{codes}")
    return SpecificationRuntime(
        specification=specification,
        validation=validation,
        assertions=RuntimeAssertionEngine(),
        gates=DeploymentGateEvaluator(),
    )
