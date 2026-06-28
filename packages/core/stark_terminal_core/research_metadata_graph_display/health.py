from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.research_metadata_graph_display.safety import (
    research_metadata_graph_display_forbidden_actions,
)


class ResearchMetadataGraphDisplayHealthStatus(BaseModel):
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
    graph_database_enabled: bool
    persistent_writes_enabled: bool
    graph_traversal_enabled: bool
    graph_search_enabled: bool
    graph_ranking_enabled: bool
    graph_retrieval_enabled: bool
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


def research_metadata_graph_display_health(settings: object | None = None) -> ResearchMetadataGraphDisplayHealthStatus:
    enabled = getattr(settings, "research_metadata_graph_display_enabled", True)
    schema_version = getattr(settings, "research_metadata_graph_display_schema_version", "v1")
    stage = getattr(settings, "research_metadata_graph_display_stage", "display_contract_skeleton")
    dangerous_flags = {
        "active_ui_enabled": getattr(settings, "research_metadata_graph_display_allow_active_ui", False),
        "frontend_components_enabled": getattr(
            settings,
            "research_metadata_graph_display_allow_frontend_components",
            False,
        ),
        "desktop_components_enabled": getattr(
            settings,
            "research_metadata_graph_display_allow_desktop_components",
            False,
        ),
        "graph_database_enabled": getattr(settings, "research_metadata_graph_display_allow_graph_database", False),
        "persistent_writes_enabled": getattr(
            settings,
            "research_metadata_graph_display_allow_persistent_writes",
            False,
        ),
        "graph_traversal_enabled": getattr(settings, "research_metadata_graph_display_allow_graph_traversal", False),
        "graph_search_enabled": getattr(settings, "research_metadata_graph_display_allow_graph_search", False),
        "graph_ranking_enabled": getattr(settings, "research_metadata_graph_display_allow_graph_ranking", False),
        "graph_retrieval_enabled": getattr(settings, "research_metadata_graph_display_allow_graph_retrieval", False),
        "embeddings_enabled": getattr(settings, "research_metadata_graph_display_allow_embeddings", False),
        "vector_store_enabled": getattr(settings, "research_metadata_graph_display_allow_vector_store", False),
        "active_ingestion_enabled": getattr(
            settings,
            "research_metadata_graph_display_allow_active_ingestion",
            False,
        ),
        "file_uploads_enabled": getattr(settings, "research_metadata_graph_display_allow_file_uploads", False),
        "file_downloads_enabled": getattr(settings, "research_metadata_graph_display_allow_file_downloads", False),
        "file_previews_enabled": getattr(settings, "research_metadata_graph_display_allow_file_previews", False),
        "paper_parsing_enabled": getattr(settings, "research_metadata_graph_display_allow_paper_parsing", False),
        "strategy_generation_enabled": getattr(
            settings,
            "research_metadata_graph_display_allow_strategy_generation",
            False,
        ),
        "backtesting_enabled": getattr(settings, "research_metadata_graph_display_allow_backtesting", False),
        "recommendations_enabled": getattr(settings, "research_metadata_graph_display_allow_recommendations", False),
        "execution_enabled": getattr(settings, "research_metadata_graph_display_allow_execution", False),
    }
    healthy = enabled and stage == "display_contract_skeleton" and not any(dangerous_flags.values())
    return ResearchMetadataGraphDisplayHealthStatus(
        service="stark-terminal-research-metadata-graph-display",
        enabled=enabled,
        stage=stage,
        schema_version=schema_version,
        display_contract_skeleton_only=True,
        read_only=True,
        unavailable_by_default=True,
        forbidden_action_count=len(research_metadata_graph_display_forbidden_actions()),
        **dangerous_flags,
        status="healthy" if healthy else "blocked",
    )
