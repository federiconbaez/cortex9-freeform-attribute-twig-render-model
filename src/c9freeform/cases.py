"""Fixture loading shared by tests and scripts/gen_results.py."""
from __future__ import annotations

import json
from pathlib import Path

from . import attributes

ROOT = Path(__file__).resolve().parents[2]


def load() -> list:
    data = json.loads((ROOT / "fixtures/cases.json").read_text(encoding="utf-8"))
    return data["cases"]


def run(case: dict, version: str):
    """Return (label, result) where result is 'TWIG_ERROR' or [[k, v], ...]."""
    label, rows = attributes.evaluate(
        version, [tuple(a) for a in case["attrs"]], case["props"])
    if label == "TWIG_ERROR":
        return label, "TWIG_ERROR"
    return label, [[k, v] for k, v, _d in rows]


def rules(case: dict, version: str) -> str:
    label, rows = attributes.evaluate(
        version, [tuple(a) for a in case["attrs"]], case["props"])
    if label == "TWIG_ERROR":
        return "L300"
    return ";".join(d for _k, _v, d in rows)
