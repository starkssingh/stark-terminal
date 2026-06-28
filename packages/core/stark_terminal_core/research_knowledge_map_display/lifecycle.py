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


class KnowledgeMapLifecycleDisplayState(StrEnum):
    PLANNED = "PLANNED"
    REFERENCED = "REFERENCED"
    DRAFT = "DRAFT"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCKED = "BLOCKED"
    DEFERRED = "DEFERRED"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


FORBIDDEN_LIFECYCLE_DISPLAY_MEANINGS = {
    "INDEXED",
    "SEARCHABLE",
    "RANKED",
    "EMBEDDED",
    "RETRIEVED",
    "VALIDATED_STRATEGY",
    "BACKTESTED_PROFITABLE",
    "RECOMMENDED",
    "READY_TO_TRADE",
    "EXECUTABLE",
}


class KnowledgeMapLifecycleDisplayPlaceholder(BaseModel):
    lifecycle_display_id: str
    state: KnowledgeMapLifecycleDisplayState
    display_label: str
    descriptive_only: bool = True
    indexed: bool = False
    searchable: bool = False
    ranked: bool = False
    embedded: bool = False
    retrieved: bool = False
    validated_strategy: bool = False
    backtested_profitable: bool = False
    recommended: bool = False
    ready_to_trade: bool = False
    executable: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("lifecycle_display_id", "display_label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map lifecycle display placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def lifecycle_display_must_not_imply_forbidden_meanings(self) -> KnowledgeMapLifecycleDisplayPlaceholder:
        if not self.descriptive_only:
            raise ValueError("Research Knowledge Map lifecycle display placeholders must remain descriptive only")
        if self.state.value in FORBIDDEN_LIFECYCLE_DISPLAY_MEANINGS:
            raise ValueError("Research Knowledge Map lifecycle display state cannot imply unsafe capability")
        dangerous_flags = {
            "indexed": self.indexed,
            "searchable": self.searchable,
            "ranked": self.ranked,
            "embedded": self.embedded,
            "retrieved": self.retrieved,
            "validated strategy": self.validated_strategy,
            "backtested profitable": self.backtested_profitable,
            "recommended": self.recommended,
            "ready-to-trade": self.ready_to_trade,
            "executable": self.executable,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Research Knowledge Map lifecycle display cannot imply: " + ", ".join(enabled))
        return self


class KnowledgeMapLifecycleBadgePlaceholder(KnowledgeMapLifecycleDisplayPlaceholder):
    badge_placeholder_only: bool = True


def default_knowledge_map_lifecycle_display_placeholder() -> KnowledgeMapLifecycleDisplayPlaceholder:
    return KnowledgeMapLifecycleDisplayPlaceholder(
        lifecycle_display_id="research-knowledge-map-lifecycle-display-placeholder-v1",
        state=KnowledgeMapLifecycleDisplayState.PLANNED,
        display_label="Knowledge map lifecycle display placeholder",
        notes=["Lifecycle display is descriptive only and does not imply indexed, recommended, or executable state."],
    )


def default_knowledge_map_lifecycle_badge_placeholder() -> KnowledgeMapLifecycleBadgePlaceholder:
    return KnowledgeMapLifecycleBadgePlaceholder(
        lifecycle_display_id="research-knowledge-map-lifecycle-badge-placeholder-v1",
        state=KnowledgeMapLifecycleDisplayState.UNAVAILABLE,
        display_label="Knowledge map lifecycle badge placeholder",
        notes=["Badge placeholder is unavailable and cannot imply ready-to-trade or executable status."],
    )
