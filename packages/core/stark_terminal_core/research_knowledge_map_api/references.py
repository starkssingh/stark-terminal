from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_knowledge_map.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class KnowledgeMapApiReferencePlaceholder(BaseModel):
    reference_id: str
    reference_kind: str
    descriptive_only: bool = True
    fetch_enabled: bool = False
    retrieval_enabled: bool = False
    source_truth_validation_enabled: bool = False
    persistence_implied: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("reference_id", "reference_kind", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map API reference placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def reference_must_remain_descriptive(self) -> KnowledgeMapApiReferencePlaceholder:
        if not self.descriptive_only:
            raise ValueError("Research Knowledge Map API references must remain descriptive only")
        dangerous_flags = {
            "fetch": self.fetch_enabled,
            "retrieve": self.retrieval_enabled,
            "validate source truth": self.source_truth_validation_enabled,
            "imply persistence": self.persistence_implied,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Research Knowledge Map API reference placeholder cannot enable: " + ", ".join(enabled))
        return self


class KnowledgeMapItemReferencePlaceholder(KnowledgeMapApiReferencePlaceholder):
    reference_kind: str = "KNOWLEDGE_MAP_ITEM_REFERENCE_PLACEHOLDER"


class KnowledgeMapRelationshipReferencePlaceholder(KnowledgeMapApiReferencePlaceholder):
    reference_kind: str = "KNOWLEDGE_MAP_RELATIONSHIP_REFERENCE_PLACEHOLDER"


class KnowledgeMapProvenanceReferencePlaceholder(KnowledgeMapApiReferencePlaceholder):
    reference_kind: str = "KNOWLEDGE_MAP_PROVENANCE_REFERENCE_PLACEHOLDER"


def default_knowledge_map_api_reference_placeholder() -> KnowledgeMapApiReferencePlaceholder:
    return KnowledgeMapApiReferencePlaceholder(
        reference_id="research-knowledge-map-api-reference-placeholder-v1",
        reference_kind="KNOWLEDGE_MAP_API_REFERENCE_PLACEHOLDER",
        notes=["Descriptive API reference placeholder only; no fetch, retrieval, validation, or persistence."],
    )


def default_knowledge_map_item_reference_placeholder() -> KnowledgeMapItemReferencePlaceholder:
    return KnowledgeMapItemReferencePlaceholder(
        reference_id="research-knowledge-map-api-item-reference-placeholder-v1",
        notes=["Descriptive item reference placeholder only."],
    )


def default_knowledge_map_relationship_reference_placeholder() -> KnowledgeMapRelationshipReferencePlaceholder:
    return KnowledgeMapRelationshipReferencePlaceholder(
        reference_id="research-knowledge-map-api-relationship-reference-placeholder-v1",
        notes=["Descriptive relationship reference placeholder only; no traversal or ranking."],
    )


def default_knowledge_map_provenance_reference_placeholder() -> KnowledgeMapProvenanceReferencePlaceholder:
    return KnowledgeMapProvenanceReferencePlaceholder(
        reference_id="research-knowledge-map-api-provenance-reference-placeholder-v1",
        notes=["Descriptive provenance reference placeholder only; no source truth claim."],
    )
