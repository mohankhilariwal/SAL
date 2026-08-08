# 05 — Data and Schema Register

**Version:** `1.2.0`  
**Existing objects:** `DATA-001`–`078` and `INT-001`–`052` remain accepted. `DATA-009` remains `1.1.0`.

## 1. New data objects

| ID | Name | Purpose / owner | Key constraints |
|---|---|---|---|
| `DATA-079` | ContextRegenerationPlan | `CMP-003`; reproducible input plan for context assembly | `authoritative_regeneration_v1`; exact tenant/case/user scope; binds `DATA-009` version and budgets. |
| `DATA-080` | ContextSnapshot | `CMP-003`; compact invocation context and evidence | `deterministic_extractive_v1`; included IDs, omitted refs, facts, source bindings, counts and digest. No authority. |
| `DATA-081` | CaseWorkingMemoryRecord | `CMP-003/010`; optional continuity memory | only `case_working`; consent ID; tenant/case/user authorization; authoritative origins; expiry/status/idempotency/digest. |
| `DATA-082` | MemoryConsentGrant | `CMP-007`; operation and purpose authorization | purpose `case_session_continuity`; write/read/delete allowlist; issue/expiry/revocation; exact scope. |
| `DATA-083` | MemoryQuery | `CMP-003`; scoped read request | tenant/case/user, kind `case_working`, stale disabled by default. |
| `DATA-084` | MemoryReadResult | `CMP-003/010`; read result | returned/stale/denied IDs and authorized records. |
| `DATA-085` | MemoryDeletionRequest | `CMP-007/010`; delete command | exact scope/record/reason/request time. |
| `DATA-086` | MemoryLifecycleResult | `CMP-010`; deletion/expiry evidence | previous/new status, content removed, tombstone path and completion time. |

Draft 2020-12 schema artefacts are under `schemas/DATA-079...DATA-086*.schema.json`. Application validation remains authoritative for cross-object semantic rules.

## 2. Updated objects

- `DATA-071 AgentSpecification` advances from `AGT-001-spec 1.0.0` to `1.1.0` and declares the narrow memory boundary.
- `DATA-077 ContextPolicyProfile` advances to `1.1.0`; it retains the hard 8/12,000 budget and permits only harness-managed `case_working` context when explicit consent and scope checks pass.
- `DATA-063 HarnessManifest` advances to `1.2.0`; graph and state bindings remain `1.1.0`.
- `DATA-065 AuthorizedContextEnvelope` remains the invocation envelope; `DATA-080` is its regenerated/compacted source for S05B.

## 3. New interfaces

| ID | Name | Input → output | Authorization/control |
|---|---|---|---|
| `INT-053` | Context Regeneration Contract | scope + authorized `DATA-009` + source metadata → `DATA-079` + typed context items | exact tenant/case/user; authoritative sources only; no model call. |
| `INT-054` | Context Compaction Contract | regenerated items + budgets → `DATA-080` | complete-item selection; required items pinned; unauthorized omitted; omissions recorded. |
| `INT-055` | Case Working Memory Write Contract | `DATA-080` + `DATA-082` + idempotency key → `DATA-081` | consent/purpose/scope/origin/provenance/TTL/poison checks; no model-direct caller. |
| `INT-056` | Case Working Memory Read Contract | `DATA-083` + `DATA-082` + current source versions → `DATA-084` | exact partition and user; active/unexpired/non-stale by default. |
| `INT-057` | Memory Delete and Expire Contract | `DATA-085` or retention timer → `DATA-086` | authorized delete or policy expiry; content removal; minimal tombstone. |
| `INT-058` | Memory Policy and Consent Validation Contract | principal/scope/purpose/operation/grant/policy → allow/deny obligations | deny by default; conceptually owned by `CMP-007`; local synthetic grant only. |

## 4. State-versus-memory rules

- `DATA-009` always wins over `DATA-081`.
- Current source versions win over stored source bindings.
- A conflicting/stale record is excluded rather than merged automatically.
- A new record supersedes the previous active record; history is not consolidated into an ever-growing profile.
- Deleted/expired content cannot be reconstructed from the tombstone.
- Memory records cannot contain callback/approval tokens, signatures, hidden chain-of-thought, final legal conclusions or final compliance closure.

## 5. Storage layout

```text
<configured-memory-root>/
└── <tenant_id>/
    └── <case_id>/
        ├── MWR-*.record.json
        └── MWR-*.tombstone.json
```

User identity is verified in the record/consent, not encoded as a path segment. The local path design includes safe-identifier and root-containment checks. It is a tutorial layout, not a production tenancy model.
