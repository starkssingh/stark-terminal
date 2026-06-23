from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_boundary.forbidden import (
    REQUIRED_RETAIL_DASHBOARD_FORBIDDEN_BEHAVIORS,
    RetailDashboardBoundarySeverity,
    RetailDashboardForbiddenBehavior,
    RetailDashboardForbiddenBehaviorKind,
    RetailDashboardForbiddenBehaviorRegistry,
    default_retail_dashboard_forbidden_behavior_registry,
    default_retail_dashboard_forbidden_behaviors,
)


def _behavior(**overrides: object) -> RetailDashboardForbiddenBehavior:
    data = {
        "behavior_id": "behavior-test",
        "kind": RetailDashboardForbiddenBehaviorKind.ACTIVE_UI,
        "name": "Active UI",
        "description": "Active dashboard UI remains forbidden.",
    }
    data.update(overrides)
    return RetailDashboardForbiddenBehavior(**data)


def test_default_retail_dashboard_forbidden_behavior_registry_validates() -> None:
    registry = default_retail_dashboard_forbidden_behavior_registry()

    assert registry.complete is True
    assert REQUIRED_RETAIL_DASHBOARD_FORBIDDEN_BEHAVIORS.issubset(
        {behavior.kind for behavior in registry.behaviors}
    )
    assert registry.active_ui_allowed is False
    assert registry.frontend_components_allowed is False
    assert registry.desktop_components_allowed is False
    assert registry.recommendations_allowed is False
    assert registry.action_generation_allowed is False
    assert registry.confidence_scoring_allowed is False
    assert registry.decision_object_generation_allowed is False
    assert registry.readiness_to_trade_allowed is False
    assert registry.broker_controls_allowed is False
    assert registry.execution_allowed is False
    assert registry.approval_allowed is False
    assert registry.override_allowed is False


@pytest.mark.parametrize(
    "kind",
    [
        RetailDashboardForbiddenBehaviorKind.ACTIVE_UI,
        RetailDashboardForbiddenBehaviorKind.FRONTEND_COMPONENT,
        RetailDashboardForbiddenBehaviorKind.DESKTOP_COMPONENT,
        RetailDashboardForbiddenBehaviorKind.RECOMMENDATION_CARD,
        RetailDashboardForbiddenBehaviorKind.ACTION_BUTTON,
        RetailDashboardForbiddenBehaviorKind.CONFIDENCE_SCORE,
        RetailDashboardForbiddenBehaviorKind.DECISION_OBJECT_DISPLAY,
        RetailDashboardForbiddenBehaviorKind.READINESS_TO_TRADE,
        RetailDashboardForbiddenBehaviorKind.BROKER_CONTROL,
        RetailDashboardForbiddenBehaviorKind.ORDER_BUTTON,
        RetailDashboardForbiddenBehaviorKind.EXECUTION,
        RetailDashboardForbiddenBehaviorKind.APPROVAL_CONTROL,
        RetailDashboardForbiddenBehaviorKind.OVERRIDE_CONTROL,
        RetailDashboardForbiddenBehaviorKind.REAL_DATA_DISPLAY,
    ],
)
def test_forbidden_registry_includes_required_behavior(kind: RetailDashboardForbiddenBehaviorKind) -> None:
    registry = default_retail_dashboard_forbidden_behavior_registry()
    assert kind in {behavior.kind for behavior in registry.behaviors}


@pytest.mark.parametrize(
    "field_name",
    ["forbidden_now", "requires_future_prompt", "requires_audit_before_unlock"],
)
def test_forbidden_behavior_fail_closed_fields_are_enforced(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _behavior(**{field_name: False})


def test_forbidden_behavior_rejects_unknown_kind_and_severity() -> None:
    with pytest.raises(ValidationError):
        _behavior(kind=RetailDashboardForbiddenBehaviorKind.UNKNOWN)
    with pytest.raises(ValidationError):
        _behavior(severity=RetailDashboardBoundarySeverity.UNKNOWN)


@pytest.mark.parametrize(
    "field_name",
    [
        "active_ui_allowed",
        "frontend_components_allowed",
        "desktop_components_allowed",
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "readiness_to_trade_allowed",
        "broker_controls_allowed",
        "execution_allowed",
        "approval_allowed",
        "override_allowed",
    ],
)
def test_forbidden_registry_rejects_dangerous_allowed_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        RetailDashboardForbiddenBehaviorRegistry(
            registry_id="registry-test",
            behaviors=default_retail_dashboard_forbidden_behaviors(),
            **{field_name: True},
        )
