from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.research_metadata_graph_display.contracts import (
    default_research_metadata_graph_display_contract,
)
from stark_terminal_core.research_metadata_graph_display.edges import (
    default_graph_edge_display_placeholders,
    default_research_metadata_graph_edge_display_placeholder,
)
from stark_terminal_core.research_metadata_graph_display.health import (
    research_metadata_graph_display_health,
)
from stark_terminal_core.research_metadata_graph_display.lifecycle import (
    default_graph_lifecycle_badge_placeholder,
    default_graph_lifecycle_display_placeholder,
)
from stark_terminal_core.research_metadata_graph_display.nodes import (
    default_graph_node_display_placeholders,
    default_research_metadata_graph_node_display_placeholder,
)
from stark_terminal_core.research_metadata_graph_display.provenance import (
    default_graph_audit_display_placeholder,
    default_graph_provenance_display_placeholder,
    default_graph_source_display_placeholder,
)
from stark_terminal_core.research_metadata_graph_display.references import (
    default_graph_dependency_reference_display_placeholder,
    default_graph_reference_display_placeholder,
    default_graph_relationship_reference_display_placeholder,
)
from stark_terminal_core.research_metadata_graph_display.safety import (
    research_metadata_graph_display_forbidden_actions,
)
from stark_terminal_core.research_metadata_graph_display.unavailable import (
    unavailable_graph_display_response_template,
)

router = APIRouter()


def _safe_flags() -> dict[str, bool]:
    return {
        "display_contract_skeleton_only": True,
        "read_only": True,
        "unavailable_by_default": True,
        "active_ui_enabled": False,
        "frontend_components_enabled": False,
        "desktop_components_enabled": False,
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
        "service": "stark-terminal-research-metadata-graph-display",
        "no_active_ui": True,
        "no_frontend_desktop": True,
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


@router.get("/research-metadata-graph-display/health")
def research_metadata_graph_display_health_endpoint() -> dict[str, Any]:
    status = research_metadata_graph_display_health(get_settings())
    return {
        **_base_response(),
        **status.model_dump(mode="json"),
    }


@router.get("/research-metadata-graph-display/contracts")
def research_metadata_graph_display_contracts_endpoint() -> dict[str, Any]:
    contract = default_research_metadata_graph_display_contract(get_settings())
    return {
        **_base_response(),
        "contract": contract.model_dump(mode="json"),
        "forbidden_actions": list(research_metadata_graph_display_forbidden_actions()),
    }


@router.get("/research-metadata-graph-display/unavailable-template")
def research_metadata_graph_display_unavailable_template_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "unavailable_response": unavailable_graph_display_response_template().model_dump(mode="json"),
    }


@router.get("/research-metadata-graph-display/node-placeholder")
def research_metadata_graph_display_node_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "node_placeholder": default_research_metadata_graph_node_display_placeholder().model_dump(mode="json"),
        "node_placeholders": {
            key: value.model_dump(mode="json") for key, value in default_graph_node_display_placeholders().items()
        },
        "no_active_ui_rendering": True,
        "no_graph_database_query": True,
        "no_graph_data_retrieval": True,
        "no_search_result_display": True,
        "no_ranking_display": True,
        "no_embedding_display": True,
        "no_parsed_paper_display": True,
        "no_generated_strategy_display": True,
        "no_backtest_result_display": True,
        "no_recommendation_display": True,
        "no_execution_controls_display": True,
    }


@router.get("/research-metadata-graph-display/edge-placeholder")
def research_metadata_graph_display_edge_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "edge_placeholder": default_research_metadata_graph_edge_display_placeholder().model_dump(mode="json"),
        "edge_placeholders": {
            key: value.model_dump(mode="json") for key, value in default_graph_edge_display_placeholders().items()
        },
        "no_traversal": True,
        "no_relationship_ranking": True,
        "no_artifact_retrieval": True,
        "no_strategy_value_inference": True,
        "no_recommendation_implication": True,
    }


@router.get("/research-metadata-graph-display/provenance-placeholder")
def research_metadata_graph_display_provenance_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "provenance_placeholder": default_graph_provenance_display_placeholder().model_dump(mode="json"),
        "source_placeholder": default_graph_source_display_placeholder().model_dump(mode="json"),
        "audit_placeholder": default_graph_audit_display_placeholder().model_dump(mode="json"),
        "no_source_truth_validation": True,
        "no_external_fetch": True,
        "no_local_file_read": True,
        "no_trusted_research_status": True,
    }


@router.get("/research-metadata-graph-display/lifecycle-placeholder")
def research_metadata_graph_display_lifecycle_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "lifecycle_placeholder": default_graph_lifecycle_display_placeholder().model_dump(mode="json"),
        "lifecycle_badge_placeholder": default_graph_lifecycle_badge_placeholder().model_dump(mode="json"),
        "allowed_lifecycle_meanings": [
            "PLANNED",
            "REFERENCED",
            "DRAFT",
            "REVIEW_REQUIRED",
            "BLOCKED",
            "DEFERRED",
            "UNAVAILABLE",
            "UNKNOWN",
        ],
        "forbidden_lifecycle_meanings": [
            "INDEXED",
            "SEARCHABLE",
            "RANKED",
            "EMBEDDED",
            "RETRIEVED",
            "VALIDATED_STRATEGY",
            "BACKTESTED_PROFITABLE",
            "RECOMMENDED",
            "READY_TO_TRADE",
            "EXECUTABLE",
        ],
    }


@router.get("/research-metadata-graph-display/reference-placeholder")
def research_metadata_graph_display_reference_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "reference_placeholder": default_graph_reference_display_placeholder().model_dump(mode="json"),
        "dependency_reference": default_graph_dependency_reference_display_placeholder().model_dump(mode="json"),
        "relationship_reference": default_graph_relationship_reference_display_placeholder().model_dump(mode="json"),
        "no_lookup": True,
        "no_retrieval": True,
        "no_traversal": True,
        "no_search": True,
        "no_ranking": True,
        "no_file_access": True,
        "no_external_fetch": True,
    }
