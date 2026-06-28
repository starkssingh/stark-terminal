from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.research_knowledge_map_display.contracts import (
    default_research_knowledge_map_display_contract,
)
from stark_terminal_core.research_knowledge_map_display.evidence import (
    default_knowledge_map_evidence_display_placeholder,
    default_knowledge_map_evidence_reference_display_placeholder,
)
from stark_terminal_core.research_knowledge_map_display.health import (
    research_knowledge_map_display_health,
)
from stark_terminal_core.research_knowledge_map_display.items import (
    default_knowledge_map_item_display_placeholders,
    default_research_knowledge_map_item_display_placeholder,
)
from stark_terminal_core.research_knowledge_map_display.lifecycle import (
    default_knowledge_map_lifecycle_badge_placeholder,
    default_knowledge_map_lifecycle_display_placeholder,
)
from stark_terminal_core.research_knowledge_map_display.provenance import (
    default_knowledge_map_audit_display_placeholder,
    default_knowledge_map_provenance_display_placeholder,
    default_knowledge_map_source_display_placeholder,
)
from stark_terminal_core.research_knowledge_map_display.relationships import (
    default_knowledge_map_relationship_display_placeholders,
    default_research_knowledge_map_relationship_display_placeholder,
)
from stark_terminal_core.research_knowledge_map_display.safety import (
    research_knowledge_map_display_forbidden_actions,
)
from stark_terminal_core.research_knowledge_map_display.unavailable import (
    unavailable_knowledge_map_display_response_template,
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
        "active_map_enabled": False,
        "database_enabled": False,
        "persistent_writes_enabled": False,
        "traversal_enabled": False,
        "search_enabled": False,
        "ranking_enabled": False,
        "retrieval_enabled": False,
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
        "service": "stark-terminal-research-knowledge-map-display",
        "no_active_ui": True,
        "no_frontend_desktop": True,
        "no_active_map": True,
        "no_database": True,
        "no_persistent_writes": True,
        "no_traversal": True,
        "no_search": True,
        "no_ranking": True,
        "no_retrieval": True,
        "no_embeddings_vector_store": True,
        "no_paper_parsing": True,
        "no_strategy_generation": True,
        "no_backtesting": True,
        "no_recommendations": True,
        "no_execution": True,
        **_safe_flags(),
    }


@router.get("/research-knowledge-map-display/health")
def research_knowledge_map_display_health_endpoint() -> dict[str, Any]:
    status = research_knowledge_map_display_health(get_settings())
    return {
        **_base_response(),
        **status.model_dump(mode="json"),
    }


@router.get("/research-knowledge-map-display/contracts")
def research_knowledge_map_display_contracts_endpoint() -> dict[str, Any]:
    contract = default_research_knowledge_map_display_contract(get_settings())
    return {
        **_base_response(),
        "contract": contract.model_dump(mode="json"),
        "forbidden_actions": list(research_knowledge_map_display_forbidden_actions()),
    }


@router.get("/research-knowledge-map-display/unavailable-template")
def research_knowledge_map_display_unavailable_template_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "unavailable_response": unavailable_knowledge_map_display_response_template().model_dump(mode="json"),
    }


@router.get("/research-knowledge-map-display/item-placeholder")
def research_knowledge_map_display_item_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "item_placeholder": default_research_knowledge_map_item_display_placeholder().model_dump(mode="json"),
        "item_placeholders": {
            key: value.model_dump(mode="json") for key, value in default_knowledge_map_item_display_placeholders().items()
        },
        "no_active_ui_rendering": True,
        "no_database_query": True,
        "no_knowledge_map_data_retrieval": True,
        "no_search_result_display": True,
        "no_ranking_display": True,
        "no_embedding_display": True,
        "no_parsed_paper_display": True,
        "no_generated_strategy_display": True,
        "no_backtest_result_display": True,
        "no_recommendation_display": True,
        "no_execution_controls_display": True,
    }


@router.get("/research-knowledge-map-display/relationship-placeholder")
def research_knowledge_map_display_relationship_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "relationship_placeholder": default_research_knowledge_map_relationship_display_placeholder().model_dump(
            mode="json"
        ),
        "relationship_placeholders": {
            key: value.model_dump(mode="json")
            for key, value in default_knowledge_map_relationship_display_placeholders().items()
        },
        "no_traversal": True,
        "no_relationship_ranking": True,
        "no_artifact_retrieval": True,
        "no_strategy_quality_inference": True,
        "no_recommendation_implication": True,
    }


@router.get("/research-knowledge-map-display/evidence-placeholder")
def research_knowledge_map_display_evidence_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "evidence_placeholder": default_knowledge_map_evidence_display_placeholder().model_dump(mode="json"),
        "evidence_reference_placeholder": default_knowledge_map_evidence_reference_display_placeholder().model_dump(
            mode="json"
        ),
        "no_truth_validation": True,
        "no_research_approval": True,
        "no_trade_readiness": True,
        "no_decision_generation": True,
    }


@router.get("/research-knowledge-map-display/provenance-placeholder")
def research_knowledge_map_display_provenance_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "provenance_placeholder": default_knowledge_map_provenance_display_placeholder().model_dump(mode="json"),
        "source_placeholder": default_knowledge_map_source_display_placeholder().model_dump(mode="json"),
        "audit_placeholder": default_knowledge_map_audit_display_placeholder().model_dump(mode="json"),
        "no_external_fetch": True,
        "no_local_file_read": True,
        "no_source_validation": True,
        "no_trusted_research_status": True,
    }


@router.get("/research-knowledge-map-display/lifecycle-placeholder")
def research_knowledge_map_display_lifecycle_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "lifecycle_placeholder": default_knowledge_map_lifecycle_display_placeholder().model_dump(mode="json"),
        "lifecycle_badge_placeholder": default_knowledge_map_lifecycle_badge_placeholder().model_dump(mode="json"),
        "allowed_lifecycle_display_states": [
            "PLANNED",
            "REFERENCED",
            "DRAFT",
            "REVIEW_REQUIRED",
            "BLOCKED",
            "DEFERRED",
            "UNAVAILABLE",
            "UNKNOWN",
        ],
        "forbidden_lifecycle_display_meanings": [
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
