import pytest
from northstar_compliance.capstone import EvidenceItem, reconcile_evidence


def item(eid, authority="none"):
    return EvidenceItem(evidence_id=eid, title=eid, status="present", source="test", authority_effect=authority)


@pytest.mark.parametrize("required", [("A",), ("A","B"), ("A","B","C"), tuple()])
def test_complete_reconciliation(required):
    result = reconcile_evidence([item(x) for x in required], required)
    assert result.complete


@pytest.mark.parametrize("present,required,missing", [(("A",),("A","B"),("B",)), (tuple(),("A",),("A",))])
def test_missing_evidence(present, required, missing):
    result = reconcile_evidence([item(x) for x in present], required)
    assert result.missing_ids == missing
    assert not result.complete


def test_duplicate_evidence_fails():
    result = reconcile_evidence([item("A"), item("A")], ["A"])
    assert result.duplicate_ids == ("A",)
    assert not result.complete


def test_authority_effect_is_none():
    assert item("A").authority_effect == "none"
