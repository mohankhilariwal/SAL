from time import perf_counter
from .helpers import make_engine

def test_735_report_under_one_second():
    e=make_engine(); start=perf_counter(); e.report(); assert perf_counter()-start < 1.0

def test_736_validation_under_one_second():
    e=make_engine(); start=perf_counter(); assert e.validate()==[]; assert perf_counter()-start < 1.0
