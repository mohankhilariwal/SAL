# 04 — Component and Agent Catalogue

**Version:** `1.0.0`

## 1. Components

| ID | Name | Stage 4C responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Calls harness start/status/decision/resume surfaces; no browser UI implemented. |
| `CMP-002` | Regulatory Intake Boundary | Retained bounded publication intake and provenance. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Owns the framework-neutral harness lifecycle and delegates execution to unchanged `GRAPH-001` 1.1.0. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Supplies authorized typed context sources; access remains before text assembly. |
| `CMP-005` | Enterprise Integration Boundary | Authoritative frozen tool registry/gateway; `TOOL-001`–`006` only; idempotent effects retained. |
| `CMP-006` | Human Review and Approval Boundary | Existing external typed decision service; harness exposes lifecycle but does not approve or interpret decisions. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Synthetic principal/role checks retained; context authorization input and enterprise IAM/PDP remain pending. |
| `CMP-008` | Evaluation and Assurance Boundary | Deterministic validators and observer-only lifecycle evaluation hooks. |
| `CMP-009` | Observability and Audit Boundary | Redacted local JSONL trace evidence; explicitly not production audit. |
| `CMP-010` | Runtime and Deployment Boundary | Python 3.13.5, SQLite, session/workspace manager, local filesystem, sequential runner and resume lease. |
| `CMP-011` | Source-of-Truth Governance Pack | Updated to architecture/repository/handoff 1.0.0. |## 2. Agent inventory

| ID | Name | Authority | S04C status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | May propose registered `TOOL-001`–`006`, complete or escalate within its existing goal. Cannot register capabilities, grant authority, choose graph nodes, set waits/timeouts/leases, approve/finalize, access memory, delegate or create agents. | Only agent; executed through the harness. |

## 3. Harness submodules (not new components or agents)

| Module | Responsibility | Explicit non-responsibility |
|---|---|---|
| `harness.factory` | Compose accepted adapters from versioned config. | No dynamic service discovery or control plane. |
| `harness.instructions` | Load and hash `DATA-064`. | No authorization or policy enforcement. |
| `harness.context` | Access-before-load, ordering, quotas and `DATA-065`. | No memory and no semantic trust of content. |
| `harness.registries` | Duplicate rejection and freeze semantics. | No distributed registry or runtime tool creation. |
| `harness.workspace` | Session root, JSON/JSONL allowlist and byte quotas. | No code execution sandbox, DLP or records management. |
| `harness.validation` | Cross-cutting lifecycle assertions. | Does not replace graph/tool/approval owners. |
| `harness.hooks` | Observer-only evaluation findings. | Cannot mutate, authorize or route. |
| `harness.tracing` | Correlated redacted local events. | Not audit/WORM or hidden reasoning. |
| `harness.runtime` | Start/decision/resume composition and typed result. | Does not become a second workflow engine. |

## 4. Component-change rule

No `CMP-*` ID is added or renamed. A later extraction into a separately deployed harness service would require scaling/trust/ownership evidence and a new ADR.
