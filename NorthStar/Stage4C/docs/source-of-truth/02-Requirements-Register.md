# 02 — Requirements Register

**Version:** `1.0.0`

## 1. Inherited register

All accepted `FR-001`–`105`, `NFR-001`–`083`, `POL-*` and `CTL-001`–`059` remain in force. S04C does not renumber or weaken them. The S04B constraints on access-before-context, gateway-only tools, budgets/recovery/reconciliation, typed graph state, durable waits, timeout, lease ownership and preliminary human-accountability semantics remain mandatory.

## 2. New functional requirements

| ID | Requirement | Architecture/implementation | Controls | Verification |
|---|---|---|---|---|
| `FR-106` | Load one immutable, versioned harness manifest binding AGT-001, GRAPH-001 1.1.0, tools, instructions, validators and hooks. | CMP-003/CMP-010; DATA-063; INT-041 | CTL-060, CTL-061 | TEST-159, TEST-160; EVAL-040 |
| `FR-107` | Resolve the AGT-001 system instruction by name/version and verify its SHA-256 before execution. | CMP-003; DATA-064; INT-042 | CTL-062 | TEST-161; EVAL-040 |
| `FR-108` | Authorize each context source before invoking its loader or exposing its text. | CMP-004/CMP-007; INT-043 | CTL-063 | TEST-162; EVAL-040 |
| `FR-109` | Assemble a bounded, ordered, provenance-preserving typed context envelope and record omitted/truncated sources. | CMP-003/CMP-004; DATA-065; INT-043 | CTL-064 | TEST-163, TEST-164 |
| `FR-110` | Create one isolated session and bounded workspace for each harness run without persisting raw approval tokens or secrets. | CMP-003/CMP-010; DATA-066, DATA-067; INT-044 | CTL-065, CTL-066 | TEST-166, TEST-171, TEST-180; EVAL-041 |
| `FR-111` | Delegate execution to unchanged GRAPH-001 1.1.0 and preserve application-owned route, checkpoint, approval and lease semantics. | CMP-003/CMP-006/CMP-010; INT-041 | CTL-067 | TEST-170, TEST-172–177; EVAL-037–039 |
| `FR-112` | Expose only the immutable registered TOOL-001–006 set and continue every tool call through CMP-005/INT-017. | CMP-005; INT-041 | CTL-068 | TEST-165, TEST-169, TEST-172 |
| `FR-113` | Run deterministic validators at pre-start, post-context, post-start, pre-resume and post-resume lifecycle points. | CMP-003/CMP-008; INT-045 | CTL-069 | TEST-159–164, TEST-176, TEST-177 |
| `FR-114` | Run observer-only evaluation hooks that cannot mutate state, register capabilities, grant authority or choose routes. | CMP-008; DATA-069; INT-045 | CTL-070 | TEST-168; EVAL-040 |
| `FR-115` | Emit correlated, redacted local trace events for start, suspend, accepted decision, resume and completion. | CMP-009; DATA-068; INT-046 | CTL-071 | TEST-167, TEST-180, TEST-181; EVAL-037–041 |
| `FR-116` | Persist replayable session metadata, instruction metadata, context envelope and non-secret run results in the workspace. | CMP-003/CMP-010; DATA-064–067, DATA-070; INT-044 | CTL-065, CTL-066 | TEST-170, TEST-171, TEST-175 |
| `FR-117` | Bind restarted sessions to the accepted manifest, graph version, instruction digest and context digest and fail closed on mismatch. | CMP-003/CMP-010; DATA-063, DATA-066; INT-041, INT-044 | CTL-060, CTL-061, CTL-067 | TEST-175–177 |
| `FR-118` | Keep memory, concurrent graph branches and multiple agents disabled and reject attempts to introduce them through configuration or context. | CMP-003/CMP-010; DATA-063; INT-041, INT-043 | CTL-061, CTL-064 | TEST-160, TEST-163, TEST-168, TEST-182; EVAL-040 |
| `FR-119` | Return one typed harness result while retaining preliminary human-accountability dispositions and external human decisions. | CMP-003/CMP-006; DATA-070; INT-041 | CTL-067, CTL-069 | TEST-170, TEST-172–174, TEST-178–179; EVAL-037–039 |

## 3. New non-functional requirements

| ID | Quality | Requirement |
|---|---|---|
| `NFR-084` | Reproducibility | The manifest, instruction and context are versioned/hashed so a run can be attributed to the exact assembled inputs. |
| `NFR-085` | Fail-closed compatibility | Manifest, graph, session, instruction or context mismatch must stop before continuation. |
| `NFR-086` | Privacy | Trace/workspace output must redact or reject approval tokens, credentials, authorization headers and hidden reasoning. |
| `NFR-087` | Bounded storage | Per-file and per-workspace quotas must cap local artefact growth. |
| `NFR-088` | Framework neutrality | Harness contracts must not expose framework-specific types and must preserve migration options. |
| `NFR-089` | Low local dependency | The runnable reference runtime remains Python-standard-library-only; pytest is development-only. |
| `NFR-090` | Lifecycle correlation | Session, run and trace identifiers must correlate start, wait, decision and resume evidence. |
| `NFR-091` | Session isolation | Workspace paths are session-scoped and path traversal is rejected. |
| `NFR-092` | Authority preservation | Instructions, hooks and model arguments cannot grant tool, approval, routing or state authority. |
| `NFR-093` | Operational separation | Tracing is diagnostic evidence and must not be represented as the production audit ledger. |
| `NFR-094` | Compatibility | DATA-009 remains 1.1.0 and GRAPH-001 remains 1.1.0 for all Stage 4C runs. |
| `NFR-095` | Testability | Every harness lifecycle boundary must be substitutable and covered by deterministic local tests. |

## 4. New deterministic controls

| ID | Control | Enforcement |
|---|---|---|
| `CTL-060` | Manifest digest verification | Calculate DATA-063 digest and compare it at start/resume. |
| `CTL-061` | Future-capability deny rule | Reject memory_enabled, concurrent_graph_branches or multiple_agents_enabled. |
| `CTL-062` | Instruction integrity check | Verify DATA-064 SHA-256 against DATA-063 before context or graph execution. |
| `CTL-063` | Access-before-load | Do not invoke a ContextSource loader until its authorization decision is true. |
| `CTL-064` | Typed context allowlist and budget | Allow only publication/evidence/run_state/policy_context; reject memory; bound item/character counts. |
| `CTL-065` | Workspace containment and quotas | Resolve paths under the session root, allow only JSON/JSONL, enforce file/workspace byte limits. |
| `CTL-066` | Sensitive-field exclusion | Reject raw secret/token/authorization/hidden-reasoning fields; allow only explicit redacted placeholders. |
| `CTL-067` | Graph and approval delegation | Harness calls existing graph/approval contracts; it cannot choose routes or interpret decisions. |
| `CTL-068` | Frozen capability registry | Reject duplicate registrations and freeze before runtime; model text cannot alter it. |
| `CTL-069` | Lifecycle validation pipeline | Run manifest, context and result validators at defined lifecycle points. |
| `CTL-070` | Observer-only hooks | Hooks receive copied summaries, return findings, and have no graph/store/gateway handles. |
| `CTL-071` | Redacted trace emission | Sanitize sensitive keys, truncate long strings and label local JSONL as non-audit evidence. |

## 5. Traceability summary

- `FR-106`–`119` trace to `DATA-063`–`070`, `INT-041`–`046`, `ADR-033`–`035`, `CTL-060`–`071`, `TEST-159`–`182` and `EVAL-037`–`041`.
- No new requirement authorizes final legal/compliance closure, memory, concurrent graph branches, a second agent, delegation or tool bypass.
- Production SLO thresholds remain open under `ISS-048`; this stage measures control behavior, not enterprise capacity.
