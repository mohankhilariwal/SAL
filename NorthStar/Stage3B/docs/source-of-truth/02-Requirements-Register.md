# 02 — Requirements Register

**Version:** `0.6.0`

All previously accepted `US-001`–`US-012`, `FR-001`–`FR-060`, `NFR-001`–`NFR-046`, `POL-*` and `CTL-001`–`CTL-026` retain their accepted meaning. S03B adds only the following requirements.

## Functional requirements

| ID | Requirement | Component/data/interface | Control | Verification |
|---|---|---|---|---|
| `FR-061` | Accept one typed goal, assign `RUN-*` identity and instantiate executable `DATA-009 AgentRunState`. | `CMP-003`, `DATA-009`, `DATA-041`, `INT-021` | `CTL-028` | `TEST-078`, `TEST-086` |
| `FR-062` | Request exactly one schema-valid decision per iteration: `call_tool`, `complete` or `escalate`. | `AGT-001`, `DATA-042`, `INT-022` | `CTL-027` | `TEST-074`, `TEST-075` |
| `FR-063` | Permit `AGT-001` to propose only `TOOL-001`–`TOOL-006`; inject trusted principal context outside the decision provider and route every call through `INT-017`. | `AGT-001`, `CMP-005`, `DATA-034` | `CTL-031` | `TEST-083`, `TEST-084` |
| `FR-064` | Convert only validated gateway results into `DATA-043 AgentObservation` and update application-owned artifacts/milestones. | `CMP-003`, `DATA-038`, `DATA-043`, `INT-023` | `CTL-028` | `TEST-078`, `TEST-086` |
| `FR-065` | Track action signatures, repeated actions and no-progress windows; stop with an explicit guard reason. | `DATA-009`, `INT-024` | `CTL-029` | `TEST-081` |
| `FR-066` | Treat completion as valid only when required milestones and unapproved/human-review invariants are present. | `DATA-009`, `DATA-044`, `INT-024` | `CTL-030` | `TEST-077`, `TEST-079` |
| `FR-067` | Support terminal outcomes `completed`, `escalated` and `terminated_guard`, each with a typed reason and partial milestone/artifact summary. | `DATA-044`, `INT-025` | `CTL-032` | `TEST-079`–`TEST-082` |
| `FR-068` | Persist final local run state and outcome without representing them as an enterprise record or audit ledger. | `CMP-009`, `CMP-010`, `DATA-044`, `INT-025` | `CTL-032` | `TEST-078` |
| `FR-069` | Keep the decision provider behind a provider-neutral contract; use a deterministic rule provider as the accepted offline oracle. | `AGT-001`, `INT-022` | `CTL-027` | `TEST-078`, `EVAL-018` |
| `FR-070` | Stop S03B before graph, durable recovery, memory, multi-agent, MCP/A2A or production control-plane implementation. | architecture/repository | stage boundary | `TEST-087`, consistency audit |

## Non-functional requirements

| ID | Requirement | Verification |
|---|---|---|
| `NFR-047` | A run must have a finite positive iteration limit; disabling the limit is not accepted in S03B. | `TEST-076`, `TEST-080` |
| `NFR-048` | Decision and terminal schemas must fail closed on missing or contradictory fields. | `TEST-074`, `TEST-075` |
| `NFR-049` | Completion, authority and final disposition must be deterministic application decisions outside model reasoning. | `TEST-079`, `TEST-083`, `TEST-084` |
| `NFR-050` | Progress milestones are monotonic within a run and derived only from validated tool outputs. | `TEST-078`, `TEST-086` |
| `NFR-051` | Terminal output must preserve `preliminary_grounded_unapproved` and `human_review_required=true`. | `TEST-078`, `TEST-080` |
| `NFR-052` | The local accepted implementation must run without a managed model or paid service. | demo/test evidence |
| `NFR-053` | Persist concise reasons, actions, observations and outcomes; do not require hidden chain-of-thought. | code inspection, consistency audit |
| `NFR-054` | Existing S01/S02/S03A evidence, permission and tool-gateway invariants remain compatible. | `TEST-085`, structural validation |

## New control objectives

| ID | Name | Enforced by |
|---|---|---|
| `CTL-027` | Structured Agent Decision Contract | `AgentDecision.validate`, `INT-022` |
| `CTL-028` | Agent Run State Integrity | `DATA-009`, runtime projection, typed observations |
| `CTL-029` | Iteration, Repetition and Progress Guard | `TerminationEvaluator` |
| `CTL-030` | Deterministic Completion Invariant | required milestones and status/linkage checks |
| `CTL-031` | Agent Authority Boundary | allowlisted tools, application-injected principal, `CMP-005` |
| `CTL-032` | Terminal Outcome Evidence | final local state/outcome file with typed reason |

## Evaluation claims

| Evaluation | Claim |
|---|---|
| `EVAL-018` | The accepted happy-path run reaches six milestones and completes only after a seventh decision. |
| `EVAL-019` | Premature completion, explicit escalation and iteration exhaustion produce the correct non-success terminal reasons. |
| `EVAL-020` | Non-allowlisted tools and model-supplied authority fields cannot bypass deterministic enforcement. |
| `EVAL-021` | Maya receives zero restricted Borealis citations; S03B adds exactly one agent and no graph/memory/multi-agent modules. |
