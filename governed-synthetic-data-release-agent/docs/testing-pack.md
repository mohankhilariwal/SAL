# Testing pack

## Test layers

| Layer | Coverage |
|---|---|
| Unit | domain rules, classification, privacy/utility metrics, redaction, hash chain, budget and export rules |
| Policy | allow, approval, deny, injection, kill switch, missing evidence and expiry conditions |
| Security | path traversal, destination allow-list, raw identifiers, self/duplicate approval, replay, prompt injection and log redaction |
| Integration | SQLite, FastAPI, evidence, approval persistence, plus optional SDV, SDMetrics and Presidio smoke tests |
| Acceptance | all four required scenarios with exact decision and terminal-stage assertions |

## Commands

```bash
make test
make test-fast
make test-integration
make lint
make typecheck
make scenarios
make evidence-check
```

## Test data

`data/test_vectors/scenario_requests.json` contains the four request templates. `scripts/generate_source_data.py` creates the entirely fictional MapleBridge source dataset. The attack scenario deterministically injects exact rows, near duplicates and rare combinations.

## Retained executed evidence

See `artifacts/verification-report.md`, `artifacts/test-results-detailed.txt`, `artifacts/scenario-results.json`, and `artifacts/sample-evidence/`.
