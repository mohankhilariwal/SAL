from __future__ import annotations
import json
from dataclasses import replace
from pathlib import Path
from .canonical import sha256_hex
from .models import TaskProfile
FORBIDDEN=("delegate","handoff","spawn","sub-agent","subagent","shared memory","approve","finalize","final legal","concurrent branch","mcp","a2a")
def _profile(x):
    return TaskProfile(x["profile_id"],x["profile_version"],x["agent_id"],x["graph_id"],x["graph_version"],x["node_key"],x["purpose"],x["instruction_ref"],tuple(x["context_kinds"]),tuple(x["exposed_tools"]),x["output_contract"],x["memory_access"],bool(x["can_delegate"]),bool(x["can_handoff"]),bool(x["can_approve"]),bool(x["can_finalize"]),bool(x["can_write_memory"]),bool(x["concurrent_execution"]))
def load_task_profiles(path,policy):
    raw=json.loads(Path(path).read_text()).get("profiles")
    if not isinstance(raw,list): raise ValueError("profiles must be list")
    ps=tuple(_profile(x) for x in raw); validate_task_profiles(ps,policy)
    return tuple(replace(p,profile_sha256=sha256_hex(p)) for p in ps)
def validate_task_profiles(profiles,policy):
    ps=tuple(profiles)
    if len(ps)!=6: raise ValueError("exactly six profiles required")
    if len({p.profile_id for p in ps})!=6 or len({p.node_key for p in ps})!=6: raise ValueError("duplicate profile or node")
    for p in ps:
        if p.agent_id!="AGT-001" or p.agent_id not in policy.allowed_agent_ids: raise ValueError("new agent identity")
        if (p.graph_id,p.graph_version)!=("GRAPH-001","1.1.0"): raise ValueError("graph incompatibility")
        if set(p.exposed_tools)-set(policy.allowed_tool_ids): raise ValueError("unknown tool")
        if any((p.can_delegate,p.can_handoff,p.can_approve,p.can_finalize,p.can_write_memory,p.concurrent_execution)): raise ValueError("prohibited capability")
        if p.memory_access not in {"none","via_harness_context_only"}: raise ValueError("memory mode")
        if any(m in f"{p.purpose} {p.instruction_ref} {p.output_contract}".lower() for m in FORBIDDEN): raise ValueError("authority-like language")
        if not p.instruction_ref or not p.output_contract: raise ValueError("missing profile contract")
