from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_metadata_graph.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)
from stark_terminal_core.research_metadata_graph_api.unavailable import (
    ResearchMetadataGraphApiUnavailableResponse,
    unavailable_graph_api_response_template,
)


class ResearchMetadataGraphResponsePlaceholder(BaseModel):
    response_id: str
    response_kind: str
    unavailable_by_default: bool = True
    placeholder_only: bool = True
    retrieved_graph_data_present: bool = False
    search_results_present: bool = False
    rankings_present: bool = False
    embeddings_present: bool = False
    parsed_paper_content_present: bool = False
    generated_strategies_present: bool = False
    backtest_results_present: bool = False
    recommendations_present: bool = False
    execution_controls_present: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)
    unavailable_response: ResearchMetadataGraphApiUnavailableResponse = Field(
        default_factory=unavailable_graph_api_response_template
    )

    @field_validator("response_id", "response_kind", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph API response placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def response_must_remain_placeholder_only(self) -> ResearchMetadataGraphResponsePlaceholder:
        if not self.unavailable_by_default:
            raise ValueError("Research Metadata Graph API response placeholder must be unavailable-by-default")
        if not self.placeholder_only:
            raise ValueError("Research Metadata Graph API response placeholder must remain placeholder-only")
        dangerous_flags = {
            "retrieved graph data": self.retrieved_graph_data_present,
            "search results": self.search_results_present,
            "rankings": self.rankings_present,
            "embeddings": self.embeddings_present,
            "parsed paper content": self.parsed_paper_content_present,
            "generated strategies": self.generated_strategies_present,
            "backtest results": self.backtest_results_present,
            "recommendations": self.recommendations_present,
            "execution controls": self.execution_controls_present,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Research Metadata Graph API response placeholder cannot include: " + ", ".join(enabled))
        return self


class GraphNodeResponsePlaceholder(ResearchMetadataGraphResponsePlaceholder):
    response_kind: str = "GRAPH_NODE_RESPONSE_PLACEHOLDER"


class GraphEdgeResponsePlaceholder(ResearchMetadataGraphResponsePlaceholder):
    response_kind: str = "GRAPH_EDGE_RESPONSE_PLACEHOLDER"


class GraphRelationshipResponsePlaceholder(ResearchMetadataGraphResponsePlaceholder):
    response_kind: str = "GRAPH_RELATIONSHIP_RESPONSE_PLACEHOLDER"


class GraphProvenanceResponsePlaceholder(ResearchMetadataGraphResponsePlaceholder):
    response_kind: str = "GRAPH_PROVENANCE_RESPONSE_PLACEHOLDER"


def default_graph_node_response_placeholder() -> GraphNodeResponsePlaceholder:
    return GraphNodeResponsePlaceholder(
        response_id="research-metadata-graph-api-node-response-placeholder-v1",
        notes=["No retrieved graph node data is present."],
    )


def default_graph_edge_response_placeholder() -> GraphEdgeResponsePlaceholder:
    return GraphEdgeResponsePlaceholder(
        response_id="research-metadata-graph-api-edge-response-placeholder-v1",
        notes=["No retrieved graph edge data is present."],
    )


def default_graph_relationship_response_placeholder() -> GraphRelationshipResponsePlaceholder:
    return GraphRelationshipResponsePlaceholder(
        response_id="research-metadata-graph-api-relationship-response-placeholder-v1",
        notes=["No traversal, search, ranking, or retrieval result is present."],
    )


def default_graph_provenance_response_placeholder() -> GraphProvenanceResponsePlaceholder:
    return GraphProvenanceResponsePlaceholder(
        response_id="research-metadata-graph-api-provenance-response-placeholder-v1",
        notes=["No source truth validation or parsed paper content is present."],
    )


def default_research_metadata_graph_response_placeholder() -> ResearchMetadataGraphResponsePlaceholder:
    return ResearchMetadataGraphResponsePlaceholder(
        response_id="research-metadata-graph-api-response-placeholder-v1",
        response_kind="RESEARCH_METADATA_GRAPH_API_RESPONSE_PLACEHOLDER",
        notes=["Aggregate API response placeholder; unavailable and fail-closed."],
    )
