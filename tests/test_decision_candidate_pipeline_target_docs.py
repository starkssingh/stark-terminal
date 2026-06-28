from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/DECISION_CANDIDATE_PIPELINE_TARGET.md"


def test_decision_candidate_pipeline_doc_exists() -> None:
    assert DOC.exists()


def test_decision_candidate_pipeline_boundaries_are_explicit() -> None:
    text = DOC.read_text(encoding="utf-8").lower()

    for phrase in [
        "market data is not a decision",
        "features/regimes are not trades",
        "deterministic quant engine output is not a trade",
        "decision candidate is not a trade",
        "a candidate is only a candidate",
        "must pass verifier checks",
        "no direct trade commit path is allowed",
        "no direct market-data-to-trade path is allowed",
        "no direct signal-to-trade path is allowed",
        "execution apis remain forbidden",
    ]:
        assert phrase in text


def test_decision_candidate_pipeline_does_not_enable_current_capabilities() -> None:
    text = DOC.read_text(encoding="utf-8").lower()

    for phrase in [
        "does not implement active decision generation",
        "recommendation generation",
        "confidence scoring",
        "paper trading",
        "broker controls",
        "market-data ingestion",
        "strategy generation",
        "backtesting",
        "execution apis",
    ]:
        assert phrase in text

