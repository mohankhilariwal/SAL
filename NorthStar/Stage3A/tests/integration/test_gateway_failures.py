from __future__ import annotations

from dataclasses import replace

from northstar_compliance.tools.adapters import FlakyAdapter, MalformedOutputAdapter, SleepAdapter
from northstar_compliance.tools.controls import CircuitBreaker, SlidingWindowRateLimiter
from northstar_compliance.tools.gateway import ToolGateway
from northstar_compliance.tools.models import RetryPolicy, ToolInvocationRequest, ToolStatus
from northstar_compliance.tools.registry import ToolRegistry


def request(principal, n, tool, args, key=None):
    return ToolInvocationRequest(
        invocation_id=f"TINV-FAIL-{n:03d}",tool_id=tool,tool_version="1.0.0",
        principal=principal,arguments=args,idempotency_key=key)


def read_args():
    return {"query":"ability","jurisdiction":"CA","as_of_date":None,"limit":5}


def write_args():
    return {"publication_id":"REG-F","title":"Failure scenario publication","jurisdictions":["CA"],"candidate_domains":["lending"],"source_citation_ids":["CIT-F"]}


def test_063_read_only_transient_failure_retries_with_bound(repo_root, maya):
    loaded=ToolRegistry.load(repo_root/"config"/"tools")
    descriptor=loaded.resolve("TOOL-001","1.0.0")
    output={"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","additionalProperties":False,"properties":{"ok":{"type":"boolean"},"calls":{"type":"integer"}},"required":["ok","calls"]}
    descriptor=replace(descriptor,output_schema=output,retry_policy=RetryPolicy(2,("TransientToolError",)))
    flaky=FlakyAdapter(transient_failures=1)
    result=ToolGateway(ToolRegistry([descriptor]),{"TOOL-001":flaky}).invoke(request(maya,1,"TOOL-001",read_args()))
    assert result.status == ToolStatus.SUCCESS
    assert result.attempts == 2
    assert flaky.calls == 2


def test_064_reversible_write_is_never_automatically_retried(repo_root, maya):
    loaded=ToolRegistry.load(repo_root/"config"/"tools")
    descriptor=replace(loaded.resolve("TOOL-004","1.0.0"),retry_policy=RetryPolicy(3,("TransientToolError",)))
    flaky=FlakyAdapter(transient_failures=3)
    result=ToolGateway(ToolRegistry([descriptor]),{"TOOL-004":flaky}).invoke(request(maya,1,"TOOL-004",write_args(),"WRITE-FAIL"))
    assert result.status == ToolStatus.EXECUTION_ERROR
    assert result.attempts == 1
    assert flaky.calls == 1


def test_065_timeout_is_bounded(repo_root, maya):
    loaded=ToolRegistry.load(repo_root/"config"/"tools")
    descriptor=replace(loaded.resolve("TOOL-001","1.0.0"),timeout_ms=10)
    result=ToolGateway(ToolRegistry([descriptor]),{"TOOL-001":SleepAdapter(0.1)}).invoke(request(maya,1,"TOOL-001",read_args()))
    assert result.status == ToolStatus.TIMEOUT
    assert result.duration_ms < 90


def test_066_malformed_output_is_rejected(repo_root, maya):
    registry=ToolRegistry.load(repo_root/"config"/"tools")
    result=ToolGateway(registry,{"TOOL-001":MalformedOutputAdapter()}).invoke(request(maya,1,"TOOL-001",read_args()))
    assert result.status == ToolStatus.OUTPUT_VALIDATION_ERROR


def test_067_result_size_limit_is_enforced(repo_root, maya):
    class LargeAdapter:
        def execute(self, arguments, principal):
            return {"matches":[{"publication_id":"REG-X","title":"x"*1000,"jurisdiction":"CA","published_date":"2026-01-01","authority":"A","source_uri":"local://x"}],"result_count":1,"catalogue_version":"v1","authoritative_live_source":False}
    loaded=ToolRegistry.load(repo_root/"config"/"tools")
    descriptor=replace(loaded.resolve("TOOL-001","1.0.0"),max_result_bytes=256)
    result=ToolGateway(ToolRegistry([descriptor]),{"TOOL-001":LargeAdapter()}).invoke(request(maya,1,"TOOL-001",read_args()))
    assert result.status == ToolStatus.RESULT_TOO_LARGE


def test_068_rate_limit_fails_closed(repo_root, maya):
    registry=ToolRegistry.load(repo_root/"config"/"tools")
    from northstar_compliance.tools.adapters import RegulatoryCatalogueSearchAdapter
    gateway=ToolGateway(registry,{"TOOL-001":RegulatoryCatalogueSearchAdapter()},rate_limiter=SlidingWindowRateLimiter(limit=1,window_seconds=60))
    assert gateway.invoke(request(maya,1,"TOOL-001",read_args())).status == ToolStatus.SUCCESS
    assert gateway.invoke(request(maya,2,"TOOL-001",read_args())).status == ToolStatus.RATE_LIMITED


def test_069_circuit_breaker_opens_after_failure(repo_root, maya):
    loaded=ToolRegistry.load(repo_root/"config"/"tools")
    descriptor=replace(loaded.resolve("TOOL-001","1.0.0"),retry_policy=RetryPolicy(1,()))
    flaky=FlakyAdapter(transient_failures=5)
    gateway=ToolGateway(ToolRegistry([descriptor]),{"TOOL-001":flaky},circuit_breaker=CircuitBreaker(failure_threshold=1,reset_seconds=60))
    assert gateway.invoke(request(maya,1,"TOOL-001",read_args())).status == ToolStatus.EXECUTION_ERROR
    assert gateway.invoke(request(maya,2,"TOOL-001",read_args())).status == ToolStatus.CIRCUIT_OPEN
    assert flaky.calls == 1
