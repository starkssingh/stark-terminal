from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.research_metadata_graph.edges import (
    default_research_metadata_graph_edge_placeholders,
)
from stark_terminal_core.research_metadata_graph.health import (
    research_metadata_graph_health,
)
from stark_terminal_core.research_metadata_graph.lifecycle import (
    default_graph_lifecycle_reference_placeholder,
)
from stark_terminal_core.research_metadata_graph.nodes import (
    default_research_metadata_graph_node_placeholders,
)
from stark_terminal_core.research_metadata_graph.planning import (
    default_research_metadata_graph_planning_contract,
)
from stark_terminal_core.research_metadata_graph.provenance import (
    default_graph_provenance_reference_placeholders,
)
from stark_terminal_core.research_metadata_graph.readiness import (
    research_metadata_graph_readiness,
)
from stark_terminal_core.research_metadata_graph.references import (
    default_graph_reference_placeholders,
)

router = APIRouter()


def _safe_flags() -> dict[str, bool]:
    return {
        "planning_only": True,
        "read_only": True,
        "unavailable_by_default": True,
        "graph_database_enabled": False,
        "persistent_writes_enabled": False,
        "graph_traversal_enabled": False,
        "graph_search_enabled": False,
        "graph_ranking_enabled": False,
        "graph_retrieval_enabled": False,
        "embeddings_enabled": False,
        "vector_store_enabled": False,
        "active_ingestion_enabled": False,
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


def _base_response() -> dict[str, Any]:
    return {
        "service": "stark-terminal-research-metadata-graph",
        "no_graph_database": True,
        "no_persistent_writes": True,
        "no_graph_traversal": True,
        "no_graph_search": True,
        "no_graph_ranking": True,
        "no_graph_retrieval": True,
        "no_embeddings_vector_store": True,
        "no_ingestion_storage_upload_download_preview": True,
        "no_paper_parsing": True,
        "no_strategy_generation": True,
        "no_backtesting": True,
        "no_recommendations": True,
        "no_execution": True,
        **_safe_flags(),
    }


@router.get("/research-metadata-graph/health")
def research_metadata_graph_health_endpoint() -> dict[str, Any]:
    status = research_metadata_graph_health(get_settings())
    return {
        **_base_response(),
        **status.model_dump(mode="json"),
    }


@router.get("/research-metadata-graph/planning")
def research_metadata_graph_planning_endpoint() -> dict[str, Any]:
    contract = default_research_metadata_graph_planning_contract(get_settings())
    return {
        **_base_response(),
        "planning_contract": contract.model_dump(mode="json"),
    }


@router.get("/research-metadata-graph/readiness")
def research_metadata_graph_readiness_endpoint() -> dict[str, Any]:
    readiness = research_metadata_graph_readiness(get_settings())
    return {
        **_base_response(),
        "readiness": readiness.model_dump(mode="json"),
        "next_allowed_phase": readiness.next_allowed_phase,
    }


@router.get("/research-metadata-graph/node-placeholder")
def research_metadata_graph_node_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "node_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_research_metadata_graph_node_placeholders()
        ],
    }


@router.get("/research-metadata-graph/edge-placeholder")
def research_metadata_graph_edge_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "edge_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_research_metadata_graph_edge_placeholders()
        ],
    }


@router.get("/research-metadata-graph/provenance-placeholder")
def research_metadata_graph_provenance_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "provenance_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_graph_provenance_reference_placeholders()
        ],
    }


@router.get("/research-metadata-graph/lifecycle-placeholder")
def research_metadata_graph_lifecycle_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "lifecycle_placeholder": default_graph_lifecycle_reference_placeholder().model_dump(mode="json"),
    }


@router.get("/research-metadata-graph/reference-placeholder")
def research_metadata_graph_reference_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "reference_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_graph_reference_placeholders()
        ],
    }
