# 03 — Architecture Baseline

**Architecture version:** `0.8.0`

## Architecture before S04A

`CMP-003` owns an imperative S03C loop with application-owned budgets, recovery, cancellation, checkpoint and deterministic termination. The logic is correct but increasingly branched and difficult to review independently.

## Architecture after S04A

`CMP-003` now contains `GRAPH-001 Regulatory Impact Assessment Execution Graph`. The graph has nine explicit nodes and named conditional/error/terminal edges. `DATA-054` wraps the unchanged `DATA-009`. Nodes return `DATA-055` and `DATA-056`; `INT-033` applies only node-owned paths. `DATA-057` records every transition. `DATA-050` checkpoints the graph state after every accepted transition.

The graph does not replace `AGT-001`, `CMP-005`, `INT-026`–`030` or deterministic completion. It only makes their orchestration explicit.

## Cumulative Mermaid

See `docs/architecture/diagrams/cumulative-logical-architecture.mmd` and focused graph/state/recovery/trust diagrams.

## Graph ownership summary

| Node | Type | Owner/responsibility |
|---|---|---|
| `N00_VALIDATE_CONTEXT` | deterministic | Runtime validates immutable invariants. |
| `N10_GUARD_CHECK` | deterministic | Cancellation and graph budget. |
| `N20_MODEL_DECIDE` | model | `AGT-001` proposes only. |
| `N30_POLICY_GATE` | policy | Preflight; gateway still authorizes. |
| `N40_TOOL_EXECUTE` | tool | Calls `CMP-005` only. |
| `N50_RECOVERY` | recovery | Reuses S03C fallback/reconciliation. |
| `N60_OBSERVE` | deterministic | Projects validated milestones/artifacts. |
| `N70_COMPLETION_CHECK` | deterministic | Enforces completion invariants. |
| `N90_TERMINATE` | termination | Produces local terminal state/outcome. |
