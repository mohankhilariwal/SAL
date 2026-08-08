# 04 — Component and Agent Catalogue

**Version:** `1.1.0`

## Components

| ID | Name | S05A responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Calls the specification-guarded harness surfaces; no new authority/UI. |
| `CMP-002` | Regulatory Intake Boundary | Retained bounded publication intake/provenance. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Resolves/binds `DATA-071`, executes pre/post assertions, delegates unchanged execution to `GRAPH-001`. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Supplies context allowed by `DATA-077`; access still precedes loading. |
| `CMP-005` | Enterprise Integration Boundary | Remains authoritative gateway and exact tool registry; specification only declares expected tools. |
| `CMP-006` | Human Review and Approval Boundary | Remains authoritative decision service; specification declares required semantics. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Remains external authority/PDP boundary; local synthetic claims remain a limitation. |
| `CMP-008` | Evaluation and Assurance Boundary | Owns structural/semantic validation, runtime assertion evidence and deny-by-default local gate. |
| `CMP-009` | Observability and Audit Boundary | May record specification digest/assertion/gate evidence in redacted local traces; still not audit/WORM. |
| `CMP-010` | Runtime and Deployment Boundary | Standard-library Python local runtime, file config, gate execution and SQLite/files inherited; no production attestation. |
| `CMP-011` | Source-of-Truth Governance Pack | Owns specification/ADR/register change control and version `1.1.0`. |

No new numbered component is added.

## Agent catalogue

| ID | Name | Purpose/authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | Produces an evidence-backed preliminary regulatory impact assessment. May propose exact `TOOL-001`–`006` through the gateway and complete/escalate. Cannot grant authority, approve/finalize, choose graph routes, alter budgets/leases/policy, invoke direct adapters, use memory, delegate, create agents or run concurrent branches. | Only agent; now formally specified by `AGT-001-spec` `1.0.0`. |

## Specification ownership

- Business owner: Daniel Brooks.
- Technical owner: Priya Raman.
- Risk/model-governance owner: Sofia Alvarez.
- Operations owner: Liam O'Connor.
- Security review: Marcus Green.
- Primary user: Maya Chen.

The owner fields establish accountability, not runtime permission.
