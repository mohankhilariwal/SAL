from __future__ import annotations

import json


def test_required_evaluations_are_declared():
    config = json.loads(open("config/evaluation/stage5b.json", encoding="utf-8").read())
    assert config["required_evaluations"] == [
        "EVAL-048", "EVAL-049", "EVAL-050", "EVAL-051", "EVAL-052", "EVAL-053", "EVAL-054"
    ]
    assert config["deny_by_default"] is True
