from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_metadata_graph.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class GraphLifecycleState(StrEnum):
    PLANNED = "PLANNED"
    REFERENCED = "REFERENCED"
    DRAFT = "DRAFT"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCKED = "BLOCKED"
    DEFERRED = "DEFERRED"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


FORBIDDEN_LIFECYCLE_MEANINGS = {
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


class GraphLifecycleReferencePlaceholder(BaseModel):
    lifecycle_id: str
    state: GraphLifecycleState
    label: str
    description: str
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

    @field_validator("lifecycle_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph lifecycle text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def lifecycle_must_not_imply_forbidden_meanings(self) -> GraphLifecycleReferencePlaceholder:
        if not self.descriptive_only:
            raise ValueError("graph lifecycle placeholders must remain descriptive only")
        if self.state.value in FORBIDDEN_LIFECYCLE_MEANINGS:
            raise ValueError("graph lifecycle state cannot imply unsafe capability")
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
            raise ValueError("graph lifecycle placeholder cannot imply: " + ", ".join(enabled))
        return self


def default_graph_lifecycle_reference_placeholder() -> GraphLifecycleReferencePlaceholder:
    return GraphLifecycleReferencePlaceholder(
        lifecycle_id="research-metadata-graph-lifecycle-placeholder",
        state=GraphLifecycleState.PLANNED,
        label="Graph lifecycle placeholder",
        description="Planning lifecycle placeholder; no indexed, searchable, ranked, recommended, or executable meaning.",
    )
