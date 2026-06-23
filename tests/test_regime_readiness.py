import pytest

from stark_terminal_analytics.regime.contracts import default_regime_analytics_plan
from stark_terminal_analytics.regime.evidence import (
    build_regime_evidence_checklist,
    default_regime_evidence_requirements,
)
from stark_terminal_analytics.regime.readiness import (
    RegimeReadinessReport,
    build_regime_readiness_report,
    regime_ready_for_classification,
    regime_ready_for_feature_preparation,
    regime_ready_for_production,
)
from stark_terminal_analytics.regime.safety import default_regime_safety_policy, evaluate_regime_plan_safety


def test_readiness_report_defaults_block_classification_and_production() -> None:
    plan = default_regime_analytics_plan()
    checklist = build_regime_evidence_checklist()
    safety = evaluate_regime_plan_safety(plan, default_regime_safety_policy())
    report = build_regime_readiness_report(plan, checklist, safety)

    assert report.ready_for_feature_preparation is False
    assert report.ready_for_classification is False
    assert report.ready_for_production is False
    assert report.blockers
    assert regime_ready_for_feature_preparation(report) is False
    assert regime_ready_for_classification(report) is False
    assert regime_ready_for_production(report) is False


def test_complete_evidence_can_make_feature_preparation_ready_only() -> None:
    plan = default_regime_analytics_plan()
    requirements = default_regime_evidence_requirements()
    completed = {requirement.requirement_id for requirement in requirements}
    checklist = build_regime_evidence_checklist(requirements=requirements, completed_requirement_ids=completed)
    safety = evaluate_regime_plan_safety(plan, default_regime_safety_policy())

    report = build_regime_readiness_report(plan, checklist, safety)

    assert report.ready_for_feature_preparation is True
    assert report.ready_for_classification is False
    assert report.ready_for_production is False


@pytest.mark.parametrize(
    "override",
    [
        {"ready_for_classification": True},
        {"ready_for_production": True},
        {"ready_for_feature_preparation": True, "evidence_complete": False},
        {"ready_for_feature_preparation": True, "blockers": ["missing evidence"]},
    ],
)
def test_readiness_report_rejects_unsafe_readiness(override: dict[str, object]) -> None:
    data = {
        "report_id": "report",
        "plan_id": "plan",
        "planning_stage": default_regime_analytics_plan().stage,
        "evidence_complete": True,
        "safety_decision": "planning_allowed",
    }
    data.update(override)

    with pytest.raises(ValueError):
        RegimeReadinessReport(**data)
