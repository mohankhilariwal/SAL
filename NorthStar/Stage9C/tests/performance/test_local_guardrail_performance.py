import time
from northstar_compliance.guardrails.models import GuardrailRequest, GuardrailStage

def test_871_one_thousand_local_evaluations_under_2_5_seconds(engine):
    req=GuardrailRequest('R',GuardrailStage.INPUT,'T','C','RUN','TASK',payload={'text':'normal'},metadata={'content_type':'text/plain','malware_status':'clean'})
    start=time.perf_counter()
    for _ in range(1000): engine.evaluate(req)
    assert time.perf_counter()-start < 2.5
