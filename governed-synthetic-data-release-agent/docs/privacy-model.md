# Privacy model

Synthetic data is not assumed to be anonymous. The final determination combines dataset characteristics, purpose, recipient, destination, release duration, auxiliary-data risk and technical privacy metrics.

## Classification

Column-name rules, data types, structured patterns and explicit metadata classify direct identifiers, quasi-identifiers, sensitive attributes, operational fields and derived features. Deterministic rules are authoritative; an optional model suggestion cannot silently override them.

## Reproducible privacy gates

1. Exact normalized source-row match rate.
2. Nearest-neighbour source-to-synthetic similarity and near-duplicate rate.
3. Rare city/merchant-category exposure.
4. Composite quasi-identifier screening risk.

Scenario 3 deliberately copies source rows, makes near duplicates and retains rare combinations. The failed candidate moves to quarantine, keeps its metrics and must never be accepted by the export gateway.

## Limitations

The implementation does not claim differential privacy, formal anonymity, membership-inference resistance, attribute-inference resistance or legal compliance. A production assessment should add a documented adversary model, population representativeness, external attack testing, recipient controls, contractual restrictions and periodic re-evaluation.
