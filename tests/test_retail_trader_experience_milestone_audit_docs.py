from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

MILESTONE_DOCS = [
    "docs/RETAIL_TRADER_EXPERIENCE_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PLANNING_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_SAFETY_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PHASE_NO_ACTIVE_UI_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PHASE_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PHASE_NO_SUITABILITY_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NEXT_PHASE_PLAN.md",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_60_milestone_audit_docs_exist() -> None:
    for path in MILESTONE_DOCS:
        assert (ROOT / path).exists(), path


def test_prompt_60_milestone_audit_docs_capture_phase_boundaries() -> None:
    text = "\n".join(_read(path) for path in MILESTONE_DOCS)
    lower = text.lower()

    for phrase in [
        "prompts 56-59",
        "no active ui",
        "no frontend implementation",
        "no desktop implementation",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "active decisionobject generation",
        "no broker controls",
        "no readiness-to-trade",
        "no suitability profiling",
        "no execution apis",
    ]:
        assert phrase in lower


def test_prompt_60_status_docs_reflect_milestone_completion() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    project_map = _read("PROJECT_MAP.md")
    prompt_log = _read("docs/PROMPT_LOG.md")

    assert "Current Prompt: 60" in north_star
    assert "Completed Prompts: 61 after completion" in north_star
    assert "Retail Trader Experience Planning Phase - Milestone Audit completed" in north_star
    assert "Prompt 60 Retail Trader Experience Milestone Audit" in project_map
    assert "Prompt 60 - Retail Trader Experience Milestone Audit" in prompt_log
