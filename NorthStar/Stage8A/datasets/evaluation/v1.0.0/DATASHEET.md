# DATA-132 / EDS-001–008 Dataset Datasheet

- **Purpose:** deterministic offline validation of NorthStar's bounded AGT-001 workflow and evaluation plumbing.
- **Version:** 1.0.0.
- **Composition:** 24 synthetic cases: 10 dev, 8 validation, 6 logically sealed test.
- **Categories:** normal, negative, permission, tool failure, adversarial, temporal, multilingual, and conflicting evidence.
- **Provenance:** authored for Stage 8A; no production documents, customer records, or real regulatory conclusions.
- **Language:** English (Canada) and French (Canada) synthetic cases.
- **Sensitive data:** none intended. Raw customer data and hidden chain-of-thought fields are rejected by validation.
- **Intended use:** local architecture testing, deterministic grader verification, regression-suite scaffolding.
- **Prohibited use:** legal interpretation, production model ranking, compliance approval, routing decisions, or claims of real-world accuracy.
- **Known limitations:** small size, synthetic language, no production distribution, no domain-expert labels, no genuine long-document payloads.
- **Contamination control:** immutable case digests, split-specific files, cross-split exact and 4-gram Jaccard checks, sealed-test execution gate.
- **Review trigger:** any new production sample, new jurisdiction, new task type, model change, prompt/graph change, or observed field failure.
