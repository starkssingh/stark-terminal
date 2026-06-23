from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard.cards import RetailDashboardCardPlaceholder
from stark_terminal_core.retail_dashboard.planning import RetailDashboardPlanningContract, default_retail_dashboard_planning_contract
from stark_terminal_core.retail_dashboard.safety import (
    RetailDashboardSafetyPolicy,
    default_retail_dashboard_safety_policy,
    evaluate_retail_dashboard_cards_safety,
    evaluate_retail_dashboard_plan_safety,
    evaluate_retail_dashboard_sections_safety,
    reject_dashboard_as_active_ui,
    reject_dashboard_as_execution_surface,
    reject_dashboard_as_recommendation,
)
from stark_terminal_core.retail_dashboard.sections import RetailDashboardSectionPlaceholder


def test_default_retail_dashboard_safety_policy_forbids_dangerous_behavior() -> None:
    policy = default_retail_dashboard_safety_policy()

    assert policy.allow_active_ui is False
    assert policy.allow_recommendations is False
    assert policy.allow_action_generation is False
    assert policy.allow_confidence_scoring is False
    assert policy.allow_decision_object_generation is False
    assert policy.allow_readiness_to_trade is False
    assert policy.allow_broker_controls is False
    assert policy.allow_execution is False
    assert policy.allow_approval is False
    assert policy.allow_override is False
    assert policy.require_planning_only is True


@pytest.mark.parametrize(
    "field_name",
    [
        "allow_active_ui",
        "allow_recommendations",
        "allow_action_generation",
        "allow_confidence_scoring",
        "allow_decision_object_generation",
        "allow_readiness_to_trade",
        "allow_broker_controls",
        "allow_execution",
        "allow_approval",
        "allow_override",
    ],
)
def test_retail_dashboard_safety_policy_rejects_unsafe_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        RetailDashboardSafetyPolicy(
            policy_id="policy-test",
            name="Policy Test",
            **{field_name: True},
        )


def test_retail_dashboard_plan_safety_rejects_unsafe_plan() -> None:
    plan_data = default_retail_dashboard_planning_contract().model_dump()
    plan_data["recommendations_allowed"] = True
    unsafe_plan = RetailDashboardPlanningContract.model_construct(
        **plan_data,
    )
    result = evaluate_retail_dashboard_plan_safety(unsafe_plan, default_retail_dashboard_safety_policy())

    assert result.safe is False
    assert result.planning_only is True
    assert result.recommendations_allowed is False
    assert result.execution_allowed is False


def test_retail_dashboard_section_and_card_safety_reject_unsafe_placeholders() -> None:
    unsafe_section = RetailDashboardSectionPlaceholder.model_construct(
        section_id="section-unsafe",
        active_ui=True,
        unavailable=True,
        planning_only=True,
        recommendations_allowed=False,
        action_generation_allowed=False,
        confidence_scoring_allowed=False,
        decision_object_generation_allowed=False,
        readiness_to_trade_allowed=False,
        broker_controls_allowed=False,
        execution_allowed=False,
    )
    section_result = evaluate_retail_dashboard_sections_safety([unsafe_section], default_retail_dashboard_safety_policy())
    assert section_result.safe is False

    unsafe_card = RetailDashboardCardPlaceholder.model_construct(
        card_id="card-unsafe",
        active_ui=False,
        unavailable=True,
        planning_only=True,
        recommendation_card=True,
        action_card=False,
        confidence_display=False,
        decision_object_display=False,
        readiness_to_trade_display=False,
        broker_control=False,
        execution_control=False,
        approval_control=False,
        override_control=False,
    )
    card_result = evaluate_retail_dashboard_cards_safety([unsafe_card], default_retail_dashboard_safety_policy())
    assert card_result.safe is False


def test_retail_dashboard_reject_helpers_return_blocking_safe_results() -> None:
    for result in [
        reject_dashboard_as_recommendation(),
        reject_dashboard_as_execution_surface(),
        reject_dashboard_as_active_ui(),
    ]:
        assert result.safe is False
        assert result.planning_only is True
        assert result.active_ui_allowed is False
        assert result.recommendations_allowed is False
        assert result.execution_allowed is False
