# 02 — Requirements Register

**Version:** `1.2.0`  
**Prior requirements:** `FR-001`–`136`, `NFR-001`–`107`, and `CTL-001`–`084` remain accepted.

## 1. Functional requirements added in S05B

| ID | Requirement | Owner / implementation | Verification |
|---|---|---|---|
| `FR-137` | Regenerate invocation context from authorized `DATA-009` state and current source references without a model call. | `CMP-003`; `ContextRegenerator`; `INT-053` | `TEST-213/214/220`, `EVAL-048` |
| `FR-138` | Separate authoritative state, disposable context snapshots and optional memory records. | `CMP-003/004`; `DATA-079`–`081` | `TEST-213/216`, `EVAL-048` |
| `FR-139` | Compact context deterministically by selecting complete typed items while preserving source bindings and omissions. | `CMP-003`; `ContextCompactor`; `INT-054` | `TEST-215`–`218/222`, `EVAL-049` |
| `FR-140` | Preserve required case-state and approval-state items; fail closed when they cannot fit. | `CMP-003`; `CTL-087` | `TEST-216/222` |
| `FR-141` | Keep the hard context limit at eight items/12,000 characters. | `DATA-077 v1.1.0`; `MEM-POL-001` | `TEST-215/221`, `EVAL-049` |
| `FR-142` | Enable only `case_working` memory for `case_session_continuity`. | `CMP-003`; `DATA-081`; `INT-055/056` | `TEST-225/232/241`, `EVAL-050` |
| `FR-143` | Require explicit, unexpired, unrevoked opt-in consent for memory write/read/delete. | `CMP-007`; `DATA-082`; `INT-058` | `TEST-223/224/233`–`235`, `EVAL-051` |
| `FR-144` | Restrict memory facts to authoritative state or human-decision references with source ID, version and digest. | `CMP-003/004`; `MemoryPolicy`; `CTL-091` | `TEST-213/236`, `EVAL-050/052` |
| `FR-145` | Isolate memory by tenant, case and authorized user. | `CMP-007/010`; `LocalCaseMemoryStore` | `TEST-220/233`–`235/240`, `EVAL-051` |
| `FR-146` | Make memory writes idempotent and reject reuse of a key with different content. | `CMP-003/010`; `write_request_id` | `TEST-226/227`, `EVAL-050` |
| `FR-147` | Keep at most one active continuity record per case; a new record supersedes the prior one. | `CMP-003`; local store | `TEST-228`, `EVAL-050` |
| `FR-148` | Mark source-version conflicts stale and exclude stale memory by default. | `CMP-004`; `INT-056` | `TEST-231`, `EVAL-052` |
| `FR-149` | Enforce provisional TTL, automatic expiry and content removal. | `CMP-010`; `INT-057` | `TEST-230`, `EVAL-053` |
| `FR-150` | Support authorized deletion with a content-free lifecycle tombstone. | `CMP-007/010`; `DATA-085/086` | `TEST-229`, `EVAL-053` |
| `FR-151` | Reject model-generated facts, instruction-like memory and prohibited authority/sensitive fields. | `CMP-003/008`; write validator | `TEST-236`–`238`, `EVAL-052` |
| `FR-152` | Verify local memory content digests and reject tampered records. | `CMP-009/010`; local store | `TEST-239`, `EVAL-052` |
| `FR-153` | Permit context regeneration and workflow resumption without memory. | `CMP-003`; `ContextLifecycleEngine` | `TEST-232`, `EVAL-048` |
| `FR-154` | Preserve one agent, sequential graph execution, gateway authority and external human approval. | all existing control owners | `TEST-242`, `EVAL-054` |

## 2. Non-functional requirements added in S05B

| ID | Requirement | Measure / status |
|---|---|---|
| `NFR-108` | Deterministic regeneration for identical state/version inputs except generation timestamps. | Passed locally (`TEST-214`). |
| `NFR-109` | Deterministic extractive compaction; no model summarization on the critical path. | Passed locally. |
| `NFR-110` | Default target ≤6 items and ≤8,000 characters; hard maximum unchanged. | Passed locally; production tuning pending. |
| `NFR-111` | Local context lifecycle remains standard-library-only and runnable offline. | Passed on Python 3.13.5. |
| `NFR-112` | Memory operations fail closed on missing/invalid consent or scope mismatch. | Passed locally. |
| `NFR-113` | Local writes are atomic and content-addressed/digest-verified. | Passed locally; no KMS/signature. |
| `NFR-114` | Memory content is minimized and time-limited; default 14 days, maximum 30 days are provisional tutorial values. | Implemented; legal/records approval pending. |
| `NFR-115` | Deletion/expiry removes content and leaves no fact values in the tombstone. | Passed locally. |
| `NFR-116` | Context lifecycle adds no concurrency or multi-agent behavior. | Passed structurally. |
| `NFR-117` | Stale-source detection is deterministic and default-excluding. | Passed locally. |
| `NFR-118` | Security-sensitive tokens and hidden reasoning are excluded from regenerated/persisted content. | Passed locally. |
| `NFR-119` | Local performance is benchmarked without claiming production SLOs. | `EVAL-054`; report generated. |
| `NFR-120` | Memory policy/configuration is versioned and deny-by-default. | `MEM-POL-001`; passed validator. |
| `NFR-121` | All schema, repository, diagram, ADR and handoff references remain consistent. | Stage consistency audit. |

## 3. Controls added in S05B

| ID | Control |
|---|---|
| `CTL-085` | Authoritative-state-first context regeneration. |
| `CTL-086` | Access and scope verification before content assembly. |
| `CTL-087` | Required-context pinning and fail-closed overflow. |
| `CTL-088` | Complete-item extractive compaction with omission ledger. |
| `CTL-089` | Hard context budget preservation. |
| `CTL-090` | Explicit consent and purpose validation for each memory operation. |
| `CTL-091` | Provenance/origin allowlist for memory facts. |
| `CTL-092` | Tenant/case/user partition and safe-path validation. |
| `CTL-093` | Idempotent write request and content-conflict rejection. |
| `CTL-094` | Single active record with supersession. |
| `CTL-095` | Source-version staleness filtering. |
| `CTL-096` | TTL ceiling, automatic expiry and deletion. |
| `CTL-097` | Poisoning/authority-field/token exclusion. |
| `CTL-098` | SHA-256 record-integrity verification. |
| `CTL-099` | Structural future-capability denial: one agent, no concurrency, no cross-case/profile/semantic/episodic/organizational/shared memory. |

## 4. Traceability summary

Every new functional requirement maps to at least one accepted component, one implementation module or interface, one deterministic control, one numbered test and one evaluation. `ADR-040`–`043` record the selected designs. No previous requirement or control is renamed, renumbered or superseded.
