from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.strategy_research_workspace_boundary.endpoints import (
    DEFAULT_STRATEGY_RESEARCH_FORBIDDEN_ENDPOINT_OUTPUTS,
    StrategyResearchEndpointBoundaryPolicy,
    default_strategy_research_endpoint_boundary_policies,
    evaluate_strategy_research_endpoint_boundary_policies,
)
from stark_terminal_core.strategy_research_workspace_boundary.forbidden import (
    StrategyResearchForbiddenBehaviorKind,
)


def test_strategy_research_endpoint_boundary_default_policies_validate() -> None:
    policies = default_strategy_research_endpoint_boundary_policies()
    families = {policy.endpoint_family for policy in policies}

    assert families == {
        "strategy-research-workspace",
        "strategy-research-workspace-api",
        "strategy-research-workspace-display",
        "strategy-research-workspace-boundary",
    }
    for policy in policies:
        assert policy.allowed_methods == ["GET"]
        assert policy.read_only is True
        assert policy.unavailable_by_default is True
        assert policy.accepts_paper_input is False
        assert policy.accepts_market_data_for_research_decision is False
        assert policy.generates_strategy is False
        assert policy.generates_backtest is False
        assert policy.generates_recommendation is False
        assert policy.generates_decision_object is False
        assert policy.exposes_broker_controls is False
        assert policy.executes_trade is False
    assert evaluate_strategy_research_endpoint_boundary_policies(policies) == []


def _policy(**overrides: object) -> StrategyResearchEndpointBoundaryPolicy:
    data = {
        "policy_id": "strategy-research-test-endpoint-policy-v1",
        "endpoint_family": "strategy-research-workspace-boundary",
        "allowed_methods": ["GET"],
        "forbidden_methods": ["POST", "PUT", "PATCH", "DELETE"],
        "forbidden_outputs": list(DEFAULT_STRATEGY_RESEARCH_FORBIDDEN_ENDPOINT_OUTPUTS),
    }
    data.update(overrides)
    return StrategyResearchEndpointBoundaryPolicy(**data)


@pytest.mark.parametrize(
    "field_name",
    [
        "accepts_paper_input",
        "accepts_market_data_for_research_decision",
        "generates_active_ui",
        "ingests_paper",
        "parses_paper",
        "generates_strategy",
        "generates_backtest",
        "generates_recommendation",
        "generates_decision_object",
        "exposes_broker_controls",
        "executes_trade",
    ],
)
def test_strategy_research_endpoint_boundary_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _policy(**{field_name: True})


@pytest.mark.parametrize("field_name", ["read_only", "unavailable_by_default"])
def test_strategy_research_endpoint_boundary_enforces_safe_booleans(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _policy(**{field_name: False})


def test_strategy_research_endpoint_boundary_rejects_unknown_forbidden_output() -> None:
    with pytest.raises(ValidationError):
        _policy(forbidden_outputs=[StrategyResearchForbiddenBehaviorKind.UNKNOWN])
