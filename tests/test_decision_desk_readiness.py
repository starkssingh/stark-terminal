import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_desk.evidence import build_retail_decision_evidence_checklist
from stark_terminal_core.decision_desk.human_review import build_retail_human_review_checklist
from stark_terminal_core.decision_desk.planning import RetailDecisionDeskStage, default_retail_decision_desk_plan
from stark_terminal_core.decision_desk.readiness import (
    RetailDecisionDeskReadinessReport,
    build_retail_decision_desk_readiness_report,
    retail_decision_desk_ready_for_decision_objects,
    retail_decision_desk_ready_for_display_contracts,
    retail_decision_desk_ready_for_evidence_bundle_contracts,
    retail_decision_desk_ready_for_execution,
    retail_decision_desk_ready_for_recommendations,
)
from stark_terminal_core.decision_desk.safety import (
    default_retail_decision_desk_safety_policy,
    evaluate_retail_decision_desk_plan_safety,
)


def test_readiness_report_with_missing_evidence_and_review_has_blockers() -> None:
    plan = default_retail_decision_desk_plan()
    policy = default_retail_decision_desk_safety_policy()
    safety = evaluate_retail_decision_desk_plan_safety(plan, policy)

    report = build_retail_decision_desk_readiness_report(
        plan,
        build_retail_decision_evidence_checklist(),
        build_retail_human_review_checklist(),
        safety,
    )

    assert report.evidence_complete is False
    assert report.human_review_complete is False
    assert report.blockers
    assert retail_decision_desk_ready_for_display_contracts(report) is False
    assert retail_decision_desk_ready_for_evidence_bundle_contracts(report) is False
    assert retail_decision_desk_ready_for_recommendations(report) is False
    assert retail_decision_desk_ready_for_decision_objects(report) is False
    assert retail_decision_desk_ready_for_execution(report) is False


@pytest.mark.parametrize(
    "override",
    [
        {"ready_for_recommendations": True},
        {"ready_for_confidence_scoring": True},
        {"ready_for_decision_objects": True},
        {"ready_for_execution": True},
        {"ready_for_display_contracts": True, "blockers": ["blocked"]},
        {"ready_for_evidence_bundle_contracts": True, "blockers": ["blocked"]},
    ],
)
def test_readiness_report_rejects_unsafe_readiness(override: dict[str, object]) -> None:
    kwargs = {
        "report_id": "readiness-test",
        "plan_id": "plan-test",
        "planning_stage": RetailDecisionDeskStage.PLANNING_ONLY,
        "evidence_complete": False,
        "human_review_complete": False,
        "safety_decision": "blocked",
        **override,
    }

    with pytest.raises(ValidationError):
        RetailDecisionDeskReadinessReport(**kwargs)
