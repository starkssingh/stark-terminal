from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_knowledge_map.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class KnowledgeMapRelationshipKind(StrEnum):
    SUPPORTS = "SUPPORTS"
    CONTRADICTS = "CONTRADICTS"
    DERIVED_FROM = "DERIVED_FROM"
    DEPENDS_ON = "DEPENDS_ON"
    EVALUATES = "EVALUATES"
    REFERENCES = "REFERENCES"


class KnowledgeMapRelationshipPlaceholder(BaseModel):
    relationship_id: str
    relationship_kind: KnowledgeMapRelationshipKind
    label: str
    description: str
    descriptive_only: bool = True
    read_only: bool = True
    persisted: bool = False
    traversal_enabled: bool = False
    relationship_ranking_enabled: bool = False
    artifact_retrieval_enabled: bool = False
    strategy_quality_inference_enabled: bool = False
    recommendations_enabled: bool = False
    execution_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("relationship_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map relationship text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def relationship_must_remain_placeholder(self) -> KnowledgeMapRelationshipPlaceholder:
        if not self.descriptive_only or not self.read_only:
            raise ValueError("research knowledge map relationships are descriptive read-only placeholders")
        dangerous_flags = {
            "persist relationships": self.persisted,
            "traverse graph": self.traversal_enabled,
            "rank relationships": self.relationship_ranking_enabled,
            "retrieve artifacts": self.artifact_retrieval_enabled,
            "infer strategy quality": self.strategy_quality_inference_enabled,
            "recommendations": self.recommendations_enabled,
            "execution": self.execution_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("research knowledge map relationship placeholder cannot enable: " + ", ".join(enabled))
        return self


class SupportsRelationshipPlaceholder(KnowledgeMapRelationshipPlaceholder):
    relationship_kind: KnowledgeMapRelationshipKind = KnowledgeMapRelationshipKind.SUPPORTS


class ContradictsRelationshipPlaceholder(KnowledgeMapRelationshipPlaceholder):
    relationship_kind: KnowledgeMapRelationshipKind = KnowledgeMapRelationshipKind.CONTRADICTS


class DerivedFromRelationshipPlaceholder(KnowledgeMapRelationshipPlaceholder):
    relationship_kind: KnowledgeMapRelationshipKind = KnowledgeMapRelationshipKind.DERIVED_FROM


class DependsOnRelationshipPlaceholder(KnowledgeMapRelationshipPlaceholder):
    relationship_kind: KnowledgeMapRelationshipKind = KnowledgeMapRelationshipKind.DEPENDS_ON


class EvaluatesRelationshipPlaceholder(KnowledgeMapRelationshipPlaceholder):
    relationship_kind: KnowledgeMapRelationshipKind = KnowledgeMapRelationshipKind.EVALUATES


class ReferencesRelationshipPlaceholder(KnowledgeMapRelationshipPlaceholder):
    relationship_kind: KnowledgeMapRelationshipKind = KnowledgeMapRelationshipKind.REFERENCES


def default_research_knowledge_map_relationship_placeholders() -> list[KnowledgeMapRelationshipPlaceholder]:
    return [
        SupportsRelationshipPlaceholder(
            relationship_id="research-knowledge-map-supports-relationship-placeholder",
            label="Supports relationship placeholder",
            description="Descriptive support relationship only; no ranking or recommendation.",
        ),
        ContradictsRelationshipPlaceholder(
            relationship_id="research-knowledge-map-contradicts-relationship-placeholder",
            label="Contradicts relationship placeholder",
            description="Descriptive contradiction relationship only; no inference engine.",
        ),
        DerivedFromRelationshipPlaceholder(
            relationship_id="research-knowledge-map-derived-from-relationship-placeholder",
            label="Derived-from relationship placeholder",
            description="Descriptive derivation relationship only; no traversal or retrieval.",
        ),
        DependsOnRelationshipPlaceholder(
            relationship_id="research-knowledge-map-depends-on-relationship-placeholder",
            label="Depends-on relationship placeholder",
            description="Descriptive dependency relationship only; no graph database write.",
        ),
        EvaluatesRelationshipPlaceholder(
            relationship_id="research-knowledge-map-evaluates-relationship-placeholder",
            label="Evaluates relationship placeholder",
            description="Descriptive evaluation relationship only; no strategy quality inference.",
        ),
        ReferencesRelationshipPlaceholder(
            relationship_id="research-knowledge-map-references-relationship-placeholder",
            label="References relationship placeholder",
            description="Descriptive reference relationship only; no lookup, search, or retrieval.",
        ),
    ]
