# ADR-077 - Execute the dedicated judge stage before metrics/deployment gates

**Status:** Accepted

**Context:** The S08A handoff named metrics, regression testing and deployment gates as Stage 8B and deferred LLM-as-a-Judge. The user explicitly requested Stage 8B - LLM-as-a-Judge.

**Decision:** Execute the requested dedicated bias/calibration stage now as a bounded advisory overlay. Do not implement CI/CD promotion, production routing or production claims. Record `ISS-123`.

**Alternatives:** Refuse progression; silently implement the handoff stage; combine both large stages.

**Rationale:** The execution controller gives the explicitly requested stage precedence, while conservative boundaries prevent unsafe sequencing effects.

**Consequences:** Metrics/deployment gates remain unresolved and become the next problem.

**Review trigger:** Before any deployment gate or route activation.
