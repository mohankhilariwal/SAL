# 08 — Risk, Assumption and Issue Register

**Version:** `1.0.0`

## 1. Inherited state

All active S00–S04B risks, assumptions and issues remain unless explicitly closed. In particular, enterprise identity/connectors/legal review/records, production performance/deployment/DR, graph migration, dual approval, distributed timers/workers and Mermaid rendering remain unresolved.

## 2. New risks

| ID | Severity | Risk | Treatment / residual gap |
|---|---|---|---|
| `RSK-087` | High | Manifest drift could bind a run to unreviewed versions. | Digest validation, versioned config, fail closed; production signed configuration remains open. |
| `RSK-088` | High | Instruction tampering could change agent behavior. | Instruction SHA-256 bound to manifest; repository/change controls required. |
| `RSK-089` | High | Unauthorized or poisoned context could be loaded. | Access-before-loader, kind allowlist, provenance/hash, untrusted-content treatment; semantic poisoning remains. |
| `RSK-090` | High | Workspace or trace could leak callback tokens, credentials or regulated text. | Sensitive-field exclusion, redaction, quotas, session roots; production DLP/retention absent. |
| `RSK-091` | Medium | A hook could become an implicit policy or mutation path. | Observer-only API and invariant tests; plugin isolation/signing absent. |
| `RSK-092` | Medium | Duplicated validation between harness and graph could diverge. | Harness validates cross-cutting bindings; graph remains owner of routes/state; contract tests. |
| `RSK-093` | Medium | Harness may become a god object and couple every subsystem. | Composition, protocols, narrow lifecycle, no business reasoning; review trigger on dependency growth. |
| `RSK-094` | Medium | Registry mutation or shadow registration could expand capabilities. | Immutable startup registries and duplicate rejection; distributed registry governance deferred. |
| `RSK-095` | High | Local JSONL traces may be mistaken for audit evidence. | Explicit non-audit label and preliminary disposition; Stage 10 audit architecture remains required. |
| `RSK-096` | Medium | Session/workspace persistence may grow without bounds. | Local quotas and lifecycle status; retention/deletion policy deferred. |
| `RSK-097` | High | Restart under incompatible code/config may corrupt continuation. | Session/manifest/graph bindings and checksum/lease controls; graph migration not implemented. |
| `RSK-098` | Medium | Harness overhead may increase latency/cost. | No additional model calls; bounded hashing/I/O; production benchmark remains open. |

## 3. New assumptions

| ID | Assumption |
|---|---|
| `ASM-031` | The supplied S04B handoff accurately represents the accepted 0.9.0 baseline even though the byte-exact repository was not mounted. |
| `ASM-032` | A single local process and SQLite host remain sufficient for the Stage 4C teaching boundary. |
| `ASM-033` | Synthetic identity claims and local HMAC secret are acceptable only for deterministic control demonstrations. |
| `ASM-034` | Instruction/context sizes in the synthetic fixtures fit the configured local quotas; production values require measurement. |

## 4. New/open issues

| ID | Status | Issue |
|---|---|---|
| `ISS-043` | Open | S04C is a compatible reconstruction overlay from the supplied handoff, not a byte-exact patch to the S04B archive. |
| `ISS-044` | Open | Enterprise IAM/PDP, reviewer authentication, KMS/secret rotation and callback/session binding are absent. |
| `ISS-045` | Open | Workspace isolation is filesystem containment, not a production code/file sandbox, DLP service or records store. |
| `ISS-046` | Open | JSONL tracing is not OpenTelemetry export, append-only audit, WORM, integrity chain or enterprise retention. |
| `ISS-047` | Open | No live model/provider, enterprise connector, framework SDK or workflow engine conformance test was executed. |
| `ISS-048` | Open | No production concurrency, latency, throughput, workspace-volume, reliability or cost benchmark exists. |
| `ISS-049` | Open | Mermaid was structurally reviewed but not rendered with a Mermaid CLI in this environment. |

## 5. Stage close assessment

- No new risk is represented as production-closed.
- Controls prove local fail-closed behavior, not identity assurance, operational availability, legal correctness or regulatory compliance.
- `RSK-095`/`ISS-046` require the next production observability/audit stages to avoid treating diagnostic traces as official evidence.
