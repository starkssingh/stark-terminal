from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


ACTIVE_DECISION_DOCS = [
    "docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md",
    "docs/DECISION_CANDIDATE_PIPELINE_TARGET.md",
    "docs/VERIFIER_LAYER_TARGET_ARCHITECTURE.md",
    "docs/HUMAN_REVIEW_PAPER_TRADE_GATE_TARGET.md",
    "docs/AUDIT_LOG_JOURNAL_TARGET.md",
]


def test_active_decision_phase_doc_preserves_target_architecture() -> None:
    text = (ROOT / "docs/phases/active_decision_architecture.md").read_text(encoding="utf-8")

    required = [
        "Market data",
        "Data quality + provenance layer",
        "Timeseries engine",
        "Feature / regime / state engine",
        "Deterministic quant engine",
        "Decision candidate",
        "Verifier layer",
        "Human review / paper-trade gate",
        "Audit log + journal",
    ]

    for phrase in required:
        assert phrase in text


def test_active_decision_original_docs_remain_preserved() -> None:
    for path in ACTIVE_DECISION_DOCS:
        assert (ROOT / path).exists()

    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in ACTIVE_DECISION_DOCS)

    assert "Decision candidate is not a trade" in combined
    assert "No direct signal-to-trade path" in combined
    assert "Execution APIs remain forbidden" in combined
