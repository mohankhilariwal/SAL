# 00 - Project Constitution

| Field | Value |
|---|---|
| Project | NorthStar Agentic AI Architecture Playbook |
| Repository | `northstar-agentic-compliance` |
| Stage | Stage 0 - Playbook Foundation and Architecture Constitution |
| Constitution version | 0.1.0 |
| Baseline date | 2026-07-31 |
| Status | Baseline candidate; Stage 1 is blocked until review and acceptance |

## 1. Authority and source precedence

The project uses the following precedence when instructions conflict:

1. The latest explicit user instruction for the current execution.
2. The Execution Controller, which governs stage sequencing, cumulative artefacts and change control.
3. The Narrative-Driven Agentic AI Architecture Playbook, which defines the book scope, NorthStar story and progressive architecture.
4. The continuation prompt, which is the standard invocation pattern for later stages.
5. Earlier or alternative master prompts, used only where they do not conflict with items 1-4.
6. General model knowledge, which may supplement but may not silently replace source-defined facts.

Any conflict must be recorded as an issue and resolved through an ADR before technical progression.

## 2. Book purpose

The playbook teaches experienced software, cloud, enterprise and solution architects how to progress from a manual regulated-enterprise workflow to a production-grade, human-accountable Agentic AI architecture. It combines architecture reasoning, implementation, testing, security, governance, performance, operations and economics in one continuous NorthStar Financial Services narrative.

The book is not a product catalogue and does not assume that an agent framework, a large model or a multi-agent design is inherently appropriate.

## 3. Target audience

Primary readers:

- Software, cloud, platform, enterprise and solution architects.
- Technical leads moving into Agentic AI architecture.
- AI platform, MLOps, LLMOps, AgentOps and DevSecOps practitioners.
- Security, model-risk, governance and compliance architects.
- Senior engineers responsible for production implementation and operations.

Assumed knowledge:

- APIs, distributed systems, cloud and container fundamentals.
- Identity and access management basics.
- Databases, messaging, observability and CI/CD concepts.
- Basic Python literacy.

The reader is not assumed to understand advanced agent loops, graph execution, model inference, evaluation science or agent authorization.

## 4. Learning outcomes

By the end of the playbook, a reader should be able to:

1. Distinguish deterministic automation, search, RAG, assistants, bounded agents, graphs and multi-agent systems.
2. Translate a business problem into requirements, state, tools, authority, policies, tests and operational objectives.
3. Design a progressively evolving single-agent and multi-agent architecture.
4. Implement and locally run the NorthStar reference project.
5. Evaluate model, retrieval, tool, agent, graph, multi-agent and business outcomes.
6. Design identity, authorization, guardrails, blast-radius controls and human approvals outside probabilistic reasoning.
7. Engineer performance, concurrency, inference, cost, resilience, audit and production operations.
8. Produce an architecture package suitable for regulated-enterprise review.

## 5. Narrative constitution

The fictional enterprise is **NorthStar Financial Services**, operating in Canada, the United States and selected European markets across banking, payments, lending and insurance-related services.

The primary workflow is regulatory change impact assessment. The organization receives regulatory notices, policy updates, supervisory publications and legal changes. The system must assist people without transferring accountability to autonomous AI.

The main user story is `US-001` and all later stages must retain the accepted organization, personas, workflow, terminology and business boundaries recorded in `01-Business-and-User-Story-Baseline.md`.

## 6. Architecture principles

| ID | Principle | Consequence |
|---|---|---|
| AP-001 | Simplest sufficient architecture | Introduce a capability only after the current architecture demonstrates a concrete limitation. |
| AP-002 | Human accountability is non-transferable | AI prepares evidence and recommendations; accountable people approve regulated or high-impact decisions. |
| AP-003 | Bounded autonomy and authority | Autonomy and permission are separate; both must be explicitly limited. |
| AP-004 | Evidence before assertion | Material claims must link to source evidence and provenance. |
| AP-005 | Deterministic enforcement for critical controls | Authorization, financial, privacy, legal and safety controls must not rely only on prompts or model judgment. |
| AP-006 | Explicit, typed state | Business state, workflow state and memory must have defined ownership and schemas. |
| AP-007 | Zero Trust for agents and tools | Every identity, delegation, tool call and data access is verified, scoped and auditable. |
| AP-008 | Contract-first interfaces | Tools, agents, events and data objects use versioned contracts and explicit error semantics. |
| AP-009 | Evaluation-driven delivery | A capability is not accepted without tests or evaluations tied to requirements. |
| AP-010 | Observability and audit by design | Traces, evidence and policy outcomes are architectural concerns, not later instrumentation. |
| AP-011 | Failure containment | Retries, budgets, isolation, approvals and recovery limit blast radius and failure propagation. |
| AP-012 | Vendor-neutral core | Business contracts and architecture remain portable; vendor mappings are adapters. |
| AP-013 | Durable, idempotent side effects | Side-effecting actions need idempotency, retry and compensation semantics. |
| AP-014 | Privacy, residency and minimization | Data use is purpose-bound, minimized, classified, retained and located deliberately. |
| AP-015 | Cost is an operational constraint | Token, tool, infrastructure, evaluation and human-review costs are measured per completed business outcome. |
| AP-016 | No hidden chain-of-thought dependency | Store concise evidence, actions, decisions and policy results, not private model reasoning. |
| AP-017 | Compatibility is cumulative | Accepted names, IDs, schemas and paths are preserved or changed only through impact analysis and ADRs. |

## 7. Security and governance principles

| ID | Principle |
|---|---|
| SG-001 | Deny by default and grant least privilege. |
| SG-002 | Read-only is the default tool authority. |
| SG-003 | User identity, workload identity, agent identity and tool identity remain distinguishable. |
| SG-004 | Delegation attenuates authority; unrestricted user credentials are never passed to an agent or tool. |
| SG-005 | High-risk or irreversible actions require explicit human approval and, where appropriate, dual control. |
| SG-006 | All material actions produce tamper-evident audit evidence. |
| SG-007 | Retrieval and memory enforce access control and case isolation. |
| SG-008 | Models and tools are treated as untrusted or partially trusted dependencies. |
| SG-009 | Safety and policy controls fail closed unless an approved degraded mode exists. |
| SG-010 | Legal and regulatory interpretation remains subject to qualified human review. |

## 8. Stable identifier conventions

| Artefact type | Pattern | Example |
|---|---|---|
| Architecture principle | `AP-NNN` | `AP-001` |
| Security/governance principle | `SG-NNN` | `SG-001` |
| Business success criterion | `BSC-NNN` | `BSC-001` |
| User story | `US-NNN` | `US-001` |
| Functional requirement | `FR-NNN` | `FR-001` |
| Non-functional requirement | `NFR-NNN` | `NFR-001` |
| Component | `CMP-NNN` | `CMP-001` |
| Agent | `AGT-NNN` | `AGT-001` |
| Tool | `TOOL-NNN` | `TOOL-001` |
| Data object | `DATA-NNN` | `DATA-001` |
| Interface | `INT-NNN` | `INT-001` |
| Policy | `POL-NNN` | `POL-001` |
| Risk | `RSK-NNN` | `RSK-001` |
| Control | `CTL-NNN` | `CTL-001` |
| Evaluation | `EVAL-NNN` | `EVAL-001` |
| ADR | `ADR-NNN` | `ADR-001` |
| Test | `TEST-NNN` | `TEST-001` |
| Assumption | `ASM-NNN` | `ASM-001` |
| Issue | `ISS-NNN` | `ISS-001` |
| Stage | `SNN` or `SNNX` | `S00`, `S04A` |

Identifiers are never reused. Renaming, retirement or supersession preserves the original ID and records the reason, date and replacement.

## 9. Naming conventions

- Organization and product names use title case: `NorthStar Financial Services`.
- Repository, package and path names use lowercase kebab case or snake case as appropriate.
- Python modules, functions and variables use `snake_case`; classes use `PascalCase`; constants use `UPPER_SNAKE_CASE`.
- Components use a stable architectural noun plus responsibility, for example `Regulatory Intake Boundary`.
- Agents, when introduced, use role-oriented names ending in `Agent`.
- Interfaces describe the business contract rather than a vendor protocol.
- Data objects use singular nouns and include a schema version.
- Mermaid node labels include the stable ID and accepted name.

## 10. Diagram conventions

1. Mermaid is the canonical diagram format.
2. The cumulative logical architecture diagram is updated at every stage.
3. Existing names and IDs remain unchanged.
4. New current-stage elements use class `new`; planned elements use class `planned`; external systems use class `external`; human roles use class `human`; security boundaries use subgraphs.
5. Solid lines show active data or control flow; dashed lines show planned or conditional relationships.
6. Every diagram has a title, purpose and immediate explanation.
7. Diagrams must agree with the component catalogue, interface register and repository manifest.
8. Mermaid rendering is validated when a renderer is available; otherwise structural syntax checks are recorded honestly.

## 11. Code conventions

- Baseline language: Python 3.12, selected as a conservative project baseline and subject to review before implementation stages.
- New modules include type hints and docstrings for public contracts.
- Data and tool boundaries use explicit schemas; untyped dictionaries are not accepted at architectural boundaries.
- External dependencies are pinned only after official documentation and compatibility verification in the stage that introduces them.
- Critical controls are deterministic and unit tested.
- Side effects require idempotency keys and explicit error semantics when introduced.
- Secrets are provided through environment variables or approved secret stores, never committed.
- Logging excludes secrets and protected personal data.
- Examples include local mocks when paid or external services are optional.

## 12. Repository conventions

Canonical repository: `northstar-agentic-compliance`.

Canonical source-of-truth path: `docs/source-of-truth/`.

Core layout:

```text
northstar-agentic-compliance/
├── README.md
├── pyproject.toml
├── .env.example
├── config/
├── docs/
│   ├── source-of-truth/
│   ├── stages/
│   ├── architecture/
│   ├── adr/
│   └── runbooks/
├── src/northstar_agentic_compliance/
├── tests/
├── datasets/
├── scripts/
├── deployment/
└── notebooks/
```

Repository changes are cumulative. Each stage reports files added, modified and retired plus migration notes.

## 13. Testing conventions

Testing layers are introduced only when relevant, but identifiers are stable from first use:

- Unit and schema tests.
- Contract and integration tests.
- Retrieval and evaluation tests.
- Agent-loop and graph-path tests.
- Security and authorization tests.
- Performance and concurrency tests.
- Failure, recovery and chaos tests.
- Human-review and business-outcome evaluation.

Every test record includes objective, fixture, expected result, actual result, status and linked requirements. A test must not be marked passed unless it was executed or explicitly identified as a design-only test.

## 14. Citation standards

1. Use primary sources whenever possible: official documentation, standards and original research.
2. Date rapidly changing technical claims.
3. Mark vendor-specific, preview, beta, experimental and deprecated capabilities.
4. Separate source-derived facts, architectural inference and project assumptions.
5. Do not invent standards, benchmarks, costs, product capabilities or legal conclusions.
6. Use inline citations near the supported statement and maintain an annotated bibliography in the final stage.
7. Code and version claims are verified against current official documentation in the stage that introduces them.
8. Legal and compliance mappings are high-level architecture guidance and require qualified review.

## 15. Technology-selection rules

1. Define the business capability and constraints before selecting a product.
2. Compare deterministic automation, search, RAG, tool use, graphs and agents before increasing autonomy.
3. Prefer open contracts and replaceable adapters.
4. Select frameworks only after the control-flow, state, durability and evaluation requirements are known.
5. Evaluate managed and self-hosted options across quality, latency, cost, privacy, residency, operations and lock-in.
6. No universal winner is declared; decisions are documented in ADRs with review triggers.
7. Experimental techniques require isolation, benchmark evidence and fallback plans.
8. Paid infrastructure is optional for local labs unless it is the subject of the stage.

## 16. Stage roadmap

| Stage | Title | Major outcome |
|---|---|---|
| S00 | Playbook Foundation and Architecture Constitution | Stable story, requirements, identifiers, conventions, baseline architecture, repository and handoff. |
| S01 | From a Manual Regulatory Process to the First AI Assistant | Current-state analysis and a limited document summarizer. |
| S02 | Retrieval and Grounded Knowledge | Evidence-backed RAG and retrieval evaluation. |
| S03 | Single-Agent Loop and Tools | Tool-using bounded agent, state and recovery. |
| S04 | Graph and Harness Engineering | Controlled graph, approvals, durable state and harness. |
| S05 | Specification, Context and Memory | Machine-readable specification and bounded memory. |
| S06 | Multi-Agent Architecture and Interoperability | Evidence-based multi-agent decision, handoffs and communication. |
| S07 | Performance and Inference | Workload, concurrency, model routing and inference benchmarks. |
| S08 | Evaluation Engineering | Full evaluation hierarchy and judge-bias laboratory. |
| S09 | Security, Authorization and Governance | Threat model, tokenized authority, blast radius and control plane. |
| S10 | Observability, Reliability and Production | Audit, AgentOps, failure engineering, deployment, CI/CD and FinOps. |
| S11 | Final Capstone | Consolidated architecture, repository, runbooks, assessment and bibliography. |

Substages may be introduced at natural architectural boundaries without changing accepted stage outcomes.

## 17. Definition of done

### 17.1 Definition of done for every stage

A stage is done only when:

1. Context is reconstructed from all ten source-of-truth artefacts.
2. The NorthStar narrative explains why the capability is needed now.
3. Requirements and options are documented.
4. A selected design is recorded in an ADR.
5. The cumulative architecture and relevant focused diagrams are updated.
6. Repository changes are compatible and executable where implementation is required.
7. Security, governance, performance, cost and failure implications are addressed.
8. Tests or evaluations are defined and executed where possible.
9. Requirements traceability is updated.
10. All affected source-of-truth artefacts are updated.
11. The consistency audit is completed honestly.
12. A complete stage handoff pack is produced.
13. No later-stage capability is falsely described as implemented.

### 17.2 Stage-specific definition of done

| Stage | Additional completion condition |
|---|---|
| S00 | All ten artefacts exist, IDs and conventions are stable, source conflicts are resolved, baseline repository validation passes. |
| S01 | Manual process and first summarizer are runnable and limitations motivate retrieval. |
| S02 | Grounded retrieval returns attributable evidence and passes retrieval tests. |
| S03 | Bounded agent loop uses controlled tools, state and recovery with executed tests. |
| S04 | Graph and harness enforce explicit transitions, approvals and checkpointing. |
| S05 | Agent specification, context assembly and memory boundaries are machine-readable and tested. |
| S06 | Multi-agent choice is justified by measured need; contracts and coordination tests exist. |
| S07 | Workload profiles and benchmarks establish latency, throughput and cost evidence. |
| S08 | Evaluation datasets, metrics and judge-bias tests gate deployment. |
| S09 | Threats, identities, policies and blast-radius controls are mapped and tested. |
| S10 | Tracing, audit, reliability, deployment, CI/CD and runbooks support production operation. |
| S11 | Final package is internally consistent, production-readiness gaps are explicit and the single/multi-agent conclusion is evidence based. |

## 18. Change-control protocol

For any revision:

1. Identify accepted IDs and artefacts affected.
2. Record a change-impact analysis.
3. Create or supersede an ADR.
4. Update diagrams, schemas, code, tests and traceability.
5. Preserve a change-history entry.
6. Update the handoff pack.

Silent contradiction is prohibited.

## 19. Acceptance gate

Stage 1 must not begin until this Stage 0 baseline is reviewed and accepted. Acceptance freezes the identifiers and conventions except through the change-control protocol.
