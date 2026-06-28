from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ACTIVE_DECISION_DOCS = [
    "ACTIVE_DECISION_ARCHITECTURE_TARGET.md",
    "DECISION_CANDIDATE_PIPELINE_TARGET.md",
    "VERIFIER_LAYER_TARGET_ARCHITECTURE.md",
    "HUMAN_REVIEW_PAPER_TRADE_GATE_TARGET.md",
    "AUDIT_LOG_JOURNAL_TARGET.md",
]


def _doc_text(name: str) -> str:
    return (ROOT / "docs" / name).read_text(encoding="utf-8")


def test_active_decision_target_docs_exist() -> None:
    for doc in ACTIVE_DECISION_DOCS:
        assert (ROOT / "docs" / doc).exists(), doc


def test_active_decision_target_architecture_contains_pipeline_stages() -> None:
    text = _doc_text("ACTIVE_DECISION_ARCHITECTURE_TARGET.md")

    for stage in [
        "Market data",
        "Data quality + provenance layer",
        "Timeseries engine",
        "Feature / regime / state engine",
        "Deterministic quant engine",
        "Decision candidate",
        "Verifier layer",
        "Human review / paper-trade gate",
        "Audit log + journal",
    ]:
        assert stage in text


def test_active_decision_target_docs_state_future_not_implementation() -> None:
    combined = "\n".join(_doc_text(doc) for doc in ACTIVE_DECISION_DOCS).lower()

    for phrase in [
        "future target",
        "not current implementation",
        "not active implementation",
        "contract/skeleton/audit/boundary-first",
        "active implementation requires future prompts",
        "execution apis remain forbidden",
        "decision candidate is not a trade",
        "no direct market-data-to-trade path is allowed",
        "no direct signal-to-trade path is allowed",
        "no llm/autonomous model may bypass the verifier",
    ]:
        assert phrase in combined


def test_active_decision_target_status_docs_are_updated() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    safety = (ROOT / "docs/SAFETY_AUDIT.md").read_text(encoding="utf-8")
    data_policy = (ROOT / "docs/DATA_POLICY.md").read_text(encoding="utf-8")
    infrastructure = (ROOT / "docs/INFRASTRUCTURE_STACK.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Active Decision Architecture Target" in north_star
    assert "Decision candidate is not a trade" in north_star
    assert "execution APIs remain forbidden" in north_star
    assert "Active Decision Architecture Target Safety Note" in safety
    assert "Active Decision Architecture Target Data Policy" in data_policy
    assert "Active Decision Architecture Target" in infrastructure
    assert "Interlude Active Decision Architecture Target Documentation" in project_map
    assert "Interlude - Active Decision Architecture Target Documentation" in prompt_log

