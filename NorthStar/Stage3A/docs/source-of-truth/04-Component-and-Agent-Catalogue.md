# 04 — Component and Agent Catalogue

**Version:** `0.5.0`

## Components

| ID | Name | S03A status/responsibility |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Partial local caller/display. |
| `CMP-002` | Regulatory Intake Boundary | Retained S01 bounded intake. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Partial deterministic call sequence; no agent state/loop. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Implemented through S02B; exposed by `TOOL-003` without access widening. |
| `CMP-005` | Enterprise Integration Boundary | **Partial/new:** tool registry, gateway and six local adapters. No live enterprise connector. |
| `CMP-006` | Human Review and Approval Boundary | Planned; `TOOL-006` creates only a local queued request. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Planned enterprise service; local deterministic policy uses unauthenticated claims. |
| `CMP-008` | Evaluation and Assurance Boundary | Partial preparation, retrieval and tool/gateway evaluation. |
| `CMP-009` | Observability and Audit Boundary | Partial local JSONL execution evidence; not audit ledger. |
| `CMP-010` | Runtime and Deployment Boundary | Partial local Python runtime. |
| `CMP-011` | Source-of-Truth Governance Pack | Implemented and updated to `0.5.0`. |

## Agent inventory

None. No `AGT-*` identifier is allocated. The demo is a deterministic application caller and cannot select actions from a goal, replan, maintain `DATA-009`, or determine termination.

## Tool inventory

| ID | Name | Impact | Authority and implementation status |
|---|---|---|---|
| `TOOL-001` | `search_regulatory_catalogue` | Read-only | Synthetic local catalogue; not live/authoritative. |
| `TOOL-002` | `query_control_catalogue` | Read-only | Synthetic local controls; not authoritative repository. |
| `TOOL-003` | `search_authorized_evidence` | Read-only | Local adapter preserving S02B authorization and citation semantics. |
| `TOOL-004` | `create_draft_regulatory_case` | Reversible write | Local `DRAFT_UNAPPROVED` artefact only. |
| `TOOL-005` | `save_candidate_mapping` | Reversible write | Local `CANDIDATE_UNAPPROVED`, `accepted=false` only. |
| `TOOL-006` | `queue_human_review_request` | Reversible write | Local queue record; `approval_granted=false`, no external notification. |

No irreversible write, financial, administrative or safety-critical tool is registered.
