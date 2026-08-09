# ADR-072 — Establish evaluation evidence before final model selection and routing

- **Status:** Accepted
- **Context:** The S07C handoff nominated Stage 7D model selection and routing, while the requested stage is S08A. A model portfolio cannot be selected defensibly without task-specific datasets, stable outcome criteria and comparable evaluation runs.
- **Decision:** Execute S08A as an evidence prerequisite. Do not select a model portfolio, activate routing or alter `DATA-106`. Record the sequence deviation as `ISS-114`; return to model selection only after relevant evaluation evidence exists.
- **Alternatives:** Stop because Stage 7D was skipped; select models from public benchmarks; implement routing and evaluation together.
- **Rationale:** A provider-neutral dataset and harness reduces benchmark-chasing and prevents routing from being justified by incomparable demonstrations.
- **Consequences:** Model selection remains unresolved. Stage 8A can evaluate future candidates but does not name a production model.
- **Risks:** Evaluation design may embed assumptions that favour later candidates.
- **Mitigations:** Multi-category datasets, explicit incompleteness, immutable versions, domain review and future cross-family evaluation.
- **Review trigger:** Approved Stage 7D resumption, materially changed use cases, or evidence that the suite does not discriminate candidate quality.
