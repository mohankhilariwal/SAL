import pytest
from hashlib import sha256

from northstar_compliance.evaluation.judge.io import default_criteria
from northstar_compliance.evaluation.judge.models import (
    DeterministicFinding, EvaluationMode, JudgeEvaluationEnvelope, JudgePolicy,
)


def finding(passed=True):
    return DeterministicFinding("GRD-001", passed, True, sha256(b"x").hexdigest())


def envelope(**overrides):
    data = dict(
        envelope_id="JENV-999", case_id="JCAL-999", candidate_label="Candidate-A",
        candidate_text="Text", rubric_id="R", rubric_version="1.0.0",
        criteria=default_criteria(), evidence={"EVID-1":"x"}, reference_facts=("x",),
        deterministic_findings=(finding(),), locale="en", risk_tier="medium",
        authorization_scope="evaluation:synthetic", authority_effect="none", metadata={},
    )
    data.update(overrides)
    return JudgeEvaluationEnvelope(**data)


def test_563_policy_authority_none():
    assert JudgePolicy("JUDGE-POLICY-001", "1.0.0").authority_effect == "none"


def test_564_policy_rejects_authority():
    with pytest.raises(ValueError):
        JudgePolicy("JUDGE-POLICY-001", "1.0.0", authority_effect="approve")


def test_565_envelope_digest_stable():
    assert envelope().digest == envelope().digest


def test_566_envelope_rejects_unanonymized_candidate():
    with pytest.raises(ValueError):
        envelope(candidate_label="Model-X")


def test_567_envelope_rejects_hidden_chain_of_thought():
    with pytest.raises(ValueError):
        envelope(hidden_chain_of_thought="private")


def test_568_envelope_rejects_authority_effect():
    with pytest.raises(ValueError):
        envelope(authority_effect="route")


def test_569_model_identity_hidden_by_default():
    with pytest.raises(ValueError):
        envelope(candidate_model_identity="FAMILY-X")


def test_570_model_identity_allowed_only_for_probe():
    env = envelope(candidate_model_identity="FAMILY-X", metadata={"self_preference_probe": True})
    assert env.candidate_model_identity == "FAMILY-X"
