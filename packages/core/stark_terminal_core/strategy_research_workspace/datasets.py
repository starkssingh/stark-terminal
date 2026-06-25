from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace.planning import (
    StrategyResearchDatasetReferenceKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_notes,
)


class StrategyResearchDatasetReferencePlaceholder(BaseModel):
    dataset_reference_id: str
    dataset_kind: StrategyResearchDatasetReferenceKind
    title: str
    planning_only: bool = True
    real_market_data: bool = False
    live_data: bool = False
    validated_for_research: bool = False
    validated_for_backtest: bool = False
    validated_for_execution: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("dataset_reference_id", "title", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research dataset reference text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def dataset_reference_must_remain_placeholder(self) -> StrategyResearchDatasetReferencePlaceholder:
        if self.dataset_kind == StrategyResearchDatasetReferenceKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research dataset reference kind is not allowed")
        if not self.planning_only:
            raise ValueError("Strategy Research dataset reference must remain planning-only")
        forbidden = {
            "real market data": self.real_market_data,
            "live data": self.live_data,
            "validated for research": self.validated_for_research,
            "validated for backtest": self.validated_for_backtest,
            "validated for execution": self.validated_for_execution,
        }
        enabled = [name for name, value in forbidden.items() if value]
        if enabled:
            raise ValueError("Strategy Research dataset reference cannot be: " + ", ".join(enabled))
        return self


def default_strategy_research_dataset_reference_placeholders() -> list[StrategyResearchDatasetReferencePlaceholder]:
    return [
        StrategyResearchDatasetReferencePlaceholder(
            dataset_reference_id="strategy-research-synthetic-dataset-reference-placeholder-v1",
            dataset_kind=StrategyResearchDatasetReferenceKind.SYNTHETIC_DATASET_REFERENCE,
            title="Synthetic Dataset Reference Placeholder",
            notes=["Synthetic/local references remain placeholders and are not trusted real market data."],
        ),
        StrategyResearchDatasetReferencePlaceholder(
            dataset_reference_id="strategy-research-local-file-reference-placeholder-v1",
            dataset_kind=StrategyResearchDatasetReferenceKind.LOCAL_FILE_REFERENCE,
            title="Local File Reference Placeholder",
            notes=["No local file is validated for research, backtesting, or execution by this placeholder."],
        ),
        StrategyResearchDatasetReferencePlaceholder(
            dataset_reference_id="strategy-research-metadata-reference-placeholder-v1",
            dataset_kind=StrategyResearchDatasetReferenceKind.METADATA_REFERENCE,
            title="Metadata Reference Placeholder",
            notes=["Metadata references do not imply live data or strategy validation."],
        ),
    ]
