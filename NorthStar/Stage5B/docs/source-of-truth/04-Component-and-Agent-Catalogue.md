# 04 — Component and Agent Catalogue

**Version:** `1.2.0`

## 1. Components

No new numbered component is introduced. Existing boundaries receive these S05B responsibilities:

| ID | Name | S05B responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Requests resume and displays consent/continuity status; no new authority or UI implementation claim. |
| `CMP-002` | Regulatory Intake Boundary | Continues source identity/version/provenance; no memory ownership. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Owns context regeneration, compaction and calls to the memory lifecycle service. It never lets memory override `DATA-009`. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Supplies current authorized source bindings and versions used for context and stale-memory checks. |
| `CMP-005` | Enterprise Integration Boundary | Unchanged authoritative gateway for `TOOL-001`–`006`; memory is not a tool capability. |
| `CMP-006` | Human Review and Approval Boundary | Unchanged authoritative decision service; decision references may be projected, but signatures/tokens are excluded. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Owns consent, purpose and scope decisions conceptually; implementation uses synthetic local grants. |
| `CMP-008` | Evaluation and Assurance Boundary | Validates context/memory policy and runs `EVAL-048`–`054`. |
| `CMP-009` | Observability and Audit Boundary | Receives redacted lifecycle evidence; no fact content required in tombstones; still not audit/WORM. |
| `CMP-010` | Runtime and Deployment Boundary | Hosts the local atomic JSON store, expiry and deletion jobs; no production database/KMS. |
| `CMP-011` | Source-of-Truth Governance Pack | Maintains version `1.2.0`, policy, schemas, ADRs, traceability and handoff. |

## 2. Agent inventory

| ID | Name | Authority and S05B memory boundary | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | May propose exact `TOOL-001`–`006` only through `CMP-005`. It cannot write memory directly, grant consent, widen scope, approve/finalize, choose graph routes, delegate, create agents or run concurrent branches. It may receive a harness-built `DATA-080` snapshot containing authorized case-local continuity facts. | Only agent; `AGT-001-spec` advances to `1.1.0`. |

## 3. Tool catalogue

`TOOL-001`–`003` remain read-only and `TOOL-004`–`006` remain reversible unapproved writes, all version `1.0.0` and gateway-only. Memory operations are internal harness/service interfaces, not agent tools. This prevents a model from selecting a memory-write capability or persisting arbitrary free text.

## 4. Component interaction constraints

1. `CMP-003` asks `CMP-007` for memory-operation authorization before `CMP-010` is accessed.
2. `CMP-004` must provide current source versions before memory is considered fresh.
3. `CMP-010` cannot return records outside the resolved tenant/case partition.
4. `CMP-008` blocks a release that enables forbidden memory categories or expands context budgets.
5. `CMP-009` records identifiers/status/timing but should not duplicate protected memory values.
