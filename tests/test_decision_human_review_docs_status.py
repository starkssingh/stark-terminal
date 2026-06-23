from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_decision_human_review_docs_exist_and_state_boundaries() -> None:
    required_docs = [
        "docs/DECISION_HUMAN_REVIEW_WORKFLOW_SKELETON.md",
        "docs/DECISION_REVIEW_TASK_PLACEHOLDERS.md",
        "docs/DECISION_REVIEW_ROLE_PLACEHOLDERS.md",
        "docs/DECISION_REVIEW_QUEUE_PLACEHOLDERS.md",
        "docs/DECISION_REVIEW_UNAVAILABLE_RESPONSES.md",
        "docs/DECISION_REVIEW_NO_APPROVAL_POLICY.md",
    ]
    for doc in required_docs:
        assert (ROOT / doc).exists()

    docs_text = "\n".join((ROOT / doc).read_text(encoding="utf-8") for doc in required_docs)
    for phrase in [
        "Decision Human Review",
        "workflow skeleton",
        "task placeholder",
        "role placeholder",
        "queue placeholder",
        "unavailable",
        "no active workflow",
        "no task assignment",
        "no reviewer auth",
        "no notifications",
        "no approvals",
        "no overrides",
        "no recommendations",
        "no confidence scoring",
        "no action generation",
        "no active DecisionObject generation",
        "no readiness-to-trade",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in docs_text


def test_decision_human_review_status_docs_are_updated() -> None:
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 45 - Decision Desk Human Review Workflow Skeleton" in prompt_log
    assert "Current Prompt: 45" in north_star
    assert "Decision Desk Human Review Workflow Skeleton" in north_star
    assert "decision_human_review" in project_map
    assert "Decision Human Review workflow skeleton" in project_map
