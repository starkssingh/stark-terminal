from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_decision_display_and_human_review_do_not_create_active_ui_or_workflow() -> None:
    roots = [
        ROOT / "packages/core/stark_terminal_core/decision_display",
        ROOT / "packages/core/stark_terminal_core/decision_human_review",
        ROOT / "packages/core/stark_terminal_core/decision_boundary",
    ]
    forbidden = [
        "import pyside6",
        "from pyside6",
        "import react",
        "build_active_ui",
        "build_active_decision_card",
        "def assign_review_task",
        "def authenticate_reviewer",
        "def send_review_notification",
        "active_workflow: bool = true",
        "active_ui: bool = true",
        "task_assignment_allowed: bool = true",
        "reviewer_auth_allowed: bool = true",
        "notifications_allowed: bool = true",
    ]
    bad: list[str] = []
    for root in roots:
        for path in root.glob("*.py"):
            text = path.read_text(encoding="utf-8").lower()
            for phrase in forbidden:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")

    assert bad == []


def test_prompt_47_docs_explicitly_state_no_active_ui_or_workflow() -> None:
    docs_text = "\n".join(
        [
            (ROOT / "docs/DECISION_DESK_SYSTEM_BOUNDARY_HARDENING.md").read_text(encoding="utf-8"),
            (ROOT / "docs/DECISION_CROSS_MODULE_INVARIANTS.md").read_text(encoding="utf-8"),
            (ROOT / "docs/DECISION_MODULE_BOUNDARY_POLICY.md").read_text(encoding="utf-8"),
        ]
    )

    assert "no active UI" in docs_text
    assert "no active workflow" in docs_text
    assert "no task assignment" in docs_text
    assert "no reviewer auth" in docs_text
    assert "no notifications" in docs_text
