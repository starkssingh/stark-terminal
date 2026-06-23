from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_boundary.forbidden import (
    DecisionBoundarySeverity,
    DecisionForbiddenBehavior,
    DecisionForbiddenBehaviorKind,
    DecisionForbiddenBehaviorRegistry,
    default_decision_forbidden_behavior_registry,
    default_decision_forbidden_behaviors,
)


REQUIRED_KINDS = {
    DecisionForbiddenBehaviorKind.RECOMMENDATION,
    DecisionForbiddenBehaviorKind.ACTION_GENERATION,
    DecisionForbiddenBehaviorKind.CONFIDENCE_SCORING,
    DecisionForbiddenBehaviorKind.DECISION_OBJECT_GENERATION,
    DecisionForbiddenBehaviorKind.EXECUTION,
    DecisionForbiddenBehaviorKind.APPROVAL,
    DecisionForbiddenBehaviorKind.OVERRIDE,
    DecisionForbiddenBehaviorKind.ACTIVE_UI,
    DecisionForbiddenBehaviorKind.ACTIVE_WORKFLOW,
    DecisionForbiddenBehaviorKind.READINESS_TO_TRADE,
}


def _behavior(**overrides: object) -> DecisionForbiddenBehavior:
    data = {
        "behavior_id": "behavior-test",
        "kind": DecisionForbiddenBehaviorKind.RECOMMENDATION,
        "name": "Recommendation",
        "description": "Recommendation generation remains forbidden.",
    }
    data.update(overrides)
    return DecisionForbiddenBehavior(**data)


def test_default_forbidden_behavior_registry_validates_and_is_complete() -> None:
    registry = default_decision_forbidden_behavior_registry()

    assert registry.complete is True
    assert registry.behaviors
    assert REQUIRED_KINDS.issubset({behavior.kind for behavior in registry.behaviors})
    assert registry.recommendations_allowed is False
    assert registry.action_generation_allowed is False
    assert registry.confidence_scoring_allowed is False
    assert registry.decision_object_generation_allowed is False
    assert registry.execution_allowed is False
    assert registry.approval_allowed is False
    assert registry.override_allowed is False
    assert registry.active_ui_allowed is False
    assert registry.active_workflow_allowed is False
    assert registry.readiness_to_trade_allowed is False


@pytest.mark.parametrize(
    "field_name",
    ["forbidden_now", "requires_future_prompt", "requires_audit_before_unlock"],
)
def test_forbidden_behavior_enforces_fail_closed_fields(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _behavior(**{field_name: False})


def test_forbidden_behavior_rejects_unknown_kind_and_severity() -> None:
    with pytest.raises(ValidationError):
        _behavior(kind=DecisionForbiddenBehaviorKind.UNKNOWN)
    with pytest.raises(ValidationError):
        _behavior(severity=DecisionBoundarySeverity.UNKNOWN)


@pytest.mark.parametrize(
    "field_name",
    [
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "execution_allowed",
        "approval_allowed",
        "override_allowed",
        "active_ui_allowed",
        "active_workflow_allowed",
        "readiness_to_trade_allowed",
    ],
)
def test_forbidden_behavior_registry_rejects_dangerous_allowed_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        DecisionForbiddenBehaviorRegistry(
            registry_id="registry-test",
            behaviors=default_decision_forbidden_behaviors(),
            **{field_name: True},
        )


def test_forbidden_behavior_registry_requires_core_forbidden_kinds() -> None:
    behaviors = [
        behavior
        for behavior in default_decision_forbidden_behaviors()
        if behavior.kind != DecisionForbiddenBehaviorKind.EXECUTION
    ]

    with pytest.raises(ValidationError):
        DecisionForbiddenBehaviorRegistry(registry_id="registry-test", behaviors=behaviors)
