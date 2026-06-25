from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_boundary.endpoints import (
    DEFAULT_RETAIL_TRADER_EXPERIENCE_FORBIDDEN_ENDPOINT_OUTPUTS,
    RetailTraderExperienceEndpointBoundaryPolicy,
    default_retail_trader_experience_endpoint_boundary_policies,
    evaluate_retail_trader_experience_endpoint_boundary_policies,
)
from stark_terminal_core.retail_trader_experience_boundary.forbidden import (
    RetailTraderExperienceForbiddenBehaviorKind,
)


def _policy(**overrides: object) -> RetailTraderExperienceEndpointBoundaryPolicy:
    data = {
        "policy_id": "retail-trader-experience-test-boundary-policy",
        "endpoint_family": "retail-trader-experience-test",
        "allowed_methods": ["GET"],
        "forbidden_methods": ["POST", "PUT", "PATCH", "DELETE"],
        "forbidden_outputs": list(DEFAULT_RETAIL_TRADER_EXPERIENCE_FORBIDDEN_ENDPOINT_OUTPUTS),
    }
    data.update(overrides)
    return RetailTraderExperienceEndpointBoundaryPolicy(**data)


def test_default_endpoint_boundary_policies_validate() -> None:
    policies = default_retail_trader_experience_endpoint_boundary_policies()
    families = {policy.endpoint_family for policy in policies}

    assert families == {
        "retail-trader-experience",
        "retail-trader-experience-api",
        "retail-trader-experience-display",
        "retail-trader-experience-boundary",
    }
    assert evaluate_retail_trader_experience_endpoint_boundary_policies(policies) == []
    for policy in policies:
        assert policy.read_only is True
        assert policy.unavailable_by_default is True
        assert policy.allowed_methods == ["GET"]
        assert "POST" in policy.forbidden_methods


@pytest.mark.parametrize("field_name", ["read_only", "unavailable_by_default"])
def test_endpoint_policy_enforces_true_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _policy(**{field_name: False})


@pytest.mark.parametrize(
    "field_name",
    [
        "accepts_market_data_for_trader_decision",
        "generates_recommendation",
        "generates_active_ui",
        "generates_decision_object",
        "generates_suitability_profile",
        "exposes_broker_controls",
        "executes_trade",
    ],
)
def test_endpoint_policy_rejects_dangerous_generation_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _policy(**{field_name: True})


def test_endpoint_policy_rejects_unknown_forbidden_output() -> None:
    with pytest.raises(ValidationError):
        _policy(forbidden_outputs=[RetailTraderExperienceForbiddenBehaviorKind.UNKNOWN])
