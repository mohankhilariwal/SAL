# 00 — Project Constitution

**Project:** NorthStar Agentic AI Architecture Playbook  
**Current architecture/repository version:** `0.7.0`  
**Current stage:** `S03C — Loop Failures, Recovery and Budgets`

## Preserved constitutional rules

1. NorthStar Financial Services, the eight accepted personas and `US-001`–`US-012` retain their meanings.
2. Human accountability is never transferred to an autonomous AI system.
3. `AGT-001 Regulatory Impact Assessment Agent` remains the only accepted agent.
4. The agent may propose only `TOOL-001`–`TOOL-006`; every call uses `CMP-005` and `INT-017`.
5. Identity, authority, policy, completion, budgets, retry safety, final disposition and approval remain application-owned deterministic controls.
6. Retrieval authorization precedes scoring, text exposure and context assembly.
7. All outputs remain preliminary/unapproved. The only terminal disposition is `preliminary_grounded_unapproved`, with `human_review_required=true`.
8. No graph, memory, MCP/A2A, sub-agent, second agent, live enterprise connector, enterprise audit ledger or production control plane is introduced in S03C.
9. Stable IDs are never silently renamed or reused.
10. Every claimed capability must trace to code, tests and an accepted ADR.

## Stage 3C additions

- Independent runtime budgets are mandatory for model iterations, wall time, tokens, cost, tool calls, model calls, failures, retries and replans.
- Recovery is typed and bounded. Prompts cannot authorize retries.
- Read-only fallback is allowed only to a registered semantically equivalent adapter.
- Reversible writes are never blindly retried after an ambiguous post-dispatch failure.
- Checkpoint/resume preserves the same run and authority envelope; it is not memory or audit.
- Partial completion must identify completed and missing milestones without claiming success.

## Definition of done for S03C

The stage is done only if the repository runs locally, tests all budget/recovery classes, reconciles an ambiguous write without duplicate side effects, resumes from a validated checkpoint, preserves permission and human-review invariants, updates all ten source-of-truth artefacts and stops before graph engineering.

## Reconstruction exception

The byte-exact `0.6.0` repository and nine detailed registers were not mounted in this execution. The supplied S03B handoff and full S03B chapter were treated as authoritative reconstruction sources. `ISS-029` records the compatible-overlay limitation.
