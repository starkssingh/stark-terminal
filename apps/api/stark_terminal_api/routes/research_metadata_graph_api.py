from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.research_metadata_graph_api.contracts import (
    default_research_metadata_graph_api_contract,
)
from stark_terminal_core.research_metadata_graph_api.health import (
    research_metadata_graph_api_health,
)
from stark_terminal_core.research_metadata_graph_api.references import (
    default_graph_api_edge_reference_placeholder,
    default_graph_api_node_reference_placeholder,
    default_graph_api_provenance_reference_placeholder,
    default_graph_api_reference_placeholder,
)
from stark_terminal_core.research_metadata_graph_api.requests import (
    default_graph_edge_lookup_request_placeholder,
    default_graph_node_lookup_request_placeholder,
    default_graph_provenance_request_placeholder,
    default_graph_relationship_request_placeholder,
    default_research_metadata_graph_request_placeholder,
)
from stark_terminal_core.research_metadata_graph_api.responses import (
    default_graph_edge_response_placeholder,
    default_graph_node_response_placeholder,
    default_graph_provenance_response_placeholder,
    default_graph_relationship_response_placeholder,
    default_research_metadata_graph_response_placeholder,
)
from stark_terminal_core.research_metadata_graph_api.safety import (
    research_metadata_graph_api_forbidden_actions,
)
from stark_terminal_core.research_metadata_graph_api.unavailable import (
    unavailable_graph_api_response_template,
)

router = APIRouter()


def _safe_flags() -> dict[str, bool]:
    return {
        "api_contract_skeleton_only": True,
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
        "service": "stark-terminal-research-metadata-graph-api",
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


@router.get("/research-metadata-graph-api/health")
def research_metadata_graph_api_health_endpoint() -> dict[str, Any]:
    status = research_metadata_graph_api_health(get_settings())
    return {
        **_base_response(),
        **status.model_dump(mode="json"),
    }


@router.get("/research-metadata-graph-api/contracts")
def research_metadata_graph_api_contracts_endpoint() -> dict[str, Any]:
    contract = default_research_metadata_graph_api_contract(get_settings())
    return {
        **_base_response(),
        "contract": contract.model_dump(mode="json"),
        "forbidden_actions": list(research_metadata_graph_api_forbidden_actions()),
    }


@router.get("/research-metadata-graph-api/unavailable-template")
def research_metadata_graph_api_unavailable_template_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "unavailable_response": unavailable_graph_api_response_template().model_dump(mode="json"),
    }


@router.get("/research-metadata-graph-api/request-placeholder")
def research_metadata_graph_api_request_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "request_placeholder": default_research_metadata_graph_request_placeholder().model_dump(mode="json"),
        "request_placeholders": {
            "node": default_graph_node_lookup_request_placeholder().model_dump(mode="json"),
            "edge": default_graph_edge_lookup_request_placeholder().model_dump(mode="json"),
            "relationship": default_graph_relationship_request_placeholder().model_dump(mode="json"),
            "provenance": default_graph_provenance_request_placeholder().model_dump(mode="json"),
        },
        "no_lookup_trigger": True,
        "no_traversal_trigger": True,
        "no_search_trigger": True,
        "no_retrieval_trigger": True,
        "no_file_bytes": True,
        "no_raw_paper_content": True,
        "no_market_data_for_recommendations": True,
        "no_strategy_generation_instructions": True,
    }


@router.get("/research-metadata-graph-api/response-placeholder")
def research_metadata_graph_api_response_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "response_placeholder": default_research_metadata_graph_response_placeholder().model_dump(mode="json"),
        "response_placeholders": {
            "node": default_graph_node_response_placeholder().model_dump(mode="json"),
            "edge": default_graph_edge_response_placeholder().model_dump(mode="json"),
            "relationship": default_graph_relationship_response_placeholder().model_dump(mode="json"),
            "provenance": default_graph_provenance_response_placeholder().model_dump(mode="json"),
        },
        "no_retrieved_graph_data": True,
        "no_search_results": True,
        "no_rankings": True,
        "no_embeddings": True,
        "no_parsed_paper_content": True,
        "no_generated_strategies": True,
        "no_backtest_results": True,
        "no_recommendations": True,
        "no_execution_controls": True,
    }


@router.get("/research-metadata-graph-api/reference-placeholder")
def research_metadata_graph_api_reference_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "api_reference": default_graph_api_reference_placeholder().model_dump(mode="json"),
        "node_reference": default_graph_api_node_reference_placeholder().model_dump(mode="json"),
        "edge_reference": default_graph_api_edge_reference_placeholder().model_dump(mode="json"),
        "provenance_reference": default_graph_api_provenance_reference_placeholder().model_dump(mode="json"),
        "no_fetch": True,
        "no_retrieval": True,
        "no_source_truth_validation": True,
        "no_graph_persistence_claim": True,
    }
