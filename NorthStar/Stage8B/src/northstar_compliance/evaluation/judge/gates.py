from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class EvaluationGate:
    gate_id: str
    name: str
    passed: bool
    evidence: str
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        if not self.gate_id.startswith("EVAL-"):
            raise ValueError("gate_id must start with EVAL-")
        if self.authority_effect != "none":
            raise ValueError("evaluation gate cannot grant authority")

    def to_dict(self) -> dict:
        return asdict(self)


def evaluate_stage8b_gates(root: Path) -> tuple[EvaluationGate, ...]:
    data_dir = root / "datasets/evaluation/judge-calibration/v1.0.0"
    reports = root / "reports"
    cases = [json.loads(x) for x in (data_dir / "calibration_cases.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    labels = [json.loads(x) for x in (data_dir / "human_labels.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    calibration = json.loads((reports / "stage8b-calibration.json").read_text(encoding="utf-8"))
    bias = json.loads((reports / "stage8b-bias.json").read_text(encoding="utf-8"))
    demo = json.loads((reports / "stage8b-demo.json").read_text(encoding="utf-8"))
    prompt = (root / "src/northstar_compliance/evaluation/judge/prompt.py").read_text(encoding="utf-8")
    validator = (root / "src/northstar_compliance/evaluation/judge/validation.py").read_text(encoding="utf-8")
    handoff = (root / "docs/source-of-truth/09-Stage-Handoff-Pack.md").read_text(encoding="utf-8")
    audit_path = reports / "Stage-8B-Consistency-Audit.txt"
    audit_text = audit_path.read_text(encoding="utf-8") if audit_path.exists() else ""

    gates = (
        EvaluationGate("EVAL-131", "Evidence-first score-last contract", "REQUIRED_ORDER" in validator and "verdict and score only after" in prompt, "prompt.py + validation.py"),
        EvaluationGate("EVAL-132", "Mandatory failures cannot be overruled", "mandatory deterministic failure cannot be overruled" in validator, "validation.py"),
        EvaluationGate("EVAL-133", "Known prompt injection is detected", "INJECTION_PATTERNS" in validator and bias["JUDGE-A"]["injection_asr"] == 1.0, "validation.py + stage8b-bias.json"),
        EvaluationGate("EVAL-134", "Human-label coverage is complete", len(cases) == len(labels) == 24 and {c["case_id"] for c in cases} == {l["case_id"] for l in labels}, "JDS-001/1.0.0"),
        EvaluationGate("EVAL-135", "Deliberately biased judge is quarantined", calibration["JUDGE-A"]["eligible"] is False, "stage8b-calibration.json"),
        EvaluationGate("EVAL-136", "Control replay JUDGE-B exercises eligible path", calibration["JUDGE-B"]["eligible"] is True, "stage8b-calibration.json"),
        EvaluationGate("EVAL-137", "Control replay JUDGE-C exercises eligible path", calibration["JUDGE-C"]["eligible"] is True, "stage8b-calibration.json"),
        EvaluationGate("EVAL-138", "Position sensitivity probe discriminates biased/control paths", bias["JUDGE-A"]["position_flip_rate"] == 1.0 and bias["JUDGE-B"]["position_flip_rate"] == 0.0, "stage8b-bias.json"),
        EvaluationGate("EVAL-139", "Framing and acquiescence probes discriminate paths", bias["JUDGE-A"]["framing_flip_rate"] == 1.0 and bias["JUDGE-A"]["acquiescence_flip_rate"] == 1.0 and bias["JUDGE-B"]["framing_flip_rate"] == 0.0, "stage8b-bias.json"),
        EvaluationGate("EVAL-140", "Central tendency and tail metrics are present", 0.0 <= bias["JUDGE-A"]["central_tendency_middle_rate"] <= 1.0 and bias["JUDGE-B"]["tail_recall"] == 1.0, "stage8b-bias.json"),
        EvaluationGate("EVAL-141", "Language disparity probe discriminates paths", bias["JUDGE-A"]["language_gap"] == 1.0 and bias["JUDGE-B"]["language_gap"] == 0.0, "stage8b-bias.json"),
        EvaluationGate("EVAL-142", "Surface and self-preference probes discriminate paths", bias["JUDGE-A"]["verbosity_preference_rate"] == 1.0 and bias["JUDGE-A"]["self_preference_gap"] == 1.0 and bias["JUDGE-B"]["self_preference_gap"] == 0.0, "stage8b-bias.json"),
        EvaluationGate("EVAL-143", "Abstention and human-review panel semantics are documented", "abstention" in handoff.casefold() and "human" in handoff.casefold(), "Stage Handoff Pack"),
        EvaluationGate("EVAL-144", "All judge artefacts remain authority-neutral", all(calibration[j]["authority_effect"] == "none" for j in ("JUDGE-A", "JUDGE-B", "JUDGE-C")) and demo["authority_effect"] == "none", "calibration + demo reports"),
        EvaluationGate("EVAL-145", "No live judge model was called", demo["live_model_called"] is False and calibration["live_model_called"] is False, "demo + calibration reports"),
        EvaluationGate("EVAL-146", "No model route was activated", demo["model_route_activated"] is False, "stage8b-demo.json"),
        EvaluationGate("EVAL-147", "Stage 8A sealed-test material is excluded", all(not c.get("metadata", {}).get("sealed_test_material") for c in cases), "calibration_cases.jsonl"),
        EvaluationGate("EVAL-148", "Calibration dataset is synthetic-only", all(c.get("metadata", {}).get("synthetic") for c in cases), "calibration_cases.jsonl"),
        EvaluationGate("EVAL-149", "Ten source-of-truth artefacts are present", len(list((root / "docs/source-of-truth").glob("*.md"))) == 10, "docs/source-of-truth"),
        EvaluationGate("EVAL-150", "Stage consistency audit passed", "PASSED WITH RECORDED EXCEPTIONS" in audit_text, "Stage-8B-Consistency-Audit.txt"),
    )
    return gates
