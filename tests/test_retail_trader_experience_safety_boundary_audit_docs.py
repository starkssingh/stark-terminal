from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT_59_DOCS = [
    "docs/RETAIL_TRADER_EXPERIENCE_SAFETY_BOUNDARY_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_BOUNDARY_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_ACTIVE_UI_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_RECOMMENDATION_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_EXECUTION_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_SUITABILITY_PROFILING_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_MILESTONE_READINESS.md",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_retail_trader_experience_safety_boundary_audit_docs_exist() -> None:
    for doc in PROMPT_59_DOCS:
        assert (ROOT / doc).exists(), doc


def test_safety_boundary_audit_docs_capture_prompt_56_to_58_scope() -> None:
    combined = "\n".join(_read(doc) for doc in PROMPT_59_DOCS).lower()

    for phrase in [
        "prompts 56-58",
        "retail trader experience planning and guardrails",
        "retail trader experience api contract skeleton",
        "retail trader experience display contract skeleton",
        "verification summary",
        "planning boundary verdict",
        "api boundary verdict",
        "display boundary verdict",
        "no-active-ui verdict",
        "no-recommendation verdict",
        "no-suitability-profiling verdict",
        "no-broker-control verdict",
        "no-execution verdict",
        "milestone-readiness verdict",
    ]:
        assert phrase in combined


def test_safety_boundary_audit_docs_state_all_forbidden_surfaces() -> None:
    combined = "\n".join(_read(doc) for doc in PROMPT_59_DOCS).lower()

    for phrase in [
        "no active ui",
        "no frontend implementation",
        "no desktop implementation",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "decisionobject generation",
        "no broker controls",
        "no readiness-to-trade",
        "no suitability profiling",
        "no execution apis",
    ]:
        assert phrase in combined


def test_milestone_readiness_doc_points_to_prompt_60_only() -> None:
    readiness = _read("docs/RETAIL_TRADER_EXPERIENCE_MILESTONE_READINESS.md")

    assert "Prompt 60 - Retail Trader Experience Milestone Audit" in readiness
    assert "Retail Trader Experience Milestone Audit only" in readiness
    assert "active retail trader experience ui is still not allowed" in readiness.lower()
    assert "recommendation cards are still not allowed" in readiness.lower()
    assert "suitability profiling is still not allowed" in readiness.lower()
    assert "broker controls are still not allowed" in readiness.lower()
