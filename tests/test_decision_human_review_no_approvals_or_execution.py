from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_decision_human_review_modules_do_not_generate_approvals_or_execution() -> None:
    module_root = ROOT / "packages/core/stark_terminal_core/decision_human_review"
    route_path = ROOT / "apps/api/stark_terminal_api/routes/decision_human_review.py"
    text = "\n".join(path.read_text(encoding="utf-8") for path in module_root.glob("*.py"))
    text += "\n" + route_path.read_text(encoding="utf-8")

    forbidden = [
        "def approve_decision",
        "def override_decision",
        "def assign_review_task",
        "def authenticate_reviewer",
        "def send_review_notification",
        "def generate_decision_object",
        "def generate_recommendation",
        "def generate_action",
        "def generate_readiness_status",
        "def score_confidence",
        "def compute_confidence",
        "DecisionObject(",
        "@router.post",
    ]
    for phrase in forbidden:
        assert phrase not in text


def test_decision_human_review_routes_and_docs_forbid_active_review_behavior() -> None:
    route_text = (ROOT / "apps/api/stark_terminal_api/routes/decision_human_review.py").read_text(
        encoding="utf-8"
    )
    docs_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            ROOT / "docs/DECISION_HUMAN_REVIEW_WORKFLOW_SKELETON.md",
            ROOT / "docs/DECISION_REVIEW_NO_APPROVAL_POLICY.md",
            ROOT / "docs/API_SURFACE_INVENTORY.md",
        ]
    )

    assert "/decision-human-review" in route_text
    assert "active_workflow_allowed_now" in route_text
    assert "task_assignment_allowed_now" in route_text
    assert "reviewer_auth_allowed_now" in route_text
    assert "notifications_allowed_now" in route_text
    assert "approval_allowed_now" in route_text
    assert "override_allowed_now" in route_text
    assert "execution_allowed_now" in route_text
    assert "no active workflow" in docs_text
    assert "no task assignment" in docs_text
    assert "no reviewer auth" in docs_text
    assert "no notifications" in docs_text
    assert "no approvals" in docs_text
    assert "no overrides" in docs_text
    assert "no DecisionObject generation" in docs_text
    assert "no execution APIs" in docs_text
    assert "/approve" not in route_text.lower()
    assert "/override" not in route_text.lower()
    assert "buy/sell/hold/watch/avoid" not in route_text.lower()
