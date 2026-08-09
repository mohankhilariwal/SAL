from __future__ import annotations
import json
from pathlib import Path
import pytest
from northstar_compliance.guardrails.policy import PolicyBundle

ROOT=Path(__file__).resolve().parents[2]

def test_793_bundle_loads(bundle): assert len(bundle.controls)==59

def test_794_bundle_is_approved(bundle): assert bundle.status=='approved'

def test_795_hard_controls_are_sync(bundle): assert all(c.synchronous for c in bundle.controls if c.hard)

def test_796_hard_controls_not_overrideable(bundle): assert all(not c.overrideable for c in bundle.controls if c.hard)

def test_797_model_controls_not_hard(bundle): assert all(not c.hard for c in bundle.controls if c.model_assisted)

def test_798_all_stages_have_controls(bundle): assert len({c.stage for c in bundle.controls})==10

def test_799_unique_ids(bundle): assert len({c.control_id for c in bundle.controls})==len(bundle.controls)

def test_800_authority_effect_none_in_config():
    raw=json.loads((ROOT/'config/guardrails/guardrail_policy_bundle.json').read_text())
    assert raw['authority_effect']=='none'

def test_801_control_plane_profile_is_bounded():
    raw=json.loads((ROOT/'config/guardrails/control_plane_profile.json').read_text())
    assert raw['full_control_plane_implemented'] is False and raw['stage8d_resolved'] is False

def test_802_duplicate_control_rejected(tmp_path):
    raw=json.loads((ROOT/'config/guardrails/guardrail_policy_bundle.json').read_text())
    raw['controls'].append(raw['controls'][0])
    p=tmp_path/'bad.json'; p.write_text(json.dumps(raw))
    with pytest.raises(ValueError,match='duplicate'): PolicyBundle.load(p)

def test_803_hard_override_rejected(tmp_path):
    raw=json.loads((ROOT/'config/guardrails/guardrail_policy_bundle.json').read_text())
    raw['controls'][0]['overrideable']=True
    p=tmp_path/'bad.json'; p.write_text(json.dumps(raw))
    with pytest.raises(ValueError,match='overrideable'): PolicyBundle.load(p)

def test_804_hard_async_rejected(tmp_path):
    raw=json.loads((ROOT/'config/guardrails/guardrail_policy_bundle.json').read_text())
    raw['controls'][0]['synchronous']=False
    p=tmp_path/'bad.json'; p.write_text(json.dumps(raw))
    with pytest.raises(ValueError,match='synchronous'): PolicyBundle.load(p)
