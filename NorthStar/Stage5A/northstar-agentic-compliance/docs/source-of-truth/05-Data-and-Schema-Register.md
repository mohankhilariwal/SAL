# 05 — Data and Schema Register

**Version:** `1.1.0`

`DATA-001`–`070` and `INT-001`–`046` remain accepted. `DATA-009` remains schema `1.1.0`.

## New data objects

| ID | Name | Purpose/owner | Persistence/authority |
|---|---|---|---|
| `DATA-071` | AgentSpecification | Complete machine-readable definition of `AGT-001`; `CMP-011` governance, `CMP-003/008` consumption. | Repository JSON. Declarative; grants no authority. |
| `DATA-072` | SpecificationBinding | Binds spec ID/version/digest to agent, graph, instruction and harness manifest/session. | Manifest/session evidence; not signing/attestation. |
| `DATA-073` | RuntimeAssertionResult | Named deterministic pre-start/post-result checks and failures. | Local evidence/trace; not audit. |
| `DATA-074` | SpecificationValidationReport | Structural and semantic findings with paths/codes. | CI/local validation evidence. |
| `DATA-075` | EvaluationObligation | Required test/evaluation/security evidence derived from the spec. | Evaluation configuration/report. |
| `DATA-076` | DeploymentGateResult | Fail-closed local allow/deny result and blocking reasons. | Release evidence; not production deployment authorization. |
| `DATA-077` | ContextPolicyProfile | Allowed/prohibited kinds, access ordering, provenance and size rules. | Embedded in `DATA-071`; memory/compaction disabled. |
| `DATA-078` | RetirementDecision | Lifecycle decision and effects for active/deprecated/retired specification. | Governance record; production workflow deferred. |

All schemas are under `schemas/DATA-071...DATA-078*.schema.json`.

## New interfaces

| ID | Contract | Input -> output | Control boundary |
|---|---|---|---|
| `INT-047` | Agent Specification Resolution Contract | Repository path/expected identity -> immutable `DATA-071` + canonical digest | Controlled source; unknown/empty/non-object fails. |
| `INT-048` | Specification Validation and Compatibility Contract | `DATA-071` + manifest -> `DATA-074` | Schema + application semantic checks; deny on error. |
| `INT-049` | Runtime Specification Assertion Contract | spec/binding/context/result -> `DATA-073` | Pre-start/post-result checks only; no routing/authorization. |
| `INT-050` | Evaluation and Deployment Gate Contract | `DATA-074/075` + evidence -> `DATA-076` | Deny-by-default; evaluation is not authority. |
| `INT-051` | Context Policy Binding Contract | `DATA-077` + `DATA-065` -> pass/fail assertion | Authorization-before-load retained; no memory. |
| `INT-052` | Specification Lifecycle and Retirement Contract | spec status/criteria/change decision -> `DATA-078` | Retired denies new starts; in-flight migration deferred. |

## Canonicalization

The local digest is SHA-256 of UTF-8 JSON serialized with sorted keys, compact separators and Unicode preserved. This provides deterministic content binding only; it does not establish signer identity, non-repudiation, WORM retention or deployment provenance.
