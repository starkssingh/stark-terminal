from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace.planning import (
    StrategyResearchExperimentKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_notes,
)


class StrategyResearchExperimentPlaceholder(BaseModel):
    experiment_id: str
    experiment_kind: StrategyResearchExperimentKind
    title: str
    description: str
    planning_only: bool = True
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
        return _non_empty_text(value, "strategy research experiment placeholder text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def experiment_must_remain_placeholder(self) -> StrategyResearchExperimentPlaceholder:
        if self.experiment_kind == StrategyResearchExperimentKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research experiment kind is not allowed")
        if not self.planning_only:
            raise ValueError("Strategy Research experiment must remain planning-only")
        forbidden = {
            "executable": self.executable,
            "backtest executable": self.backtest_executable,
            "optimization executable": self.optimization_executable,
            "strategy executable": self.strategy_executable,
            "live ready": self.live_ready,
            "recommendation ready": self.recommendation_ready,
            "execution ready": self.execution_ready,
        }
        enabled = [name for name, value in forbidden.items() if value]
        if enabled:
            raise ValueError("Strategy Research experiment cannot be: " + ", ".join(enabled))
        return self


def default_strategy_research_experiment_placeholders() -> list[StrategyResearchExperimentPlaceholder]:
    return [
        StrategyResearchExperimentPlaceholder(
            experiment_id="strategy-research-experiment-plan-placeholder-v1",
            experiment_kind=StrategyResearchExperimentKind.EXPERIMENT_PLAN_PLACEHOLDER,
            title="Experiment Plan Placeholder",
            description="Planning-only experiment plan; no executable research workflow.",
        ),
        StrategyResearchExperimentPlaceholder(
            experiment_id="strategy-research-backtest-plan-placeholder-v1",
            experiment_kind=StrategyResearchExperimentKind.BACKTEST_PLAN_PLACEHOLDER,
            title="Backtest Plan Placeholder",
            description="Planning-only backtest plan; no backtest engine, optimizer, or performance claim.",
        ),
        StrategyResearchExperimentPlaceholder(
            experiment_id="strategy-research-safety-review-plan-placeholder-v1",
            experiment_kind=StrategyResearchExperimentKind.SAFETY_REVIEW_PLAN_PLACEHOLDER,
            title="Safety Review Plan Placeholder",
            description="Planning-only safety review plan; no approval, override, recommendation, or execution.",
        ),
    ]
