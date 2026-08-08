# 00 — Project Constitution

**Architecture version:** `1.2.0`  
**Repository version:** `1.2.0`  
**Current completed stage:** `S05B`  
**Status:** Accepted local/offline tutorial baseline

## 1. Purpose and scope

The NorthStar Agentic AI Architecture Playbook remains a cumulative, narrative-driven implementation project for **NorthStar Financial Services**. The primary user story, eight accepted personas, `US-001`–`012`, `CMP-001`–`011`, `AGT-001`, `GRAPH-001`, `DATA-009`, `TOOL-001`–`006`, and all accepted external human-approval semantics remain unchanged.

Stage `S05B` adds only the minimum memory capability justified by long-running investigations: deterministic context regeneration, deterministic extractive compaction, and explicitly consented, case-local working memory for session continuity.

## 2. Constitutional invariants carried forward

1. `AGT-001 Regulatory Impact Assessment Agent` remains the only agent.
2. `GRAPH-001` and `DATA-009` remain version `1.1.0`; graph routes, node ownership and state ownership remain application-controlled.
3. Every `TOOL-001`–`006` call remains gateway-only through `CMP-005`; memory cannot grant, widen or replay tool authority.
4. `CMP-006` remains the authoritative human-decision boundary. Timeout never approves, late decisions fail closed, and approved/rejected outcomes remain preliminary rather than final legal/compliance closure.
5. Prompts, specifications, context snapshots, memory, evaluators and registries cannot grant authority.
6. Access authorization occurs before content is loaded into context or memory.
7. Trace, workspace, checkpoint, context and memory records are not audit/WORM, event sourcing, exactly-once proof or final enterprise records.
8. No concurrent graph branches, delegation, MCP, A2A or second agent are enabled.

## 3. S05B state, context and memory constitution

### 3.1 Authoritative state

`DATA-009` remains the current operational truth for the active case. A memory record never overrides, mutates or substitutes for authoritative case state, graph state, approval state, tool results or source repositories.

### 3.2 Context

Context is a time-bounded, purpose-specific projection assembled for one model invocation or work unit. It is regenerated from authorized sources, may be compacted, and is disposable. `DATA-080 ContextSnapshot` is evidence of what was assembled, not a new system of record.

### 3.3 Memory

Only `case_working` memory is enabled. Its sole purpose is `case_session_continuity`. It must:

- be explicitly opted into through `DATA-082 MemoryConsentGrant`;
- be isolated by tenant, case and authorized user;
- contain only facts extracted from authoritative state or human-decision references;
- retain source reference, version and SHA-256 provenance;
- expire within the configured retention ceiling;
- support deletion and content-free tombstones;
- be treated as stale when source versions conflict; and
- never contain approval/callback tokens, signatures, hidden chain-of-thought or final legal/compliance conclusions.

The following remain disabled: cross-case recall, user-profile memory, semantic memory, episodic memory, organizational memory, shared-agent memory and model-direct memory writes.

## 4. Context lifecycle invariants

1. Regeneration uses `authoritative_regeneration_v1` without a model call.
2. Compaction uses `deterministic_extractive_v1`, selects complete typed items, preserves provenance and records omissions.
3. Required case and approval state cannot be evicted. If a required item cannot fit, processing fails closed.
4. The hard Stage 5A boundary remains eight items and 12,000 characters; S05B targets six items and 8,000 characters without expanding the hard maximum.
5. Unauthorized items are omitted before rendering.
6. Model-generated summaries and inferred facts cannot become memory under the accepted S05B policy.
7. Rehydrated memory remains subordinate to current state and current source versions.

## 5. Security and governance principles added

- Explicit purpose limitation and opt-in consent.
- Deny-by-default memory operations.
- Strict tenant/case/user partitioning.
- Idempotent writes and conflict rejection.
- Content hashing and tamper detection for local records.
- Data minimization, bounded values and short provisional retention.
- Deletion/expiry removes record content and retains only a minimal lifecycle tombstone.
- Memory poisoning defenses reject unapproved origins, instruction-like content and authority-bearing fields.
- Production legal basis, retention, records classification, IAM/PDP, KMS, encryption and audit integration remain unresolved.

## 6. Technology and verification baseline

- Python target: `>=3.11,<3.15`.
- Executed interpreter: Python `3.13.5`.
- Runtime dependencies: Python standard library only.
- Test dependency: `pytest 9.0.2`.
- Local persistence: atomic JSON files under a strictly partitioned directory; this is not a production database.
- Schemas: JSON Schema Draft 2020-12 artefacts plus application semantic checks.

## 7. Stage definition of done

S05B is complete only when:

- the state/context/memory boundary is documented and implemented;
- regeneration and compaction are deterministic and budget-bound;
- only case-local working memory is enabled;
- consent, scope, provenance, freshness, expiry and deletion controls are executable;
- all new data/interfaces/ADRs/risks and traceability are registered;
- `TEST-213`–`242` and `EVAL-048`–`054` pass;
- no future-stage agent/concurrency/interoperability capability is enabled; and
- the stage consistency audit passes with explicit exceptions.

## 8. Change history

- `1.1.0` — S05A formal specification and bounded no-memory context policy.
- `1.2.0` — S05B deterministic context lifecycle and minimum case-local working memory.
