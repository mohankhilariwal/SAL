"""Control-plane artifact loading + the per-request version vector.

The data plane reads *pinned* control-plane artifacts (models.yaml, policy.yaml,
taxonomy.yaml, prompts/, schemas/, lexicons/) and stamps a version vector on every
request. It never reads "latest" from a remote source; artifacts are promoted via
git + the regression gate (control_plane/regression.py).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path(os.environ.get("SPINCHECK_CONFIG_DIR", "config"))
PROMPT_DIR = Path(os.environ.get("SPINCHECK_PROMPT_DIR", "prompts"))
SCHEMA_DIR = Path(os.environ.get("SPINCHECK_SCHEMA_DIR", "schemas"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


@dataclass
class Prompt:
    prompt_id: str
    template: str
    sha: str

    def render(self, **kw: Any) -> str:
        out = self.template
        for k, v in kw.items():  # simple, brace-safe substitution
            out = out.replace("{" + k + "}", str(v))
        return out


@dataclass
class ControlPlane:
    models: dict
    policy: dict
    taxonomy: dict
    schema: dict
    prompts: dict[str, Prompt]
    lexicons: dict[str, list[str]]
    hashes: dict[str, str] = field(default_factory=dict)

    # ---------------- loading ----------------
    @classmethod
    def load(cls, root: Path | None = None) -> "ControlPlane":
        root = root or Path(".")
        cdir, pdir, sdir = root / CONFIG_DIR, root / PROMPT_DIR, root / SCHEMA_DIR
        models = yaml.safe_load((cdir / "models.yaml").read_text())
        policy = yaml.safe_load((cdir / "policy.yaml").read_text())
        taxonomy = yaml.safe_load((cdir / "taxonomy.yaml").read_text())
        schema = json.loads((sdir / "analysis.schema.json").read_text())
        prompts: dict[str, Prompt] = {}
        for f in sorted(pdir.glob("*_v*.md")):
            pid = f.stem
            prompts[pid] = Prompt(pid, f.read_text(), _sha(f))
        lexicons = {
            f.stem: [ln.strip() for ln in f.read_text().splitlines() if ln.strip()]
            for f in sorted((cdir / "lexicons").glob("*.txt"))
        }
        hashes = {
            "models": _sha(cdir / "models.yaml"),
            "policy": _sha(cdir / "policy.yaml"),
            "taxonomy": _sha(cdir / "taxonomy.yaml"),
            "schema": _sha(sdir / "analysis.schema.json"),
        }
        return cls(models, policy, taxonomy, schema, prompts, lexicons, hashes)

    # ---------------- accessors ----------------
    def layer(self, name: str) -> dict:
        return self.models["layers"][name]

    def prompt(self, prefix: str) -> Prompt:
        """Latest pinned version of a prompt family, e.g. 'tier1_analysis'."""
        cands = sorted(k for k in self.prompts if k.startswith(prefix))
        if not cands:
            raise KeyError(f"no prompt for {prefix}")
        return self.prompts[cands[-1]]

    def calibration_map(self) -> dict[str, str]:
        """bucket -> displayed bucket; identity when no fitted map is deployed."""
        p = Path(self.policy["confidence"].get("calibration_map", ""))
        if p and p.exists():
            return json.loads(p.read_text())
        return {"low": "low", "medium": "medium", "high": "high"}

    # ---------------- version vector ----------------
    def version_vector(self) -> dict[str, Any]:
        t1, t2 = self.layer("tier1"), self.layer("tier2")
        return {
            "models_version": self.models.get("version"),
            "policy_version": self.policy.get("version"),
            "taxonomy_version": self.taxonomy.get("version"),
            "tier1_pin": f'{t1["provider"]}:{t1["model"]}@{t1.get("snapshot_date","-")}',
            "tier2_pin": f'{t2["provider"]}:{t2["model"]}@{t2.get("snapshot_date","-")}',
            "prompt_pins": {k: v.sha for k, v in self.prompts.items()},
            "artifact_hashes": self.hashes,
        }


_INJ_CACHE: list[re.Pattern] | None = None


def injection_regexes(cp: ControlPlane) -> list[re.Pattern]:
    global _INJ_CACHE
    if _INJ_CACHE is None:
        _INJ_CACHE = [re.compile(p, re.I) for p in cp.lexicons.get("injection_patterns", [])]
    return _INJ_CACHE
