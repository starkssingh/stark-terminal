from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_knowledge_map.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class KnowledgeMapRelationshipDisplayPlaceholder(BaseModel):
    placeholder_id: str
    relationship_kind: str
    display_label: str
    descriptive_only: bool = True
    traversal_enabled: bool = False
    relationship_ranking_enabled: bool = False
    artifact_retrieval_enabled: bool = False
    strategy_quality_inference_enabled: bool = False
    recommendation_implied: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("placeholder_id", "relationship_kind", "display_label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map relationship display placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def relationship_display_must_remain_descriptive(self) -> KnowledgeMapRelationshipDisplayPlaceholder:
        if not self.descriptive_only:
            raise ValueError("Research Knowledge Map relationship display placeholders must be descriptive only")
        dangerous_flags = {
            "traversal": self.traversal_enabled,
            "relationship ranking": self.relationship_ranking_enabled,
            "artifact retrieval": self.artifact_retrieval_enabled,
            "strategy quality inference": self.strategy_quality_inference_enabled,
            "recommendation implication": self.recommendation_implied,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Research Knowledge Map relationship display cannot enable: " + ", ".join(enabled))
        return self


class SupportsRelationshipDisplayPlaceholder(KnowledgeMapRelationshipDisplayPlaceholder):
    relationship_kind: str = "SUPPORTS_RELATIONSHIP_DISPLAY_PLACEHOLDER"


class ContradictsRelationshipDisplayPlaceholder(KnowledgeMapRelationshipDisplayPlaceholder):
    relationship_kind: str = "CONTRADICTS_RELATIONSHIP_DISPLAY_PLACEHOLDER"


class DerivedFromRelationshipDisplayPlaceholder(KnowledgeMapRelationshipDisplayPlaceholder):
    relationship_kind: str = "DERIVED_FROM_RELATIONSHIP_DISPLAY_PLACEHOLDER"


class DependsOnRelationshipDisplayPlaceholder(KnowledgeMapRelationshipDisplayPlaceholder):
    relationship_kind: str = "DEPENDS_ON_RELATIONSHIP_DISPLAY_PLACEHOLDER"


class EvaluatesRelationshipDisplayPlaceholder(KnowledgeMapRelationshipDisplayPlaceholder):
    relationship_kind: str = "EVALUATES_RELATIONSHIP_DISPLAY_PLACEHOLDER"


class ReferencesRelationshipDisplayPlaceholder(KnowledgeMapRelationshipDisplayPlaceholder):
    relationship_kind: str = "REFERENCES_RELATIONSHIP_DISPLAY_PLACEHOLDER"


def default_research_knowledge_map_relationship_display_placeholder() -> KnowledgeMapRelationshipDisplayPlaceholder:
    return KnowledgeMapRelationshipDisplayPlaceholder(
        placeholder_id="research-knowledge-map-relationship-display-placeholder-v1",
        relationship_kind="RESEARCH_KNOWLEDGE_MAP_RELATIONSHIP_DISPLAY_PLACEHOLDER",
        display_label="Knowledge map relationship display placeholder",
        notes=["Descriptive display metadata only; no traversal, ranking, retrieval, or recommendation."],
    )


def default_knowledge_map_relationship_display_placeholders() -> dict[str, KnowledgeMapRelationshipDisplayPlaceholder]:
    return {
        "supports": SupportsRelationshipDisplayPlaceholder(
            placeholder_id="research-knowledge-map-supports-display-v1",
            display_label="Supports relationship display placeholder",
        ),
        "contradicts": ContradictsRelationshipDisplayPlaceholder(
            placeholder_id="research-knowledge-map-contradicts-display-v1",
            display_label="Contradicts relationship display placeholder",
        ),
        "derived_from": DerivedFromRelationshipDisplayPlaceholder(
            placeholder_id="research-knowledge-map-derived-from-display-v1",
            display_label="Derived-from relationship display placeholder",
        ),
        "depends_on": DependsOnRelationshipDisplayPlaceholder(
            placeholder_id="research-knowledge-map-depends-on-display-v1",
            display_label="Depends-on relationship display placeholder",
        ),
        "evaluates": EvaluatesRelationshipDisplayPlaceholder(
            placeholder_id="research-knowledge-map-evaluates-display-v1",
            display_label="Evaluates relationship display placeholder",
        ),
        "references": ReferencesRelationshipDisplayPlaceholder(
            placeholder_id="research-knowledge-map-references-display-v1",
            display_label="References relationship display placeholder",
        ),
    }
