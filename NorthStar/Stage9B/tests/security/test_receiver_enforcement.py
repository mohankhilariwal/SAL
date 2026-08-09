from dataclasses import replace
from datetime import timedelta
import pytest
from northstar_compliance.security.identity import *


def auth(env, grant=None, envelope=None, proof=None, context=None, budget=None, nonce="n1", now=None):
    grant=grant or env["grant"]; envelope=envelope or env["envelope"]; context=context or env["context"]; budget=budget or env["budget"]
    proof=proof or ProofService.create(grant,context,env["workload_key"],request_nonce=nonce,now=now or env["now"])
    return env["gateway"].authorize(grant,envelope,proof,context,budget,now=now or env["now"])


def test_happy_path(env): assert auth(env).allowed

def test_replay_denied(env):
    p=ProofService.create(env["grant"],env["context"],env["workload_key"],request_nonce="same",now=env["now"])
    assert env["gateway"].authorize(env["grant"],env["envelope"],p,env["context"],env["budget"],now=env["now"]).allowed
    d=env["gateway"].authorize(env["grant"],env["envelope"],p,env["context"],env["budget"],now=env["now"])
    assert not d.allowed and "proof_replay" in d.reason_codes

@pytest.mark.parametrize("field,value,code",[
 ("tenant_id","OTHER","tenant_mismatch"),("case_id","OTHER","case_mismatch"),("run_id","OTHER","run_mismatch"),("task_id","OTHER","task_mismatch"),("execution_id","OTHER","execution_mismatch"),("human_actor_id","OTHER","human_actor_mismatch"),("workload_principal_id","OTHER","workload_mismatch"),("audience","OTHER","audience_mismatch"),("tool_id","TOOL-005","tool_mismatch"),("operation","delete","operation_not_granted"),("resource","case://OTHER/x","resource_out_of_scope"),("data_scope","restricted","data_scope_out_of_scope"),("region","US","region_not_allowed")])
def test_binding_failures(env,field,value,code):
    c=replace(env["context"],**{field:value})
    p=ProofService.create(env["grant"],c,env["workload_key"],request_nonce=field,now=env["now"])
    d=env["gateway"].authorize(env["grant"],env["envelope"],p,c,env["budget"],now=env["now"])
    assert not d.allowed and code in d.reason_codes

def test_expired_grant(env):
    d=auth(env,now=env["grant"].expires_at+timedelta(seconds=1))
    assert not d.allowed and "grant_expired" in d.reason_codes

def test_revoked_grant(env):
    env["gateway"].revocations.revoke(env["grant"].grant_id,"incident",env["now"])
    d=auth(env)
    assert not d.allowed and "grant_revoked" in d.reason_codes

def test_use_limit(env):
    assert auth(env,nonce="a").allowed
    env["gateway"].blast.complete_write(env["budget"].budget_id)
    assert auth(env,nonce="b").allowed
    env["gateway"].blast.complete_write(env["budget"].budget_id)
    d=auth(env,nonce="c")
    assert not d.allowed and "grant_use_limit_exceeded" in d.reason_codes

def test_wrong_proof_key(env):
    other=Ed25519KeyPair("other")
    with pytest.raises(ValueError): ProofService.create(env["grant"],env["context"],other,now=env["now"])

def test_stale_proof(env):
    p=ProofService.create(env["grant"],env["context"],env["workload_key"],request_nonce="stale",now=env["now"]-timedelta(seconds=31))
    d=env["gateway"].authorize(env["grant"],env["envelope"],p,env["context"],env["budget"],now=env["now"])
    assert not d.allowed and "proof_outside_time_window" in d.reason_codes

def test_tampered_grant_payload(env):
    bad=replace(env["grant"],audience="evil")
    p=ProofService.create(bad,replace(env["context"],audience="evil"),env["workload_key"],request_nonce="t",now=env["now"])
    d=env["gateway"].authorize(bad,env["envelope"],p,replace(env["context"],audience="evil"),env["budget"],now=env["now"])
    assert not d.allowed and "grant_payload_mismatch" in d.reason_codes

def test_tier5_always_denied(env):
    c=replace(env["context"],authority_tier=AuthorityTier.PROHIBITED_AUTONOMOUS)
    p=ProofService.create(env["grant"],c,env["workload_key"],request_nonce="t5",now=env["now"])
    d=env["gateway"].authorize(env["grant"],env["envelope"],p,c,env["budget"],now=env["now"])
    assert not d.allowed and "prohibited_autonomous_action" in d.reason_codes

def test_high_impact_requires_dual_control(env):
    c=replace(env["context"],authority_tier=AuthorityTier.HIGH_IMPACT_REGULATED)
    p=ProofService.create(env["grant"],c,env["workload_key"],request_nonce="t4",now=env["now"])
    d=env["gateway"].authorize(env["grant"],env["envelope"],p,c,env["budget"],now=env["now"])
    assert not d.allowed and "high_impact_requires_approval" in d.reason_codes


def test_proof_body_digest_mismatch(env):
    c=replace(env["context"],body_digest="different")
    p=ProofService.create(env["grant"],env["context"],env["workload_key"],request_nonce="body",now=env["now"])
    d=env["gateway"].authorize(env["grant"],env["envelope"],p,c,env["budget"],now=env["now"])
    assert not d.allowed and "proof_body_digest_mismatch" in d.reason_codes

def test_grant_numeric_record_limit(env):
    c=replace(env["context"],record_count=env["grant"].max_records+1)
    p=ProofService.create(env["grant"],c,env["workload_key"],request_nonce="records",now=env["now"])
    d=env["gateway"].authorize(env["grant"],env["envelope"],p,c,env["budget"],now=env["now"])
    assert not d.allowed and "record_limit_exceeded" in d.reason_codes
