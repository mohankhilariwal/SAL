# ADR-066 — Standard-library planning simulator with external benchmark adapters

- **Status:** Accepted
- **Context:** The repository must run locally without GPUs or paid services, while remaining compatible with future endpoint benchmarking.
- **Decision:** Implement a deterministic standard-library discrete-event simulator and command/trace adapters for current endpoint tools. The simulator is a planning proxy, not an inference benchmark.
- **Alternatives:** Require a GPU endpoint; embed a heavyweight serving engine; spreadsheet-only model.
- **Rationale:** Provides reproducible tests and auditable formulas on modest hardware without selecting a production inference stack prematurely.
- **Consequences:** Kernel, KV-cache, batching and hardware behaviour require later endpoint calibration.
- **Risks:** False precision from simulated numbers.
- **Mitigations:** Evidence labels, warnings, calibration fields and no automatic admission changes.
- **Review trigger:** Production model/server/hardware is selected or endpoint access exists.
