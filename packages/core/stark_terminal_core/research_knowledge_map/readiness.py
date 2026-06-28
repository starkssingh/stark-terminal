from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_knowledge_map.planning import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchKnowledgeMapReadinessStatus(BaseModel):
    status_id: str = "research-knowledge-map-readiness-v1"
    ready_for_planning: bool = True
    ready_for_api_contract_skeleton: bool = False
    ready_for_active_map: bool = False
    ready_for_database: bool = False
    ready_for_persistent_writes: bool = False
    ready_for_traversal: bool = False
    ready_for_search: bool = False
    ready_for_ranking: bool = False
    ready_for_retrieval: bool = False
    ready_for_embeddings: bool = False
    ready_for_vector_store: bool = False
    ready_for_ingestion: bool = False
    ready_for_file_uploads: bool = False
    ready_for_file_downloads: bool = False
    ready_for_file_previews: bool = False
    ready_for_paper_parsing: bool = False
    ready_for_strategy_generation: bool = False
    ready_for_backtesting: bool = False
    ready_for_recommendations: bool = False
    ready_for_execution: bool = False
    next_allowed_phase: str = "api_contract_skeleton"
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("status_id", "next_allowed_phase", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map readiness text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def readiness_must_remain_planning_only(self) -> ResearchKnowledgeMapReadinessStatus:
        if not self.ready_for_planning:
            raise ValueError("research knowledge map must remain ready for planning")
        dangerous_readiness = {
            "active map": self.ready_for_active_map,
            "database": self.ready_for_database,
            "persistent writes": self.ready_for_persistent_writes,
            "traversal": self.ready_for_traversal,
            "search": self.ready_for_search,
            "ranking": self.ready_for_ranking,
            "retrieval": self.ready_for_retrieval,
            "embeddings": self.ready_for_embeddings,
            "vector store": self.ready_for_vector_store,
            "ingestion": self.ready_for_ingestion,
            "file uploads": self.ready_for_file_uploads,
            "file downloads": self.ready_for_file_downloads,
            "file previews": self.ready_for_file_previews,
            "paper parsing": self.ready_for_paper_parsing,
            "strategy generation": self.ready_for_strategy_generation,
            "backtesting": self.ready_for_backtesting,
            "recommendations": self.ready_for_recommendations,
            "execution": self.ready_for_execution,
        }
        enabled = [name for name, value in dangerous_readiness.items() if value]
        if enabled:
            raise ValueError("research knowledge map readiness cannot allow: " + ", ".join(enabled))
        if self.ready_for_api_contract_skeleton:
            raise ValueError("Research Knowledge Map API contract skeleton readiness is reserved for a future prompt")
        if self.next_allowed_phase != "api_contract_skeleton":
            raise ValueError("Research Knowledge Map next phase must be api_contract_skeleton")
        return self


def research_knowledge_map_readiness(settings: object | None = None) -> ResearchKnowledgeMapReadinessStatus:
    schema_version = getattr(settings, "research_knowledge_map_schema_version", "v1")
    return ResearchKnowledgeMapReadinessStatus(schema_version=schema_version)
