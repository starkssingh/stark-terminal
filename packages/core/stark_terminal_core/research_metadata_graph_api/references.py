from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_metadata_graph.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class GraphApiReferencePlaceholder(BaseModel):
    reference_id: str
    reference_kind: str
    descriptive_only: bool = True
    fetch_enabled: bool = False
    retrieval_enabled: bool = False
    source_truth_validation_enabled: bool = False
    graph_persistence_implied: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("reference_id", "reference_kind", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph API reference placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def reference_must_remain_descriptive(self) -> GraphApiReferencePlaceholder:
        if not self.descriptive_only:
            raise ValueError("Research Metadata Graph API references must remain descriptive only")
        dangerous_flags = {
            "fetch": self.fetch_enabled,
            "retrieve": self.retrieval_enabled,
            "validate source truth": self.source_truth_validation_enabled,
            "imply graph persistence": self.graph_persistence_implied,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Research Metadata Graph API reference placeholder cannot enable: " + ", ".join(enabled))
        return self


class GraphApiNodeReferencePlaceholder(GraphApiReferencePlaceholder):
    reference_kind: str = "GRAPH_API_NODE_REFERENCE_PLACEHOLDER"


class GraphApiEdgeReferencePlaceholder(GraphApiReferencePlaceholder):
    reference_kind: str = "GRAPH_API_EDGE_REFERENCE_PLACEHOLDER"


class GraphApiProvenanceReferencePlaceholder(GraphApiReferencePlaceholder):
    reference_kind: str = "GRAPH_API_PROVENANCE_REFERENCE_PLACEHOLDER"


def default_graph_api_reference_placeholder() -> GraphApiReferencePlaceholder:
    return GraphApiReferencePlaceholder(
        reference_id="research-metadata-graph-api-reference-placeholder-v1",
        reference_kind="GRAPH_API_REFERENCE_PLACEHOLDER",
        notes=["Descriptive API reference placeholder only; no fetch, retrieval, validation, or persistence."],
    )


def default_graph_api_node_reference_placeholder() -> GraphApiNodeReferencePlaceholder:
    return GraphApiNodeReferencePlaceholder(
        reference_id="research-metadata-graph-api-node-reference-placeholder-v1",
        notes=["Descriptive node reference placeholder only."],
    )


def default_graph_api_edge_reference_placeholder() -> GraphApiEdgeReferencePlaceholder:
    return GraphApiEdgeReferencePlaceholder(
        reference_id="research-metadata-graph-api-edge-reference-placeholder-v1",
        notes=["Descriptive edge reference placeholder only."],
    )


def default_graph_api_provenance_reference_placeholder() -> GraphApiProvenanceReferencePlaceholder:
    return GraphApiProvenanceReferencePlaceholder(
        reference_id="research-metadata-graph-api-provenance-reference-placeholder-v1",
        notes=["Descriptive provenance reference placeholder only; no source truth claim."],
    )
