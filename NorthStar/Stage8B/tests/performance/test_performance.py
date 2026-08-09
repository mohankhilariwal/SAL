import json
from pathlib import Path
import time

from northstar_compliance.evaluation.judge.io import envelope_from_case
from northstar_compliance.evaluation.judge.prompt import build_judge_prompt

ROOT=Path(__file__).resolve().parents[2]
rows=[json.loads(x) for x in (ROOT/"datasets/evaluation/judge-calibration/v1.0.0/calibration_cases.jsonl").read_text().splitlines() if x]


def test_617_prompt_build_is_bounded():
    start=time.perf_counter()
    prompts=[build_judge_prompt(envelope_from_case(x)) for x in rows]
    elapsed=time.perf_counter()-start
    assert elapsed < 1.0 and max(map(len,prompts)) < 20000


def test_618_envelope_digest_is_bounded():
    start=time.perf_counter()
    digests=[envelope_from_case(x).digest for x in rows for _ in range(20)]
    assert time.perf_counter()-start < 1.0 and all(len(x)==64 for x in digests)
