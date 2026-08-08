# 01 — Business and User Story Baseline

**Version:** `1.2.0`

## 1. Context carried forward

Maya Chen can run the formally specified `AGT-001` workflow, pause for human review and resume safely. The S05A context envelope is authorized and bounded, but an investigation spanning many documents and sessions cannot carry every prior detail without exceeding the eight-item/12,000-character limit.

## 2. S05B narrative state

After reviewing twelve publications and dozens of evidence passages, Maya returns to a case following a human-review wait. Priya Raman refuses two unsafe shortcuts: appending the full transcript and asking a model to create an unconstrained summary. The first would reintroduce stale, restricted and lost-in-the-middle context; the second could silently change qualifiers or invent a durable “fact.”

Elena Petrov implements deterministic regeneration from `DATA-009` and current source references. Marcus Green requires strict tenant/case/user isolation and rejects direct model writes. Sofia Alvarez requires opt-in purpose limitation, provenance, expiry and deletion. Liam O’Connor requires idempotency, tamper detection, bounded storage and failure evidence.

The result is not a general personal-memory system. It is a narrow continuity mechanism for one user working on one regulatory case.

## 3. User-story impact

The accepted `US-001`–`012` remain unchanged. S05B materially advances:

- **`US-001`** — Maya can resume a long investigation with a regenerated, provenance-preserving context.
- **`US-002`** — Daniel retains human accountability because memory cannot approve or finalize.
- **`US-006`** — Sofia can review consent, retention, provenance and deletion evidence.
- **`US-007`** — Liam can detect stale, tampered, expired and deleted local continuity records.
- **`US-009`** — Maya receives only case-scoped, authorized continuity information.
- **`US-011`** — Aisha's ownership and human-reviewed decisions remain authoritative state, not memory-derived conclusions.
- **`US-012`** — Priya can preserve compatibility while keeping future memory categories disabled.

## 4. Business acceptance criteria

1. A case can resume without memory by regenerating context from authoritative state.
2. With valid opt-in, a compact case-local continuity record can be written and read.
3. A record from another tenant, case or unauthorized user is never returned.
4. Current authoritative state and current source versions take precedence over memory.
5. Stale records are excluded by default.
6. Expiry and user-requested deletion remove record content.
7. Memory cannot contain approval tokens, signatures, final closure or hidden reasoning.
8. The hard S05A context budget is not expanded.
9. Human review and all tool controls are unchanged.

## 5. Explicitly out of scope

- Remembering preferences across cases or users.
- Learning organization-wide regulatory knowledge from cases.
- Vector/semantic memory search.
- Episodic transcript memory.
- Shared multi-agent memory or blackboard coordination.
- Model-authored durable summaries.
- Autonomous conflict resolution between sources.
- Production records-management or legal conclusions.

## 6. Business outcome of S05B

NorthStar can now preserve case continuity without treating a growing transcript as truth. The implementation reduces repeated context transfer while retaining explicit source bindings, but it remains a local tutorial control path with synthetic identity and consent.

## 7. Unresolved business question

`AGT-001` still spans research, obligation extraction, policy/control mapping, risk assessment and report generation. NorthStar must next decide whether the single agent plus specialized graph nodes remains the safer design or whether distinct bounded agents create enough value to justify new handoff, coordination, authority and shared-context risks.
