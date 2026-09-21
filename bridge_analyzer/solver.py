"""Double-dummy solving via a separate Python that has endplay installed.

The analyzer itself runs on any Python; endplay (which bundles Bo Haglund's DDS)
has no wheel for 3.14, so it lives in its own venv and is called as a subprocess.
Set BRIDGE_SOLVER_PYTHON to that venv's python.exe to override the default.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from .lin_tools import SUITS

DEFAULT_PYTHON = Path(r"C:\Users\My Computer\agentul meu\analizor done\solver-env\Scripts\python.exe")
WORKER = Path(__file__).with_name("dd_worker.py")


class SolverUnavailable(RuntimeError):
    pass


def solver_python() -> Path:
    return Path(os.environ.get("BRIDGE_SOLVER_PYTHON", DEFAULT_PYTHON))


def _pbn(hand: dict) -> str:
    return ".".join("".join(hand[s]) for s in SUITS)


def solve(board) -> dict:
    """Double-dummy table and par for a board (see dd_worker for the shape)."""
    py = solver_python()
    if not py.exists():
        raise SolverUnavailable(f"solver Python not found: {py} (set BRIDGE_SOLVER_PYTHON)")
    req = {
        "hands": {p: _pbn(h) for p, h in board.hands.items()},
        "dealer": board.dealer,
        "vul": board.vulnerability,
    }
    proc = subprocess.run(
        [str(py), str(WORKER)], input=json.dumps(req), capture_output=True,
        text=True, encoding="utf-8", timeout=120,
    )
    if proc.returncode != 0:
        raise SolverUnavailable(f"solver failed: {proc.stderr.strip()[-300:]}")
    return json.loads(proc.stdout)
