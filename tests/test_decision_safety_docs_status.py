from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_decision_safety_docs_exist_and_state_boundaries() -> None:
    required_docs = [
        "docs/DECISION_SAFETY_GUARDRAILS.md",
        "docs/DECISION_HUMAN_REVIEW_GATES.md",
        "docs/DECISION_APPROVAL_PLACEHOLDERS.md",
        "docs/DECISION_OVERRIDE_PROHIBITION.md",
        "docs/DECISION_BLOCKED_OUTPUT_POLICY.md",
        "docs/DECISION_SAFETY_READINESS_POLICY.md",
    ]
    for path in required_docs:
        assert (ROOT / path).exists()

    docs_text = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in required_docs)
    for phrase in [
        "Decision Safety",
        "human-review gates",
        "approval placeholders",
        "override prohibition",
        "blocked output policy",
        "no approvals",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in docs_text


def test_decision_safety_status_docs_updated() -> None:
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 39 - Decision Safety and Human-Review Guardrails" in prompt_log
    assert "Current Prompt: 40" in north_star
    assert "Decision Safety and Human-Review Guardrails" in project_map
    assert "packages/core/stark_terminal_core/decision_safety/" in project_map
