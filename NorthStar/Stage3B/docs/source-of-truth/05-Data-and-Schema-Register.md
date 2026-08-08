# 05 — Data and Schema Register

**Version:** `0.6.0`

`DATA-001`–`DATA-040` and `INT-001`–`INT-020` remain accepted. S03B makes the pre-existing conceptual `DATA-009 AgentRunState` executable and adds `DATA-041`–`DATA-044` and `INT-021`–`INT-025`.

## Executable agent data

### `DATA-009 AgentRunState`

Owner: `CMP-003`. Schema version `1.0.0`.

Required logical fields:

- `run_id`, `agent_id=AGT-001`, typed `goal`;
- terminal-capable `status`;
- iteration and configured guard limits;
- monotonic `progress_milestones`;
- ordered structured decisions and observations;
- application-owned artifact references;
- last action signature and consecutive repeat/no-progress counters;
- terminal reason and concise summary.

This state is not model context by default, not long-term memory, not a case system of record and not hidden chain-of-thought.

### `DATA-041 AgentGoal`

Typed, immutable goal envelope containing goal/publication identity, title, objective, jurisdictions, business domains and evidence query. Owner: `CMP-003`; supplied through `INT-021`.

### `DATA-042 AgentDecision`

One of:

```json
{
  "kind": "call_tool | complete | escalate",
  "reason_summary": "concise auditable reason",
  "expected_progress": "specific expected state change",
  "tool_id": "TOOL-001 only for call_tool",
  "tool_version": "1.0.0 only for call_tool",
  "arguments": {}
}
```

Terminal decisions cannot contain tool fields. The reason is a concise decision summary, not hidden reasoning.

### `DATA-043 AgentObservation`

Application-owned projection of a validated gateway result: iteration, tool/status, action signature, milestone set before/after and non-sensitive result summary. Raw secrets and unrestricted tool payloads are not copied into the decision provider contract.

### `DATA-044 AgentRunOutcome`

Fields include `completed|escalated|terminated_guard`, termination reason, concise summary, iteration count, milestones, artifact references, `human_review_required=true` and fixed `final_disposition=preliminary_grounded_unapproved`.

## New interfaces

| ID | Contract | Security/compatibility rule |
|---|---|---|
| `INT-021` | Agent Run Contract: goal + trusted principal + guard configuration → state/outcome. | Caller supplies principal through application boundary, not model output. |
| `INT-022` | Structured Decision Provider Contract: bounded goal/state/tool view → one `DATA-042`. | Provider may propose; it cannot authorize or terminate successfully by assertion. |
| `INT-023` | State Projection and Observation Contract: validated `DATA-038` → `DATA-043` + milestone/artifact update. | Only application mappings mutate state. |
| `INT-024` | Termination Evaluation Contract: state + decision/observation → continue or typed terminal reason. | Deterministic and fail-closed. |
| `INT-025` | Agent Run Evidence Contract: final `DATA-009` + `DATA-044` → atomic local JSON. | Evidence only; not audit/system-of-record status. |

## State ownership rules

- Decision provider: proposes `DATA-042`; owns no authoritative state.
- Runtime: owns iteration, signatures, milestones and terminal state.
- Gateway: owns tool enforcement and `DATA-038`.
- Adapters: own local synthetic result construction, not agent completion.
- Human boundary: owns future review decision; no `DATA-007 ReviewDecision` is instantiated.
