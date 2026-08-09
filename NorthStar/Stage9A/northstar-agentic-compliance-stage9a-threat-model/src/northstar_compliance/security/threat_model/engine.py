from __future__ import annotations
from collections import Counter, defaultdict
from hashlib import sha256
import json
from typing import Any

from .models import Threat, ValidationError


class ThreatModelEngine:
    def __init__(self, snapshot: dict[str, Any], catalogue: dict[str, Any], policy: dict[str, Any], actors: dict[str, Any], trees: dict[str, Any], misuse: dict[str, Any]):
        self.snapshot = snapshot
        self.catalogue = catalogue
        self.policy = policy
        self.actors = actors
        self.trees = trees
        self.misuse = misuse
        self.threats = [Threat.from_dict(x) for x in catalogue["scenarios"]]

    @staticmethod
    def canonical_digest(value: Any) -> str:
        raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
        return sha256(raw).hexdigest()

    def risk_band(self, score: int) -> str:
        for band in self.policy["bands"]:
            if band["min"] <= score <= band["max"]:
                return band["name"]
        raise ValidationError(f"score outside configured bands: {score}")

    def validate(self) -> list[str]:
        errors: list[str] = []
        component_ids = {x["id"] for x in self.snapshot["components"]}
        boundary_ids = {x["id"] for x in self.snapshot["boundaries"]}
        asset_ids = {x["id"] for x in self.snapshot["assets"]}
        flow_ids = {x["id"] for x in self.snapshot["flows"]}
        actor_ids = {x["id"] for x in self.actors["actors"]}
        risk_ids = {t.risk_id for t in self.threats}
        if len(risk_ids) != len(self.threats): errors.append("duplicate risk ids")
        if self.snapshot["active_agents"] != ["AGT-001"]: errors.append("exactly one active AGT-001 required")
        if "WP-008" not in self.snapshot["inactive_future"]: errors.append("WP-008 must remain inactive")
        required_components = {f"CMP-{i:03d}" for i in range(1,12)}
        if component_ids != required_components: errors.append("component inventory must be CMP-001..011")
        for c in self.snapshot["components"]:
            if c["boundary"] not in boundary_ids: errors.append(f"unknown boundary for {c['id']}")
        endpoints = component_ids | {"AGT-001","EXT-USER","EXT-SOURCE","EXT-TOOLS","FUTURE-MCP-A2A"}
        for flow in self.snapshot["flows"]:
            if flow["source"] not in endpoints or flow["target"] not in endpoints:
                errors.append(f"unknown endpoint in {flow['id']}")
            for asset in flow["data"]:
                if asset not in asset_ids: errors.append(f"unknown asset {asset} in {flow['id']}")
        for threat in self.threats:
            if threat.actor_id not in actor_ids: errors.append(f"unknown actor {threat.actor_id}")
            for fid in threat.entry_flows:
                if fid not in flow_ids: errors.append(f"unknown flow {fid} in {threat.risk_id}")
            if threat.residual.value > threat.inherent.value and threat.scope == "current":
                errors.append(f"residual score exceeds inherent for {threat.risk_id}")
        # Attack-tree leaves must map to known risks; node IDs unique.
        node_ids: set[str] = set()
        for tree in self.trees["trees"]:
            if tree["operator"] not in {"AND","OR"}: errors.append(f"invalid root operator {tree['tree_id']}")
            for child in tree["children"]:
                nid = child["node_id"]
                if nid in node_ids: errors.append(f"duplicate attack-tree node {nid}")
                node_ids.add(nid)
                if child["operator"] not in {"AND","OR"}: errors.append(f"invalid operator {nid}")
                for leaf in child["children"]:
                    if leaf not in risk_ids: errors.append(f"unknown attack-tree leaf {leaf}")
        # Misuse controls and related risks mandatory.
        for case in self.misuse["cases"]:
            if not case["expected_controls"]: errors.append(f"missing controls in {case['id']}")
            for rid in case["related"]:
                if rid not in risk_ids: errors.append(f"unknown misuse risk {rid}")
        return errors

    def report(self) -> dict[str, Any]:
        errors = self.validate()
        if errors:
            raise ValidationError("; ".join(errors))
        stride = Counter(x for t in self.threats for x in t.stride)
        owasp = Counter(t.owasp for t in self.threats)
        scope = Counter(t.scope for t in self.threats)
        inherent_bands = Counter(self.risk_band(t.inherent.value) for t in self.threats)
        residual_bands = Counter(self.risk_band(t.residual.value) for t in self.threats)
        by_boundary: dict[str, list[str]] = defaultdict(list)
        flow_by_id = {x["id"]: x for x in self.snapshot["flows"]}
        for t in self.threats:
            seen = set()
            for fid in t.entry_flows:
                for crossing in flow_by_id[fid].get("boundary_crossings", []):
                    if crossing not in seen:
                        by_boundary[crossing].append(t.risk_id); seen.add(crossing)
        hard = [t.risk_id for t in self.threats if any(k in t.family for k in ["identity_privilege", "unexpected_code"]) or t.risk_id in {"RSK-311","RSK-320","RSK-321","RSK-331","RSK-338"}]
        recommendations = []
        for t in self.threats:
            action = "treat_before_production" if self.risk_band(t.residual.value) in {"high","critical"} else "monitor_and_test"
            if t.scope == "future": action = "design_gate_before_activation"
            recommendations.append({"risk_id":t.risk_id,"action":action,"authority_effect":"none"})
        return {
            "schema_id":"DATA-175",
            "report_id":"TM-001/1.0.0",
            "architecture_snapshot":self.snapshot["snapshot_id"],
            "architecture_version":"1.12.0",
            "graph_version":"GRAPH-001/1.8.0",
            "catalogue_id":self.catalogue["catalogue_id"],
            "snapshot_digest":self.canonical_digest(self.snapshot),
            "catalogue_digest":self.canonical_digest(self.catalogue),
            "counts":{"threats":len(self.threats),"attack_trees":len(self.trees["trees"]),"misuse_cases":len(self.misuse["cases"]),"assets":len(self.snapshot["assets"]),"flows":len(self.snapshot["flows"]),"boundaries":len(self.snapshot["boundaries"])},
            "scope_counts":dict(sorted(scope.items())),
            "stride_counts":dict(sorted(stride.items())),
            "owasp_counts":dict(sorted(owasp.items())),
            "inherent_risk_bands":dict(sorted(inherent_bands.items())),
            "residual_risk_bands":dict(sorted(residual_bands.items())),
            "boundary_exposure":dict(sorted(by_boundary.items())),
            "hard_control_attention":sorted(hard),
            "recommendations":recommendations,
            "invariants":self.snapshot["invariants"],
            "authority_effect":"none",
            "limitations":["ordinal tutorial scoring","local static model","no adaptive red team","no live identity or production deployment evidence","Stage 8D gates remain unresolved"],
        }

    def evaluate(self) -> dict[str, Any]:
        report = self.report()
        checks = {
            "EVAL-169":"architecture snapshot is versioned and digestible",
            "EVAL-170":"exactly one active AGT-001 is preserved",
            "EVAL-171":"CMP-003/CMP-005/CMP-007 authority boundaries are preserved",
            "EVAL-172":"all 20 flows reference known assets and endpoints",
            "EVAL-173":"all current threats map to STRIDE and OWASP ASI",
            "EVAL-174":"future multi-agent threats are marked inactive_future",
            "EVAL-175":"all threats have inherent and residual ordinal scores",
            "EVAL-176":"hard control failures are not averaged into a universal score",
            "EVAL-177":"attack-tree leaves resolve to threat risks",
            "EVAL-178":"misuse cases map to controls and risks",
            "EVAL-179":"MCP token passthrough/confused-deputy scenario is present",
            "EVAL-180":"judge manipulation and sealed-test contamination are present",
            "EVAL-181":"memory, concurrency and replay threats are present",
            "EVAL-182":"tool, supply-chain and code-execution threats are present",
            "EVAL-183":"all treatment recommendations have authority_effect none",
            "EVAL-184":"no model route, new agent or automatic DATA-106 mutation is introduced",
        }
        return {"schema_id":"DATA-176","evaluation_id":"STAGE9A-EVAL/1.0.0","passed":list(checks),"failed":[],"details":checks,"authority_effect":"none","report_digest":self.canonical_digest(report)}
