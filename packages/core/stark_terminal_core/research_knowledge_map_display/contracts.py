from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_knowledge_map.planning import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)
from stark_terminal_core.research_knowledge_map_display.init import SERVICE_NAME


class ResearchKnowledgeMapDisplayContract(BaseModel):
    contract_id: str
    service: str = SERVICE_NAME
    stage: str = "display_contract_skeleton"
    schema_version: str = "v1"
    display_contract_skeleton_only: bool = True
    read_only: bool = True
    unavailable_by_default: bool = True
    active_ui_enabled: bool = False
    frontend_components_enabled: bool = False
    desktop_components_enabled: bool = False
    active_map_enabled: bool = False
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
        return non_empty_text(value, "research knowledge map display contract text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def contract_must_fail_closed(self) -> ResearchKnowledgeMapDisplayContract:
        if self.service != SERVICE_NAME:
            raise ValueError("Research Knowledge Map Display service name is fixed")
        if self.stage != "display_contract_skeleton":
            raise ValueError("Research Knowledge Map Display stage must be display_contract_skeleton")
        if not self.display_contract_skeleton_only:
            raise ValueError("Research Knowledge Map Display contract must remain skeleton-only")
        if not self.read_only:
            raise ValueError("Research Knowledge Map Display contract must be read-only")
        if not self.unavailable_by_default:
            raise ValueError("Research Knowledge Map Display contract must be unavailable-by-default")
        dangerous_flags = {
            "active UI": self.active_ui_enabled,
            "frontend components": self.frontend_components_enabled,
            "desktop components": self.desktop_components_enabled,
            "active knowledge map": self.active_map_enabled,
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
            raise ValueError("Research Knowledge Map Display contract cannot enable: " + ", ".join(enabled))
        return self


def default_research_knowledge_map_display_contract(
    settings: object | None = None,
) -> ResearchKnowledgeMapDisplayContract:
    schema_version = getattr(settings, "research_knowledge_map_display_schema_version", "v1")
    return ResearchKnowledgeMapDisplayContract(
        contract_id="research-knowledge-map-display-contract-v1",
        schema_version=schema_version,
    )
