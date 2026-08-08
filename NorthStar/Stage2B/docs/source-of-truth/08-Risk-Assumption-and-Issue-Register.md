# 08 — Risk, Assumption and Issue Register

## Preserved active items

All accepted S01/S02A identifiers retain their meanings. Immediate S02B inputs include `RSK-024`–`RSK-027`, `RSK-032`, `ASM-012`, `ISS-011`, `ISS-012`, `ISS-014` and `ISS-015` from the supplied handoff.

## New or updated risks

| ID | Risk | Status / mitigation |
|---|---|---|
| `RSK-024` | Restricted content may leak if filtering follows retrieval. | Materially mitigated locally by `ADR-014`, `CTL-016`, `TEST-034`, `EVAL-012`; enterprise identity remains open. |
| `RSK-025` | Exact terminology and paraphrases may be missed by one retriever. | Partially mitigated by hybrid retrieval and evaluation; recall remains variable. |
| `RSK-026` | Overlap may duplicate evidence and distort context. | Mitigated locally by deterministic overlap suppression and duplicate-span metric. |
| `RSK-027` | Highest raw score may not be best evidence. | Partially mitigated by fusion/reranking; human-labeled tuning remains open. |
| `RSK-032` | Corpus/index may become stale or incompatible. | Mitigated by corpus/config/source-version binding and explicit rebuild failure. |
| `RSK-033` | Local LSA may create weak or misleading semantic similarity. | Open POC limitation; optional production adapter and benchmark required. |
| `RSK-034` | Shared caches, telemetry or vector stores may leak existence/content across access boundaries. | Not solved by local code; production threat model and tenancy controls required. |
| `RSK-035` | Heuristic authority/domain boosts may over-rank broad text. | Bounded weights, ranking reasons and regression cases; human labels required. |
| `RSK-036` | Citation-correct evidence may still support an incorrect interpretation. | Candidate-only output; human review and future grounded-answer evaluation required. |
| `RSK-037` | Retrieved content may contain indirect prompt injection or poisoned precedent. | Context notice, risk flags and no generator/tool in S02B; later prompt/tool controls required. |
| `RSK-038` | Hybrid retrieval/reranking increases latency, compute and operational cost. | Local measurements captured; production workload benchmark deferred. |
| `RSK-039` | A five-document English synthetic corpus can produce misleadingly strong metrics. | Results explicitly scoped; expand dataset before pilot. |

## Assumptions

| ID | Assumption | Status |
|---|---|---|
| `ASM-012` | Prepared chunks and access metadata supplied through `INT-010` are internally consistent. | Accepted for S02B and independently revalidated. |
| `ASM-013` | Retrieval principal attributes in local tests represent the intended access scenario. | Accepted only for tutorial tests; not authentication. |
| `ASM-014` | Exact source-line reconstruction is sufficient for citation integrity in text/Markdown sources. | Accepted for current formats; layout/PDF citations need a future design. |
| `ASM-015` | NumPy is available in the local execution environment. | Verified with 2.3.5. |

## Issues

| ID | Issue | Status |
|---|---|---|
| `ISS-011` | Retrieval evaluation corpus is small and synthetic. | Open; expanded human-labeled, multilingual, temporal and adversarial cases required. |
| `ISS-012` | Controlled actions and case/review operations are absent. | Open; natural next-stage trigger. |
| `ISS-014` | Mermaid sources were structurally inspected but not rendered with Mermaid CLI. | Open tooling exception. |
| `ISS-015` | Python 3.12 direct execution remains unverified. | Open; Python 3.13.5 passed. |
| `ISS-016` | Managed/open production embedding and cross-encoder paths were not live benchmarked. | Open verification exception. |
| `ISS-017` | Retrieval indexes are rebuilt in memory per authorized subset and are not enterprise-scale. | Open by design for local safety demonstration. |
| `ISS-018` | No enterprise IdP/PDP authenticates `DATA-026`. | Open production blocker. |
| `ISS-019` | Nine detailed S02A registers and the byte-exact prior repository were not attached. | Recorded reconstruction exception. |
| `ISS-020` | No grounded generator exists, so faithfulness, answer correctness and answer relevance are not measured. | Open; intentionally outside S02B. |
