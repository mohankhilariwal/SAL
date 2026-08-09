# ADR-075 — Prefer deterministic and human evaluation; defer LLM-as-a-Judge

- **Status:** Accepted
- **Context:** Stage 8A must establish valid datasets and hard gates. Model-based graders introduce calibration, bias, prompt-injection and self-preference risks that belong to a dedicated stage.
- **Decision:** Implement deterministic graders for schema, expected outcomes, citations, permissions, human authority, tool boundaries, termination, recovery, injection resistance, temporal validity, non-authority and payload minimization. Define human-review sampling. Do not implement an LLM judge in S08A.
- **Alternatives:** LLM judge for all quality criteria; human-only grading; deterministic-only forever.
- **Rationale:** Hard controls are directly testable. Subjective dimensions require human anchors before model-based automation.
- **Consequences:** Open-ended semantic quality is only partially covered in S08A.
- **Risks:** False confidence from a perfect deterministic score.
- **Mitigations:** Synthetic-only label, known limitations, future human calibration and Stage 8C judge-bias laboratory.
- **Review trigger:** Approved rubrics and human labels, subjective dimensions becoming deployment gates, or Stage 8C.
