from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_boundary.forbidden import RetailDashboardForbiddenBehaviorKind
from stark_terminal_core.retail_dashboard_boundary.modules import (
    DEFAULT_RETAIL_DASHBOARD_FORBIDDEN_MODULE_BEHAVIORS,
    RetailDashboardModuleBoundaryPolicy,
    default_retail_dashboard_module_boundary_policies,
    evaluate_retail_dashboard_module_boundary_policies,
)


def _policy(**overrides: object) -> RetailDashboardModuleBoundaryPolicy:
    data = {
        "policy_id": "retail-dashboard-test-module-boundary-policy",
        "module_family": "retail_dashboard_test",
        "allowed_purpose": "boundary test placeholder only",
        "forbidden_behaviors": list(DEFAULT_RETAIL_DASHBOARD_FORBIDDEN_MODULE_BEHAVIORS),
    }
    data.update(overrides)
    return RetailDashboardModuleBoundaryPolicy(**data)


def test_default_module_boundary_policies_validate() -> None:
    policies = default_retail_dashboard_module_boundary_policies()
    families = {policy.module_family for policy in policies}

    assert families == {
        "retail_dashboard",
        "retail_dashboard_api",
        "retail_dashboard_display",
        "retail_dashboard_boundary",
    }
    assert evaluate_retail_dashboard_module_boundary_policies(policies) == []
    for policy in policies:
        assert policy.forbidden_behaviors
        assert policy.may_create_active_ui is False
        assert policy.may_generate_recommendations is False
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
        "may_expose_broker_controls",
        "may_execute",
        "may_grant_approval",
        "may_grant_override",
    ],
)
def test_module_policy_rejects_dangerous_may_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _policy(**{field_name: True})


def test_module_policy_rejects_unknown_forbidden_behavior() -> None:
    with pytest.raises(ValidationError):
        _policy(forbidden_behaviors=[RetailDashboardForbiddenBehaviorKind.UNKNOWN])
