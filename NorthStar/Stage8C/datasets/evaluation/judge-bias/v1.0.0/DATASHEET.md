# JBD-001/1.0.0 - Judge Bias Laboratory Dataset

- Purpose: validate Stage 8C contracts, paired estimators, counterbalancing, uncertainty reporting, quarantine semantics and audit evidence.
- Composition: 23 synthetic probe families, 12 matched pairs per family, 3 repetitions, 2 replay judges, 3312 observations.
- Data: synthetic NorthStar-style labels and metadata only; no customer, production or Stage 8A sealed-test content.
- Replay judges: `JUDGE-CONTROL` and deliberately biased `JUDGE-BIASED`; neither represents a provider or model family.
- Intended use: code/test plumbing and bias-method demonstration.
- Prohibited claim: production prevalence, fairness, reliability, model ranking, deployment eligibility or regulatory correctness.
- Immutability: corrections create a new version and digest; do not edit accepted rows in place.
