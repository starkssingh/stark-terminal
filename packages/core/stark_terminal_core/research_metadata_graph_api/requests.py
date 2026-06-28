from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_metadata_graph.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class ResearchMetadataGraphRequestPlaceholder(BaseModel):
    request_id: str
    request_kind: str
    metadata_only: bool = True
    read_only: bool = True
    lookup_trigger_enabled: bool = False
    traversal_trigger_enabled: bool = False
    search_trigger_enabled: bool = False
    retrieval_trigger_enabled: bool = False
    accepts_file_bytes: bool = False
    accepts_raw_paper_content: bool = False
    accepts_market_data_for_recommendations: bool = False
    accepts_strategy_generation_instructions: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("request_id", "request_kind", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph API request placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def request_must_remain_placeholder_only(self) -> ResearchMetadataGraphRequestPlaceholder:
        if not self.metadata_only or not self.read_only:
            raise ValueError("Research Metadata Graph API requests are metadata-only read-only placeholders")
        dangerous_flags = {
            "lookup trigger": self.lookup_trigger_enabled,
            "traversal trigger": self.traversal_trigger_enabled,
            "search trigger": self.search_trigger_enabled,
            "retrieval trigger": self.retrieval_trigger_enabled,
            "file bytes": self.accepts_file_bytes,
            "raw paper content": self.accepts_raw_paper_content,
            "market data for recommendations": self.accepts_market_data_for_recommendations,
            "strategy-generation instructions": self.accepts_strategy_generation_instructions,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Research Metadata Graph API request placeholder cannot enable: " + ", ".join(enabled))
        return self


class GraphNodeLookupRequestPlaceholder(ResearchMetadataGraphRequestPlaceholder):
    request_kind: str = "GRAPH_NODE_LOOKUP_PLACEHOLDER"


class GraphEdgeLookupRequestPlaceholder(ResearchMetadataGraphRequestPlaceholder):
    request_kind: str = "GRAPH_EDGE_LOOKUP_PLACEHOLDER"


class GraphRelationshipRequestPlaceholder(ResearchMetadataGraphRequestPlaceholder):
    request_kind: str = "GRAPH_RELATIONSHIP_PLACEHOLDER"


class GraphProvenanceRequestPlaceholder(ResearchMetadataGraphRequestPlaceholder):
    request_kind: str = "GRAPH_PROVENANCE_PLACEHOLDER"


def default_graph_node_lookup_request_placeholder() -> GraphNodeLookupRequestPlaceholder:
    return GraphNodeLookupRequestPlaceholder(
        request_id="research-metadata-graph-api-node-request-placeholder-v1",
        notes=["Node lookup request placeholder only; no lookup is triggered."],
    )


def default_graph_edge_lookup_request_placeholder() -> GraphEdgeLookupRequestPlaceholder:
    return GraphEdgeLookupRequestPlaceholder(
        request_id="research-metadata-graph-api-edge-request-placeholder-v1",
        notes=["Edge lookup request placeholder only; no traversal or retrieval is triggered."],
    )


def default_graph_relationship_request_placeholder() -> GraphRelationshipRequestPlaceholder:
    return GraphRelationshipRequestPlaceholder(
        request_id="research-metadata-graph-api-relationship-request-placeholder-v1",
        notes=["Relationship request placeholder only; no graph query, ranking, or search is triggered."],
    )


def default_graph_provenance_request_placeholder() -> GraphProvenanceRequestPlaceholder:
    return GraphProvenanceRequestPlaceholder(
        request_id="research-metadata-graph-api-provenance-request-placeholder-v1",
        notes=["Provenance request placeholder only; no source fetch or truth validation is triggered."],
    )


def default_research_metadata_graph_request_placeholder() -> ResearchMetadataGraphRequestPlaceholder:
    return ResearchMetadataGraphRequestPlaceholder(
        request_id="research-metadata-graph-api-request-placeholder-v1",
        request_kind="RESEARCH_METADATA_GRAPH_API_REQUEST_PLACEHOLDER",
        notes=["Aggregate API request placeholder; metadata only and fail-closed."],
    )
