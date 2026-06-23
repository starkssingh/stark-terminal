from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOCS = [
    ROOT / "docs/RETAIL_DASHBOARD_DISPLAY_CONTRACT_SKELETON.md",
    ROOT / "docs/RETAIL_DASHBOARD_LAYOUT_PLACEHOLDERS.md",
    ROOT / "docs/RETAIL_DASHBOARD_WIDGET_PLACEHOLDERS.md",
    ROOT / "docs/RETAIL_DASHBOARD_VISUAL_SECTION_PLACEHOLDERS.md",
    ROOT / "docs/RETAIL_DASHBOARD_DISPLAY_UNAVAILABLE_RESPONSES.md",
    ROOT / "docs/RETAIL_DASHBOARD_DISPLAY_SAFETY_BOUNDARY.md",
    ROOT / "docs/RETAIL_DASHBOARD_DISPLAY_NO_RECOMMENDATION_POLICY.md",
    ROOT / "docs/RETAIL_DASHBOARD_DISPLAY_NO_EXECUTION_POLICY.md",
]


def test_retail_dashboard_display_docs_exist_and_state_boundaries() -> None:
    for path in DOCS:
        assert path.exists(), path

    docs_text = "\n".join(path.read_text(encoding="utf-8") for path in DOCS)
    for phrase in [
        "Retail Dashboard Display",
        "display contract skeleton",
        "unavailable by default",
        "no active UI",
        "no frontend component",
        "no desktop UI component",
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
        assert phrase in docs_text


def test_prompt_51_status_docs_are_updated() -> None:
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 51 - Retail Dashboard Display Contract Skeleton" in prompt_log
    assert "Current Prompt: 54" in north_star
    assert "Completed Prompts: 55 after completion" in north_star
    assert "Retail Dashboard Display Contract Skeleton" in project_map
