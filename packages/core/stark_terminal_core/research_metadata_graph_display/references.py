from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_metadata_graph.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class GraphReferenceDisplayPlaceholder(BaseModel):
    placeholder_id: str
    reference_kind: str
    display_label: str
    descriptive_only: bool = True
    lookup_enabled: bool = False
    retrieval_enabled: bool = False
    traversal_enabled: bool = False
    search_enabled: bool = False
    ranking_enabled: bool = False
    file_access_enabled: bool = False
    external_fetch_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("placeholder_id", "reference_kind", "display_label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph reference display placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def reference_display_must_remain_descriptive(self) -> GraphReferenceDisplayPlaceholder:
        if not self.descriptive_only:
            raise ValueError("Research Metadata Graph reference display placeholders must be descriptive only")
        dangerous_flags = {
            "lookup": self.lookup_enabled,
            "retrieval": self.retrieval_enabled,
            "traversal": self.traversal_enabled,
            "search": self.search_enabled,
            "ranking": self.ranking_enabled,
            "file access": self.file_access_enabled,
            "external fetch": self.external_fetch_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Research Metadata Graph reference display placeholder cannot enable: " + ", ".join(enabled))
        return self


class GraphDependencyReferenceDisplayPlaceholder(GraphReferenceDisplayPlaceholder):
    reference_kind: str = "GRAPH_DEPENDENCY_REFERENCE_DISPLAY_PLACEHOLDER"


class GraphRelationshipReferenceDisplayPlaceholder(GraphReferenceDisplayPlaceholder):
    reference_kind: str = "GRAPH_RELATIONSHIP_REFERENCE_DISPLAY_PLACEHOLDER"


def default_graph_reference_display_placeholder() -> GraphReferenceDisplayPlaceholder:
    return GraphReferenceDisplayPlaceholder(
        placeholder_id="research-metadata-graph-reference-display-placeholder-v1",
        reference_kind="GRAPH_REFERENCE_DISPLAY_PLACEHOLDER",
        display_label="Graph reference display placeholder",
        notes=["Descriptive reference display only; no lookup, retrieval, traversal, search, ranking, or fetch."],
    )


def default_graph_dependency_reference_display_placeholder() -> GraphDependencyReferenceDisplayPlaceholder:
    return GraphDependencyReferenceDisplayPlaceholder(
        placeholder_id="research-metadata-graph-dependency-reference-display-v1",
        display_label="Graph dependency reference display placeholder",
    )


def default_graph_relationship_reference_display_placeholder() -> GraphRelationshipReferenceDisplayPlaceholder:
    return GraphRelationshipReferenceDisplayPlaceholder(
        placeholder_id="research-metadata-graph-relationship-reference-display-v1",
        display_label="Graph relationship reference display placeholder",
    )
