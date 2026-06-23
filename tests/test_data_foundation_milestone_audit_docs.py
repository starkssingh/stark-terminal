from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read_doc(name: str) -> str:
    return (ROOT / "docs" / name).read_text(encoding="utf-8")


def test_prompt_22_milestone_audit_docs_exist() -> None:
    required = [
        "DATA_FOUNDATION_MILESTONE_AUDIT.md",
        "SYNTHETIC_STORAGE_EXPORT_AUDIT.md",
        "PROVIDER_GUARDRAIL_AUDIT.md",
        "LOCAL_SAMPLE_PROVIDER_AUDIT.md",
        "DATA_FOUNDATION_MILESTONE_NEXT_PHASE.md",
    ]
    for doc in required:
        assert (ROOT / "docs" / doc).exists()


def test_prompt_22_milestone_docs_cover_required_safety_scope() -> None:
    text = "\n".join(
        _read_doc(name)
        for name in [
            "DATA_FOUNDATION_MILESTONE_AUDIT.md",
            "SYNTHETIC_STORAGE_EXPORT_AUDIT.md",
            "PROVIDER_GUARDRAIL_AUDIT.md",
            "LOCAL_SAMPLE_PROVIDER_AUDIT.md",
            "DATA_FOUNDATION_MILESTONE_NEXT_PHASE.md",
        ]
    )
    required_phrases = [
        "Prompts 18-21",
        "synthetic OHLCV storage",
        "synthetic OHLCV research lake export",
        "provider guardrails",
        "Local Sample Provider Adapter v0",
        "no real ingestion",
        "no external calls",
        "no scraping",
        "no credentials",
        "no execution APIs",
        "no analytics/signals/decisions",
        "Mac mini M2",
        "Windows-native",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_prompt_22_next_phase_doc_recommends_prompt_23_sequence() -> None:
    text = _read_doc("DATA_FOUNDATION_MILESTONE_NEXT_PHASE.md")
    required = [
        "Prompt 28 - Returns and Rolling Window Analytics v0",
        "Prompt 28 - Returns and Rolling Window Analytics v0",
        "Prompt 28 - Returns and Rolling Window Analytics v0",
        "Prompt 29 - Volatility and Drawdown Analytics v0",
        "Prompt 34 - Regime Feature Preparation Contracts",
    ]
    for phrase in required:
        assert phrase in text
