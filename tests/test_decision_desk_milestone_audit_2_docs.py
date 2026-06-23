from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

AUDIT_DOCS = [
    "docs/DECISION_DESK_MILESTONE_AUDIT_2.md",
    "docs/DECISION_READINESS_API_BOUNDARY_AUDIT.md",
    "docs/DECISION_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/DECISION_EVIDENCE_VALIDATION_BOUNDARY_AUDIT.md",
    "docs/DECISION_HUMAN_REVIEW_WORKFLOW_BOUNDARY_AUDIT.md",
    "docs/DECISION_NO_APPROVAL_WORKFLOW_AUDIT.md",
    "docs/DECISION_DESK_NEXT_PHASE_PLAN_2.md",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_46_audit_docs_exist() -> None:
    for path in AUDIT_DOCS:
        assert (ROOT / path).exists(), path


def test_prompt_46_audit_docs_cover_second_skeleton_phase_boundaries() -> None:
    text = "\n".join(_read(path) for path in AUDIT_DOCS)

    for phrase in [
        "Prompts 42-45",
        "Decision Desk Readiness API Skeleton",
        "Decision Desk Display Contract Skeleton",
        "Decision Evidence Bundle Validation v0",
        "Decision Human Review Workflow Skeleton",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no approvals",
        "no overrides",
        "no active workflow",
        "no active UI",
        "no readiness-to-trade",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_prompt_46_status_docs_are_current() -> None:
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    project_map = _read("PROJECT_MAP.md")

    assert "Current Prompt: 46" in north_star
    assert "Decision Desk Milestone Audit 2 completed" in north_star
    assert "Prompt 47 - Decision Desk System Boundary Hardening" in prompt_log
    assert "Prompt 46 Decision Desk Milestone Audit 2" in project_map
