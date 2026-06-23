from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

AUDIT_DOCS = [
    "docs/DECISION_DESK_MILESTONE_AUDIT.md",
    "docs/DECISION_DESK_BOUNDARY_AUDIT.md",
    "docs/DECISION_EVIDENCE_BOUNDARY_AUDIT.md",
    "docs/DECISION_SAFETY_BOUNDARY_AUDIT.md",
    "docs/DECISION_API_SKELETON_AUDIT.md",
    "docs/DECISION_NO_RECOMMENDATION_AUDIT.md",
    "docs/DECISION_DESK_NEXT_PHASE_PLAN.md",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_41_audit_docs_exist() -> None:
    for path in AUDIT_DOCS:
        assert (ROOT / path).exists(), path


def test_prompt_41_audit_docs_cover_decision_desk_milestone_boundaries() -> None:
    text = "\n".join(_read(path) for path in AUDIT_DOCS)

    for phrase in [
        "Prompts 36-40",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObject generation",
        "no approvals",
        "no overrides",
        "no execution APIs",
        "unavailable-by-default",
        "Decision Desk Readiness API Skeleton",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_prompt_41_status_docs_are_current() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    project_map = _read("PROJECT_MAP.md")

    assert "Current Prompt: 44" in north_star
    assert "Completed Prompts: 42 after completion" in north_star
    assert "Decision Desk Milestone Audit completed" in north_star
    assert "## Prompt 41 - Decision Desk Milestone Audit" in prompt_log
    assert "Prompt 41 Decision Desk Milestone Audit" in project_map

