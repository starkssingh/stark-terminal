from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.research_knowledge_map.evidence import (
    default_research_knowledge_map_evidence_placeholders,
)
from stark_terminal_core.research_knowledge_map.health import (
    research_knowledge_map_health,
)
from stark_terminal_core.research_knowledge_map.items import (
    default_research_knowledge_map_item_placeholders,
)
from stark_terminal_core.research_knowledge_map.lifecycle import (
    default_research_knowledge_map_lifecycle_placeholder,
)
from stark_terminal_core.research_knowledge_map.planning import (
    default_research_knowledge_map_planning_contract,
)
from stark_terminal_core.research_knowledge_map.provenance import (
    default_research_knowledge_map_provenance_placeholders,
)
from stark_terminal_core.research_knowledge_map.readiness import (
    research_knowledge_map_readiness,
)
from stark_terminal_core.research_knowledge_map.relationships import (
    default_research_knowledge_map_relationship_placeholders,
)

router = APIRouter()


def _safe_flags() -> dict[str, bool]:
    return {
        "planning_only": True,
        "read_only": True,
        "unavailable_by_default": True,
        "active_map_enabled": False,
        "persistent_writes_enabled": False,
        "database_enabled": False,
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
        "service": "stark-terminal-research-knowledge-map",
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


@router.get("/research-knowledge-map/health")
def research_knowledge_map_health_endpoint() -> dict[str, Any]:
    status = research_knowledge_map_health(get_settings())
    return {
        **_base_response(),
        **status.model_dump(mode="json"),
    }


@router.get("/research-knowledge-map/planning")
def research_knowledge_map_planning_endpoint() -> dict[str, Any]:
    contract = default_research_knowledge_map_planning_contract(get_settings())
    return {
        **_base_response(),
        "planning_contract": contract.model_dump(mode="json"),
    }


@router.get("/research-knowledge-map/readiness")
def research_knowledge_map_readiness_endpoint() -> dict[str, Any]:
    readiness = research_knowledge_map_readiness(get_settings())
    return {
        **_base_response(),
        "readiness": readiness.model_dump(mode="json"),
        "next_allowed_phase": readiness.next_allowed_phase,
    }


@router.get("/research-knowledge-map/item-placeholder")
def research_knowledge_map_item_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "item_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_research_knowledge_map_item_placeholders()
        ],
    }


@router.get("/research-knowledge-map/relationship-placeholder")
def research_knowledge_map_relationship_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "relationship_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_research_knowledge_map_relationship_placeholders()
        ],
    }


@router.get("/research-knowledge-map/evidence-placeholder")
def research_knowledge_map_evidence_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "evidence_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_research_knowledge_map_evidence_placeholders()
        ],
    }


@router.get("/research-knowledge-map/provenance-placeholder")
def research_knowledge_map_provenance_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "provenance_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_research_knowledge_map_provenance_placeholders()
        ],
    }


@router.get("/research-knowledge-map/lifecycle-placeholder")
def research_knowledge_map_lifecycle_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "lifecycle_placeholder": default_research_knowledge_map_lifecycle_placeholder().model_dump(mode="json"),
    }
