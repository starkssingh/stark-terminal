from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator


SERVICE_NAME = "stark-terminal-research-metadata-graph"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def non_empty_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


def sanitized_text_list(value: list[str]) -> list[str]:
    normalized = [item.strip() for item in value if item.strip()]
    if len(normalized) != len(value):
        raise ValueError("text lists cannot contain empty values")
    return normalized


class ResearchMetadataGraphPlanningContract(BaseModel):
    contract_id: str
    service: str = SERVICE_NAME
    stage: str = "planning_and_guardrails"
    schema_version: str = "v1"
    read_only: bool = True
    unavailable_by_default: bool = True
    planning_only: bool = True
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
    notes: list[str] = Field(default_factory=list)

    @field_validator("contract_id", "service", "stage", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph planning contract text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def contract_must_remain_planning_only(self) -> ResearchMetadataGraphPlanningContract:
        if self.service != SERVICE_NAME:
            raise ValueError("research metadata graph service name is fixed")
        if self.stage != "planning_and_guardrails":
            raise ValueError("research metadata graph stage must be planning_and_guardrails")
        if not self.read_only:
            raise ValueError("research metadata graph planning contract must be read-only")
        if not self.unavailable_by_default:
            raise ValueError("research metadata graph planning contract must be unavailable-by-default")
        if not self.planning_only:
            raise ValueError("research metadata graph planning contract must remain planning-only")
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
            raise ValueError("research metadata graph planning cannot enable: " + ", ".join(enabled))
        return self


def default_research_metadata_graph_planning_contract(
    settings: object | None = None,
) -> ResearchMetadataGraphPlanningContract:
    schema_version = getattr(settings, "research_metadata_graph_schema_version", "v1")
    return ResearchMetadataGraphPlanningContract(
        contract_id="research-metadata-graph-planning-contract-v1",
        schema_version=schema_version,
        notes=[
            "Planning and guardrails only.",
            "No graph database, traversal, search, retrieval, embeddings, storage, recommendations, or execution.",
        ],
    )
