from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOCS = [
    "docs/RETAIL_DASHBOARD_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
    "docs/RETAIL_DASHBOARD_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md",
    "docs/RETAIL_DASHBOARD_API_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/RETAIL_DASHBOARD_BOUNDARY_INTEGRATION_AUDIT.md",
    "docs/RETAIL_DASHBOARD_INTEGRATION_NO_ACTIVE_UI_AUDIT.md",
    "docs/RETAIL_DASHBOARD_INTEGRATION_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_READINESS_PLAN.md",
]


def test_retail_dashboard_api_display_integration_docs_exist() -> None:
    for doc in DOCS:
        assert (ROOT / doc).exists()


def test_retail_dashboard_api_display_integration_docs_contain_required_language() -> None:
    text = "\n".join((ROOT / doc).read_text(encoding="utf-8") for doc in DOCS)
    for phrase in [
        "Prompts 49-54",
        "no active UI",
        "no frontend implementation",
        "no desktop implementation",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no broker controls",
        "no readiness-to-trade",
        "no execution APIs",
        "Retail Trader Experience Planning and Guardrails only",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_prompt_55_status_docs_are_updated() -> None:
    assert "Prompt 55 - Retail Dashboard API/Display Integration Readiness Audit" in (
        ROOT / "docs/PROMPT_LOG.md"
    ).read_text(encoding="utf-8")
    assert "Current Prompt: 60" in (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    assert "Retail Dashboard API/Display Integration Readiness Audit" in (
        ROOT / "PROJECT_MAP.md"
    ).read_text(encoding="utf-8")
