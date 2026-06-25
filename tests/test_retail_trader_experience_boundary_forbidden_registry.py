from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_boundary.forbidden import (
    REQUIRED_RETAIL_TRADER_EXPERIENCE_FORBIDDEN_BEHAVIORS,
    RetailTraderExperienceBoundarySeverity,
    RetailTraderExperienceForbiddenBehavior,
    RetailTraderExperienceForbiddenBehaviorKind,
    RetailTraderExperienceForbiddenBehaviorRegistry,
    default_retail_trader_experience_forbidden_behavior_registry,
    default_retail_trader_experience_forbidden_behaviors,
)


def _behavior(**overrides: object) -> RetailTraderExperienceForbiddenBehavior:
    data = {
        "behavior_id": "behavior-test",
        "kind": RetailTraderExperienceForbiddenBehaviorKind.ACTIVE_UI,
        "name": "Active UI",
        "description": "Active trader experience UI remains forbidden.",
    }
    data.update(overrides)
    return RetailTraderExperienceForbiddenBehavior(**data)


def test_default_forbidden_behavior_registry_validates() -> None:
    registry = default_retail_trader_experience_forbidden_behavior_registry()

    assert registry.complete is True
    assert REQUIRED_RETAIL_TRADER_EXPERIENCE_FORBIDDEN_BEHAVIORS.issubset(
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
    assert registry.suitability_profiling_allowed is False
    assert registry.broker_controls_allowed is False
    assert registry.execution_allowed is False
    assert registry.approval_allowed is False
    assert registry.override_allowed is False


@pytest.mark.parametrize("kind", sorted(REQUIRED_RETAIL_TRADER_EXPERIENCE_FORBIDDEN_BEHAVIORS, key=str))
def test_forbidden_registry_includes_required_behavior(
    kind: RetailTraderExperienceForbiddenBehaviorKind,
) -> None:
    registry = default_retail_trader_experience_forbidden_behavior_registry()
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
        _behavior(kind=RetailTraderExperienceForbiddenBehaviorKind.UNKNOWN)
    with pytest.raises(ValidationError):
        _behavior(severity=RetailTraderExperienceBoundarySeverity.UNKNOWN)


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
        "suitability_profiling_allowed",
        "broker_controls_allowed",
        "execution_allowed",
        "approval_allowed",
        "override_allowed",
    ],
)
def test_forbidden_registry_rejects_dangerous_allowed_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceForbiddenBehaviorRegistry(
            registry_id="registry-test",
            behaviors=default_retail_trader_experience_forbidden_behaviors(),
            **{field_name: True},
        )
