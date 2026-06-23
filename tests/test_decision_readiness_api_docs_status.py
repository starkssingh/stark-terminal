from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_decision_readiness_api_docs_exist_and_forbid_recommendations() -> None:
    docs = [
        ROOT / "docs/DECISION_DESK_READINESS_API_SKELETON.md",
        ROOT / "docs/DECISION_READINESS_REQUEST_RESPONSE_PLACEHOLDERS.md",
        ROOT / "docs/DECISION_READINESS_REFERENCE_PLACEHOLDERS.md",
        ROOT / "docs/DECISION_READINESS_UNAVAILABLE_RESPONSES.md",
        ROOT / "docs/DECISION_READINESS_API_SAFETY_BOUNDARY.md",
        ROOT / "docs/DECISION_READINESS_NO_RECOMMENDATION_POLICY.md",
    ]

    for path in docs:
        assert path.exists(), f"missing {path}"

    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs)
    required_phrases = [
        "Decision Desk Readiness API",
        "readiness contract skeleton",
        "request placeholder",
        "response placeholder",
        "reference placeholder",
        "unavailable response",
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
        assert phrase in combined


def test_prompt_42_status_docs_updated() -> None:
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 42" in prompt_log
    assert "Current Prompt: 44" in north_star
    assert "Decision Desk Readiness API Skeleton" in project_map
