from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_metadata_graph.lifecycle import (
    FORBIDDEN_LIFECYCLE_MEANINGS,
    GraphLifecycleState,
)
from stark_terminal_core.research_metadata_graph.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class GraphLifecycleDisplayPlaceholder(BaseModel):
    placeholder_id: str
    state: GraphLifecycleState
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

    @field_validator("placeholder_id", "display_label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph lifecycle display placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def lifecycle_display_must_not_imply_forbidden_meanings(self) -> GraphLifecycleDisplayPlaceholder:
        if not self.descriptive_only:
            raise ValueError("Research Metadata Graph lifecycle display placeholders must be descriptive only")
        if self.state.value in FORBIDDEN_LIFECYCLE_MEANINGS:
            raise ValueError("Research Metadata Graph lifecycle display state cannot imply unsafe capability")
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
            raise ValueError("Research Metadata Graph lifecycle display placeholder cannot imply: " + ", ".join(enabled))
        return self


class GraphLifecycleBadgePlaceholder(GraphLifecycleDisplayPlaceholder):
    badge_kind: str = "GRAPH_LIFECYCLE_BADGE_PLACEHOLDER"

    @field_validator("badge_kind")
    @classmethod
    def badge_kind_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph lifecycle badge text")


def default_graph_lifecycle_display_placeholder() -> GraphLifecycleDisplayPlaceholder:
    return GraphLifecycleDisplayPlaceholder(
        placeholder_id="research-metadata-graph-lifecycle-display-placeholder-v1",
        state=GraphLifecycleState.PLANNED,
        display_label="Graph lifecycle display placeholder",
        notes=["Allowed lifecycle display metadata only; no indexed, ranked, recommended, or executable meaning."],
    )


def default_graph_lifecycle_badge_placeholder() -> GraphLifecycleBadgePlaceholder:
    return GraphLifecycleBadgePlaceholder(
        placeholder_id="research-metadata-graph-lifecycle-badge-placeholder-v1",
        state=GraphLifecycleState.UNAVAILABLE,
        display_label="Graph lifecycle badge placeholder",
        notes=["Unavailable lifecycle badge placeholder only; no active UI rendering."],
    )
