# 04 — Component and Agent Catalogue

## Component inventory

| ID | Name | Current responsibility/status after S02B |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Partial local CLI/evidence consumer; no authenticated enterprise UI. |
| `CMP-002` | Regulatory Intake Boundary | Retained bounded S01 publication intake. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Partial one-shot flow; may call fixed retrieval service but owns no durable case/workflow state. |
| `CMP-004` | Knowledge and Evidence Access Boundary | **Partial implemented:** S02A preparation plus S02B authorized filtering, BM25, latent semantic ranking, RRF, deterministic reranking, overlap suppression, exact citations and context assembly. No live connector or grounded answer generation. |
| `CMP-005` | Enterprise Integration Boundary | Planned; no authoritative repository, regulator, control, case or notification connector. |
| `CMP-006` | Human Review and Approval Boundary | Planned; S01 preliminary/human-review semantics retained. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Planned; S02B consumes locally asserted principal attributes and does not authenticate them. |
| `CMP-008` | Evaluation and Assurance Boundary | Partial implemented: preparation integrity plus retrieval relevance, citation, duplication, latency and permission-boundary cases. |
| `CMP-009` | Observability and Audit Boundary | Partial local manifests, ranking reasons and reports; not append-only/tamper-evident audit. |
| `CMP-010` | Runtime and Deployment Boundary | Partial local Python 3.13.5 runtime. |
| `CMP-011` | Source-of-Truth Governance Pack | Implemented and updated to `0.4.0`. |

## Internal responsibilities within `CMP-004`

- Prepared corpus loader and validator.
- Query-time authorization filter.
- BM25 lexical ranker.
- Latent semantic vector ranker.
- RRF fusion.
- Metadata-aware deterministic reranker.
- Overlap-aware evidence selector.
- Citation builder and validator.
- Retrieval context assembler.
- Index-manifest builder and compatibility validator.

These are modules inside one logical boundary, not newly numbered enterprise components.

## Agent inventory

None. No `AGT-*` identifier is allocated. The service follows a fixed application pipeline and cannot choose tools, replan, delegate, loop or own authority.

## Tool inventory

None. No `TOOL-*` identifier is allocated. `INT-012`–`INT-015` are service contracts, not model-selectable capabilities.
