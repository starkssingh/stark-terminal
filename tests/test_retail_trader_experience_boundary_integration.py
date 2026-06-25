from __future__ import annotations

from pathlib import Path

from stark_terminal_core.retail_trader_experience_boundary.endpoints import (
    default_retail_trader_experience_endpoint_boundary_policies,
)
from stark_terminal_core.retail_trader_experience_boundary.forbidden import (
    default_retail_trader_experience_forbidden_behavior_registry,
)
from stark_terminal_core.retail_trader_experience_boundary.invariants import (
    evaluate_retail_trader_experience_boundary_invariants,
)
from stark_terminal_core.retail_trader_experience_boundary.modules import (
    default_retail_trader_experience_module_boundary_policies,
)


ROOT = Path(__file__).resolve().parents[1]


def test_boundary_integration_covers_expected_families() -> None:
    endpoint_families = {
        policy.endpoint_family
        for policy in default_retail_trader_experience_endpoint_boundary_policies()
    }
    module_families = {
        policy.module_family
        for policy in default_retail_trader_experience_module_boundary_policies()
    }
    assert {
        "retail-trader-experience",
        "retail-trader-experience-api",
        "retail-trader-experience-display",
        "retail-trader-experience-boundary",
    }.issubset(endpoint_families)
    assert {
        "retail_trader_experience",
        "retail_trader_experience_api",
        "retail_trader_experience_display",
        "retail_trader_experience_boundary",
    }.issubset(module_families)


def test_boundary_registry_and_invariants_remain_safe_by_default() -> None:
    registry = default_retail_trader_experience_forbidden_behavior_registry()
    result = evaluate_retail_trader_experience_boundary_invariants(registry=registry)
    assert registry.complete is True
    assert registry.recommendations_allowed is False
    assert registry.suitability_profiling_allowed is False
    assert registry.execution_allowed is False
    assert result.passed is True
    assert result.blockers == []
    assert result.recommendations_allowed is False
    assert result.suitability_profiling_allowed is False
    assert result.execution_allowed is False


def test_boundary_integration_docs_forbid_bypass_paths() -> None:
    text = (ROOT / "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_INTEGRATION_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "forbidden behavior registry integration",
        "endpoint boundary policy integration",
        "module boundary policy integration",
        "cross-module invariant integration",
        "boundary-hardening-only",
        "suitability profiling",
        "broker controls",
        "execution apis",
        "boundary bypass paths",
    ]:
        assert phrase in text.lower()

