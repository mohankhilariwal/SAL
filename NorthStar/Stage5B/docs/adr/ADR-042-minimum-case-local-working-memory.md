# ADR-042 — Enable Only Case-Local Working Memory

- **Status:** Accepted
- **Date:** 2026-08-01

## Context

Maya needs continuity across sessions and human waits. The master architecture also discusses episodic, semantic, user-profile, organizational, shared and private memory, but enabling all categories would expand risk and authority prematurely.

## Decision

Enable only `DATA-081 CaseWorkingMemoryRecord` for `case_session_continuity`. It is managed by the harness, not a direct model tool. It stores only structured facts derived from authoritative state or human-decision references. It is partitioned by tenant/case/user.

Explicitly disable cross-case recall, user-profile, semantic, episodic, organizational and shared-agent memory.

## Alternatives

- No memory — insufficient for repeated-session continuity.
- Full conversation memory — rejected for privacy, poisoning and authority ambiguity.
- Semantic vector memory — rejected because cross-case recall, ranking and deletion complexity are not justified.
- User-profile personalization — rejected because it is unrelated to the current regulatory case goal.

## Rationale

The selected design solves the demonstrated problem with the smallest new attack surface.

## Consequences

NorthStar does not learn reusable case patterns in this stage. Each case remains isolated, and knowledge continues to come from the authorized retrieval boundary.

## Risks and mitigations

- **Risk:** memory is mistaken for organizational knowledge. **Mitigation:** memory kind and purpose are fixed in schema and code.
- **Risk:** model output contaminates memory. **Mitigation:** allowed origins are deterministic and validated.

## Review triggers

A measured business requirement for cross-case precedent retrieval, a second agent, personalization, or knowledge consolidation.
