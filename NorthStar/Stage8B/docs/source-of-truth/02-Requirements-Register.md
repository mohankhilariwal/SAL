# 02 - Requirements Register - S08B Overlay 1.10.0

| ID | Requirement |
|---|---|
| `S08B-REQ-001` | Resolve the S08A continuation conflict explicitly without implementing metrics/deployment gates. |
| `S08B-REQ-002` | Introduce LLM-as-a-Judge only as an advisory semantic grader within CMP-008. |
| `S08B-REQ-003` | Run deterministic mandatory graders before any model judge. |
| `S08B-REQ-004` | Define pointwise, pairwise and listwise options and select pointwise as default. |
| `S08B-REQ-005` | Use evidence-first, criterion-isolated, score-last judging. |
| `S08B-REQ-006` | Return strictly validated structured JSON without hidden chain-of-thought. |
| `S08B-REQ-007` | Separate judge instructions from untrusted candidate/reference content. |
| `S08B-REQ-008` | Anonymize candidate identity except in authorized self-preference probes. |
| `S08B-REQ-009` | Define immutable calibration cases, human labels and paired perturbations. |
| `S08B-REQ-010` | Measure central tendency and tail recall. |
| `S08B-REQ-011` | Measure acquiescence and framing sensitivity. |
| `S08B-REQ-012` | Measure premature commitment through score-first/evidence-first deltas. |
| `S08B-REQ-013` | Measure position, primacy and recency sensitivity. |
| `S08B-REQ-014` | Measure verbosity, style, fluency, length and formatting sensitivity. |
| `S08B-REQ-015` | Measure authority, bandwagon, confidence and familiarity effects. |
| `S08B-REQ-016` | Measure self-preference and sycophancy. |
| `S08B-REQ-017` | Measure leniency/severity and reference-answer sensitivity. |
| `S08B-REQ-018` | Measure language/cultural disparity. |
| `S08B-REQ-019` | Test prompt injection and instruction contamination against the judge. |
| `S08B-REQ-020` | Calibrate against human labels using coverage, confusion matrix, accuracy, F1 and Cohen's kappa. |
| `S08B-REQ-021` | Allow abstention and require human review on disagreement or insufficient evidence. |
| `S08B-REQ-022` | Use qualified panels only; no majority can override mandatory failures. |
| `S08B-REQ-023` | Preserve bounded local execution and provider-neutral adapters. |
| `S08B-REQ-024` | Do not select a live judge model, provider or route. |
| `S08B-REQ-025` | Update all source-of-truth artefacts and pass consistency checks. |
