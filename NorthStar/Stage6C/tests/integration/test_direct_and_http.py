from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

from northstar_compliance.interoperability.adapters.direct import DirectAdapter
from northstar_compliance.interoperability.adapters.http_json import HttpJsonAdapter
from northstar_compliance.interoperability.fixtures import build_fixture

ROOT = Path(__file__).resolve().parents[2]


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _start_server(port: int) -> subprocess.Popen[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    proc = subprocess.Popen(
        [sys.executable, str(ROOT / "scripts/run_reference_server.py"), "--port", str(port)],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert proc.stdout is not None
    line = proc.stdout.readline().strip()
    if not line.startswith("READY"):
        stderr = proc.stderr.read() if proc.stderr else ""
        proc.kill()
        raise RuntimeError(f"server_failed:{line}:{stderr}")
    return proc


def test_344_direct_reference_roundtrip():
    receipt = DirectAdapter().deliver(build_fixture())
    assert receipt.terminal_status == "completed" and receipt.semantic_loss == ()


def test_345_http_real_process_boundary_roundtrip():
    port = _free_port()
    proc = _start_server(port)
    try:
        receipt = HttpJsonAdapter(f"http://127.0.0.1:{port}/handoff").deliver(build_fixture())
        assert receipt.terminal_status == "completed"
        assert receipt.remote_endpoint_id == "CAND-EVIDENCE-VERIFIER-001"
        assert receipt.semantic_loss == ()
    finally:
        proc.terminate()
        proc.wait(timeout=5)


def test_346_http_server_remains_single_request_reference():
    port = _free_port()
    proc = _start_server(port)
    try:
        adapter = HttpJsonAdapter(f"http://127.0.0.1:{port}/handoff")
        first = adapter.deliver(build_fixture())
        second = adapter.deliver(build_fixture())
        assert first.receipt_id == second.receipt_id == "RCP-HTTP-001"
    finally:
        proc.terminate()
        proc.wait(timeout=5)
