from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactIndexApiUnavailableResponse(BaseModel):
    unavailable: bool = True
    reason: str
    allowed_stage: str = "api_contract_skeleton"
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
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("reason", "allowed_stage", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index API unavailable response text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def unavailable_response_must_fail_closed(self) -> ResearchArtifactIndexApiUnavailableResponse:
        if not self.unavailable:
            raise ValueError("Research Artifact Index API unavailable response must remain unavailable")
        if self.allowed_stage != "api_contract_skeleton":
            raise ValueError("Research Artifact Index API unavailable response stage must be api_contract_skeleton")
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
            raise ValueError(f"Research Artifact Index API unavailable response cannot enable: {', '.join(enabled)}")
        return self


def unavailable_response_template() -> ResearchArtifactIndexApiUnavailableResponse:
    return ResearchArtifactIndexApiUnavailableResponse(
        reason=(
            "Research Artifact Index API is a read-only contract skeleton; indexing, search, ranking, "
            "retrieval, embeddings, vector store, ingestion, storage, file upload/download/preview, "
            "paper parsing, strategy generation, backtesting, recommendations, and execution are unavailable."
        ),
    )
