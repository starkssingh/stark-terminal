from __future__ import annotations

from pathlib import Path

from stark_terminal_core.strategy_research_workspace_boundary.endpoints import (
    default_strategy_research_endpoint_boundary_policies,
)
from stark_terminal_core.strategy_research_workspace_boundary.forbidden import (
    default_strategy_research_forbidden_behavior_registry,
)
from stark_terminal_core.strategy_research_workspace_boundary.invariants import (
    evaluate_strategy_research_boundary_invariants,
)
from stark_terminal_core.strategy_research_workspace_boundary.modules import (
    default_strategy_research_module_boundary_policies,
)


ROOT = Path(__file__).resolve().parents[1]


def test_boundary_integration_covers_expected_families() -> None:
    endpoint_families = {
        policy.endpoint_family
        for policy in default_strategy_research_endpoint_boundary_policies()
    }
    module_families = {
        policy.module_family
        for policy in default_strategy_research_module_boundary_policies()
    }
    assert {
        "strategy-research-workspace",
        "strategy-research-workspace-api",
        "strategy-research-workspace-display",
        "strategy-research-workspace-boundary",
    }.issubset(endpoint_families)
    assert {
        "strategy_research_workspace",
        "strategy_research_workspace_api",
        "strategy_research_workspace_display",
        "strategy_research_workspace_boundary",
    }.issubset(module_families)


def test_boundary_registry_and_invariants_remain_safe_by_default() -> None:
    registry = default_strategy_research_forbidden_behavior_registry()
    result = evaluate_strategy_research_boundary_invariants(registry=registry)
    assert registry.complete is True
    assert registry.paper_parsing_allowed is False
    assert registry.strategy_generation_allowed is False
    assert registry.backtesting_allowed is False
    assert registry.recommendations_allowed is False
    assert registry.execution_allowed is False
    assert result.passed is True
    assert result.blockers == []
    assert result.strategy_generation_allowed is False
    assert result.backtesting_allowed is False
    assert result.execution_allowed is False


def test_boundary_integration_docs_forbid_bypass_paths() -> None:
    text = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_BOUNDARY_INTEGRATION_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "forbidden behavior registry integration",
        "endpoint boundary policy integration",
        "module boundary policy integration",
        "cross-module invariant integration",
        "api-to-display strategy paths",
        "api-to-display backtest paths",
        "api-to-display recommendation paths",
        "research-to-execution",
        "execution apis",
    ]:
        assert phrase in text
