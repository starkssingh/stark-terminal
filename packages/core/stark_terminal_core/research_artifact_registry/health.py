from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.research_artifact_registry.interactions import (
    default_research_artifact_forbidden_interactions,
)
from stark_terminal_core.research_artifact_registry.placeholders import (
    default_research_artifact_registry_planning_contract,
)


class ResearchArtifactRegistryHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    stage: str
    planning_only: bool
    unavailable_by_default: bool
    artifact_kind_count: int
    metadata_placeholder_count: int
    reference_placeholder_count: int
    provenance_placeholder_count: int
    lifecycle_placeholder_count: int
    forbidden_interaction_count: int
    active_ingestion_enabled: bool
    persistent_storage_enabled: bool
    file_uploads_enabled: bool
    file_downloads_enabled: bool
    paper_parsing_enabled: bool
    pdf_parsing_enabled: bool
    arxiv_ingestion_enabled: bool
    llm_analysis_enabled: bool
    strategy_generation_enabled: bool
    backtesting_enabled: bool
    recommendations_enabled: bool
    execution_enabled: bool
    broker_controls_enabled: bool = False
    readiness_to_trade_enabled: bool = False
    active_decision_objects_enabled: bool = False
    status: str
    error: str | None = None


def check_research_artifact_registry_health(settings: object | None = None) -> ResearchArtifactRegistryHealthStatus:
    contract = default_research_artifact_registry_planning_contract()
    forbidden = default_research_artifact_forbidden_interactions()
    enabled = getattr(settings, "research_artifact_registry_enabled", True)
    schema_version = getattr(settings, "research_artifact_registry_schema_version", "v1")
    stage = getattr(settings, "research_artifact_registry_stage", "planning")
    dangerous_flags = {
        "active_ingestion_enabled": getattr(settings, "research_artifact_registry_allow_active_ingestion", False),
        "persistent_storage_enabled": getattr(settings, "research_artifact_registry_allow_persistent_storage", False),
        "file_uploads_enabled": getattr(settings, "research_artifact_registry_allow_file_uploads", False),
        "file_downloads_enabled": getattr(settings, "research_artifact_registry_allow_file_downloads", False),
        "paper_parsing_enabled": getattr(settings, "research_artifact_registry_allow_paper_parsing", False),
        "pdf_parsing_enabled": getattr(settings, "research_artifact_registry_allow_pdf_parsing", False),
        "arxiv_ingestion_enabled": getattr(settings, "research_artifact_registry_allow_arxiv_ingestion", False),
        "llm_analysis_enabled": getattr(settings, "research_artifact_registry_allow_llm_analysis", False),
        "strategy_generation_enabled": getattr(settings, "research_artifact_registry_allow_strategy_generation", False),
        "backtesting_enabled": getattr(settings, "research_artifact_registry_allow_backtesting", False),
        "recommendations_enabled": getattr(settings, "research_artifact_registry_allow_recommendations", False),
        "execution_enabled": getattr(settings, "research_artifact_registry_allow_execution", False),
    }
    error = None
    if any(dangerous_flags.values()):
        error = "Research Artifact Registry dangerous settings must remain disabled"
    if stage not in {"planning", "audit_only", "blocked"}:
        error = "Research Artifact Registry stage is unsupported"
    return ResearchArtifactRegistryHealthStatus(
        enabled=enabled,
        schema_version=schema_version,
        stage=stage,
        planning_only=contract.planning_only,
        unavailable_by_default=contract.unavailable_by_default,
        artifact_kind_count=len(contract.artifact_kinds),
        metadata_placeholder_count=len(contract.metadata_placeholders),
        reference_placeholder_count=len(contract.reference_placeholders),
        provenance_placeholder_count=len(contract.provenance_placeholders),
        lifecycle_placeholder_count=len(contract.lifecycle_placeholders),
        forbidden_interaction_count=len(forbidden),
        **dangerous_flags,
        status="healthy" if error is None and enabled else "disabled",
        error=error,
    )

