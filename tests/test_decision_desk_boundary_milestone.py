from __future__ import annotations

from pathlib import Path

from stark_terminal_core.decision_desk.action_placeholders import default_retail_action_placeholder_contracts
from stark_terminal_core.decision_desk.display import default_retail_display_boundary_contract
from stark_terminal_core.decision_desk.evidence import build_retail_decision_evidence_checklist
from stark_terminal_core.decision_desk.human_review import build_retail_human_review_checklist
from stark_terminal_core.decision_desk.planning import default_retail_decision_desk_plan


ROOT = Path(__file__).resolve().parents[1]


def _package_text() -> str:
    package_root = ROOT / "packages/core/stark_terminal_core/decision_desk"
    route = ROOT / "apps/api/stark_terminal_api/routes/decision_desk.py"
    return "\n".join(path.read_text(encoding="utf-8") for path in package_root.glob("*.py")) + route.read_text(
        encoding="utf-8",
    )


def test_decision_desk_package_remains_planning_only() -> None:
    plan = default_retail_decision_desk_plan()
    placeholders = default_retail_action_placeholder_contracts()
    evidence = build_retail_decision_evidence_checklist()
    review = build_retail_human_review_checklist()
    display = default_retail_display_boundary_contract()

    assert plan.recommendations_allowed is False
    assert plan.action_generation_allowed is False
    assert plan.confidence_scoring_allowed is False
    assert plan.decision_object_generation_allowed is False
    assert plan.execution_allowed is False
    assert plan.requires_human_review is True
    assert all(placeholder.planning_only for placeholder in placeholders)
    assert all(not placeholder.generated_now for placeholder in placeholders)
    assert evidence.recommendations_allowed is False
    assert evidence.action_generation_allowed is False
    assert evidence.decision_object_generation_allowed is False
    assert review.recommendations_allowed is False
    assert review.decision_objects_allowed is False
    assert review.execution_allowed is False
    assert display.planning_only is True
    assert display.recommendations_allowed is False
    assert display.confidence_scoring_allowed is False


def test_decision_desk_code_has_no_active_generation_functions() -> None:
    text = _package_text()
    for phrase in [
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def compute_confidence",
        "def create_decision_object",
        "DecisionObject(",
        "@router.post",
    ]:
        assert phrase not in text

