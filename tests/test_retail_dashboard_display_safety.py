from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_display.contracts import default_retail_dashboard_display_contract_metadata
from stark_terminal_core.retail_dashboard_display.layouts import (
    RetailDashboardLayoutPlaceholder,
    default_retail_dashboard_layout_placeholders,
)
from stark_terminal_core.retail_dashboard_display.safety import (
    RetailDashboardDisplaySafetyPolicy,
    default_retail_dashboard_display_safety_policy,
    evaluate_retail_dashboard_display_contract_safety,
    evaluate_retail_dashboard_layouts_safety,
    evaluate_retail_dashboard_widgets_safety,
    reject_display_as_active_ui,
    reject_display_as_execution_surface,
    reject_display_as_recommendation,
)
from stark_terminal_core.retail_dashboard_display.widgets import (
    RetailDashboardWidgetPlaceholder,
    default_retail_dashboard_widget_placeholders,
)


def test_default_retail_dashboard_display_safety_policy_is_fail_closed() -> None:
    policy = default_retail_dashboard_display_safety_policy()

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
    assert policy.require_display_contract_only is True


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
def test_retail_dashboard_display_safety_policy_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        RetailDashboardDisplaySafetyPolicy(
            policy_id="retail-dashboard-display-safety-test",
            name="Retail Dashboard Display Safety Test",
            **{field_name: True},
        )


def test_retail_dashboard_display_contract_safety_passes_for_default_contract() -> None:
    policy = default_retail_dashboard_display_safety_policy()
    result = evaluate_retail_dashboard_display_contract_safety(
        default_retail_dashboard_display_contract_metadata(),
        policy,
    )

    assert result.safe is True
    assert result.display_contract_only is True
    assert result.execution_allowed is False


def test_retail_dashboard_display_layout_safety_rejects_unsafe_layout_without_mutating_inputs() -> None:
    policy = default_retail_dashboard_display_safety_policy()
    unsafe_layout = RetailDashboardLayoutPlaceholder.model_construct(
        layout_id="unsafe-layout",
        layout_kind=default_retail_dashboard_layout_placeholders()[0].layout_kind,
        title="Unsafe",
        description="Unsafe",
        active_ui=True,
        rendered_now=True,
        unavailable=False,
        display_contract_only=False,
        recommendations_allowed=True,
        action_generation_allowed=False,
        confidence_scoring_allowed=False,
        decision_object_generation_allowed=False,
        readiness_to_trade_allowed=True,
        broker_controls_allowed=True,
        execution_allowed=True,
        schema_version="v1",
        notes=[],
    )
    result = evaluate_retail_dashboard_layouts_safety([unsafe_layout], policy)

    assert result.safe is False
    assert unsafe_layout.active_ui is True
    assert result.execution_allowed is False


def test_retail_dashboard_display_widget_safety_rejects_unsafe_widget_without_mutating_inputs() -> None:
    policy = default_retail_dashboard_display_safety_policy()
    unsafe_widget = RetailDashboardWidgetPlaceholder.model_construct(
        widget_id="unsafe-widget",
        widget_kind=default_retail_dashboard_widget_placeholders()[0].widget_kind,
        title="Unsafe",
        description="Unsafe",
        active_ui=True,
        rendered_now=True,
        unavailable=False,
        display_contract_only=False,
        recommendation_widget=True,
        action_widget=True,
        confidence_widget=True,
        decision_object_widget=True,
        readiness_to_trade_widget=True,
        broker_control_widget=True,
        execution_widget=True,
        approval_widget=True,
        override_widget=True,
        schema_version="v1",
        notes=[],
    )
    result = evaluate_retail_dashboard_widgets_safety([unsafe_widget], policy)

    assert result.safe is False
    assert unsafe_widget.recommendation_widget is True
    assert result.execution_allowed is False


def test_retail_dashboard_display_rejection_helpers_return_blocking_results() -> None:
    for result in [
        reject_display_as_active_ui(),
        reject_display_as_recommendation(),
        reject_display_as_execution_surface(),
    ]:
        assert result.safe is False
        assert result.display_contract_only is True
        assert result.active_ui_allowed is False
        assert result.recommendations_allowed is False
        assert result.broker_controls_allowed is False
        assert result.execution_allowed is False
