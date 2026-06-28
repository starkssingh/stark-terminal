from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.research_artifact_index.interactions import (
    default_research_artifact_index_forbidden_interactions,
)
from stark_terminal_core.research_artifact_index.keys import (
    default_research_artifact_index_key_placeholders,
)
from stark_terminal_core.research_artifact_index.metadata import (
    default_research_artifact_index_metadata_placeholders,
)
from stark_terminal_core.research_artifact_index.provenance import (
    default_research_artifact_index_provenance_placeholders,
)
from stark_terminal_core.research_artifact_index.references import (
    default_research_artifact_index_reference_placeholders,
)
from stark_terminal_core.research_artifact_index.tags import (
    default_research_artifact_index_tag_placeholders,
)


class ResearchArtifactIndexHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    stage: str
    planning_only: bool
    unavailable_by_default: bool
    metadata_placeholder_count: int
    key_placeholder_count: int
    reference_placeholder_count: int
    tag_placeholder_count: int
    provenance_placeholder_count: int
    forbidden_interaction_count: int
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


def check_research_artifact_index_health(settings: object | None = None) -> ResearchArtifactIndexHealthStatus:
    enabled = getattr(settings, "research_artifact_index_enabled", True)
    schema_version = getattr(settings, "research_artifact_index_schema_version", "v1")
    stage = getattr(settings, "research_artifact_index_stage", "planning_and_guardrails")
    dangerous_flags = {
        "indexing_engine_enabled": getattr(settings, "research_artifact_index_allow_indexing_engine", False),
        "search_engine_enabled": getattr(settings, "research_artifact_index_allow_search_engine", False),
        "ranking_engine_enabled": getattr(settings, "research_artifact_index_allow_ranking_engine", False),
        "retrieval_engine_enabled": getattr(settings, "research_artifact_index_allow_retrieval_engine", False),
        "embeddings_enabled": getattr(settings, "research_artifact_index_allow_embeddings", False),
        "vector_store_enabled": getattr(settings, "research_artifact_index_allow_vector_store", False),
        "active_ingestion_enabled": getattr(settings, "research_artifact_index_allow_active_ingestion", False),
        "persistent_storage_enabled": getattr(settings, "research_artifact_index_allow_persistent_storage", False),
        "file_uploads_enabled": getattr(settings, "research_artifact_index_allow_file_uploads", False),
        "file_downloads_enabled": getattr(settings, "research_artifact_index_allow_file_downloads", False),
        "file_previews_enabled": getattr(settings, "research_artifact_index_allow_file_previews", False),
        "paper_parsing_enabled": getattr(settings, "research_artifact_index_allow_paper_parsing", False),
        "pdf_parsing_enabled": getattr(settings, "research_artifact_index_allow_pdf_parsing", False),
        "arxiv_ingestion_enabled": getattr(settings, "research_artifact_index_allow_arxiv_ingestion", False),
        "llm_analysis_enabled": getattr(settings, "research_artifact_index_allow_llm_analysis", False),
        "strategy_generation_enabled": getattr(settings, "research_artifact_index_allow_strategy_generation", False),
        "backtesting_enabled": getattr(settings, "research_artifact_index_allow_backtesting", False),
        "recommendations_enabled": getattr(settings, "research_artifact_index_allow_recommendations", False),
        "execution_enabled": getattr(settings, "research_artifact_index_allow_execution", False),
    }
    error = None
    if any(dangerous_flags.values()):
        error = "Research Artifact Index dangerous settings must remain disabled"
    if stage not in {
        "planning_and_guardrails",
        "api_contract_skeleton",
        "display_contract_skeleton",
        "audit_only",
        "blocked",
    }:
        error = "Research Artifact Index stage is unsupported"
    return ResearchArtifactIndexHealthStatus(
        enabled=enabled,
        schema_version=schema_version,
        stage=stage,
        planning_only=True,
        unavailable_by_default=True,
        metadata_placeholder_count=len(default_research_artifact_index_metadata_placeholders()),
        key_placeholder_count=len(default_research_artifact_index_key_placeholders()),
        reference_placeholder_count=len(default_research_artifact_index_reference_placeholders()),
        tag_placeholder_count=len(default_research_artifact_index_tag_placeholders()),
        provenance_placeholder_count=len(default_research_artifact_index_provenance_placeholders()),
        forbidden_interaction_count=len(default_research_artifact_index_forbidden_interactions()),
        **dangerous_flags,
        status="healthy" if error is None and enabled else "disabled",
        error=error,
    )
