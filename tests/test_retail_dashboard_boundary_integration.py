from __future__ import annotations

from pathlib import Path

from stark_terminal_core.retail_dashboard_boundary.endpoints import (
    default_retail_dashboard_endpoint_boundary_policies,
)
from stark_terminal_core.retail_dashboard_boundary.forbidden import (
    default_retail_dashboard_forbidden_behavior_registry,
)
from stark_terminal_core.retail_dashboard_boundary.invariants import (
    evaluate_retail_dashboard_boundary_invariants,
)
from stark_terminal_core.retail_dashboard_boundary.modules import (
    default_retail_dashboard_module_boundary_policies,
)


ROOT = Path(__file__).resolve().parents[1]


def test_boundary_integration_covers_expected_families() -> None:
    endpoint_families = {
        policy.endpoint_family for policy in default_retail_dashboard_endpoint_boundary_policies()
    }
    module_families = {
        policy.module_family for policy in default_retail_dashboard_module_boundary_policies()
    }
    assert {
        "retail-dashboard",
        "retail-dashboard-api",
        "retail-dashboard-display",
        "retail-dashboard-boundary",
    }.issubset(endpoint_families)
    assert {
        "retail_dashboard",
        "retail_dashboard_api",
        "retail_dashboard_display",
        "retail_dashboard_boundary",
    }.issubset(module_families)


def test_boundary_registry_and_invariants_remain_safe_by_default() -> None:
    registry = default_retail_dashboard_forbidden_behavior_registry()
    result = evaluate_retail_dashboard_boundary_invariants(registry=registry)
    assert registry.complete is True
    assert registry.recommendations_allowed is False
    assert registry.execution_allowed is False
    assert result.passed is True
    assert result.blockers == []
    assert result.recommendations_allowed is False
    assert result.execution_allowed is False


def test_boundary_integration_docs_forbid_bypass_paths() -> None:
    text = (ROOT / "docs/RETAIL_DASHBOARD_BOUNDARY_INTEGRATION_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "forbidden behavior registry integration",
        "endpoint boundary policy integration",
        "module boundary policy integration",
        "cross-module invariant integration",
        "boundary-hardening-only",
        "broker controls",
        "execution apis",
    ]:
        assert phrase in text.lower()
