from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_metadata_graph.planning import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


SERVICE_NAME = "stark-terminal-research-metadata-graph-api"


class ResearchMetadataGraphApiContract(BaseModel):
    contract_id: str
    service: str = SERVICE_NAME
    stage: str = "api_contract_skeleton"
    schema_version: str = "v1"
    read_only: bool = True
    unavailable_by_default: bool = True
    api_contract_skeleton_only: bool = True
    graph_database_enabled: bool = False
    persistent_writes_enabled: bool = False
    graph_traversal_enabled: bool = False
    graph_search_enabled: bool = False
    graph_ranking_enabled: bool = False
    graph_retrieval_enabled: bool = False
    embeddings_enabled: bool = False
    vector_store_enabled: bool = False
    active_ingestion_enabled: bool = False
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
        return non_empty_text(value, "research metadata graph API contract text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def contract_must_fail_closed(self) -> ResearchMetadataGraphApiContract:
        if self.service != SERVICE_NAME:
            raise ValueError("Research Metadata Graph API service name is fixed")
        if self.stage != "api_contract_skeleton":
            raise ValueError("Research Metadata Graph API stage must be api_contract_skeleton")
        if not self.read_only:
            raise ValueError("Research Metadata Graph API contract must be read-only")
        if not self.unavailable_by_default:
            raise ValueError("Research Metadata Graph API contract must be unavailable-by-default")
        if not self.api_contract_skeleton_only:
            raise ValueError("Research Metadata Graph API contract must remain skeleton-only")
        dangerous_flags = {
            "graph database": self.graph_database_enabled,
            "persistent writes": self.persistent_writes_enabled,
            "graph traversal": self.graph_traversal_enabled,
            "graph search": self.graph_search_enabled,
            "graph ranking": self.graph_ranking_enabled,
            "graph retrieval": self.graph_retrieval_enabled,
            "embeddings": self.embeddings_enabled,
            "vector store": self.vector_store_enabled,
            "active ingestion": self.active_ingestion_enabled,
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
            raise ValueError("Research Metadata Graph API contract cannot enable: " + ", ".join(enabled))
        return self


def default_research_metadata_graph_api_contract(
    settings: object | None = None,
) -> ResearchMetadataGraphApiContract:
    schema_version = getattr(settings, "research_metadata_graph_api_schema_version", "v1")
    return ResearchMetadataGraphApiContract(
        contract_id="research-metadata-graph-api-contract-v1",
        schema_version=schema_version,
    )
