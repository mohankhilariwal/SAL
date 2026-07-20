"""CLI entry point: PYTHONPATH=src python -m spincheck.cli analyze --text '...'"""
from __future__ import annotations
import argparse, json, sys

from .config import ControlPlane
from .orchestrator import Orchestrator
from .telemetry import log_request


def main(argv=None):
    ap = argparse.ArgumentParser("spincheck")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyze"); a.add_argument("--text", required=True)
    sub.add_parser("version")
    args = ap.parse_args(argv)
    cp = ControlPlane.load()
    if args.cmd == "version":
        print(json.dumps(cp.version_vector(), indent=2)); return 0
    orch = Orchestrator(cp)
    resp = orch.analyze(args.text)
    log_request(dict(resp.to_dict()), len(args.text))
    print(json.dumps(resp.to_dict(), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
