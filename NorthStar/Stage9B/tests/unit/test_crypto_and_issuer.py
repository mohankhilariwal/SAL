from dataclasses import asdict, replace
from datetime import timedelta
import pytest
from northstar_compliance.security.identity import *


def test_grant_signature(env):
    assert Ed25519KeyPair.verify(env["envelope"],env["issuer_key"].public_key)

def test_tampered_payload_fails(env):
    e=env["envelope"]
    bad=SignedEnvelope(e.key_id,e.algorithm,{**e.payload,"audience":"evil"},e.signature)
    assert not Ed25519KeyPair.verify(bad,env["issuer_key"].public_key)

def test_wrong_key_fails(env):
    assert not Ed25519KeyPair.verify(env["envelope"],Ed25519KeyPair("other").public_key)

def test_thumbprints_are_key_specific():
    assert Ed25519KeyPair("a").thumbprint != Ed25519KeyPair("b").thumbprint

def test_issuer_rejects_long_ttl(env):
    with pytest.raises(Exception):
        GrantIssuer(env["issuer_key"]).issue(env["execution"],human_actor_id="USR-MAYA",workload_principal_id=env["execution"].workload_principal_id,purpose="x",audience="CMP-005",intended_tool="TOOL-004",operations=("create_draft_impact_assessment",),resource_prefixes=("case://",),data_scopes=("case_internal",),region_allowlist=("CA",),max_authority_tier=2,max_uses=1,max_tool_calls=1,max_records=1,max_bytes=1,max_external_messages=0,monetary_limit_cad=0,reversible_only=True,approval=env["approval"],proof_key_thumbprint=env["workload_key"].thumbprint,ttl_seconds=301,now=env["now"])

def test_issuer_rejects_human_mismatch(env):
    with pytest.raises(Exception):
        GrantIssuer(env["issuer_key"]).issue(env["execution"],human_actor_id="OTHER",workload_principal_id=env["execution"].workload_principal_id,purpose="x",audience="CMP-005",intended_tool="TOOL-004",operations=("create_draft_impact_assessment",),resource_prefixes=("case://",),data_scopes=("case_internal",),region_allowlist=("CA",),max_authority_tier=2,max_uses=1,max_tool_calls=1,max_records=1,max_bytes=1,max_external_messages=0,monetary_limit_cad=0,reversible_only=True,approval=env["approval"],proof_key_thumbprint=env["workload_key"].thumbprint,ttl_seconds=10,now=env["now"])

def test_no_user_credential_field(env):
    fields=set(asdict(env["grant"]))
    assert not ({"access_token","refresh_token","user_credential","password"} & fields)

def test_attenuation_rejects_expansion(env):
    parent=replace(env["grant"],max_delegation_depth=1)
    with pytest.raises(Exception): GrantIssuer(env["issuer_key"]).attenuate(parent,delegation_depth=1,max_records=999)

def test_attenuation_rejects_scope_expansion(env):
    parent=replace(env["grant"],max_delegation_depth=1)
    with pytest.raises(Exception): GrantIssuer(env["issuer_key"]).attenuate(parent,delegation_depth=1,operations=("create_draft_impact_assessment","delete"))

def test_attenuation_accepts_narrower(env):
    parent=replace(env["grant"],max_delegation_depth=1)
    child=GrantIssuer(env["issuer_key"]).attenuate(parent,delegation_depth=1,max_records=1,max_uses=1,expires_at=parent.expires_at-timedelta(seconds=1),parent_grant_id=parent.grant_id)
    assert child.max_records==1 and child.parent_grant_id==parent.grant_id
