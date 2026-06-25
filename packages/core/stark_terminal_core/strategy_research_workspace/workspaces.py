from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace.planning import (
    StrategyResearchSafetyLabel,
    StrategyResearchWorkspaceKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_notes,
)


class StrategyResearchWorkspacePlaceholder(BaseModel):
    workspace_id: str
    workspace_kind: StrategyResearchWorkspaceKind
    title: str
    description: str
    planning_only: bool = True
    active_ui: bool = False
    unavailable: bool = True
    paper_ingestion_allowed: bool = False
    paper_parsing_allowed: bool = False
    strategy_generation_allowed: bool = False
    backtesting_allowed: bool = False
    recommendations_allowed: bool = False
    execution_allowed: bool = False
    safety_label: StrategyResearchSafetyLabel = StrategyResearchSafetyLabel.PLANNING_ONLY
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("workspace_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace placeholder text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def placeholder_must_remain_planning_only(self) -> StrategyResearchWorkspacePlaceholder:
        if self.workspace_kind == StrategyResearchWorkspaceKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research Workspace kind is not allowed")
        if not self.planning_only:
            raise ValueError("Strategy Research Workspace placeholder must remain planning-only")
        if self.active_ui:
            raise ValueError("Strategy Research Workspace placeholder cannot be active UI")
        if not self.unavailable:
            raise ValueError("Strategy Research Workspace placeholder must remain unavailable")
        if self.paper_ingestion_allowed:
            raise ValueError("Strategy Research Workspace paper ingestion is forbidden in Prompt 63")
        if self.paper_parsing_allowed:
            raise ValueError("Strategy Research Workspace paper parsing is forbidden in Prompt 63")
        if self.strategy_generation_allowed:
            raise ValueError("Strategy Research Workspace strategy generation is forbidden in Prompt 63")
        if self.backtesting_allowed:
            raise ValueError("Strategy Research Workspace backtesting is forbidden in Prompt 63")
        if self.recommendations_allowed:
            raise ValueError("Strategy Research Workspace recommendations are forbidden in Prompt 63")
        if self.execution_allowed:
            raise ValueError("Strategy Research Workspace execution is forbidden in Prompt 63")
        if self.safety_label in {StrategyResearchSafetyLabel.UNKNOWN, StrategyResearchSafetyLabel.BLOCKED}:
            raise ValueError("Strategy Research Workspace placeholder requires a safe planning label")
        return self


def default_strategy_research_workspace_placeholders() -> list[StrategyResearchWorkspacePlaceholder]:
    return [
        StrategyResearchWorkspacePlaceholder(
            workspace_id="strategy-research-paper-workspace-placeholder-v1",
            workspace_kind=StrategyResearchWorkspaceKind.PAPER_RESEARCH_PLACEHOLDER,
            title="Paper Research Workspace Placeholder",
            description="Planning-only placeholder for future paper references; no ingestion or parsing.",
            notes=["No paper upload, PDF parsing, arXiv ingestion, or LLM paper analysis is implemented."],
        ),
        StrategyResearchWorkspacePlaceholder(
            workspace_id="strategy-research-hypothesis-workspace-placeholder-v1",
            workspace_kind=StrategyResearchWorkspaceKind.STRATEGY_HYPOTHESIS_PLACEHOLDER,
            title="Strategy Hypothesis Workspace Placeholder",
            description="Planning-only placeholder for future strategy hypotheses; no strategy generation.",
            safety_label=StrategyResearchSafetyLabel.NOT_A_STRATEGY,
            notes=["Hypotheses are labels and metadata only, not generated strategies or signals."],
        ),
        StrategyResearchWorkspacePlaceholder(
            workspace_id="strategy-research-experiment-workspace-placeholder-v1",
            workspace_kind=StrategyResearchWorkspaceKind.EXPERIMENT_PLAN_PLACEHOLDER,
            title="Experiment Plan Workspace Placeholder",
            description="Planning-only placeholder for future experiment planning; no executable backtest.",
            safety_label=StrategyResearchSafetyLabel.NOT_A_BACKTEST,
            notes=["Experiment placeholders do not run backtests, optimization, or walk-forward analysis."],
        ),
    ]
