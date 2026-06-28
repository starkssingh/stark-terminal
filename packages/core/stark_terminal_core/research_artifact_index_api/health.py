from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings


class ResearchArtifactIndexApiHealthStatus(BaseModel):
    service: str
    enabled: bool
    stage: str
    schema_version: str
    read_only: bool
    unavailable_by_default: bool
    indexing_engine_enabled: bool
    search_engine_enabled: bool
    ranking_engine_enabled: bool
    retrieval_engine_enabled: bool
    embeddings_enabled: bool
    vector_store_enabled: bool
    active_ingestion_enabled: bool
    persistent_storage_enabled: bool
    file_uploads_enabled: bool
    file_downloads_enabled: bool
    file_previews_enabled: bool
    paper_parsing_enabled: bool
    strategy_generation_enabled: bool
    backtesting_enabled: bool
    recommendations_enabled: bool
    execution_enabled: bool
    status: str
    error: str | None = None


def research_artifact_index_api_health(
    settings: Settings | None = None,
) -> ResearchArtifactIndexApiHealthStatus:
    resolved = settings or get_settings()
    dangerous_flags = {
        "indexing_engine_enabled": resolved.research_artifact_index_api_allow_indexing_engine,
        "search_engine_enabled": resolved.research_artifact_index_api_allow_search_engine,
        "ranking_engine_enabled": resolved.research_artifact_index_api_allow_ranking_engine,
        "retrieval_engine_enabled": resolved.research_artifact_index_api_allow_retrieval_engine,
        "embeddings_enabled": resolved.research_artifact_index_api_allow_embeddings,
        "vector_store_enabled": resolved.research_artifact_index_api_allow_vector_store,
        "active_ingestion_enabled": resolved.research_artifact_index_api_allow_active_ingestion,
        "persistent_storage_enabled": resolved.research_artifact_index_api_allow_persistent_storage,
        "file_uploads_enabled": resolved.research_artifact_index_api_allow_file_uploads,
        "file_downloads_enabled": resolved.research_artifact_index_api_allow_file_downloads,
        "file_previews_enabled": resolved.research_artifact_index_api_allow_file_previews,
        "paper_parsing_enabled": resolved.research_artifact_index_api_allow_paper_parsing,
        "strategy_generation_enabled": resolved.research_artifact_index_api_allow_strategy_generation,
        "backtesting_enabled": resolved.research_artifact_index_api_allow_backtesting,
        "recommendations_enabled": resolved.research_artifact_index_api_allow_recommendations,
        "execution_enabled": resolved.research_artifact_index_api_allow_execution,
    }
    has_required_configuration = (
        bool(resolved.research_artifact_index_api_schema_version.strip())
        and resolved.research_artifact_index_api_stage == "api_contract_skeleton"
    )
    error = None
    if any(dangerous_flags.values()) or resolved.execution_apis_enabled:
        error = "Research Artifact Index API contract skeleton flags must remain disabled"
    if not has_required_configuration:
        error = "Research Artifact Index API contract skeleton configuration is invalid"
    status = "healthy" if resolved.research_artifact_index_api_enabled and error is None else "blocked"
    return ResearchArtifactIndexApiHealthStatus(
        service="stark-terminal-research-artifact-index-api",
        enabled=resolved.research_artifact_index_api_enabled,
        stage=resolved.research_artifact_index_api_stage,
        schema_version=resolved.research_artifact_index_api_schema_version,
        read_only=True,
        unavailable_by_default=True,
        **dangerous_flags,
        status=status,
        error=error,
    )
