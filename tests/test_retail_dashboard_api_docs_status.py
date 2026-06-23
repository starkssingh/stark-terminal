from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_retail_dashboard_api_docs_exist_and_state_boundaries() -> None:
    docs = [
        "docs/RETAIL_DASHBOARD_API_CONTRACT_SKELETON.md",
        "docs/RETAIL_DASHBOARD_API_REQUEST_RESPONSE_PLACEHOLDERS.md",
        "docs/RETAIL_DASHBOARD_API_REFERENCE_PLACEHOLDERS.md",
        "docs/RETAIL_DASHBOARD_API_UNAVAILABLE_RESPONSES.md",
        "docs/RETAIL_DASHBOARD_API_SAFETY_BOUNDARY.md",
        "docs/RETAIL_DASHBOARD_API_NO_RECOMMENDATION_POLICY.md",
        "docs/RETAIL_DASHBOARD_API_NO_EXECUTION_POLICY.md",
    ]
    combined = "\n".join(_read(path) for path in docs)

    for path in docs:
        assert (ROOT / path).exists()
    for phrase in [
        "Retail Dashboard API",
        "API contract skeleton",
        "unavailable by default",
        "no active UI",
        "no recommendation cards",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no readiness-to-trade",
        "no broker controls",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in combined


def test_prompt_50_status_docs_are_updated() -> None:
    prompt_log = _read("docs/PROMPT_LOG.md")
    north_star = _read("docs/NORTH_STAR.md")
    project_map = _read("PROJECT_MAP.md")

    assert "Prompt 50 - Retail Dashboard API Contract Skeleton" in prompt_log
    assert "Historical verifier reference: Current Prompt: 50" in north_star
    assert "Retail Dashboard API Contract Skeleton" in project_map
    assert "retail_dashboard_api" in project_map
