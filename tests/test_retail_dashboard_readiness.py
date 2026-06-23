from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard.cards import default_retail_dashboard_card_placeholders
from stark_terminal_core.retail_dashboard.interactions import default_retail_dashboard_forbidden_interactions
from stark_terminal_core.retail_dashboard.planning import default_retail_dashboard_planning_contract
from stark_terminal_core.retail_dashboard.readiness import (
    RetailDashboardReadinessReport,
    build_retail_dashboard_readiness_report,
    retail_dashboard_ready_for_active_ui,
    retail_dashboard_ready_for_execution,
    retail_dashboard_ready_for_recommendations,
)
from stark_terminal_core.retail_dashboard.safety import (
    default_retail_dashboard_safety_policy,
    evaluate_retail_dashboard_plan_safety,
)
from stark_terminal_core.retail_dashboard.sections import default_retail_dashboard_section_placeholders


def _report() -> RetailDashboardReadinessReport:
    plan = default_retail_dashboard_planning_contract()
    sections = default_retail_dashboard_section_placeholders()
    cards = default_retail_dashboard_card_placeholders()
    interactions = default_retail_dashboard_forbidden_interactions()
    safety = evaluate_retail_dashboard_plan_safety(plan, default_retail_dashboard_safety_policy())
    return build_retail_dashboard_readiness_report(plan, sections, cards, interactions, safety)


def test_retail_dashboard_readiness_report_validates() -> None:
    report = _report()

    assert report.section_count > 0
    assert report.card_count > 0
    assert report.forbidden_interaction_count > 0
    assert report.ready_for_active_ui is False
    assert report.ready_for_recommendations is False
    assert report.ready_for_execution is False
    assert report.ready_for_broker_controls is False
    assert report.ready_for_readiness_to_trade is False
    assert retail_dashboard_ready_for_active_ui(report) is False
    assert retail_dashboard_ready_for_recommendations(report) is False
    assert retail_dashboard_ready_for_execution(report) is False


@pytest.mark.parametrize(
    "field_name",
    [
        "ready_for_active_ui",
        "ready_for_recommendations",
        "ready_for_action_generation",
        "ready_for_confidence_scoring",
        "ready_for_decision_objects",
        "ready_for_readiness_to_trade",
        "ready_for_broker_controls",
        "ready_for_execution",
    ],
)
def test_retail_dashboard_readiness_report_rejects_dangerous_readiness(field_name: str) -> None:
    data = _report().model_dump()
    data[field_name] = True

    with pytest.raises(ValidationError):
        RetailDashboardReadinessReport(**data)


def test_retail_dashboard_readiness_report_records_blockers() -> None:
    plan = default_retail_dashboard_planning_contract()
    sections = default_retail_dashboard_section_placeholders()
    cards = default_retail_dashboard_card_placeholders()
    interactions = default_retail_dashboard_forbidden_interactions()
    plan_data = plan.model_dump()
    plan_data["execution_allowed"] = True
    safety = evaluate_retail_dashboard_plan_safety(
        plan.model_construct(**plan_data),
        default_retail_dashboard_safety_policy(),
    )
    report = build_retail_dashboard_readiness_report(plan, sections, cards, interactions, safety)

    assert report.safety_result_safe is False
    assert report.blockers
    assert report.ready_for_api_contract_skeleton is False
    assert report.ready_for_display_contract_skeleton is False
