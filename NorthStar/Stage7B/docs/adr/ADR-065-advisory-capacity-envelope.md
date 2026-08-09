# ADR-065 — Capacity analysis is advisory; admission ownership is unchanged

- **Status:** Accepted
- **Context:** Stage 7B can estimate sustainable rates, but Stage 7A assigned admission and routing authority to CMP-003 through DATA-106.
- **Decision:** DATA-120 capacity envelopes and INT-093 recommendations are advisory. They cannot mutate DATA-106, routes, authority, approval or protected state.
- **Alternatives:** Automatic tuning; manual spreadsheets; runtime worker self-scaling.
- **Rationale:** Preserves existing authority and prevents unverified benchmarks from changing production behaviour.
- **Consequences:** A governed change process is required to apply recommendations.
- **Risks:** Manual action may lag demand.
- **Mitigations:** Alerts, review cadence and later controlled autoscaling ADR after production evidence.
- **Review trigger:** Production telemetry and approved autoscaling design exist.
