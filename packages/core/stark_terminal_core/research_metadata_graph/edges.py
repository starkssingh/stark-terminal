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


class ResearchMetadataGraphEdgeKind(StrEnum):
    SOURCE_TO_ARTIFACT = "SOURCE_TO_ARTIFACT"
    DATASET_TO_ARTIFACT = "DATASET_TO_ARTIFACT"
    PAPER_TO_HYPOTHESIS = "PAPER_TO_HYPOTHESIS"
    HYPOTHESIS_TO_EXPERIMENT = "HYPOTHESIS_TO_EXPERIMENT"
    EXPERIMENT_TO_STRATEGY_CANDIDATE = "EXPERIMENT_TO_STRATEGY_CANDIDATE"
    ARTIFACT_DEPENDENCY = "ARTIFACT_DEPENDENCY"


class ResearchMetadataGraphEdgePlaceholder(BaseModel):
    edge_id: str
    edge_kind: ResearchMetadataGraphEdgeKind
    label: str
    description: str
    descriptive_only: bool = True
    read_only: bool = True
    persisted: bool = False
    traversal_enabled: bool = False
    relationship_ranking_enabled: bool = False
    artifact_retrieval_enabled: bool = False
    strategy_value_inference_enabled: bool = False
    recommendations_enabled: bool = False
    execution_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("edge_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph edge text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def edge_must_remain_placeholder(self) -> ResearchMetadataGraphEdgePlaceholder:
        if not self.descriptive_only or not self.read_only:
            raise ValueError("research metadata graph edges are descriptive read-only placeholders")
        dangerous_flags = {
            "persist edges": self.persisted,
            "traversal": self.traversal_enabled,
            "rank relationships": self.relationship_ranking_enabled,
            "retrieve artifacts": self.artifact_retrieval_enabled,
            "infer strategy value": self.strategy_value_inference_enabled,
            "recommendations": self.recommendations_enabled,
            "execution": self.execution_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("research metadata graph edge placeholder cannot enable: " + ", ".join(enabled))
        return self


class SourceToArtifactEdgePlaceholder(ResearchMetadataGraphEdgePlaceholder):
    edge_kind: ResearchMetadataGraphEdgeKind = ResearchMetadataGraphEdgeKind.SOURCE_TO_ARTIFACT


class DatasetToArtifactEdgePlaceholder(ResearchMetadataGraphEdgePlaceholder):
    edge_kind: ResearchMetadataGraphEdgeKind = ResearchMetadataGraphEdgeKind.DATASET_TO_ARTIFACT


class PaperToHypothesisEdgePlaceholder(ResearchMetadataGraphEdgePlaceholder):
    edge_kind: ResearchMetadataGraphEdgeKind = ResearchMetadataGraphEdgeKind.PAPER_TO_HYPOTHESIS


class HypothesisToExperimentEdgePlaceholder(ResearchMetadataGraphEdgePlaceholder):
    edge_kind: ResearchMetadataGraphEdgeKind = ResearchMetadataGraphEdgeKind.HYPOTHESIS_TO_EXPERIMENT


class ExperimentToStrategyCandidateEdgePlaceholder(ResearchMetadataGraphEdgePlaceholder):
    edge_kind: ResearchMetadataGraphEdgeKind = ResearchMetadataGraphEdgeKind.EXPERIMENT_TO_STRATEGY_CANDIDATE


class ArtifactDependencyEdgePlaceholder(ResearchMetadataGraphEdgePlaceholder):
    edge_kind: ResearchMetadataGraphEdgeKind = ResearchMetadataGraphEdgeKind.ARTIFACT_DEPENDENCY


def default_research_metadata_graph_edge_placeholders() -> list[ResearchMetadataGraphEdgePlaceholder]:
    return [
        SourceToArtifactEdgePlaceholder(
            edge_id="research-metadata-graph-source-to-artifact-edge-placeholder",
            label="Source to artifact placeholder",
            description="Descriptive relationship placeholder from source metadata to artifact metadata.",
        ),
        DatasetToArtifactEdgePlaceholder(
            edge_id="research-metadata-graph-dataset-to-artifact-edge-placeholder",
            label="Dataset to artifact placeholder",
            description="Descriptive relationship placeholder from dataset metadata to artifact metadata.",
        ),
        PaperToHypothesisEdgePlaceholder(
            edge_id="research-metadata-graph-paper-to-hypothesis-edge-placeholder",
            label="Paper to hypothesis placeholder",
            description="Descriptive relationship placeholder; no paper parsing or method extraction.",
        ),
        HypothesisToExperimentEdgePlaceholder(
            edge_id="research-metadata-graph-hypothesis-to-experiment-edge-placeholder",
            label="Hypothesis to experiment placeholder",
            description="Descriptive relationship placeholder from hypothesis metadata to experiment metadata.",
        ),
        ExperimentToStrategyCandidateEdgePlaceholder(
            edge_id="research-metadata-graph-experiment-to-strategy-candidate-edge-placeholder",
            label="Experiment to strategy candidate placeholder",
            description="Descriptive relationship placeholder; no strategy value inference or recommendation.",
        ),
        ArtifactDependencyEdgePlaceholder(
            edge_id="research-metadata-graph-artifact-dependency-edge-placeholder",
            label="Artifact dependency placeholder",
            description="Descriptive dependency placeholder; no traversal, ranking, retrieval, or execution.",
        ),
    ]
