from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplayExperimentKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_workspace_display_notes,
)


class StrategyResearchWorkspaceDisplayExperimentPlaceholder(BaseModel):
    experiment_id: str
    experiment_kind: StrategyResearchWorkspaceDisplayExperimentKind
    title: str
    description: str
    display_contract_only: bool = True
    rendered_now: bool = False
    executable: bool = False
    backtest_executable: bool = False
    optimization_executable: bool = False
    strategy_executable: bool = False
    live_ready: bool = False
    recommendation_ready: bool = False
    execution_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("experiment_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace display experiment text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_workspace_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def experiment_placeholder_must_fail_closed(self) -> StrategyResearchWorkspaceDisplayExperimentPlaceholder:
        if self.experiment_kind == StrategyResearchWorkspaceDisplayExperimentKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research Workspace Display experiment kind is not allowed")
        if not self.display_contract_only:
            raise ValueError("Strategy Research Workspace Display experiment must remain display-contract-only")
        if (
            self.rendered_now
            or self.executable
            or self.backtest_executable
            or self.optimization_executable
            or self.strategy_executable
            or self.live_ready
            or self.recommendation_ready
            or self.execution_ready
        ):
            raise ValueError("Strategy Research Workspace Display experiment dangerous flags must be false")
        return self


def default_strategy_research_workspace_display_experiment_placeholders() -> list[
    StrategyResearchWorkspaceDisplayExperimentPlaceholder
]:
    return [
        StrategyResearchWorkspaceDisplayExperimentPlaceholder(
            experiment_id="strategy-research-display-experiment-plan-placeholder-v1",
            experiment_kind=StrategyResearchWorkspaceDisplayExperimentKind.EXPERIMENT_PLAN_VISUAL_PLACEHOLDER,
            title="Experiment Plan Visual Placeholder",
            description="Display contract placeholder only; no executable experiment.",
        ),
        StrategyResearchWorkspaceDisplayExperimentPlaceholder(
            experiment_id="strategy-research-display-backtest-plan-placeholder-v1",
            experiment_kind=StrategyResearchWorkspaceDisplayExperimentKind.BACKTEST_PLAN_VISUAL_PLACEHOLDER,
            title="Backtest Plan Visual Placeholder",
            description="Display contract placeholder only; no executable backtest or performance claim.",
        ),
        StrategyResearchWorkspaceDisplayExperimentPlaceholder(
            experiment_id="strategy-research-display-safety-review-placeholder-v1",
            experiment_kind=StrategyResearchWorkspaceDisplayExperimentKind.SAFETY_REVIEW_PLAN_VISUAL_PLACEHOLDER,
            title="Safety Review Visual Placeholder",
            description="Display contract placeholder only; no approval, override, broker control, or execution.",
        ),
    ]
