from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_metadata_graph.planning import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchMetadataGraphDisplayUnavailableResponse(BaseModel):
    unavailable: bool = True
    reason: str
    allowed_stage: str = "display_contract_skeleton"
    active_ui_enabled: bool = False
    frontend_components_enabled: bool = False
    desktop_components_enabled: bool = False
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
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("reason", "allowed_stage", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph display unavailable response text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def unavailable_response_must_fail_closed(self) -> ResearchMetadataGraphDisplayUnavailableResponse:
        if not self.unavailable:
            raise ValueError("Research Metadata Graph Display unavailable response must remain unavailable")
        if self.allowed_stage != "display_contract_skeleton":
            raise ValueError("Research Metadata Graph Display unavailable stage must be display_contract_skeleton")
        dangerous_flags = {
            "active UI": self.active_ui_enabled,
            "frontend components": self.frontend_components_enabled,
            "desktop components": self.desktop_components_enabled,
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
            raise ValueError("Research Metadata Graph Display unavailable response cannot enable: " + ", ".join(enabled))
        return self


def unavailable_graph_display_response_template() -> ResearchMetadataGraphDisplayUnavailableResponse:
    return ResearchMetadataGraphDisplayUnavailableResponse(
        reason=(
            "Research Metadata Graph Display is a backend display contract skeleton; active UI, frontend, desktop, "
            "graph database, persistent writes, traversal, query, search, ranking, retrieval, embeddings, vector "
            "store, ingestion, upload/download/preview, paper parsing, strategy generation, backtesting, "
            "recommendations, and execution are unavailable."
        ),
    )
