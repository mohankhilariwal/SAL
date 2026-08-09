# 04 - Component and Agent Catalogue - S08B Overlay 1.10.0

- `CMP-008 Evaluation and Assurance Boundary`: expanded to own judge policies, prompts, envelopes, calibration datasets, bias probes, judge validation, calibration reports and advisory panel results.
- `CMP-006 Human Review and Approval Boundary`: owns expert labels, adjudication and review of uncertain/disputed judge findings.
- `CMP-007 Identity, Authorization and Policy Boundary`: authorizes access to calibration cases, references and judge configurations.
- `CMP-009 Observability and Audit Boundary`: receives hashes and concise criterion evidence, not raw protected payloads or hidden chain-of-thought.
- `CMP-010 Runtime and Deployment Boundary`: exposes only a future adapter point; no live judge route is selected.

Agent inventory: exactly one active `AGT-001 Regulatory Impact Assessment Agent`, specification `1.1.0`, unchanged authority. No judge is an agent.
