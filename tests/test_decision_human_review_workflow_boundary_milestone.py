from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def test_decision_human_review_remains_workflow_skeleton_only() -> None:
    module_root = ROOT / "packages/core/stark_terminal_core/decision_human_review"
    route = ROOT / "apps/api/stark_terminal_api/routes/decision_human_review.py"
    text = "\n".join(path.read_text(encoding="utf-8") for path in module_root.glob("*.py"))
    text += "\n" + route.read_text(encoding="utf-8")

    for phrase in [
        "@router.post",
        "def assign_review_task",
        "def authenticate_reviewer",
        "def send_review_notification",
        "def approve_decision",
        "def override_decision",
        "def generate_recommendation",
        "def generate_decision_object",
        "DecisionObject(",
    ]:
        assert phrase not in text


def test_decision_human_review_placeholder_workflow_has_no_active_behavior() -> None:
    placeholder = client.get("/decision-human-review/placeholder-workflow").json()

    assert placeholder["workflow_skeleton_only"] is True
    assert placeholder["workflow_active"] is False
    assert placeholder["task_assignment_allowed"] is False
    assert placeholder["reviewer_auth_allowed"] is False
    assert placeholder["notifications_allowed"] is False
    assert placeholder["approval_granted"] is False
    assert placeholder["override_granted"] is False
    assert placeholder["recommendation_generated"] is False
    assert placeholder["decision_object_generated"] is False
    assert placeholder["readiness_to_trade_generated"] is False
    assert placeholder["execution_ready"] is False
