from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.strategy_research_workspace_boundary.forbidden import (
    StrategyResearchForbiddenBehaviorKind,
)
from stark_terminal_core.strategy_research_workspace_boundary.modules import (
    DEFAULT_STRATEGY_RESEARCH_FORBIDDEN_MODULE_BEHAVIORS,
    StrategyResearchModuleBoundaryPolicy,
    default_strategy_research_module_boundary_policies,
    evaluate_strategy_research_module_boundary_policies,
)


def test_strategy_research_module_boundary_default_policies_validate() -> None:
    policies = default_strategy_research_module_boundary_policies()
    families = {policy.module_family for policy in policies}

    assert families == {
        "strategy_research_workspace",
        "strategy_research_workspace_api",
        "strategy_research_workspace_display",
        "strategy_research_workspace_boundary",
    }
    for policy in policies:
        assert policy.forbidden_behaviors
        assert policy.may_create_active_ui is False
        assert policy.may_create_frontend_components is False
        assert policy.may_create_desktop_components is False
        assert policy.may_ingest_papers is False
        assert policy.may_parse_papers is False
        assert policy.may_generate_strategies is False
        assert policy.may_generate_strategy_code is False
        assert policy.may_run_backtests is False
        assert policy.may_optimize is False
        assert policy.may_generate_recommendations is False
        assert policy.may_generate_actions is False
        assert policy.may_score_confidence is False
        assert policy.may_generate_decision_objects is False
        assert policy.may_generate_readiness_to_trade is False
        assert policy.may_expose_broker_controls is False
        assert policy.may_execute is False
        assert policy.may_grant_approval is False
        assert policy.may_grant_override is False
    assert evaluate_strategy_research_module_boundary_policies(policies) == []


def _policy(**overrides: object) -> StrategyResearchModuleBoundaryPolicy:
    data = {
        "policy_id": "strategy-research-test-module-policy-v1",
        "module_family": "strategy_research_workspace_boundary",
        "allowed_purpose": "boundary-hardening contracts only",
        "forbidden_behaviors": list(DEFAULT_STRATEGY_RESEARCH_FORBIDDEN_MODULE_BEHAVIORS),
    }
    data.update(overrides)
    return StrategyResearchModuleBoundaryPolicy(**data)


@pytest.mark.parametrize(
    "field_name",
    [
        "may_create_active_ui",
        "may_create_frontend_components",
        "may_create_desktop_components",
        "may_ingest_papers",
        "may_parse_papers",
        "may_generate_strategies",
        "may_generate_strategy_code",
        "may_run_backtests",
        "may_optimize",
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
def test_strategy_research_module_boundary_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _policy(**{field_name: True})


def test_strategy_research_module_boundary_rejects_unknown_forbidden_behavior() -> None:
    with pytest.raises(ValidationError):
        _policy(forbidden_behaviors=[StrategyResearchForbiddenBehaviorKind.UNKNOWN])
