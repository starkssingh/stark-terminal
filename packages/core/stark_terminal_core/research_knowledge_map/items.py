from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_knowledge_map.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class KnowledgeMapItemKind(StrEnum):
    ARTIFACT = "ARTIFACT"
    PAPER = "PAPER"
    DATASET = "DATASET"
    HYPOTHESIS = "HYPOTHESIS"
    EXPERIMENT = "EXPERIMENT"
    EVIDENCE = "EVIDENCE"
    STRATEGY_CANDIDATE = "STRATEGY_CANDIDATE"


class KnowledgeMapItemPlaceholder(BaseModel):
    item_id: str
    item_kind: KnowledgeMapItemKind
    label: str
    description: str
    descriptive_only: bool = True
    read_only: bool = True
    persisted: bool = False
    database_query_enabled: bool = False
    graph_query_enabled: bool = False
    paper_parsing_enabled: bool = False
    file_loading_enabled: bool = False
    strategy_generation_enabled: bool = False
    backtesting_enabled: bool = False
    recommendations_enabled: bool = False
    execution_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("item_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map item text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def item_must_remain_placeholder(self) -> KnowledgeMapItemPlaceholder:
        if not self.descriptive_only or not self.read_only:
            raise ValueError("research knowledge map items are descriptive read-only placeholders")
        dangerous_flags = {
            "persist items": self.persisted,
            "query database": self.database_query_enabled,
            "query graph": self.graph_query_enabled,
            "parse papers": self.paper_parsing_enabled,
            "load files": self.file_loading_enabled,
            "generate strategies": self.strategy_generation_enabled,
            "run backtests": self.backtesting_enabled,
            "generate recommendations": self.recommendations_enabled,
            "execution": self.execution_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("research knowledge map item placeholder cannot enable: " + ", ".join(enabled))
        return self


class ArtifactKnowledgeItemPlaceholder(KnowledgeMapItemPlaceholder):
    item_kind: KnowledgeMapItemKind = KnowledgeMapItemKind.ARTIFACT


class PaperKnowledgeItemPlaceholder(KnowledgeMapItemPlaceholder):
    item_kind: KnowledgeMapItemKind = KnowledgeMapItemKind.PAPER


class DatasetKnowledgeItemPlaceholder(KnowledgeMapItemPlaceholder):
    item_kind: KnowledgeMapItemKind = KnowledgeMapItemKind.DATASET


class HypothesisKnowledgeItemPlaceholder(KnowledgeMapItemPlaceholder):
    item_kind: KnowledgeMapItemKind = KnowledgeMapItemKind.HYPOTHESIS


class ExperimentKnowledgeItemPlaceholder(KnowledgeMapItemPlaceholder):
    item_kind: KnowledgeMapItemKind = KnowledgeMapItemKind.EXPERIMENT


class EvidenceKnowledgeItemPlaceholder(KnowledgeMapItemPlaceholder):
    item_kind: KnowledgeMapItemKind = KnowledgeMapItemKind.EVIDENCE


class StrategyCandidateKnowledgeItemPlaceholder(KnowledgeMapItemPlaceholder):
    item_kind: KnowledgeMapItemKind = KnowledgeMapItemKind.STRATEGY_CANDIDATE


def default_research_knowledge_map_item_placeholders() -> list[KnowledgeMapItemPlaceholder]:
    return [
        ArtifactKnowledgeItemPlaceholder(
            item_id="research-knowledge-map-artifact-item-placeholder",
            label="Artifact knowledge placeholder",
            description="Descriptive placeholder for future artifact knowledge map placement.",
        ),
        PaperKnowledgeItemPlaceholder(
            item_id="research-knowledge-map-paper-item-placeholder",
            label="Paper knowledge placeholder",
            description="Descriptive paper placeholder; no paper parsing or file loading.",
        ),
        DatasetKnowledgeItemPlaceholder(
            item_id="research-knowledge-map-dataset-item-placeholder",
            label="Dataset knowledge placeholder",
            description="Descriptive dataset placeholder; no ingestion or storage.",
        ),
        HypothesisKnowledgeItemPlaceholder(
            item_id="research-knowledge-map-hypothesis-item-placeholder",
            label="Hypothesis knowledge placeholder",
            description="Descriptive hypothesis placeholder; no recommendation or trade readiness.",
        ),
        ExperimentKnowledgeItemPlaceholder(
            item_id="research-knowledge-map-experiment-item-placeholder",
            label="Experiment knowledge placeholder",
            description="Descriptive experiment placeholder; no backtesting or optimization.",
        ),
        EvidenceKnowledgeItemPlaceholder(
            item_id="research-knowledge-map-evidence-item-placeholder",
            label="Evidence knowledge placeholder",
            description="Descriptive evidence placeholder; no approval or source-truth validation.",
        ),
        StrategyCandidateKnowledgeItemPlaceholder(
            item_id="research-knowledge-map-strategy-candidate-item-placeholder",
            label="Strategy candidate knowledge placeholder",
            description="Descriptive candidate placeholder only; not a generated strategy, recommendation, or trade.",
        ),
    ]
