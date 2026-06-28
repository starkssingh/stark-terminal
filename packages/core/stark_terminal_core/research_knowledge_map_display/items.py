from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_knowledge_map.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class KnowledgeMapItemDisplayPlaceholder(BaseModel):
    placeholder_id: str
    item_kind: str
    display_label: str
    display_metadata_only: bool = True
    active_ui_rendering_enabled: bool = False
    database_query_enabled: bool = False
    knowledge_map_data_retrieval_enabled: bool = False
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

    @field_validator("placeholder_id", "item_kind", "display_label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map item display placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def item_display_must_remain_placeholder_only(self) -> KnowledgeMapItemDisplayPlaceholder:
        if not self.display_metadata_only:
            raise ValueError("Research Knowledge Map item display placeholders must be display metadata only")
        dangerous_flags = {
            "active UI rendering": self.active_ui_rendering_enabled,
            "database query": self.database_query_enabled,
            "knowledge map data retrieval": self.knowledge_map_data_retrieval_enabled,
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
            raise ValueError("Research Knowledge Map item display placeholder cannot enable: " + ", ".join(enabled))
        return self


class ArtifactKnowledgeItemDisplayPlaceholder(KnowledgeMapItemDisplayPlaceholder):
    item_kind: str = "ARTIFACT_KNOWLEDGE_ITEM_DISPLAY_PLACEHOLDER"


class PaperKnowledgeItemDisplayPlaceholder(KnowledgeMapItemDisplayPlaceholder):
    item_kind: str = "PAPER_KNOWLEDGE_ITEM_DISPLAY_PLACEHOLDER"


class DatasetKnowledgeItemDisplayPlaceholder(KnowledgeMapItemDisplayPlaceholder):
    item_kind: str = "DATASET_KNOWLEDGE_ITEM_DISPLAY_PLACEHOLDER"


class HypothesisKnowledgeItemDisplayPlaceholder(KnowledgeMapItemDisplayPlaceholder):
    item_kind: str = "HYPOTHESIS_KNOWLEDGE_ITEM_DISPLAY_PLACEHOLDER"


class ExperimentKnowledgeItemDisplayPlaceholder(KnowledgeMapItemDisplayPlaceholder):
    item_kind: str = "EXPERIMENT_KNOWLEDGE_ITEM_DISPLAY_PLACEHOLDER"


class EvidenceKnowledgeItemDisplayPlaceholder(KnowledgeMapItemDisplayPlaceholder):
    item_kind: str = "EVIDENCE_KNOWLEDGE_ITEM_DISPLAY_PLACEHOLDER"


class StrategyCandidateKnowledgeItemDisplayPlaceholder(KnowledgeMapItemDisplayPlaceholder):
    item_kind: str = "STRATEGY_CANDIDATE_KNOWLEDGE_ITEM_DISPLAY_PLACEHOLDER"


def default_research_knowledge_map_item_display_placeholder() -> KnowledgeMapItemDisplayPlaceholder:
    return KnowledgeMapItemDisplayPlaceholder(
        placeholder_id="research-knowledge-map-item-display-placeholder-v1",
        item_kind="RESEARCH_KNOWLEDGE_MAP_ITEM_DISPLAY_PLACEHOLDER",
        display_label="Knowledge map item display placeholder",
        notes=["Backend display metadata only; no active UI, database query, or retrieval."],
    )


def default_knowledge_map_item_display_placeholders() -> dict[str, KnowledgeMapItemDisplayPlaceholder]:
    return {
        "artifact": ArtifactKnowledgeItemDisplayPlaceholder(
            placeholder_id="research-knowledge-map-artifact-item-display-v1",
            display_label="Artifact knowledge item placeholder",
        ),
        "paper": PaperKnowledgeItemDisplayPlaceholder(
            placeholder_id="research-knowledge-map-paper-item-display-v1",
            display_label="Paper knowledge item placeholder",
        ),
        "dataset": DatasetKnowledgeItemDisplayPlaceholder(
            placeholder_id="research-knowledge-map-dataset-item-display-v1",
            display_label="Dataset knowledge item placeholder",
        ),
        "hypothesis": HypothesisKnowledgeItemDisplayPlaceholder(
            placeholder_id="research-knowledge-map-hypothesis-item-display-v1",
            display_label="Hypothesis knowledge item placeholder",
        ),
        "experiment": ExperimentKnowledgeItemDisplayPlaceholder(
            placeholder_id="research-knowledge-map-experiment-item-display-v1",
            display_label="Experiment knowledge item placeholder",
        ),
        "evidence": EvidenceKnowledgeItemDisplayPlaceholder(
            placeholder_id="research-knowledge-map-evidence-item-display-v1",
            display_label="Evidence knowledge item placeholder",
        ),
        "strategy_candidate": StrategyCandidateKnowledgeItemDisplayPlaceholder(
            placeholder_id="research-knowledge-map-strategy-candidate-item-display-v1",
            display_label="Strategy candidate knowledge item placeholder",
        ),
    }
