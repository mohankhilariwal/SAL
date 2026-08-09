from decimal import Decimal
import pytest
from northstar_compliance.finops.models import CostCategory, CostEvent, CostRate
from northstar_compliance.finops.costing import CostCalculator, RateCard, failed_run_cost, retry_cost, human_escalation_cost


def calc():
    return CostCalculator(RateCard([
        CostRate(CostCategory.MODEL_INPUT, Decimal("0.001"), "token"),
        CostRate(CostCategory.MODEL_OUTPUT, Decimal("0.002"), "token"),
        CostRate(CostCategory.RECOVERY, Decimal("2"), "minute"),
    ]))

def event(category, quantity, unit, **kw):
    return CostEvent("R1", "Q1", category, Decimal(str(quantity)), unit, "WP", "BU", "CA", "test", success=kw.get("success", True), retry=kw.get("retry", False))


def test_1017_prices_event_with_decimal_precision():
    line = calc().price_event(event(CostCategory.MODEL_INPUT, 3, "token"))
    assert line.amount == Decimal("0.003000")


def test_1018_rejects_unit_mismatch():
    with pytest.raises(ValueError): calc().price_event(event(CostCategory.MODEL_INPUT, 3, "call"))


def test_1019_rejects_missing_rate():
    with pytest.raises(KeyError): calc().price_event(event(CostCategory.RECOVERY, 1, "minute")) if False else RateCard([CostRate(CostCategory.MODEL_INPUT, Decimal("1"), "token")]).rate_for(CostCategory.RECOVERY)


def test_1020_report_computes_unit_costs():
    events = [event(CostCategory.MODEL_INPUT, 10, "token"), event(CostCategory.MODEL_OUTPUT, 2, "token")]
    report = calc().report(events, completed_task_ids=["R1"], document_ids=["D1"], human_escalation_ids=[])
    assert report.total_cost == Decimal("0.014000")
    assert report.cost_per_completed_task == Decimal("0.014000")


def test_1021_failed_run_cost():
    events = [event(CostCategory.MODEL_INPUT, 10, "token", success=False), event(CostCategory.MODEL_OUTPUT, 2, "token")]
    assert failed_run_cost(events, calc()) == Decimal("0.014000")


def test_1022_retry_cost():
    events = [event(CostCategory.MODEL_INPUT, 10, "token", retry=True), event(CostCategory.MODEL_OUTPUT, 2, "token")]
    assert retry_cost(events, calc()) == Decimal("0.010000")


def test_1023_human_escalation_cost():
    assert human_escalation_cost(Decimal("30"), Decimal("120"), Decimal("5")) == Decimal("65.000000")


def test_1024_negative_quantity_rejected():
    with pytest.raises(ValueError): event(CostCategory.MODEL_INPUT, -1, "token")


def test_1025_authority_effect_cannot_change():
    with pytest.raises(ValueError): CostEvent("R","Q",CostCategory.MODEL_INPUT,Decimal("1"),"token","WP","BU","CA","test",authority_effect="grant")
