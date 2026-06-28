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


class ResearchMetadataGraphNodeKind(StrEnum):
    ARTIFACT = "ARTIFACT"
    SOURCE = "SOURCE"
    DATASET = "DATASET"
    PAPER = "PAPER"
    HYPOTHESIS = "HYPOTHESIS"
    EXPERIMENT = "EXPERIMENT"
    STRATEGY_CANDIDATE = "STRATEGY_CANDIDATE"


class ResearchMetadataGraphNodePlaceholder(BaseModel):
    node_id: str
    node_kind: ResearchMetadataGraphNodeKind
    label: str
    description: str
    metadata_only: bool = True
    read_only: bool = True
    persisted: bool = False
    graph_database_query_enabled: bool = False
    paper_content_parsing_enabled: bool = False
    source_file_loading_enabled: bool = False
    method_extraction_enabled: bool = False
    strategy_generation_enabled: bool = False
    backtesting_enabled: bool = False
    recommendations_enabled: bool = False
    execution_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("node_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph node text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def node_must_remain_placeholder(self) -> ResearchMetadataGraphNodePlaceholder:
        if not self.metadata_only or not self.read_only:
            raise ValueError("research metadata graph nodes are metadata-only read-only placeholders")
        dangerous_flags = {
            "persist nodes": self.persisted,
            "query graph database": self.graph_database_query_enabled,
            "parse paper content": self.paper_content_parsing_enabled,
            "load source files": self.source_file_loading_enabled,
            "extract methods": self.method_extraction_enabled,
            "generate strategy": self.strategy_generation_enabled,
            "run backtests": self.backtesting_enabled,
            "generate recommendations": self.recommendations_enabled,
            "execution": self.execution_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("research metadata graph node placeholder cannot enable: " + ", ".join(enabled))
        return self


class ResearchArtifactNodePlaceholder(ResearchMetadataGraphNodePlaceholder):
    node_kind: ResearchMetadataGraphNodeKind = ResearchMetadataGraphNodeKind.ARTIFACT


class ResearchSourceNodePlaceholder(ResearchMetadataGraphNodePlaceholder):
    node_kind: ResearchMetadataGraphNodeKind = ResearchMetadataGraphNodeKind.SOURCE


class ResearchDatasetNodePlaceholder(ResearchMetadataGraphNodePlaceholder):
    node_kind: ResearchMetadataGraphNodeKind = ResearchMetadataGraphNodeKind.DATASET


class ResearchPaperNodePlaceholder(ResearchMetadataGraphNodePlaceholder):
    node_kind: ResearchMetadataGraphNodeKind = ResearchMetadataGraphNodeKind.PAPER


class ResearchHypothesisNodePlaceholder(ResearchMetadataGraphNodePlaceholder):
    node_kind: ResearchMetadataGraphNodeKind = ResearchMetadataGraphNodeKind.HYPOTHESIS


class ResearchExperimentNodePlaceholder(ResearchMetadataGraphNodePlaceholder):
    node_kind: ResearchMetadataGraphNodeKind = ResearchMetadataGraphNodeKind.EXPERIMENT


class ResearchStrategyCandidateNodePlaceholder(ResearchMetadataGraphNodePlaceholder):
    node_kind: ResearchMetadataGraphNodeKind = ResearchMetadataGraphNodeKind.STRATEGY_CANDIDATE


def default_research_metadata_graph_node_placeholders() -> list[ResearchMetadataGraphNodePlaceholder]:
    return [
        ResearchArtifactNodePlaceholder(
            node_id="research-metadata-graph-artifact-node-placeholder",
            label="Research artifact placeholder",
            description="Descriptive placeholder for a future research artifact metadata node.",
        ),
        ResearchSourceNodePlaceholder(
            node_id="research-metadata-graph-source-node-placeholder",
            label="Research source placeholder",
            description="Descriptive placeholder for a future source metadata node.",
        ),
        ResearchDatasetNodePlaceholder(
            node_id="research-metadata-graph-dataset-node-placeholder",
            label="Research dataset placeholder",
            description="Descriptive placeholder for a future dataset metadata node.",
        ),
        ResearchPaperNodePlaceholder(
            node_id="research-metadata-graph-paper-node-placeholder",
            label="Research paper placeholder",
            description="Descriptive placeholder for a future paper metadata node, not parsed paper content.",
        ),
        ResearchHypothesisNodePlaceholder(
            node_id="research-metadata-graph-hypothesis-node-placeholder",
            label="Research hypothesis placeholder",
            description="Descriptive placeholder for a future hypothesis metadata node.",
        ),
        ResearchExperimentNodePlaceholder(
            node_id="research-metadata-graph-experiment-node-placeholder",
            label="Research experiment placeholder",
            description="Descriptive placeholder for a future experiment metadata node.",
        ),
        ResearchStrategyCandidateNodePlaceholder(
            node_id="research-metadata-graph-strategy-candidate-node-placeholder",
            label="Strategy candidate placeholder",
            description="Descriptive placeholder only; not generated strategy, recommendation, or trade readiness.",
        ),
    ]
