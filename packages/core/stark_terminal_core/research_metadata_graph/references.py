from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_metadata_graph.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class GraphReferencePlaceholder(BaseModel):
    reference_id: str
    label: str
    description: str
    descriptive_only: bool = True
    lookup_enabled: bool = False
    retrieval_enabled: bool = False
    graph_traversal_enabled: bool = False
    graph_search_enabled: bool = False
    graph_ranking_enabled: bool = False
    file_access_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("reference_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph reference text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def reference_must_remain_descriptive(self) -> GraphReferencePlaceholder:
        if not self.descriptive_only:
            raise ValueError("graph references must remain descriptive only")
        dangerous_flags = {
            "lookup": self.lookup_enabled,
            "retrieval": self.retrieval_enabled,
            "graph traversal": self.graph_traversal_enabled,
            "graph search": self.graph_search_enabled,
            "graph ranking": self.graph_ranking_enabled,
            "file access": self.file_access_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("graph reference placeholder cannot enable: " + ", ".join(enabled))
        return self


class GraphDependencyReferencePlaceholder(GraphReferencePlaceholder):
    pass


class GraphRelationshipReferencePlaceholder(GraphReferencePlaceholder):
    pass


def default_graph_reference_placeholders() -> list[GraphReferencePlaceholder]:
    return [
        GraphDependencyReferencePlaceholder(
            reference_id="research-metadata-graph-dependency-reference-placeholder",
            label="Graph dependency reference placeholder",
            description="Descriptive dependency reference only; no lookup, traversal, search, ranking, retrieval, or file access.",
        ),
        GraphRelationshipReferencePlaceholder(
            reference_id="research-metadata-graph-relationship-reference-placeholder",
            label="Graph relationship reference placeholder",
            description="Descriptive relationship reference only; no graph traversal or ranking behavior.",
        ),
    ]
