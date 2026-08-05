# Demo runbook

## Prepare

```bash
make setup
make verify
make seed
```

## Interactive demo

```bash
make demo
```

Open `http://127.0.0.1:8501`. Run scenarios in order.

1. Internal allow: point out identifier removal, deterministic metrics, triggered policy IDs, seven-day expiry, receipt and authorized download.
2. External approval: demonstrate the genuine pause. Record Data Owner only, resume and show it still paused. Record Privacy Officer, resume and show release.
3. Privacy leakage: compare exact match, near duplicate and rare exposure gates; show quarantine and remediation.
4. Injection: show that no source profile, candidate or evaluator result exists; show blocked tool intentions, denial and suspension.

## Command-line evidence

```bash
make scenarios
make evidence-check
cat artifacts/scenario-results.json
```

## Clean stop and reset

Use Ctrl+C with `make demo`; the launcher terminates API and UI. Then run `make reset` when a clean demonstration is required.
