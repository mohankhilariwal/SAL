# 05 — Data and Schema Register
**Version:** `1.3.0`

All `DATA-001`–`086` and `INT-001`–`058` remain.

| ID | Name/version | Owner | Meaning |
|---|---|---|---|
| `DATA-087` | AgentBoundaryQuestionnaire 1.0.0 | `CMP-008/011` | Shared/independent boundaries and evidence status. |
| `DATA-088` | AgentBoundaryAssessment 1.0.0 | `CMP-008` | Candidate fit/eligibility, selected one-agent pattern, reasons/limitations/digest. |
| `DATA-089` | TaskProfileSet 1.0.0 | `CMP-003/011` | Six profiles for one `AGT-001`; no authority. |
| `DATA-090` | TaskProfileBinding 1.0.0 | `CMP-003` | Run/node/profile/spec/graph/digest binding and unchanged control owners. |

| ID | Contract | Control |
|---|---|---|
| `INT-059` | Agent Boundary Assessment | Design-time only; cannot allocate/authorize. |
| `INT-060` | Task Profile Load/Validation | Exact agent/graph/tools and capability denylist. |
| `INT-061` | Task Profile Runtime Binding | `CMP-003`; digest-bound; no authority transfer. |
| `INT-062` | Future Multi-Agent Capability Gate | Deny-by-default; review only; no allocation. |

No delegated-task, message, handoff, agent-card, private/shared agent-state or shared-agent-memory object is created.
