# 06 — ADR Register

**Version:** `0.8.0`

`ADR-001`–`ADR-026` remain accepted from the reconstructed `0.7.0` baseline.

## `ADR-027` — Explicit typed execution graph replaces imperative control flow

**Decision:** Use `GRAPH-001` with deterministic, model, policy, tool, recovery and termination nodes plus named conditional/error/terminal edges. Preserve one agent and existing authority.

## `ADR-028` — Framework-neutral application-owned graph kernel

**Decision:** Implement Stage 4A with Python/JSON contracts rather than adopting LangGraph, a managed state machine or Temporal immediately. Re-evaluate when distributed durability, human waits or production operations justify them.

## `ADR-029` — Node-owned copy-on-write patches and graph-version-bound checkpoints

**Decision:** Nodes return typed patches; the runtime validates exact owned paths and applies them copy-on-write. Protect identity, authority, budget, goal and final disposition. Bind resume to graph ID/version.

Full ADRs are under `docs/adr/`.
