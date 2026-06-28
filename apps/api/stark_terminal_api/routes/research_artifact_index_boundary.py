from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.research_artifact_index_boundary.endpoints import (
    default_research_artifact_index_endpoint_boundary_policies,
)
from stark_terminal_core.research_artifact_index_boundary.forbidden import (
    default_research_artifact_index_forbidden_behavior_registry,
)
from stark_terminal_core.research_artifact_index_boundary.health import (
    research_artifact_index_boundary_health,
)
from stark_terminal_core.research_artifact_index_boundary.invariants import (
    evaluate_research_artifact_index_boundary_invariants,
)
from stark_terminal_core.research_artifact_index_boundary.modules import (
    default_research_artifact_index_module_boundary_policies,
)

router = APIRouter()


def _safe_flags() -> dict[str, bool]:
    return {
        "system_boundary_hardening_only": True,
        "read_only": True,
        "active_ui_enabled": False,
        "frontend_components_enabled": False,
        "desktop_components_enabled": False,
        "indexing_engine_enabled": False,
        "search_engine_enabled": False,
        "ranking_engine_enabled": False,
        "retrieval_engine_enabled": False,
        "embeddings_enabled": False,
        "vector_store_enabled": False,
        "active_ingestion_enabled": False,
        "persistent_storage_enabled": False,
        "file_uploads_enabled": False,
        "file_downloads_enabled": False,
        "file_previews_enabled": False,
        "paper_parsing_enabled": False,
        "strategy_generation_enabled": False,
        "backtesting_enabled": False,
        "recommendations_enabled": False,
        "execution_enabled": False,
        "broker_controls_enabled": False,
        "readiness_to_trade_enabled": False,
        "active_decision_objects_enabled": False,
    }


@router.get("/research-artifact-index-boundary/health")
def research_artifact_index_boundary_health_endpoint() -> dict[str, Any]:
    return research_artifact_index_boundary_health().model_dump()


@router.get("/research-artifact-index-boundary/contracts")
def research_artifact_index_boundary_contracts() -> dict[str, Any]:
    registry = default_research_artifact_index_forbidden_behavior_registry()
    endpoint_policies = default_research_artifact_index_endpoint_boundary_policies()
    module_policies = default_research_artifact_index_module_boundary_policies()
    return {
        "service": "stark-terminal-research-artifact-index-boundary",
        "schema_version": "v1",
        "computation_scope": "system-boundary-hardening-only",
        **_safe_flags(),
        "forbidden_behaviors": [behavior.kind.value for behavior in registry.behaviors],
        "endpoint_families": [policy.endpoint_family for policy in endpoint_policies],
        "module_families": [policy.module_family for policy in module_policies],
        "no_active_ui": True,
        "no_frontend_desktop": True,
        "no_indexing_search_ranking_retrieval": True,
        "no_embeddings_vector_store": True,
        "no_ingestion_storage_upload_download_preview": True,
        "no_paper_parsing": True,
        "no_strategy_generation": True,
        "no_backtesting": True,
        "no_recommendations": True,
        "no_execution": True,
    }


@router.get("/research-artifact-index-boundary/invariants")
def research_artifact_index_boundary_invariants() -> dict[str, Any]:
    result = evaluate_research_artifact_index_boundary_invariants()
    return {
        "service": "stark-terminal-research-artifact-index-boundary",
        "computation_scope": "system-boundary-hardening-only",
        **_safe_flags(),
        "invariant_result": result.model_dump(mode="json"),
        "blockers": list(result.blockers),
        "warnings": list(result.warnings),
        "no_active_ui": True,
        "no_frontend_desktop": True,
        "no_indexing_search_ranking_retrieval": True,
        "no_embeddings_vector_store": True,
        "no_ingestion_storage_upload_download_preview": True,
        "no_paper_parsing": True,
        "no_strategy_generation": True,
        "no_backtesting": True,
        "no_recommendations": True,
        "no_execution": True,
    }

