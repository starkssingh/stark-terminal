from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactIndexApiContract(BaseModel):
    contract_id: str
    service: str = "stark-terminal-research-artifact-index-api"
    stage: str = "api_contract_skeleton"
    schema_version: str = "v1"
    read_only: bool = True
    unavailable_by_default: bool = True
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
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("contract_id", "service", "stage", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index API contract text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def contract_must_fail_closed(self) -> ResearchArtifactIndexApiContract:
        if self.stage != "api_contract_skeleton":
            raise ValueError("Research Artifact Index API contract stage must be api_contract_skeleton")
        if not self.read_only:
            raise ValueError("Research Artifact Index API contract must be read-only")
        if not self.unavailable_by_default:
            raise ValueError("Research Artifact Index API contract must be unavailable by default")
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
            raise ValueError(f"Research Artifact Index API contract cannot enable: {', '.join(enabled)}")
        return self


def default_research_artifact_index_api_contract() -> ResearchArtifactIndexApiContract:
    return ResearchArtifactIndexApiContract(
        contract_id="research-artifact-index-api-contract-v1",
    )
