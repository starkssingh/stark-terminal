from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.research_metadata_graph.edges import (
    default_research_metadata_graph_edge_placeholders,
)
from stark_terminal_core.research_metadata_graph.guardrails import (
    research_metadata_graph_forbidden_actions,
)
from stark_terminal_core.research_metadata_graph.nodes import (
    default_research_metadata_graph_node_placeholders,
)


class ResearchMetadataGraphHealthStatus(BaseModel):
    service: str
    enabled: bool
    stage: str
    schema_version: str
    planning_only: bool
    read_only: bool
    unavailable_by_default: bool
    node_placeholder_count: int
    edge_placeholder_count: int
    forbidden_action_count: int
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


def research_metadata_graph_health(settings: object | None = None) -> ResearchMetadataGraphHealthStatus:
    enabled = getattr(settings, "research_metadata_graph_enabled", True)
    schema_version = getattr(settings, "research_metadata_graph_schema_version", "v1")
    stage = getattr(settings, "research_metadata_graph_stage", "planning_and_guardrails")
    dangerous_flags = {
        "graph_database_enabled": getattr(settings, "research_metadata_graph_allow_graph_database", False),
        "persistent_writes_enabled": getattr(settings, "research_metadata_graph_allow_persistent_writes", False),
        "graph_traversal_enabled": getattr(settings, "research_metadata_graph_allow_graph_traversal", False),
        "graph_search_enabled": getattr(settings, "research_metadata_graph_allow_graph_search", False),
        "graph_ranking_enabled": getattr(settings, "research_metadata_graph_allow_graph_ranking", False),
        "graph_retrieval_enabled": getattr(settings, "research_metadata_graph_allow_graph_retrieval", False),
        "embeddings_enabled": getattr(settings, "research_metadata_graph_allow_embeddings", False),
        "vector_store_enabled": getattr(settings, "research_metadata_graph_allow_vector_store", False),
        "active_ingestion_enabled": getattr(settings, "research_metadata_graph_allow_active_ingestion", False),
        "file_uploads_enabled": getattr(settings, "research_metadata_graph_allow_file_uploads", False),
        "file_downloads_enabled": getattr(settings, "research_metadata_graph_allow_file_downloads", False),
        "file_previews_enabled": getattr(settings, "research_metadata_graph_allow_file_previews", False),
        "paper_parsing_enabled": getattr(settings, "research_metadata_graph_allow_paper_parsing", False),
        "strategy_generation_enabled": getattr(settings, "research_metadata_graph_allow_strategy_generation", False),
        "backtesting_enabled": getattr(settings, "research_metadata_graph_allow_backtesting", False),
        "recommendations_enabled": getattr(settings, "research_metadata_graph_allow_recommendations", False),
        "execution_enabled": getattr(settings, "research_metadata_graph_allow_execution", False),
    }
    healthy = enabled and stage == "planning_and_guardrails" and not any(dangerous_flags.values())
    return ResearchMetadataGraphHealthStatus(
        service="stark-terminal-research-metadata-graph",
        enabled=enabled,
        stage=stage,
        schema_version=schema_version,
        planning_only=True,
        read_only=True,
        unavailable_by_default=True,
        node_placeholder_count=len(default_research_metadata_graph_node_placeholders()),
        edge_placeholder_count=len(default_research_metadata_graph_edge_placeholders()),
        forbidden_action_count=len(research_metadata_graph_forbidden_actions()),
        **dangerous_flags,
        status="healthy" if healthy else "blocked",
    )
