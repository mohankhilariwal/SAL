from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from northstar_compliance.common.jsonutil import isoformat_utc, new_id
from northstar_compliance.graph.runtime import DurableGraphRuntime
from northstar_compliance.harness.context import ContextAssembler, ContextSource
from northstar_compliance.harness.hooks import HookManager
from northstar_compliance.harness.instructions import InstructionStore
from northstar_compliance.harness.models import HarnessManifest, HarnessRunResult, HarnessSession
from northstar_compliance.harness.tracing import JsonlTracer
from northstar_compliance.harness.validation import ValidationPipeline
from northstar_compliance.harness.workspace import WorkspaceManager


@dataclass(frozen=True)
class HarnessRequest:
    initiator_id: str
    context_sources: list[ContextSource]


class AgentHarness:
    """Framework-neutral harness composing existing graph, gateway, state and approval contracts."""

    def __init__(
        self,
        *,
        manifest: HarnessManifest,
        instructions: InstructionStore,
        context_assembler: ContextAssembler,
        workspace_manager: WorkspaceManager,
        graph_runtime: DurableGraphRuntime,
        validators: ValidationPipeline,
        hooks: HookManager,
    ):
        self.manifest = manifest
        self.instructions = instructions
        self.context_assembler = context_assembler
        self.workspaces = workspace_manager
        self.graph = graph_runtime
        self.validators = validators
        self.hooks = hooks

    def start(self, request: HarnessRequest, *, now: datetime) -> HarnessRunResult:
        self.validators.run("pre_start", self.manifest)
        instruction = self.instructions.load()
        if instruction.content_sha256 != self.manifest.instruction_sha256:
            raise RuntimeError("instruction_manifest_mismatch")
        context = self.context_assembler.assemble(agent_id="AGT-001", sources=request.context_sources, now=now)
        self.validators.run("post_context", context)

        session_id = new_id("SESSION")
        run_id = new_id("RUN")
        workspace = self.workspaces.create(session_id, isoformat_utc(now))
        tracer = JsonlTracer(workspace, session_id=session_id)
        session = HarnessSession(
            schema_version="1.0.0",
            session_id=session_id,
            initiator_id=request.initiator_id,
            manifest_digest=self.manifest.digest,
            trace_id=tracer.trace_id,
            instruction_digest=instruction.content_sha256,
            context_digest=context.content_sha256,
            workspace_path=str(workspace.root),
            status="running",
            created_at=isoformat_utc(now),
            updated_at=isoformat_utc(now),
        )
        self.graph.store.create_session(session.to_dict())
        workspace.write_json("session.json", session.to_dict())
        workspace.write_json("instruction-metadata.json", instruction.to_dict(include_content=False))
        workspace.write_json("context-envelope.json", context.to_dict(include_content=True))
        tracer.emit(
            event_type="harness.start",
            now=now,
            run_id=run_id,
            attributes={
                "agent_id": "AGT-001",
                "graph_id": "GRAPH-001",
                "graph_version": "1.1.0",
                "manifest_digest": self.manifest.digest,
                "instruction_digest": instruction.content_sha256,
                "context_digest": context.content_sha256,
                "context_items": len(context.items),
                "context_characters": context.total_characters,
            },
        )
        hook_results = list(self.hooks.emit("before_start", {
            "agent_ids": ["AGT-001"],
            "memory_enabled": self.manifest.memory_enabled,
            "multiple_agents_enabled": self.manifest.multiple_agents_enabled,
        }))
        runtime_result = self.graph.start(
            run_id=run_id,
            session_id=session_id,
            initiator_id=request.initiator_id,
            context_digest=context.content_sha256,
            instruction_digest=instruction.content_sha256,
            now=now,
        )
        result = HarnessRunResult(
            schema_version="1.0.0",
            session_id=session_id,
            run_id=run_id,
            status=runtime_result.state.status,
            current_node=runtime_result.state.current_node,
            disposition=runtime_result.state.disposition,
            review_outcome=runtime_result.state.review_outcome,
            wait_id=runtime_result.state.wait_id,
            approval_token=runtime_result.approval_token,
            manifest_digest=self.manifest.digest,
            instruction_digest=instruction.content_sha256,
            context_digest=context.content_sha256,
            trace_id=tracer.trace_id,
            hook_results=tuple(hook_results),
        )
        self.validators.run("post_start", result)
        hook_results.extend(self.hooks.emit("after_suspend", {
            "agent_ids": ["AGT-001"],
            "memory_enabled": False,
            "multiple_agents_enabled": False,
            "disposition": result.disposition,
        }))
        result = HarnessRunResult(**{**result.__dict__, "hook_results": tuple(hook_results)})
        workspace.write_json("start-result.json", result.to_dict(include_transient=False))
        tracer.emit(
            event_type="harness.suspended",
            now=now,
            run_id=run_id,
            attributes={"status": result.status, "current_node": result.current_node, "wait_id": result.wait_id, "disposition": result.disposition},
        )
        self.graph.store.update_session_status(session_id, "waiting", isoformat_utc(now))
        return result

    def submit_decision(
        self,
        *,
        session_id: str,
        token: str,
        reviewer_id: str,
        reviewer_roles: list[str],
        decision: str,
        reason: str,
        now: datetime,
    ) -> dict[str, Any]:
        session = self.graph.store.load_session(session_id)
        workspace = self.workspaces.open(session_id)
        tracer = JsonlTracer(workspace, session_id=session_id, trace_id=session["trace_id"])
        # Resolve initiator from durable session; never from reviewer input.
        payload = self.graph.approvals.submit(
            token=token,
            reviewer_id=reviewer_id,
            reviewer_roles=reviewer_roles,
            decision=decision,
            reason=reason,
            initiator_id=session["initiator_id"],
            now=now,
        )
        tracer.emit(
            event_type="approval.accepted",
            now=now,
            run_id=payload["run_id"],
            attributes={"decision_id": payload["decision_id"], "decision": payload["decision"], "reviewer_id": reviewer_id},
        )
        return payload

    def resume(self, *, session_id: str, run_id: str, worker_id: str, now: datetime) -> HarnessRunResult:
        self.validators.run("pre_resume", self.manifest)
        session = self.graph.store.load_session(session_id)
        if session["manifest_digest"] != self.manifest.digest:
            raise RuntimeError("session_manifest_mismatch")
        workspace = self.workspaces.open(session_id)
        tracer = JsonlTracer(workspace, session_id=session_id, trace_id=session["trace_id"])
        tracer.emit(event_type="harness.resume", now=now, run_id=run_id, attributes={"worker_id": worker_id})
        hook_results = list(self.hooks.emit("before_resume", {
            "agent_ids": ["AGT-001"], "memory_enabled": False, "multiple_agents_enabled": False,
        }))
        runtime_result = self.graph.resume(run_id=run_id, session_id=session_id, worker_id=worker_id, now=now)
        result = HarnessRunResult(
            schema_version="1.0.0",
            session_id=session_id,
            run_id=run_id,
            status=runtime_result.state.status,
            current_node=runtime_result.state.current_node,
            disposition=runtime_result.state.disposition,
            review_outcome=runtime_result.state.review_outcome,
            wait_id=runtime_result.state.wait_id,
            approval_token=None,
            manifest_digest=self.manifest.digest,
            instruction_digest=runtime_result.state.instruction_digest or "",
            context_digest=runtime_result.state.context_digest or "",
            trace_id=tracer.trace_id,
            hook_results=tuple(hook_results),
        )
        self.validators.run("post_resume", result)
        hook_results.extend(self.hooks.emit("after_resume", {
            "agent_ids": ["AGT-001"],
            "memory_enabled": False,
            "multiple_agents_enabled": False,
            "disposition": result.disposition,
        }))
        result = HarnessRunResult(**{**result.__dict__, "hook_results": tuple(hook_results)})
        workspace.write_json("resume-result.json", result.to_dict(include_transient=False))
        tracer.emit(
            event_type="harness.completed" if result.status in {"completed", "escalated"} else "harness.waiting",
            now=now,
            run_id=run_id,
            attributes={"status": result.status, "current_node": result.current_node, "review_outcome": result.review_outcome, "disposition": result.disposition},
        )
        self.graph.store.update_session_status(session_id, result.status, isoformat_utc(now))
        return result
