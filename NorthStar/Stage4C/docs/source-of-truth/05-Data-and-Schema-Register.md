# 05 — Data and Schema Register

**Version:** `1.0.0`

## 1. Inherited objects

`DATA-001`–`062` remain accepted. `DATA-007 ReviewDecision` stays external, typed, expiring/single-use through S04B controls. `DATA-009 AgentRunState` remains schema `1.1.0`; `DATA-058`–`062` retain durable workflow/wait/token-claims/inbox/lease semantics. No inherited schema is retired or reinterpreted as memory or audit.

## 2. New executable objects

| ID | Name | Schema | Owner | Purpose |
|---|---|---|---|---|
| `DATA-063` | HarnessManifest | `1.0.0` | CMP-003/CMP-010 | Binds architecture/repository, AGT-001, GRAPH-001 1.1.0, tool versions, instruction hash, validators/hooks and disabled future-stage flags. |
| `DATA-064` | InstructionBundle | `1.0.0` | CMP-003 | Versioned system instruction, SHA-256 and explicit critical-controls-external flag. |
| `DATA-065` | ContextEnvelope | `1.0.0` | CMP-003/CMP-004 | Ordered authorized context items, hashes, classification/purpose, truncation/omission and aggregate digest. |
| `DATA-066` | HarnessSession | `1.0.0` | CMP-003/CMP-010 | Session, initiator, manifest/trace/instruction/context digests, workspace path and lifecycle status. |
| `DATA-067` | WorkspaceManifest | `1.0.0` | CMP-010 | Session-scoped root, allowed suffixes, per-file/workspace quotas and creation time. |
| `DATA-068` | TraceEvent | `1.0.0` | CMP-009 | Trace/span/session/run correlation, lifecycle event, time and redacted attributes. |
| `DATA-069` | HookResult | `1.0.0` | CMP-008 | Observer hook name/event/status and concise findings. |
| `DATA-070` | HarnessRunResult | `1.0.0` | CMP-003 | Typed session/run status, node, preliminary disposition, review outcome, digests, trace and hook findings; token transient only. |

## 3. Interfaces

`INT-001`–`040` remain accepted. New contracts:

| ID | Name | Contract | Controls |
|---|---|---|---|
| `INT-041` | Harness Bootstrap and Lifecycle Contract | request + accepted config -> start/decision/resume result | Manifest/session binding, one agent, delegate to existing graph/gateway/approval. |
| `INT-042` | Instruction Resolution Contract | name/version/expected hash -> DATA-064 | Fail on missing file, empty content or hash mismatch. |
| `INT-043` | Context Assembly Contract | typed source descriptors + authorization + quotas -> DATA-065 | Check access before loader; reject memory/unsupported kinds; deterministic order/bounds. |
| `INT-044` | Session and Workspace Contract | session metadata + safe relative artefacts -> DATA-066/067 | Root containment, suffix allowlist, quotas, sensitive-field exclusion, no raw token. |
| `INT-045` | Lifecycle Validation and Evaluation Hook Contract | lifecycle point + immutable summary -> validation outcome/DATA-069 | Validators fail closed; hooks observe only and cannot grant authority or mutate execution. |
| `INT-046` | Trace Emission Contract | correlation + event + attributes -> DATA-068 JSONL | Redact sensitive keys, truncate long text, no chain-of-thought, not audit. |

## 4. Persistence and sensitivity

- Raw approval callback tokens are transient return values and are excluded from `DATA-066`, `DATA-067`, `DATA-068`, `DATA-070` persistence and SQLite.
- Instruction content is loaded at runtime; the workspace stores metadata/hash rather than a second authoritative prompt source.
- The local context envelope stores synthetic authorized text for reproducibility. A production profile must apply data minimization, encryption, retention and DLP.
- Trace events never require private model chain-of-thought. They record identifiers, versions, actions, concise findings and outcomes.
- Schemas are under `schemas/DATA-063...DATA-070*.schema.json`.
