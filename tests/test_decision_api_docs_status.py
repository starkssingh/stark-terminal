from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_decision_api_docs_exist_and_state_boundaries() -> None:
    required_docs = [
        "docs/DECISION_DESK_API_CONTRACT_SKELETON.md",
        "docs/DECISION_DESK_REQUEST_RESPONSE_PLACEHOLDERS.md",
        "docs/DECISION_DESK_UNAVAILABLE_RESPONSES.md",
        "docs/DECISION_DESK_API_SAFETY_BOUNDARY.md",
        "docs/DECISION_DESK_API_NO_RECOMMENDATION_POLICY.md",
    ]
    for path in required_docs:
        assert (ROOT / path).exists()

    docs_text = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in required_docs)
    for phrase in [
        "Decision Desk API",
        "contract skeleton",
        "request placeholder",
        "response placeholder",
        "unavailable response",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no approval",
        "no override",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in docs_text


def test_decision_api_status_docs_updated() -> None:
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 40 - Decision Desk API Contract Skeleton" in prompt_log
    assert "Current Prompt: 40" in north_star
    assert "Decision Desk API Contract Skeleton" in project_map
    assert "packages/core/stark_terminal_core/decision_api/" in project_map

