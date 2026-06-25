from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplayDatasetKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_workspace_display_notes,
)


class StrategyResearchWorkspaceDisplayDatasetPlaceholder(BaseModel):
    dataset_reference_id: str
    dataset_kind: StrategyResearchWorkspaceDisplayDatasetKind
    title: str
    display_contract_only: bool = True
    rendered_now: bool = False
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
        return _non_empty_text(value, "strategy research workspace display dataset text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_workspace_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def dataset_placeholder_must_fail_closed(self) -> StrategyResearchWorkspaceDisplayDatasetPlaceholder:
        if self.dataset_kind == StrategyResearchWorkspaceDisplayDatasetKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research Workspace Display dataset kind is not allowed")
        if not self.display_contract_only:
            raise ValueError("Strategy Research Workspace Display dataset must remain display-contract-only")
        if (
            self.rendered_now
            or self.real_market_data
            or self.live_data
            or self.validated_for_research
            or self.validated_for_backtest
            or self.validated_for_execution
        ):
            raise ValueError("Strategy Research Workspace Display dataset dangerous flags must be false")
        return self


def default_strategy_research_workspace_display_dataset_placeholders() -> list[
    StrategyResearchWorkspaceDisplayDatasetPlaceholder
]:
    return [
        StrategyResearchWorkspaceDisplayDatasetPlaceholder(
            dataset_reference_id="strategy-research-display-synthetic-dataset-placeholder-v1",
            dataset_kind=StrategyResearchWorkspaceDisplayDatasetKind.SYNTHETIC_DATASET_VISUAL_PLACEHOLDER,
            title="Synthetic Dataset Visual Placeholder",
            notes=["Synthetic/local references are not trusted real market data."],
        ),
        StrategyResearchWorkspaceDisplayDatasetPlaceholder(
            dataset_reference_id="strategy-research-display-local-file-placeholder-v1",
            dataset_kind=StrategyResearchWorkspaceDisplayDatasetKind.LOCAL_FILE_VISUAL_PLACEHOLDER,
            title="Local File Visual Placeholder",
            notes=["Local-file references are not validated research, backtest, or execution datasets."],
        ),
        StrategyResearchWorkspaceDisplayDatasetPlaceholder(
            dataset_reference_id="strategy-research-display-metadata-placeholder-v1",
            dataset_kind=StrategyResearchWorkspaceDisplayDatasetKind.METADATA_VISUAL_PLACEHOLDER,
            title="Metadata Visual Placeholder",
        ),
    ]
