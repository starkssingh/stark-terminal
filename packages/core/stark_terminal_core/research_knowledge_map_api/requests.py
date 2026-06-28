from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_knowledge_map.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class ResearchKnowledgeMapRequestPlaceholder(BaseModel):
    request_id: str
    request_kind: str
    metadata_only: bool = True
    read_only: bool = True
    lookup_trigger_enabled: bool = False
    traversal_trigger_enabled: bool = False
    search_trigger_enabled: bool = False
    retrieval_trigger_enabled: bool = False
    accepts_file_bytes: bool = False
    accepts_raw_paper_content: bool = False
    accepts_market_data_for_recommendations: bool = False
    accepts_strategy_generation_instructions: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("request_id", "request_kind", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map API request placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def request_must_remain_placeholder_only(self) -> ResearchKnowledgeMapRequestPlaceholder:
        if not self.metadata_only or not self.read_only:
            raise ValueError("Research Knowledge Map API requests are metadata-only read-only placeholders")
        dangerous_flags = {
            "lookup trigger": self.lookup_trigger_enabled,
            "traversal trigger": self.traversal_trigger_enabled,
            "search trigger": self.search_trigger_enabled,
            "retrieval trigger": self.retrieval_trigger_enabled,
            "file bytes": self.accepts_file_bytes,
            "raw paper content": self.accepts_raw_paper_content,
            "market data for recommendations": self.accepts_market_data_for_recommendations,
            "strategy-generation instructions": self.accepts_strategy_generation_instructions,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Research Knowledge Map API request placeholder cannot enable: " + ", ".join(enabled))
        return self


class KnowledgeItemLookupRequestPlaceholder(ResearchKnowledgeMapRequestPlaceholder):
    request_kind: str = "KNOWLEDGE_ITEM_LOOKUP_PLACEHOLDER"


class KnowledgeRelationshipRequestPlaceholder(ResearchKnowledgeMapRequestPlaceholder):
    request_kind: str = "KNOWLEDGE_RELATIONSHIP_PLACEHOLDER"


class KnowledgeEvidenceRequestPlaceholder(ResearchKnowledgeMapRequestPlaceholder):
    request_kind: str = "KNOWLEDGE_EVIDENCE_PLACEHOLDER"


class KnowledgeProvenanceRequestPlaceholder(ResearchKnowledgeMapRequestPlaceholder):
    request_kind: str = "KNOWLEDGE_PROVENANCE_PLACEHOLDER"


def default_knowledge_item_lookup_request_placeholder() -> KnowledgeItemLookupRequestPlaceholder:
    return KnowledgeItemLookupRequestPlaceholder(
        request_id="research-knowledge-map-api-item-request-placeholder-v1",
        notes=["Item lookup request placeholder only; no lookup is triggered."],
    )


def default_knowledge_relationship_request_placeholder() -> KnowledgeRelationshipRequestPlaceholder:
    return KnowledgeRelationshipRequestPlaceholder(
        request_id="research-knowledge-map-api-relationship-request-placeholder-v1",
        notes=["Relationship request placeholder only; no traversal, search, ranking, or retrieval is triggered."],
    )


def default_knowledge_evidence_request_placeholder() -> KnowledgeEvidenceRequestPlaceholder:
    return KnowledgeEvidenceRequestPlaceholder(
        request_id="research-knowledge-map-api-evidence-request-placeholder-v1",
        notes=["Evidence request placeholder only; no truth validation or decision generation is triggered."],
    )


def default_knowledge_provenance_request_placeholder() -> KnowledgeProvenanceRequestPlaceholder:
    return KnowledgeProvenanceRequestPlaceholder(
        request_id="research-knowledge-map-api-provenance-request-placeholder-v1",
        notes=["Provenance request placeholder only; no source fetch or source truth validation is triggered."],
    )


def default_research_knowledge_map_request_placeholder() -> ResearchKnowledgeMapRequestPlaceholder:
    return ResearchKnowledgeMapRequestPlaceholder(
        request_id="research-knowledge-map-api-request-placeholder-v1",
        request_kind="RESEARCH_KNOWLEDGE_MAP_API_REQUEST_PLACEHOLDER",
        notes=["Aggregate API request placeholder; metadata only and fail-closed."],
    )
