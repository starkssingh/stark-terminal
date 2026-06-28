from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_metadata_graph.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class ResearchMetadataGraphEdgeDisplayPlaceholder(BaseModel):
    placeholder_id: str
    edge_kind: str
    display_label: str
    descriptive_only: bool = True
    traversal_enabled: bool = False
    relationship_ranking_enabled: bool = False
    artifact_retrieval_enabled: bool = False
    strategy_value_inference_enabled: bool = False
    recommendation_implied: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("placeholder_id", "edge_kind", "display_label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph edge display placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def edge_display_must_remain_descriptive(self) -> ResearchMetadataGraphEdgeDisplayPlaceholder:
        if not self.descriptive_only:
            raise ValueError("Research Metadata Graph edge display placeholders must be descriptive only")
        dangerous_flags = {
            "traversal": self.traversal_enabled,
            "relationship ranking": self.relationship_ranking_enabled,
            "artifact retrieval": self.artifact_retrieval_enabled,
            "strategy value inference": self.strategy_value_inference_enabled,
            "recommendation implication": self.recommendation_implied,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Research Metadata Graph edge display placeholder cannot enable: " + ", ".join(enabled))
        return self


class SourceToArtifactEdgeDisplayPlaceholder(ResearchMetadataGraphEdgeDisplayPlaceholder):
    edge_kind: str = "SOURCE_TO_ARTIFACT_EDGE_DISPLAY_PLACEHOLDER"


class DatasetToArtifactEdgeDisplayPlaceholder(ResearchMetadataGraphEdgeDisplayPlaceholder):
    edge_kind: str = "DATASET_TO_ARTIFACT_EDGE_DISPLAY_PLACEHOLDER"


class PaperToHypothesisEdgeDisplayPlaceholder(ResearchMetadataGraphEdgeDisplayPlaceholder):
    edge_kind: str = "PAPER_TO_HYPOTHESIS_EDGE_DISPLAY_PLACEHOLDER"


class HypothesisToExperimentEdgeDisplayPlaceholder(ResearchMetadataGraphEdgeDisplayPlaceholder):
    edge_kind: str = "HYPOTHESIS_TO_EXPERIMENT_EDGE_DISPLAY_PLACEHOLDER"


class ExperimentToStrategyCandidateEdgeDisplayPlaceholder(ResearchMetadataGraphEdgeDisplayPlaceholder):
    edge_kind: str = "EXPERIMENT_TO_STRATEGY_CANDIDATE_EDGE_DISPLAY_PLACEHOLDER"


class ArtifactDependencyEdgeDisplayPlaceholder(ResearchMetadataGraphEdgeDisplayPlaceholder):
    edge_kind: str = "ARTIFACT_DEPENDENCY_EDGE_DISPLAY_PLACEHOLDER"


def default_research_metadata_graph_edge_display_placeholder() -> ResearchMetadataGraphEdgeDisplayPlaceholder:
    return ResearchMetadataGraphEdgeDisplayPlaceholder(
        placeholder_id="research-metadata-graph-edge-display-placeholder-v1",
        edge_kind="RESEARCH_METADATA_GRAPH_EDGE_DISPLAY_PLACEHOLDER",
        display_label="Graph edge display placeholder",
        notes=["Descriptive edge display metadata only; no traversal, ranking, retrieval, or recommendation."],
    )


def default_graph_edge_display_placeholders() -> dict[str, ResearchMetadataGraphEdgeDisplayPlaceholder]:
    return {
        "source_to_artifact": SourceToArtifactEdgeDisplayPlaceholder(
            placeholder_id="research-metadata-graph-source-artifact-edge-display-v1",
            display_label="Source to artifact edge placeholder",
        ),
        "dataset_to_artifact": DatasetToArtifactEdgeDisplayPlaceholder(
            placeholder_id="research-metadata-graph-dataset-artifact-edge-display-v1",
            display_label="Dataset to artifact edge placeholder",
        ),
        "paper_to_hypothesis": PaperToHypothesisEdgeDisplayPlaceholder(
            placeholder_id="research-metadata-graph-paper-hypothesis-edge-display-v1",
            display_label="Paper to hypothesis edge placeholder",
        ),
        "hypothesis_to_experiment": HypothesisToExperimentEdgeDisplayPlaceholder(
            placeholder_id="research-metadata-graph-hypothesis-experiment-edge-display-v1",
            display_label="Hypothesis to experiment edge placeholder",
        ),
        "experiment_to_strategy_candidate": ExperimentToStrategyCandidateEdgeDisplayPlaceholder(
            placeholder_id="research-metadata-graph-experiment-strategy-candidate-edge-display-v1",
            display_label="Experiment to strategy candidate edge placeholder",
        ),
        "artifact_dependency": ArtifactDependencyEdgeDisplayPlaceholder(
            placeholder_id="research-metadata-graph-artifact-dependency-edge-display-v1",
            display_label="Artifact dependency edge placeholder",
        ),
    }
