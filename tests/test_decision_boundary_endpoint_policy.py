from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_boundary.endpoints import (
    DecisionEndpointBoundaryPolicy,
    default_decision_endpoint_boundary_policies,
    evaluate_decision_endpoint_boundary_policies,
)
from stark_terminal_core.decision_boundary.forbidden import DecisionForbiddenBehaviorKind


REQUIRED_ENDPOINT_FAMILIES = {
    "decision-desk",
    "decision-evidence",
    "decision-safety",
    "decision-desk-api",
    "decision-readiness-api",
    "decision-display",
    "decision-evidence-validation",
    "decision-human-review",
    "decision-boundary",
    "retail-dashboard",
    "retail-dashboard-api",
    "retail-dashboard-display",
}


def _policy(**overrides: object) -> DecisionEndpointBoundaryPolicy:
    data = {
        "policy_id": "endpoint-policy-test",
        "endpoint_family": "decision-test",
        "allowed_methods": ["GET"],
        "forbidden_methods": ["POST"],
        "forbidden_outputs": [DecisionForbiddenBehaviorKind.RECOMMENDATION],
    }
    data.update(overrides)
    return DecisionEndpointBoundaryPolicy(**data)


def test_default_endpoint_boundary_policies_validate() -> None:
    policies = default_decision_endpoint_boundary_policies()

    assert REQUIRED_ENDPOINT_FAMILIES.issubset({policy.endpoint_family for policy in policies})
    assert evaluate_decision_endpoint_boundary_policies(policies) == []
    for policy in policies:
        assert policy.read_only is True
        assert policy.unavailable_by_default is True
        assert policy.accepts_market_data_for_decision is False
        assert policy.generates_recommendation is False
        assert policy.generates_decision_object is False
        assert policy.grants_approval is False
        assert policy.grants_override is False
        assert policy.executes_trade is False


@pytest.mark.parametrize(
    "field_name",
    [
        "read_only",
        "unavailable_by_default",
    ],
)
def test_endpoint_boundary_policy_enforces_true_safety_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _policy(**{field_name: False})


@pytest.mark.parametrize(
    "field_name",
    [
        "accepts_market_data_for_decision",
        "generates_recommendation",
        "generates_decision_object",
        "grants_approval",
        "grants_override",
        "executes_trade",
    ],
)
def test_endpoint_boundary_policy_rejects_dangerous_behavior_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _policy(**{field_name: True})


def test_endpoint_boundary_policy_rejects_unknown_forbidden_output() -> None:
    with pytest.raises(ValidationError):
        _policy(forbidden_outputs=[DecisionForbiddenBehaviorKind.UNKNOWN])
