from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_metadata_graph.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class ResearchMetadataGraphNodeDisplayPlaceholder(BaseModel):
    placeholder_id: str
    node_kind: str
    display_label: str
    display_metadata_only: bool = True
    active_ui_rendering_enabled: bool = False
    graph_database_query_enabled: bool = False
    graph_data_retrieval_enabled: bool = False
    search_results_display_enabled: bool = False
    rankings_display_enabled: bool = False
    embeddings_display_enabled: bool = False
    parsed_paper_content_display_enabled: bool = False
    generated_strategy_display_enabled: bool = False
    backtest_results_display_enabled: bool = False
    recommendations_display_enabled: bool = False
    execution_controls_display_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("placeholder_id", "node_kind", "display_label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph node display placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def node_display_must_remain_placeholder_only(self) -> ResearchMetadataGraphNodeDisplayPlaceholder:
        if not self.display_metadata_only:
            raise ValueError("Research Metadata Graph node display placeholders must be display metadata only")
        dangerous_flags = {
            "active UI rendering": self.active_ui_rendering_enabled,
            "graph database query": self.graph_database_query_enabled,
            "graph data retrieval": self.graph_data_retrieval_enabled,
            "search result display": self.search_results_display_enabled,
            "ranking display": self.rankings_display_enabled,
            "embedding display": self.embeddings_display_enabled,
            "parsed paper content display": self.parsed_paper_content_display_enabled,
            "generated strategy display": self.generated_strategy_display_enabled,
            "backtest result display": self.backtest_results_display_enabled,
            "recommendation display": self.recommendations_display_enabled,
            "execution controls display": self.execution_controls_display_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Research Metadata Graph node display placeholder cannot enable: " + ", ".join(enabled))
        return self


class ResearchArtifactNodeDisplayPlaceholder(ResearchMetadataGraphNodeDisplayPlaceholder):
    node_kind: str = "RESEARCH_ARTIFACT_NODE_DISPLAY_PLACEHOLDER"


class ResearchSourceNodeDisplayPlaceholder(ResearchMetadataGraphNodeDisplayPlaceholder):
    node_kind: str = "RESEARCH_SOURCE_NODE_DISPLAY_PLACEHOLDER"


class ResearchDatasetNodeDisplayPlaceholder(ResearchMetadataGraphNodeDisplayPlaceholder):
    node_kind: str = "RESEARCH_DATASET_NODE_DISPLAY_PLACEHOLDER"


class ResearchPaperNodeDisplayPlaceholder(ResearchMetadataGraphNodeDisplayPlaceholder):
    node_kind: str = "RESEARCH_PAPER_NODE_DISPLAY_PLACEHOLDER"


class ResearchHypothesisNodeDisplayPlaceholder(ResearchMetadataGraphNodeDisplayPlaceholder):
    node_kind: str = "RESEARCH_HYPOTHESIS_NODE_DISPLAY_PLACEHOLDER"


class ResearchExperimentNodeDisplayPlaceholder(ResearchMetadataGraphNodeDisplayPlaceholder):
    node_kind: str = "RESEARCH_EXPERIMENT_NODE_DISPLAY_PLACEHOLDER"


class ResearchStrategyCandidateNodeDisplayPlaceholder(ResearchMetadataGraphNodeDisplayPlaceholder):
    node_kind: str = "RESEARCH_STRATEGY_CANDIDATE_NODE_DISPLAY_PLACEHOLDER"


def default_research_metadata_graph_node_display_placeholder() -> ResearchMetadataGraphNodeDisplayPlaceholder:
    return ResearchMetadataGraphNodeDisplayPlaceholder(
        placeholder_id="research-metadata-graph-node-display-placeholder-v1",
        node_kind="RESEARCH_METADATA_GRAPH_NODE_DISPLAY_PLACEHOLDER",
        display_label="Graph node display placeholder",
        notes=["Backend display metadata only; no active UI or graph retrieval."],
    )


def default_graph_node_display_placeholders() -> dict[str, ResearchMetadataGraphNodeDisplayPlaceholder]:
    return {
        "artifact": ResearchArtifactNodeDisplayPlaceholder(
            placeholder_id="research-metadata-graph-artifact-node-display-v1",
            display_label="Research artifact node placeholder",
        ),
        "source": ResearchSourceNodeDisplayPlaceholder(
            placeholder_id="research-metadata-graph-source-node-display-v1",
            display_label="Research source node placeholder",
        ),
        "dataset": ResearchDatasetNodeDisplayPlaceholder(
            placeholder_id="research-metadata-graph-dataset-node-display-v1",
            display_label="Research dataset node placeholder",
        ),
        "paper": ResearchPaperNodeDisplayPlaceholder(
            placeholder_id="research-metadata-graph-paper-node-display-v1",
            display_label="Research paper node placeholder",
        ),
        "hypothesis": ResearchHypothesisNodeDisplayPlaceholder(
            placeholder_id="research-metadata-graph-hypothesis-node-display-v1",
            display_label="Research hypothesis node placeholder",
        ),
        "experiment": ResearchExperimentNodeDisplayPlaceholder(
            placeholder_id="research-metadata-graph-experiment-node-display-v1",
            display_label="Research experiment node placeholder",
        ),
        "strategy_candidate": ResearchStrategyCandidateNodeDisplayPlaceholder(
            placeholder_id="research-metadata-graph-strategy-candidate-node-display-v1",
            display_label="Research strategy candidate node placeholder",
        ),
    }
