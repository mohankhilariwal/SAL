# 05 Data and Schema Register - S08C Overlay 1.11.0

Preserve `DATA-001`-`154`; `DATA-009` remains `1.1.0`.

| ID | Name | Owner | Purpose |
|---|---|---|---|
| `DATA-155` | BiasTaxonomyEntry | CMP-008/CMP-011 | Bias definition, criticality and experiment class. |
| `DATA-156` | ProbeFamily | CMP-008 | Matched control/treatment hypothesis and slices. |
| `DATA-157` | PerturbationVariant | CMP-008 | Changed factor, digests and equivalence evidence. |
| `DATA-158` | ExperimentManifest | CMP-008/CMP-011 | Versions, seeds, repetitions and policy. |
| `DATA-159` | TrialPlan | CMP-008 | Randomized/counterbalanced execution order. |
| `DATA-160` | TrialObservation | CMP-008 | Strict structured advisory observation. |
| `DATA-161` | PairedBiasEstimate | CMP-008 | Explicit denominator, effect, CI and test. |
| `DATA-162` | BiasSliceReport | CMP-008/CMP-006 | Group/slice metrics with sample sizes. |
| `DATA-163` | LabRunReport | CMP-008/CMP-009 | Run-level minimized evidence and digest. |
| `DATA-164` | QuarantineRecommendation | CMP-008/CMP-011 | Advisory restriction; never route/approval mutation. |

All new objects require `authority_effect: none` and cannot write protected workflow state.

## New interfaces

`INT-121` Bias Taxonomy Resolution; `INT-122` Probe Family Registration; `INT-123` Experiment Manifest Resolution; `INT-124` Counterbalanced Trial Planning; `INT-125` Replay Adapter Invocation; `INT-126` Trial Observation Validation; `INT-127` Paired Bias Estimation; `INT-128` Slice and Multiple-Testing Analysis; `INT-129` Minimized Lab Evidence Export and Quarantine Recommendation.
