from __future__ import annotations

from pathlib import Path

from stark_terminal_core.research_artifact_registry_boundary.endpoints import (
    default_research_artifact_endpoint_boundary_policies,
)
from stark_terminal_core.research_artifact_registry_boundary.forbidden import (
    default_research_artifact_forbidden_behavior_registry,
)
from stark_terminal_core.research_artifact_registry_boundary.invariants import (
    evaluate_research_artifact_boundary_invariants,
)
from stark_terminal_core.research_artifact_registry_boundary.modules import (
    default_research_artifact_module_boundary_policies,
)


ROOT = Path(__file__).resolve().parents[1]


def test_research_artifact_boundary_integration_covers_expected_families() -> None:
    endpoint_families = {
        policy.endpoint_family
        for policy in default_research_artifact_endpoint_boundary_policies()
    }
    module_families = {
        policy.module_family
        for policy in default_research_artifact_module_boundary_policies()
    }
    assert {
        "research-artifact-registry",
        "research-artifact-registry-api",
        "research-artifact-registry-display",
        "research-artifact-registry-boundary",
    }.issubset(endpoint_families)
    assert {
        "research_artifact_registry",
        "research_artifact_registry_api",
        "research_artifact_registry_display",
        "research_artifact_registry_boundary",
    }.issubset(module_families)


def test_research_artifact_boundary_registry_and_invariants_remain_safe_by_default() -> None:
    registry = default_research_artifact_forbidden_behavior_registry()
    result = evaluate_research_artifact_boundary_invariants(registry=registry)
    assert registry.complete is True
    assert registry.active_ingestion_allowed is False
    assert registry.persistent_storage_allowed is False
    assert registry.file_uploads_allowed is False
    assert registry.file_downloads_allowed is False
    assert registry.paper_parsing_allowed is False
    assert registry.strategy_generation_allowed is False
    assert registry.backtesting_allowed is False
    assert registry.recommendations_allowed is False
    assert registry.execution_allowed is False
    assert result.passed is True
    assert result.blockers == []
    assert result.active_ingestion_allowed is False
    assert result.persistent_storage_allowed is False
    assert result.strategy_generation_allowed is False
    assert result.backtesting_allowed is False
    assert result.execution_allowed is False


def test_research_artifact_boundary_integration_docs_forbid_bypass_paths() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_BOUNDARY_INTEGRATION_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "forbidden behavior registry integration",
        "endpoint boundary policy integration",
        "module boundary policy integration",
        "cross-module invariant integration",
        "api-to-display artifact ingestion paths",
        "api-to-display storage paths",
        "api-to-display file preview paths",
        "artifact-to-strategy paths",
        "artifact-to-backtest paths",
        "artifact-as-recommendation paths",
        "artifact-to-execution paths",
        "execution apis",
    ]:
        assert phrase in text

