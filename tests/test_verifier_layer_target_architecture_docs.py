from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/VERIFIER_LAYER_TARGET_ARCHITECTURE.md"


def test_verifier_layer_target_doc_exists() -> None:
    assert DOC.exists()


def test_verifier_layer_target_mentions_required_checks() -> None:
    text = DOC.read_text(encoding="utf-8").lower()

    for check in [
        "data quality",
        "risk limits",
        "exposure",
        "liquidity",
        "market regime conflict",
        "expected value",
        "confidence reliability",
        "regulatory/compliance constraints",
        "strategy validity / backtest provenance",
    ]:
        assert check in text


def test_verifier_layer_target_safety_rules_are_explicit() -> None:
    text = DOC.read_text(encoding="utf-8").lower()

    for phrase in [
        "expected value must be evidence-bound",
        "confidence must be calibrated/reliability-checked",
        "backtest provenance must be available before strategy-derived candidates are trusted",
        "verifier failure must block candidate progression",
        "verifier must not place orders",
        "no llm/autonomous model may bypass the verifier",
        "execution apis remain forbidden",
    ]:
        assert phrase in text

