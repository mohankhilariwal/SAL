# 06 - ADR Register

| Field | Value |
|---|---|
| Version | 0.1.0 |
| Baseline date | 2026-07-31 |
| Status | Baseline candidate |

## ADR index

| ID | Title | Status | Decision date |
|---|---|---|---|
| ADR-001 | Instruction precedence and stage sequence | Accepted for Stage 0 baseline | 2026-07-31 |
| ADR-002 | Progressive simplest-sufficient architecture | Accepted for Stage 0 baseline | 2026-07-31 |
| ADR-003 | Human-accountable bounded autonomy | Accepted for Stage 0 baseline | 2026-07-31 |
| ADR-004 | One cumulative repository and source-of-truth location | Accepted for Stage 0 baseline | 2026-07-31 |
| ADR-005 | Evidence-first audit without hidden chain-of-thought | Accepted for Stage 0 baseline | 2026-07-31 |
| ADR-006 | Vendor-neutral contracts and deferred framework selection | Accepted for Stage 0 baseline | 2026-07-31 |
| ADR-007 | Conceptual component boundaries before runtime decomposition | Accepted for Stage 0 baseline | 2026-07-31 |

---

## ADR-001 - Instruction precedence and stage sequence

**Status:** Accepted for Stage 0 baseline

**Context:** The narrative-driven master prompt instructs the book to begin with its Stage 1, while the later execution controller explicitly requires Stage 0 before the main tutorial and states that when no stage is named, Stage 0 must be executed.

**Decision:** The execution controller governs sequencing. The narrative-driven master prompt governs scope and the NorthStar story. Stage 0 is inserted before the master prompt's Stage 1. The continuation prompt is used only after the current baseline is accepted.

**Alternatives:** Begin the master prompt's Stage 1 immediately; merge Stage 0 into Stage 1; treat all prompts as equal and improvise.

**Rationale:** The controller is the latest and more specific execution instruction. A separate foundation prevents identifier, repository and architecture drift.

**Consequences:** The roadmap is S00 followed by S01-S11. Stage 1 is blocked until Stage 0 review and acceptance.

**Risks:** Readers may confuse the controller stage numbers with older eight-stage or eleven-stage sequences.

**Mitigations:** Publish one canonical roadmap in the constitution and handoff pack; refer to stage ID and title together.

**Review trigger:** A user-approved revised controller or master roadmap.

---

## ADR-002 - Progressive simplest-sufficient architecture

**Status:** Accepted for Stage 0 baseline

**Context:** The playbook must teach architecture rather than assume that every problem requires RAG, agents, graphs or multi-agent systems.

**Decision:** Begin with the manual process and introduce each capability only after a demonstrated requirement and limitation. Every stage compares alternatives and records the selected design.

**Alternatives:** Start with a complete target architecture; use a framework-led tutorial; present isolated technology chapters.

**Rationale:** Progressive evolution exposes trade-offs, preserves narrative continuity and teaches when not to use a capability.

**Consequences:** Early architectures are intentionally limited. The cumulative diagram and repository evolve rather than restart.

**Risks:** Readers may mistake a deliberately limited early stage for the recommended production end state.

**Mitigations:** Label maturity, capabilities and limitations explicitly at every stage.

**Review trigger:** Evidence that the staged sequence prevents an executable or coherent implementation.

---

## ADR-003 - Human-accountable bounded autonomy

**Status:** Accepted for Stage 0 baseline

**Context:** Regulatory impact assessment affects legal, compliance and operational decisions. AI may assist but must not inherit accountability or unlimited authority.

**Decision:** Separate autonomy from authority. AI may draft, retrieve, classify, map, recommend and verify within bounded scopes. Named people approve high-risk or irreversible outcomes. Critical controls are deterministic and external to model reasoning.

**Alternatives:** Fully autonomous regulatory decisioning; informational-only system with no workflow actions; prompt-only behavioural constraints.

**Rationale:** This balances useful automation with regulated-enterprise accountability, least privilege and auditability.

**Consequences:** Human approval, identity, policy enforcement and evidence presentation are mandatory architecture concerns.

**Risks:** Reviewer fatigue and automation bias can still produce rubber-stamp approval.

**Mitigations:** Risk-based routing, evidence-first review, dual control for high impact, sampling and reviewer-quality evaluation.

**Review trigger:** Legal, regulatory or policy change; demonstrated low-risk use case suitable for adjusted autonomy.

---

## ADR-004 - One cumulative repository and source-of-truth location

**Status:** Accepted for Stage 0 baseline

**Context:** A long tutorial with evolving code and diagrams can easily create disconnected examples and contradictory artefacts.

**Decision:** Use one repository named `northstar-agentic-compliance`. The ten authoritative artefacts live at `docs/source-of-truth/`. Stage chapters live at `docs/stages/`. All repository changes are cumulative and versioned.

**Alternatives:** Separate repositories by chapter; keep source-of-truth files outside the repository; recreate examples for each stage.

**Rationale:** One repository makes compatibility, traceability, testing and handoff reconstructable.

**Consequences:** Each stage must inspect and update the manifest and report additions, modifications, retirements and migrations.

**Risks:** Repository complexity grows over time.

**Mitigations:** Bounded modules, clear ownership, manifest maintenance and stage-specific entry points.

**Review trigger:** Repository scale or release needs justify a monorepo-to-multirepo decision.

---

## ADR-005 - Evidence-first audit without hidden chain-of-thought

**Status:** Accepted for Stage 0 baseline

**Context:** NorthStar needs explainability and forensic reconstruction, but private model reasoning is not a stable, necessary or appropriate audit artefact.

**Decision:** Audit source references, inputs, outputs, structured decisions, tool calls, policy outcomes, approvals, versions, errors and concise rationale summaries. Do not require or retain hidden chain-of-thought.

**Alternatives:** Store full model scratchpads; retain only final output; rely on application logs without evidence lineage.

**Rationale:** Concise evidence and action records are auditable while reducing privacy, security and interpretability risks.

**Consequences:** Schemas distinguish evidence, inference and human decision. Evaluation uses observable outputs and traces.

**Risks:** Concise summaries may omit details needed for debugging.

**Mitigations:** Retain structured intermediate artefacts, state transitions, tool results and deterministic validator outcomes.

**Review trigger:** A specific approved assurance requirement demonstrates a need for an additional observable artefact.

---

## ADR-006 - Vendor-neutral contracts and deferred framework selection

**Status:** Accepted for Stage 0 baseline

**Context:** The master scope includes many vendors and frameworks, but selecting one before control-flow, state, durability and security requirements are known would create lock-in and technology-led architecture.

**Decision:** Define domain schemas, interfaces, policies and evaluations independently of vendors. Defer model, framework, vector store, workflow engine and deployment product choices to the stage where the requirement arises.

**Alternatives:** Select a single hyperscaler and agent framework in Stage 0; implement custom infrastructure for all concerns; compare all products in every stage.

**Rationale:** Replaceable adapters and decision-specific comparisons preserve learning value and architecture portability.

**Consequences:** Stage 0 contains no external runtime dependencies. Later ADRs will map neutral contracts to representative technologies.

**Risks:** Some future vendor features may require contract changes.

**Mitigations:** Versioned adapters, compatibility tests and review triggers.

**Review trigger:** A production constraint mandates a particular platform or protocol.

---

## ADR-007 - Conceptual component boundaries before runtime decomposition

**Status:** Accepted for Stage 0 baseline

**Context:** Stage 0 must establish a consistent architecture vocabulary without prematurely designing detailed services.

**Decision:** Define ten planned responsibility boundaries plus the implemented source-of-truth governance pack. Later stages may realize multiple boundaries in one process during local development and separate them only when scaling, security or ownership requires it.

**Alternatives:** No component baseline; one component per future microservice; complete production service decomposition now.

**Rationale:** Stable responsibility names support continuity while preserving implementation flexibility.

**Consequences:** Component status must clearly distinguish conceptual, local-module, deployed-service and retired states.

**Risks:** Readers may interpret a conceptual component as a required deployable service.

**Mitigations:** Repeat that component boundaries are logical responsibilities and document deployment mapping separately.

**Review trigger:** A stage demonstrates that a boundary must split, merge or change responsibility.
