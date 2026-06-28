from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT_69_DOCS = [
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_BOUNDARY_INTEGRATION_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_INTEGRATION_NO_ACTIVE_UI_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_INTEGRATION_NO_PAPER_PARSING_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_INTEGRATION_NO_STRATEGY_BACKTEST_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_INTEGRATION_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_READINESS_PLAN.md",
]


def test_strategy_research_workspace_api_display_integration_docs_exist() -> None:
    for doc in PROMPT_69_DOCS:
        assert (ROOT / doc).exists(), doc


def test_strategy_research_workspace_api_display_integration_docs_contain_required_language() -> None:
    text = "\n".join((ROOT / doc).read_text(encoding="utf-8") for doc in PROMPT_69_DOCS)
    for phrase in [
        "Prompts 63-68",
        "no active UI",
        "no paper ingestion",
        "no paper parsing",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendation generation",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no broker controls",
        "no readiness-to-trade",
        "no execution APIs",
        "Research Artifact Registry Planning and Guardrails only",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_prompt_69_status_docs_are_updated() -> None:
    assert "Prompt 69 - Strategy Research Workspace API/Display Integration Readiness Audit" in (
        ROOT / "docs/PROMPT_LOG.md"
    ).read_text(encoding="utf-8")
    assert "Current Prompt: 78" in (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    assert "Strategy Research Workspace API/Display Integration Readiness Audit" in (
        ROOT / "PROJECT_MAP.md"
    ).read_text(encoding="utf-8")
