from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings


class ResearchArtifactRegistryDisplayHealthStatus(BaseModel):
    service: str
    enabled: bool
    stage: str
    schema_version: str
    read_only: bool
    unavailable_by_default: bool
    active_ui_enabled: bool
    frontend_components_enabled: bool
    desktop_components_enabled: bool
    active_ingestion_enabled: bool
    persistent_storage_enabled: bool
    file_uploads_enabled: bool
    file_downloads_enabled: bool
    paper_parsing_enabled: bool
    strategy_generation_enabled: bool
    backtesting_enabled: bool
    recommendations_enabled: bool
    execution_enabled: bool
    status: str
    error: str | None = None


def research_artifact_registry_display_health(
    settings: Settings | None = None,
) -> ResearchArtifactRegistryDisplayHealthStatus:
    resolved = settings or get_settings()
    dangerous_flags = {
        "active_ui_enabled": resolved.research_artifact_registry_display_allow_active_ui,
        "frontend_components_enabled": resolved.research_artifact_registry_display_allow_frontend_components,
        "desktop_components_enabled": resolved.research_artifact_registry_display_allow_desktop_components,
        "active_ingestion_enabled": resolved.research_artifact_registry_display_allow_active_ingestion,
        "persistent_storage_enabled": resolved.research_artifact_registry_display_allow_persistent_storage,
        "file_uploads_enabled": resolved.research_artifact_registry_display_allow_file_uploads,
        "file_downloads_enabled": resolved.research_artifact_registry_display_allow_file_downloads,
        "paper_parsing_enabled": resolved.research_artifact_registry_display_allow_paper_parsing,
        "strategy_generation_enabled": resolved.research_artifact_registry_display_allow_strategy_generation,
        "backtesting_enabled": resolved.research_artifact_registry_display_allow_backtesting,
        "recommendations_enabled": resolved.research_artifact_registry_display_allow_recommendations,
        "execution_enabled": resolved.research_artifact_registry_display_allow_execution,
    }
    has_required_configuration = (
        bool(resolved.research_artifact_registry_display_schema_version.strip())
        and resolved.research_artifact_registry_display_stage == "display_contract_skeleton"
    )
    error = None
    if any(dangerous_flags.values()) or resolved.execution_apis_enabled:
        error = "Research Artifact Registry Display contract skeleton flags must remain disabled"
    if not has_required_configuration:
        error = "Research Artifact Registry Display contract skeleton configuration is invalid"
    status = "healthy" if resolved.research_artifact_registry_display_enabled and error is None else "blocked"
    return ResearchArtifactRegistryDisplayHealthStatus(
        service="stark-terminal-research-artifact-registry-display",
        enabled=resolved.research_artifact_registry_display_enabled,
        stage=resolved.research_artifact_registry_display_stage,
        schema_version=resolved.research_artifact_registry_display_schema_version,
        read_only=True,
        unavailable_by_default=True,
        **dangerous_flags,
        status=status,
        error=error,
    )
