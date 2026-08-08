from __future__ import annotations

import json
from pathlib import Path

from northstar_compliance.graph.factory import build_graph_runtime
from northstar_compliance.harness.context import ContextAssembler
from northstar_compliance.harness.hooks import HookManager, InvariantEvaluationHook
from northstar_compliance.harness.instructions import InstructionStore
from northstar_compliance.harness.models import HarnessManifest
from northstar_compliance.harness.runtime import AgentHarness
from northstar_compliance.harness.validation import ContextEnvelopeValidator, ManifestValidator, ResultValidator, ValidationPipeline
from northstar_compliance.harness.workspace import WorkspaceManager


def load_manifest(path: str | Path) -> HarnessManifest:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    value["validator_names"] = tuple(value["validator_names"])
    value["hook_names"] = tuple(value["hook_names"])
    return HarnessManifest(**value)


def build_harness(
    *,
    repository_root: str | Path,
    runtime_root: str | Path,
    approval_secret: bytes,
    approval_ttl_seconds: int = 3600,
) -> AgentHarness:
    repository_root = Path(repository_root)
    runtime_root = Path(runtime_root)
    manifest = load_manifest(repository_root / "config/harness/harness-manifest.json")
    instructions = InstructionStore(
        repository_root / "config/harness/instructions/AGT-001-system-1.0.0.txt",
        name=manifest.instruction_name,
        version=manifest.instruction_version,
        expected_sha256=manifest.instruction_sha256,
    )
    graph = build_graph_runtime(runtime_root / "northstar.db", approval_secret, approval_ttl_seconds=approval_ttl_seconds)
    validators = ValidationPipeline([
        ManifestValidator(manifest.digest),
        ContextEnvelopeValidator(),
        ResultValidator(),
    ])
    hooks = HookManager([InvariantEvaluationHook()])
    return AgentHarness(
        manifest=manifest,
        instructions=instructions,
        context_assembler=ContextAssembler(max_items=8, max_characters=12_000),
        workspace_manager=WorkspaceManager(runtime_root / "workspace"),
        graph_runtime=graph,
        validators=validators,
        hooks=hooks,
    )
