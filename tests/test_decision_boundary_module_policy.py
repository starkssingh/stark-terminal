from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_boundary.forbidden import DecisionForbiddenBehaviorKind
from stark_terminal_core.decision_boundary.modules import (
    DecisionModuleBoundaryPolicy,
    default_decision_module_boundary_policies,
    evaluate_decision_module_boundary_policies,
)


REQUIRED_MODULE_FAMILIES = {
    "decision_desk",
    "decision_evidence",
    "decision_safety",
    "decision_api",
    "decision_readiness_api",
    "decision_display",
    "decision_evidence_validation",
    "decision_human_review",
    "decision_boundary",
    "retail_dashboard",
    "retail_dashboard_api",
    "retail_dashboard_display",
}


def _policy(**overrides: object) -> DecisionModuleBoundaryPolicy:
    data = {
        "policy_id": "module-policy-test",
        "module_family": "decision_test",
        "allowed_purpose": "test policy only",
        "forbidden_behaviors": [DecisionForbiddenBehaviorKind.RECOMMENDATION],
    }
    data.update(overrides)
    return DecisionModuleBoundaryPolicy(**data)


def test_default_module_boundary_policies_validate() -> None:
    policies = default_decision_module_boundary_policies()

    assert REQUIRED_MODULE_FAMILIES.issubset({policy.module_family for policy in policies})
    assert evaluate_decision_module_boundary_policies(policies) == []
    for policy in policies:
        assert policy.forbidden_behaviors
        assert policy.may_generate_recommendations is False
        assert policy.may_generate_actions is False
        assert policy.may_score_confidence is False
        assert policy.may_generate_decision_objects is False
        assert policy.may_grant_approval is False
        assert policy.may_grant_override is False
        assert policy.may_execute is False
        assert policy.may_create_active_ui is False
        assert policy.may_create_active_workflow is False
        assert policy.may_generate_readiness_to_trade is False


@pytest.mark.parametrize(
    "field_name",
    [
        "may_generate_recommendations",
        "may_generate_actions",
        "may_score_confidence",
        "may_generate_decision_objects",
        "may_grant_approval",
        "may_grant_override",
        "may_execute",
        "may_create_active_ui",
        "may_create_active_workflow",
        "may_generate_readiness_to_trade",
    ],
)
def test_module_boundary_policy_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _policy(**{field_name: True})


def test_module_boundary_policy_rejects_unknown_forbidden_behavior() -> None:
    with pytest.raises(ValidationError):
        _policy(forbidden_behaviors=[DecisionForbiddenBehaviorKind.UNKNOWN])
