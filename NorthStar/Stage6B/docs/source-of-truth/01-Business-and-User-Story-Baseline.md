# 01 — Business and User Story Baseline

**Version:** `1.4.0`

## Carried-forward story

Maya Chen uses NorthStar's one-agent, graph-controlled regulatory impact workflow. `AGT-001` operates through six bounded profiles for research, extraction, mapping, risk, verification and reporting. Human approval and accountability remain external.

## S06B narrative state

Maya's case exposes a possible need for independently operated evidence verification. NorthStar does not yet have measured evidence to activate a second agent, but Priya must ensure that a future handoff would not rely on free-form chat, unrestricted credentials or shared mutable state.

The business need introduced in S06B is therefore: **define and prove the contracts for bounded work transfer before activating a second actor or selecting a communication protocol.**

## User-story acceptance additions

- Maya can see that a verification result is linked to the exact input artefact and is not an approval.
- Daniel retains final human accountability and no candidate endpoint can approve/finalize.
- Priya can review task, authority, artefact, lifecycle and termination contracts independently of transport.
- Marcus can prove that recipient authority is narrower and checked before data load.
- Sofia can trace provenance and enforce candidate/non-production status.
- Liam can reproduce cancellation, timeout, replay, tamper and terminal-state behavior locally.
- Aisha's business/control ownership is not delegated to an AI endpoint.

## S06B business outcome

NorthStar now has a safe, testable handoff substrate and a sequential contract sandbox. It still has one active agent and no production multi-agent runtime.

## Remaining business limitation

NorthStar has not selected how contracts will cross a process or service boundary, and it has not proved that a second agent improves regulatory outcomes enough to justify activation.
