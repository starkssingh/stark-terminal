from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.research_artifact_index_boundary.endpoints import (
    default_research_artifact_index_endpoint_boundary_policies,
)
from stark_terminal_core.research_artifact_index_boundary.forbidden import (
    default_research_artifact_index_forbidden_behavior_registry,
)
from stark_terminal_core.research_artifact_index_boundary.invariants import (
    evaluate_research_artifact_index_boundary_invariants,
)
from stark_terminal_core.research_artifact_index_boundary.modules import (
    default_research_artifact_index_module_boundary_policies,
)


class ResearchArtifactIndexBoundaryHealth(BaseModel):
    service: str = "stark-terminal-research-artifact-index-boundary"
    enabled: bool = True
    stage: str = "system_boundary_hardening"
    schema_version: str = "v1"
    forbidden_behavior_count: int
    endpoint_policy_count: int
    module_policy_count: int
    invariants_passed: bool
    active_ui_allowed: bool = False
    frontend_components_allowed: bool = False
    desktop_components_allowed: bool = False
    indexing_engine_allowed: bool = False
    search_engine_allowed: bool = False
    ranking_engine_allowed: bool = False
    retrieval_engine_allowed: bool = False
    embeddings_allowed: bool = False
    vector_store_allowed: bool = False
    active_ingestion_allowed: bool = False
    persistent_storage_allowed: bool = False
    file_uploads_allowed: bool = False
    file_downloads_allowed: bool = False
    file_previews_allowed: bool = False
    paper_parsing_allowed: bool = False
    strategy_generation_allowed: bool = False
    backtesting_allowed: bool = False
    recommendations_allowed: bool = False
    execution_allowed: bool = False
    status: str


def research_artifact_index_boundary_health() -> ResearchArtifactIndexBoundaryHealth:
    registry = default_research_artifact_index_forbidden_behavior_registry()
    endpoint_policies = default_research_artifact_index_endpoint_boundary_policies()
    module_policies = default_research_artifact_index_module_boundary_policies()
    invariant = evaluate_research_artifact_index_boundary_invariants(
        endpoint_policies=endpoint_policies,
        module_policies=module_policies,
        registry=registry,
    )
    return ResearchArtifactIndexBoundaryHealth(
        forbidden_behavior_count=len(registry.behaviors),
        endpoint_policy_count=len(endpoint_policies),
        module_policy_count=len(module_policies),
        invariants_passed=invariant.passed,
        status="healthy" if invariant.passed else "blocked",
    )

