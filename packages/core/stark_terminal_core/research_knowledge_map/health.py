from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.research_knowledge_map.guardrails import (
    research_knowledge_map_forbidden_actions,
)
from stark_terminal_core.research_knowledge_map.items import (
    default_research_knowledge_map_item_placeholders,
)
from stark_terminal_core.research_knowledge_map.relationships import (
    default_research_knowledge_map_relationship_placeholders,
)


class ResearchKnowledgeMapHealthStatus(BaseModel):
    service: str
    enabled: bool
    stage: str
    schema_version: str
    planning_only: bool
    read_only: bool
    unavailable_by_default: bool
    item_placeholder_count: int
    relationship_placeholder_count: int
    forbidden_action_count: int
    active_map_enabled: bool
    persistent_writes_enabled: bool
    database_enabled: bool
    traversal_enabled: bool
    search_enabled: bool
    ranking_enabled: bool
    retrieval_enabled: bool
    embeddings_enabled: bool
    vector_store_enabled: bool
    active_ingestion_enabled: bool
    file_uploads_enabled: bool
    file_downloads_enabled: bool
    file_previews_enabled: bool
    paper_parsing_enabled: bool
    strategy_generation_enabled: bool
    backtesting_enabled: bool
    recommendations_enabled: bool
    execution_enabled: bool
    status: str


def research_knowledge_map_health(settings: object | None = None) -> ResearchKnowledgeMapHealthStatus:
    enabled = getattr(settings, "research_knowledge_map_enabled", True)
    schema_version = getattr(settings, "research_knowledge_map_schema_version", "v1")
    stage = getattr(settings, "research_knowledge_map_stage", "planning_and_guardrails")
    dangerous_flags = {
        "active_map_enabled": getattr(settings, "research_knowledge_map_allow_active_map", False),
        "persistent_writes_enabled": getattr(settings, "research_knowledge_map_allow_persistent_writes", False),
        "database_enabled": getattr(settings, "research_knowledge_map_allow_database", False),
        "traversal_enabled": getattr(settings, "research_knowledge_map_allow_traversal", False),
        "search_enabled": getattr(settings, "research_knowledge_map_allow_search", False),
        "ranking_enabled": getattr(settings, "research_knowledge_map_allow_ranking", False),
        "retrieval_enabled": getattr(settings, "research_knowledge_map_allow_retrieval", False),
        "embeddings_enabled": getattr(settings, "research_knowledge_map_allow_embeddings", False),
        "vector_store_enabled": getattr(settings, "research_knowledge_map_allow_vector_store", False),
        "active_ingestion_enabled": getattr(settings, "research_knowledge_map_allow_active_ingestion", False),
        "file_uploads_enabled": getattr(settings, "research_knowledge_map_allow_file_uploads", False),
        "file_downloads_enabled": getattr(settings, "research_knowledge_map_allow_file_downloads", False),
        "file_previews_enabled": getattr(settings, "research_knowledge_map_allow_file_previews", False),
        "paper_parsing_enabled": getattr(settings, "research_knowledge_map_allow_paper_parsing", False),
        "strategy_generation_enabled": getattr(settings, "research_knowledge_map_allow_strategy_generation", False),
        "backtesting_enabled": getattr(settings, "research_knowledge_map_allow_backtesting", False),
        "recommendations_enabled": getattr(settings, "research_knowledge_map_allow_recommendations", False),
        "execution_enabled": getattr(settings, "research_knowledge_map_allow_execution", False),
    }
    healthy = enabled and stage == "planning_and_guardrails" and not any(dangerous_flags.values())
    return ResearchKnowledgeMapHealthStatus(
        service="stark-terminal-research-knowledge-map",
        enabled=enabled,
        stage=stage,
        schema_version=schema_version,
        planning_only=True,
        read_only=True,
        unavailable_by_default=True,
        item_placeholder_count=len(default_research_knowledge_map_item_placeholders()),
        relationship_placeholder_count=len(default_research_knowledge_map_relationship_placeholders()),
        forbidden_action_count=len(research_knowledge_map_forbidden_actions()),
        **dangerous_flags,
        status="healthy" if healthy else "blocked",
    )
