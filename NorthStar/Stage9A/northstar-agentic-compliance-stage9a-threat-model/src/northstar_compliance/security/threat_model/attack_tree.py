from __future__ import annotations
from typing import Any


def leaf_risks(tree: dict[str, Any]) -> set[str]:
    leaves: set[str] = set()
    for child in tree["children"]:
        leaves.update(child["children"])
    return leaves


def evaluate_boolean(tree: dict[str, Any], achieved_risks: set[str]) -> bool:
    child_values = []
    for child in tree["children"]:
        values = [rid in achieved_risks for rid in child["children"]]
        child_values.append(all(values) if child["operator"] == "AND" else any(values))
    return all(child_values) if tree["operator"] == "AND" else any(child_values)
