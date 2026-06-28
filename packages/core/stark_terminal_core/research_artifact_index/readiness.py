from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactIndexReadinessReport(BaseModel):
    index_planning_ready: bool
    ready_for_api_contract_skeleton: bool
    indexing_engine_enabled: bool = False
    search_engine_enabled: bool = False
    ranking_engine_enabled: bool = False
    retrieval_engine_enabled: bool = False
    embeddings_enabled: bool = False
    vector_store_enabled: bool = False
    active_ingestion_enabled: bool = False
    persistent_storage_enabled: bool = False
    file_uploads_enabled: bool = False
    file_downloads_enabled: bool = False
    file_previews_enabled: bool = False
    paper_parsing_enabled: bool = False
    strategy_generation_enabled: bool = False
    backtesting_enabled: bool = False
    recommendations_enabled: bool = False
    execution_enabled: bool = False
    next_allowed_phase: str = "api_contract_skeleton"
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("next_allowed_phase", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index readiness text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def readiness_must_be_planning_only(self) -> ResearchArtifactIndexReadinessReport:
        dangerous_flags = {
            "indexing engine": self.indexing_engine_enabled,
            "search engine": self.search_engine_enabled,
            "ranking engine": self.ranking_engine_enabled,
            "retrieval engine": self.retrieval_engine_enabled,
            "embeddings": self.embeddings_enabled,
            "vector store": self.vector_store_enabled,
            "active ingestion": self.active_ingestion_enabled,
            "persistent storage": self.persistent_storage_enabled,
            "file uploads": self.file_uploads_enabled,
            "file downloads": self.file_downloads_enabled,
            "file previews": self.file_previews_enabled,
            "paper parsing": self.paper_parsing_enabled,
            "strategy generation": self.strategy_generation_enabled,
            "backtesting": self.backtesting_enabled,
            "recommendations": self.recommendations_enabled,
            "execution": self.execution_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"research artifact index readiness cannot enable: {', '.join(enabled)}")
        if self.next_allowed_phase != "api_contract_skeleton":
            raise ValueError("Research Artifact Index next phase must be api_contract_skeleton")
        return self


def research_artifact_index_readiness(settings: object | None = None) -> ResearchArtifactIndexReadinessReport:
    schema_version = getattr(settings, "research_artifact_index_schema_version", "v1")
    return ResearchArtifactIndexReadinessReport(
        index_planning_ready=True,
        ready_for_api_contract_skeleton=True,
        schema_version=schema_version,
    )
