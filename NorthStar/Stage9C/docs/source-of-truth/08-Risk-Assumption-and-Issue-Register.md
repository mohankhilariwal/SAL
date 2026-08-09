# 08 — Risk, Assumption and Issue Register

**Version:** 1.14.0

Preserve all inherited active items, including `RSK-346`–`371`, `ASM-111`–`118`, `ISS-096`, `ISS-131`, `ISS-141`, `ISS-147`–`157`.

## New risks

| ID | Risk | Treatment/status |
|---|---|---|
| RSK-372 | Guardrail coverage gap | Stage inventory, traceability, negative tests; open residual. |
| RSK-373 | Wrong stage placement permits unsafe effect | PEP ownership and sequence tests. |
| RSK-374 | Authoritative metadata is wrong | Source validation, independent authorization and audit. |
| RSK-375 | Direct prompt injection evades patterns | Defense in depth, quarantine, red team future. |
| RSK-376 | Indirect injection enters context | Provenance/delimitation/no-elevation controls. |
| RSK-377 | Tool result becomes instructions | Result remains untrusted; quarantine. |
| RSK-378 | Model-assisted guardrail false negative | Never sole hard control; calibration future. |
| RSK-379 | Model-assisted false positive delays work | Human review, metrics and tuning future. |
| RSK-380 | Classifier bias/multilingual weakness | Dataset expansion and human calibration future. |
| RSK-381 | Policy bundle tampering | Immutable digest now; signing/KMS future. |
| RSK-382 | Stale/divergent policy caches | receipts, pinning, tier-based fail closed. |
| RSK-383 | Emergency suspension propagation delay | local stop plus future distributed control plane. |
| RSK-384 | Policy omission or contradictory controls | validation, tests, owner review. |
| RSK-385 | Policy-engine adapter semantic mismatch | ADR-113 conformance suite. |
| RSK-386 | Exception abuse | soft-only, dual approval, expiry, evidence. |
| RSK-387 | Compensating control failure | explicit owner and incident review. |
| RSK-388 | Reviewer self-approval | separation-of-duties hard control. |
| RSK-389 | Reviewer sees stale artefact | digest binding and expiry. |
| RSK-390 | Reviewer fatigue/automation bias | evidence design and future usability evaluation. |
| RSK-391 | False approval claim reaches users | output guardrail + human review. |
| RSK-392 | Cross-case memory leakage | tenant/case hard controls. |
| RSK-393 | Memory poisoning | provenance/type/retention controls. |
| RSK-394 | State race/stale update | version/idempotency/CMP-003 ownership. |
| RSK-395 | Data-106 bypass path | explicit hard control and code/architecture tests. |
| RSK-396 | Central release service outage | local last-known-good bundle; high-impact fail closed. |
| RSK-397 | Evidence over-redaction impairs forensics | evidence schema review; future WORM package. |
| RSK-398 | Evidence under-redaction leaks secrets | sensitive-key removal and security tests. |
| RSK-399 | Control-plane administrator compromise | dual approval and future privileged-access controls. |
| RSK-400 | Full control plane implied prematurely | status fields/ADR/handoff explicitly deny claim. |
| RSK-401 | Stage 8D bypass | hard runtime production gate. |

## New assumptions

| ID | Assumption |
|---|---|
| ASM-119 | PEPs receive trustworthy tenant/case/run/task metadata from accepted owners. |
| ASM-120 | Local system clocks are adequate for tutorial expiry checks. |
| ASM-121 | JSON policy bundle remains small enough for local memory evaluation. |
| ASM-122 | Two independent named approvers are available for policy releases/exceptions. |
| ASM-123 | Existing AUTH-001/BR-001 interfaces remain unchanged. |
| ASM-124 | Model-assisted controls remain optional/advisory until calibrated. |
| ASM-125 | No active tier-4 tool or multi-agent route is introduced. |
| ASM-126 | Production adapter selection occurs in a later controlled stage. |

## New issues

| ID | Issue | Status |
|---|---|---|
| ISS-158 | No byte-exact historical merge tree. | open |
| ISS-159 | No signed/KMS-backed policy bundle. | open |
| ISS-160 | No distributed durable policy registry or release DB. | open |
| ISS-161 | No live OPA/Cedar/SaaS adapter. | open |
| ISS-162 | No live calibrated classifier. | open |
| ISS-163 | No live human-review workflow integration. | open |
| ISS-164 | No WORM/tamper-evident decision ledger. | open |
| ISS-165 | No distributed cache convergence/emergency propagation proof. | open |
| ISS-166 | No reviewer workload/automation-bias evidence. | open |
| ISS-167 | No full enterprise control-plane registries/deployment controls. | open |
| ISS-168 | Mermaid CLI rendering not part of the executed environment. | open |
| ISS-169 | Stage 8D metrics/regression/deployment gates unresolved. | open |
