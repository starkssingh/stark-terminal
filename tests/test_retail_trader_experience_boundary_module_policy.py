from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_boundary.forbidden import (
    RetailTraderExperienceForbiddenBehaviorKind,
)
from stark_terminal_core.retail_trader_experience_boundary.modules import (
    DEFAULT_RETAIL_TRADER_EXPERIENCE_FORBIDDEN_MODULE_BEHAVIORS,
    RetailTraderExperienceModuleBoundaryPolicy,
    default_retail_trader_experience_module_boundary_policies,
    evaluate_retail_trader_experience_module_boundary_policies,
)


def _policy(**overrides: object) -> RetailTraderExperienceModuleBoundaryPolicy:
    data = {
        "policy_id": "retail-trader-experience-test-module-boundary-policy",
        "module_family": "retail_trader_experience_test",
        "allowed_purpose": "boundary test only",
        "forbidden_behaviors": list(DEFAULT_RETAIL_TRADER_EXPERIENCE_FORBIDDEN_MODULE_BEHAVIORS),
    }
    data.update(overrides)
    return RetailTraderExperienceModuleBoundaryPolicy(**data)


def test_default_module_boundary_policies_validate() -> None:
    policies = default_retail_trader_experience_module_boundary_policies()
    families = {policy.module_family for policy in policies}

    assert families == {
        "retail_trader_experience",
        "retail_trader_experience_api",
        "retail_trader_experience_display",
        "retail_trader_experience_boundary",
    }
    assert evaluate_retail_trader_experience_module_boundary_policies(policies) == []
    for policy in policies:
        assert policy.forbidden_behaviors
        assert policy.may_create_active_ui is False
        assert policy.may_generate_recommendations is False
        assert policy.may_generate_suitability_profiles is False
        assert policy.may_expose_broker_controls is False
        assert policy.may_execute is False


@pytest.mark.parametrize(
    "field_name",
    [
        "may_create_active_ui",
        "may_create_frontend_components",
        "may_create_desktop_components",
        "may_generate_recommendations",
        "may_generate_actions",
        "may_score_confidence",
        "may_generate_decision_objects",
        "may_generate_readiness_to_trade",
        "may_generate_suitability_profiles",
        "may_expose_broker_controls",
        "may_execute",
        "may_grant_approval",
        "may_grant_override",
    ],
)
def test_module_policy_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _policy(**{field_name: True})


def test_module_policy_rejects_unknown_forbidden_behavior() -> None:
    with pytest.raises(ValidationError):
        _policy(forbidden_behaviors=[RetailTraderExperienceForbiddenBehaviorKind.UNKNOWN])
