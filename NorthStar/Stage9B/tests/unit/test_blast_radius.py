from dataclasses import replace
from northstar_compliance.security.identity import *


def test_budget_reserves(env):
    br=BlastRadiusController(); assert br.evaluate_and_reserve(env["budget"],env["context"])==[]
    assert br.consumption(env["budget"].budget_id).total_calls==1

def test_emergency_stop(env):
    b=replace(env["budget"],emergency_stop=True)
    assert "emergency_stop_active" in BlastRadiusController().evaluate_and_reserve(b,env["context"])

def test_tool_allowlist(env):
    b=replace(env["budget"],allowed_tools=("TOOL-001",))
    assert "tool_not_in_budget" in BlastRadiusController().evaluate_and_reserve(b,env["context"])

def test_total_call_limit(env):
    b=replace(env["budget"],max_total_calls=1)
    br=BlastRadiusController(); assert br.evaluate_and_reserve(b,env["context"])==[]; br.complete_write(b.budget_id)
    assert "budget_total_calls_exceeded" in br.evaluate_and_reserve(b,env["context"])

def test_per_tool_limit(env):
    b=replace(env["budget"],per_tool_call_limits={**env["budget"].per_tool_call_limits,"TOOL-004":1})
    br=BlastRadiusController(); assert br.evaluate_and_reserve(b,env["context"])==[]; br.complete_write(b.budget_id)
    assert "budget_tool_calls_exceeded" in br.evaluate_and_reserve(b,env["context"])

def test_record_limit(env):
    c=replace(env["context"],record_count=101)
    assert "budget_records_exceeded" in BlastRadiusController().evaluate_and_reserve(env["budget"],c)

def test_byte_limit(env):
    c=replace(env["context"],byte_count=100001)
    assert "budget_bytes_exceeded" in BlastRadiusController().evaluate_and_reserve(env["budget"],c)

def test_cost_limit(env):
    c=replace(env["context"],estimated_cost_cad=2.01)
    assert "budget_cost_exceeded" in BlastRadiusController().evaluate_and_reserve(env["budget"],c)

def test_external_message_limit(env):
    c=replace(env["context"],external_messages=2)
    assert "budget_external_messages_exceeded" in BlastRadiusController().evaluate_and_reserve(env["budget"],c)

def test_concurrent_write_limit(env):
    br=BlastRadiusController(); assert br.evaluate_and_reserve(env["budget"],env["context"])==[]
    assert "concurrent_write_limit_exceeded" in br.evaluate_and_reserve(env["budget"],env["context"])

def test_complete_write_releases_slot(env):
    br=BlastRadiusController(); br.evaluate_and_reserve(env["budget"],env["context"]); br.complete_write(env["budget"].budget_id)
    assert br.consumption(env["budget"].budget_id).active_writes==0


def test_budget_region_limit(env):
    c=replace(env["context"],region="US")
    assert "budget_region_not_allowed" in BlastRadiusController().evaluate_and_reserve(env["budget"],c)

def test_budget_data_scope_limit(env):
    c=replace(env["context"],data_scope="restricted")
    assert "budget_data_scope_not_allowed" in BlastRadiusController().evaluate_and_reserve(env["budget"],c)
