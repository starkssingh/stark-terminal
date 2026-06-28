from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_knowledge_map.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)
from stark_terminal_core.research_knowledge_map_api.unavailable import (
    ResearchKnowledgeMapApiUnavailableResponse,
    unavailable_knowledge_map_api_response_template,
)


class ResearchKnowledgeMapResponsePlaceholder(BaseModel):
    response_id: str
    response_kind: str
    unavailable_by_default: bool = True
    placeholder_only: bool = True
    retrieved_map_data_present: bool = False
    search_results_present: bool = False
    rankings_present: bool = False
    embeddings_present: bool = False
    parsed_paper_content_present: bool = False
    generated_strategies_present: bool = False
    backtest_results_present: bool = False
    recommendations_present: bool = False
    execution_controls_present: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)
    unavailable_response: ResearchKnowledgeMapApiUnavailableResponse = Field(
        default_factory=unavailable_knowledge_map_api_response_template
    )

    @field_validator("response_id", "response_kind", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map API response placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def response_must_remain_placeholder_only(self) -> ResearchKnowledgeMapResponsePlaceholder:
        if not self.unavailable_by_default:
            raise ValueError("Research Knowledge Map API response placeholder must be unavailable-by-default")
        if not self.placeholder_only:
            raise ValueError("Research Knowledge Map API response placeholder must remain placeholder-only")
        dangerous_flags = {
            "retrieved map data": self.retrieved_map_data_present,
            "search results": self.search_results_present,
            "rankings": self.rankings_present,
            "embeddings": self.embeddings_present,
            "parsed paper content": self.parsed_paper_content_present,
            "generated strategies": self.generated_strategies_present,
            "backtest results": self.backtest_results_present,
            "recommendations": self.recommendations_present,
            "execution controls": self.execution_controls_present,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Research Knowledge Map API response placeholder cannot include: " + ", ".join(enabled))
        return self


class KnowledgeItemResponsePlaceholder(ResearchKnowledgeMapResponsePlaceholder):
    response_kind: str = "KNOWLEDGE_ITEM_RESPONSE_PLACEHOLDER"


class KnowledgeRelationshipResponsePlaceholder(ResearchKnowledgeMapResponsePlaceholder):
    response_kind: str = "KNOWLEDGE_RELATIONSHIP_RESPONSE_PLACEHOLDER"


class KnowledgeEvidenceResponsePlaceholder(ResearchKnowledgeMapResponsePlaceholder):
    response_kind: str = "KNOWLEDGE_EVIDENCE_RESPONSE_PLACEHOLDER"


class KnowledgeProvenanceResponsePlaceholder(ResearchKnowledgeMapResponsePlaceholder):
    response_kind: str = "KNOWLEDGE_PROVENANCE_RESPONSE_PLACEHOLDER"


def default_knowledge_item_response_placeholder() -> KnowledgeItemResponsePlaceholder:
    return KnowledgeItemResponsePlaceholder(
        response_id="research-knowledge-map-api-item-response-placeholder-v1",
        notes=["No retrieved knowledge map item data is present."],
    )


def default_knowledge_relationship_response_placeholder() -> KnowledgeRelationshipResponsePlaceholder:
    return KnowledgeRelationshipResponsePlaceholder(
        response_id="research-knowledge-map-api-relationship-response-placeholder-v1",
        notes=["No traversal, search, ranking, or retrieval result is present."],
    )


def default_knowledge_evidence_response_placeholder() -> KnowledgeEvidenceResponsePlaceholder:
    return KnowledgeEvidenceResponsePlaceholder(
        response_id="research-knowledge-map-api-evidence-response-placeholder-v1",
        notes=["No research approval, decision, recommendation, or trade readiness is present."],
    )


def default_knowledge_provenance_response_placeholder() -> KnowledgeProvenanceResponsePlaceholder:
    return KnowledgeProvenanceResponsePlaceholder(
        response_id="research-knowledge-map-api-provenance-response-placeholder-v1",
        notes=["No source truth validation or parsed paper content is present."],
    )


def default_research_knowledge_map_response_placeholder() -> ResearchKnowledgeMapResponsePlaceholder:
    return ResearchKnowledgeMapResponsePlaceholder(
        response_id="research-knowledge-map-api-response-placeholder-v1",
        response_kind="RESEARCH_KNOWLEDGE_MAP_API_RESPONSE_PLACEHOLDER",
        notes=["Aggregate API response placeholder; unavailable and fail-closed."],
    )
