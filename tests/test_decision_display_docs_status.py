from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_decision_display_docs_exist_and_state_boundaries() -> None:
    required_docs = [
        "docs/DECISION_DESK_DISPLAY_CONTRACT_SKELETON.md",
        "docs/DECISION_DISPLAY_CARD_PLACEHOLDERS.md",
        "docs/DECISION_DISPLAY_SECTION_PLACEHOLDERS.md",
        "docs/DECISION_DISPLAY_UNAVAILABLE_RESPONSES.md",
        "docs/DECISION_DISPLAY_SAFETY_BOUNDARY.md",
        "docs/DECISION_DISPLAY_NO_RECOMMENDATION_POLICY.md",
    ]

    for path in required_docs:
        assert (ROOT / path).exists()

    docs_text = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in required_docs)
    required_phrases = [
        "Decision Desk Display",
        "display contract skeleton",
        "card placeholder",
        "section placeholder",
        "unavailable display",
        "no active UI",
        "no readiness-to-trade",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no approval",
        "no override",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]
    for phrase in required_phrases:
        assert phrase in docs_text


def test_decision_display_status_docs_updated() -> None:
    assert "Prompt 43" in (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Current Prompt: 44" in north_star
    assert "Decision Desk Display Contract Skeleton" in north_star
    assert "Decision Desk Display Contract Skeleton" in project_map

