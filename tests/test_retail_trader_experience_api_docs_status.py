from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
    "docs/RETAIL_TRADER_EXPERIENCE_API_CONTRACT_SKELETON.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_REFERENCE_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_UNAVAILABLE_RESPONSES.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_SAFETY_BOUNDARY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_NO_EXECUTION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_NO_SUITABILITY_PROFILING_POLICY.md",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_retail_trader_experience_api_docs_exist_and_state_boundaries() -> None:
    combined = ""
    for relative_path in REQUIRED_DOCS:
        path = ROOT / relative_path
        assert path.exists(), relative_path
        combined += path.read_text(encoding="utf-8") + "\n"

    for phrase in [
        "Retail Trader Experience API",
        "API contract skeleton",
        "unavailable by default",
        "no active UI",
        "no frontend components",
        "no desktop components",
        "no recommendation cards",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no readiness-to-trade",
        "no broker controls",
        "no suitability profiling",
        "no execution APIs",
    ]:
        assert phrase in combined


def test_retail_trader_experience_api_status_docs_are_updated() -> None:
    prompt_log = _read("docs/PROMPT_LOG.md")
    north_star = _read("docs/NORTH_STAR.md")
    project_map = _read("PROJECT_MAP.md")

    assert "Prompt 57 - Retail Trader Experience API Contract Skeleton" in prompt_log
    assert "Current Prompt: 60" in north_star
    assert "Retail Trader Experience API Contract Skeleton" in project_map
    assert "retail_trader_experience_api" in project_map
    assert "Prompt 58 - Retail Trader Experience Display Contract Skeleton" in _read("docs/NEXT_PHASE_PLAN.md")
