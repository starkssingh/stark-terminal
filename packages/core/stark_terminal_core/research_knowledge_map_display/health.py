from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.research_knowledge_map_display.safety import (
    research_knowledge_map_display_forbidden_actions,
)


class ResearchKnowledgeMapDisplayHealthStatus(BaseModel):
    service: str
    enabled: bool
    stage: str
    schema_version: str
    display_contract_skeleton_only: bool
    read_only: bool
    unavailable_by_default: bool
    forbidden_action_count: int
    active_ui_enabled: bool
    frontend_components_enabled: bool
    desktop_components_enabled: bool
    active_map_enabled: bool
    database_enabled: bool
    persistent_writes_enabled: bool
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


def research_knowledge_map_display_health(settings: object | None = None) -> ResearchKnowledgeMapDisplayHealthStatus:
    enabled = getattr(settings, "research_knowledge_map_display_enabled", True)
    schema_version = getattr(settings, "research_knowledge_map_display_schema_version", "v1")
    stage = getattr(settings, "research_knowledge_map_display_stage", "display_contract_skeleton")
    dangerous_flags = {
        "active_ui_enabled": getattr(settings, "research_knowledge_map_display_allow_active_ui", False),
        "frontend_components_enabled": getattr(
            settings,
            "research_knowledge_map_display_allow_frontend_components",
            False,
        ),
        "desktop_components_enabled": getattr(
            settings,
            "research_knowledge_map_display_allow_desktop_components",
            False,
        ),
        "active_map_enabled": getattr(settings, "research_knowledge_map_display_allow_active_map", False),
        "database_enabled": getattr(settings, "research_knowledge_map_display_allow_database", False),
        "persistent_writes_enabled": getattr(
            settings,
            "research_knowledge_map_display_allow_persistent_writes",
            False,
        ),
        "traversal_enabled": getattr(settings, "research_knowledge_map_display_allow_traversal", False),
        "search_enabled": getattr(settings, "research_knowledge_map_display_allow_search", False),
        "ranking_enabled": getattr(settings, "research_knowledge_map_display_allow_ranking", False),
        "retrieval_enabled": getattr(settings, "research_knowledge_map_display_allow_retrieval", False),
        "embeddings_enabled": getattr(settings, "research_knowledge_map_display_allow_embeddings", False),
        "vector_store_enabled": getattr(settings, "research_knowledge_map_display_allow_vector_store", False),
        "active_ingestion_enabled": getattr(
            settings,
            "research_knowledge_map_display_allow_active_ingestion",
            False,
        ),
        "file_uploads_enabled": getattr(settings, "research_knowledge_map_display_allow_file_uploads", False),
        "file_downloads_enabled": getattr(settings, "research_knowledge_map_display_allow_file_downloads", False),
        "file_previews_enabled": getattr(settings, "research_knowledge_map_display_allow_file_previews", False),
        "paper_parsing_enabled": getattr(settings, "research_knowledge_map_display_allow_paper_parsing", False),
        "strategy_generation_enabled": getattr(
            settings,
            "research_knowledge_map_display_allow_strategy_generation",
            False,
        ),
        "backtesting_enabled": getattr(settings, "research_knowledge_map_display_allow_backtesting", False),
        "recommendations_enabled": getattr(settings, "research_knowledge_map_display_allow_recommendations", False),
        "execution_enabled": getattr(settings, "research_knowledge_map_display_allow_execution", False),
    }
    healthy = enabled and stage == "display_contract_skeleton" and not any(dangerous_flags.values())
    return ResearchKnowledgeMapDisplayHealthStatus(
        service="stark-terminal-research-knowledge-map-display",
        enabled=enabled,
        stage=stage,
        schema_version=schema_version,
        display_contract_skeleton_only=True,
        read_only=True,
        unavailable_by_default=True,
        forbidden_action_count=len(research_knowledge_map_display_forbidden_actions()),
        **dangerous_flags,
        status="healthy" if healthy else "blocked",
    )
