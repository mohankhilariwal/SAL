# 08 - Risk, Assumption and Issue Register

**Version:** 0.2.0

## Active S00 risks carried into S01

| ID | Risk | S01 status/response |
|---|---|---|
| RSK-003 | Prompt injection or hostile document instructions alter output. | Reduced by data/instruction separation, no tools/secret access, fixed status and adversarial test; open. |
| RSK-005 | Sensitive or unauthorized data reaches a model/provider. | Synthetic local data only; enterprise authorization/residency not implemented; open. |
| RSK-010 | AI output is mistaken for an approved compliance determination. | Fixed unapproved disposition and human-review flag; partially mitigated. |
| RSK-015 | Incomplete or fabricated evidence undermines auditability. | Exact hash/line/excerpt validation; semantic support still needs humans; partially mitigated. |
| RSK-018 | Cost, latency or provider variability makes the design unsuitable. | Input bound and offline adapter; production workload/provider benchmark open. |

## New S01 risks

| ID | Risk | Likelihood | Impact | Mitigation | Status |
|---|---|---:|---:|---|---|
| RSK-019 | Schema-valid but semantically wrong summary. | Medium | High | exact citations, uncertainty, human review, golden cases | Open |
| RSK-020 | Automation bias causes reviewers to accept fluent wording. | Medium | High | preliminary label, evidence-first UX requirement, reviewer training deferred | Open |
| RSK-021 | Local artifacts expose sensitive source content. | Medium | High | synthetic data, configured directory, no production use | Open |
| RSK-022 | Model/API behavior or schema support changes. | Medium | Medium | provider boundary, no default model, version/change record | Open |
| RSK-023 | Large or complex documents exceed context or degrade quality. | Medium | Medium | Stage 1 size/type bound; retrieval/chunking deferred | Open |

## Assumptions

- `ASM-001`: Stage 1 uses synthetic or approved public-safe text.
- `ASM-002`: A named analyst reviews every output before use.
- `ASM-005`: The local filesystem is a developer trust boundary, not a shared production environment.
- `ASM-009`: The current need is one-document preliminary summarization, not internal impact determination.

## Issues

- `ISS-002`: Production workloads, SLOs, concurrency and cost thresholds are unknown. Open.
- `ISS-003`: Entity-specific legal/regulatory control mappings require qualified review. Open.
- `ISS-004`: Mermaid received static structure review but was not rendered through Mermaid CLI. Open.
- `ISS-006`: Python 3.12 direct execution remains open; tests passed on Python 3.13.5.
- `ISS-007`: The optional managed-provider adapter was not live-called in the build environment. Open.
- `ISS-008`: Individual S00 register files were not mounted in the execution sandbox; S01 preserved identifiers and meanings from the accepted S00 chapter and handoff, and records this reconstruction boundary for reviewer confirmation. Open review item.
