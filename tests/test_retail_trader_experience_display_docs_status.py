from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DISPLAY_DOCS = [
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_CONTRACT_SKELETON.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_PERSONA_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_JOURNEY_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_SECTION_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_WIDGET_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_UNAVAILABLE_RESPONSES.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_SAFETY_BOUNDARY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_EXECUTION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_SUITABILITY_PROFILING_POLICY.md",
]


def test_retail_trader_experience_display_docs_exist_and_state_boundaries() -> None:
    combined = ""
    for relative_path in DISPLAY_DOCS:
        path = ROOT / relative_path
        assert path.exists(), relative_path
        combined += "\n" + path.read_text(encoding="utf-8")

    required = [
        "Retail Trader Experience Display",
        "display contract skeleton",
        "display-contract-skeleton-only",
        "unavailable by default",
        "no active UI",
        "no frontend components",
        "no desktop components",
        "no recommendation",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no readiness-to-trade",
        "no broker controls",
        "no suitability profiling",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]
    lowered = combined.lower()
    missing = [phrase for phrase in required if phrase.lower() not in lowered]
    assert not missing


def test_retail_trader_experience_display_status_docs_are_current() -> None:
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
    readiness_plan = (ROOT / "docs/RETAIL_TRADER_EXPERIENCE_READINESS_PLAN.md").read_text(
        encoding="utf-8"
    )

    assert "Prompt 58 - Retail Trader Experience Display Contract Skeleton" in prompt_log
    assert "Current Prompt: 60" in north_star
    assert "Completed Prompts: 61 after completion" in north_star
    assert "Retail Trader Experience Display Contract Skeleton" in project_map
    assert "Prompt 59 - Retail Trader Experience Safety Boundary Audit" in next_phase
    assert "Ready for Retail Trader Experience Milestone Audit only" in readiness_plan
