from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_knowledge_map.planning import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


SERVICE_NAME = "stark-terminal-research-knowledge-map-api"


class ResearchKnowledgeMapApiContract(BaseModel):
    contract_id: str
    service: str = SERVICE_NAME
    stage: str = "api_contract_skeleton"
    schema_version: str = "v1"
    api_contract_skeleton_only: bool = True
    read_only: bool = True
    unavailable_by_default: bool = True
    database_enabled: bool = False
    persistent_writes_enabled: bool = False
    traversal_enabled: bool = False
    search_enabled: bool = False
    ranking_enabled: bool = False
    retrieval_enabled: bool = False
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
        return non_empty_text(value, "research knowledge map API contract text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def contract_must_fail_closed(self) -> ResearchKnowledgeMapApiContract:
        if self.service != SERVICE_NAME:
            raise ValueError("Research Knowledge Map API service name is fixed")
        if self.stage != "api_contract_skeleton":
            raise ValueError("Research Knowledge Map API stage must be api_contract_skeleton")
        if not self.api_contract_skeleton_only:
            raise ValueError("Research Knowledge Map API contract must remain skeleton-only")
        if not self.read_only:
            raise ValueError("Research Knowledge Map API contract must be read-only")
        if not self.unavailable_by_default:
            raise ValueError("Research Knowledge Map API contract must be unavailable-by-default")
        dangerous_flags = {
            "database": self.database_enabled,
            "persistent writes": self.persistent_writes_enabled,
            "traversal": self.traversal_enabled,
            "search": self.search_enabled,
            "ranking": self.ranking_enabled,
            "retrieval": self.retrieval_enabled,
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
            raise ValueError("Research Knowledge Map API contract cannot enable: " + ", ".join(enabled))
        return self


def default_research_knowledge_map_api_contract(
    settings: object | None = None,
) -> ResearchKnowledgeMapApiContract:
    schema_version = getattr(settings, "research_knowledge_map_api_schema_version", "v1")
    return ResearchKnowledgeMapApiContract(
        contract_id="research-knowledge-map-api-contract-v1",
        schema_version=schema_version,
    )
