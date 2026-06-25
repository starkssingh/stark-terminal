from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplaySafetyLabel,
    StrategyResearchWorkspaceDisplayWorkspaceKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_workspace_display_notes,
)


class StrategyResearchWorkspaceDisplayWorkspacePlaceholder(BaseModel):
    workspace_id: str
    workspace_kind: StrategyResearchWorkspaceDisplayWorkspaceKind
    title: str
    description: str
    display_contract_only: bool = True
    active_ui: bool = False
    rendered_now: bool = False
    unavailable: bool = True
    paper_ingestion_allowed: bool = False
    paper_parsing_allowed: bool = False
    strategy_generation_allowed: bool = False
    backtesting_allowed: bool = False
    recommendations_allowed: bool = False
    execution_allowed: bool = False
    safety_label: StrategyResearchWorkspaceDisplaySafetyLabel = (
        StrategyResearchWorkspaceDisplaySafetyLabel.DISPLAY_CONTRACT_ONLY
    )
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("workspace_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace display workspace text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_workspace_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def workspace_placeholder_must_fail_closed(self) -> StrategyResearchWorkspaceDisplayWorkspacePlaceholder:
        if self.workspace_kind == StrategyResearchWorkspaceDisplayWorkspaceKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research Workspace Display workspace kind is not allowed")
        if not self.display_contract_only:
            raise ValueError("Strategy Research Workspace Display workspace must remain display-contract-only")
        if self.active_ui:
            raise ValueError("Strategy Research Workspace Display workspace cannot be active UI")
        if self.rendered_now:
            raise ValueError("Strategy Research Workspace Display workspace cannot render now")
        if not self.unavailable:
            raise ValueError("Strategy Research Workspace Display workspace must remain unavailable")
        if (
            self.paper_ingestion_allowed
            or self.paper_parsing_allowed
            or self.strategy_generation_allowed
            or self.backtesting_allowed
            or self.recommendations_allowed
            or self.execution_allowed
        ):
            raise ValueError("Strategy Research Workspace Display workspace dangerous flags must be false")
        if self.safety_label == StrategyResearchWorkspaceDisplaySafetyLabel.UNKNOWN:
            raise ValueError("Strategy Research Workspace Display workspace safety label cannot be UNKNOWN")
        return self


def default_strategy_research_workspace_display_workspace_placeholders() -> list[
    StrategyResearchWorkspaceDisplayWorkspacePlaceholder
]:
    return [
        StrategyResearchWorkspaceDisplayWorkspacePlaceholder(
            workspace_id="strategy-research-display-paper-workspace-placeholder-v1",
            workspace_kind=StrategyResearchWorkspaceDisplayWorkspaceKind.PAPER_RESEARCH_VISUAL_PLACEHOLDER,
            title="Paper Research Visual Placeholder",
            description="Display contract placeholder for future paper research surfaces; no rendering or parsing.",
            safety_label=StrategyResearchWorkspaceDisplaySafetyLabel.NOT_A_PAPER_PARSER,
            notes=["No frontend, desktop, paper ingestion, paper parsing, or active UI is implemented."],
        ),
        StrategyResearchWorkspaceDisplayWorkspacePlaceholder(
            workspace_id="strategy-research-display-hypothesis-workspace-placeholder-v1",
            workspace_kind=(
                StrategyResearchWorkspaceDisplayWorkspaceKind.STRATEGY_HYPOTHESIS_VISUAL_PLACEHOLDER
            ),
            title="Strategy Hypothesis Visual Placeholder",
            description="Display contract placeholder for future strategy hypotheses; no strategy generation.",
            safety_label=StrategyResearchWorkspaceDisplaySafetyLabel.NOT_A_STRATEGY,
        ),
        StrategyResearchWorkspaceDisplayWorkspacePlaceholder(
            workspace_id="strategy-research-display-experiment-workspace-placeholder-v1",
            workspace_kind=StrategyResearchWorkspaceDisplayWorkspaceKind.EXPERIMENT_PLAN_VISUAL_PLACEHOLDER,
            title="Experiment Plan Visual Placeholder",
            description="Display contract placeholder for future experiment plans; no backtesting or execution.",
            safety_label=StrategyResearchWorkspaceDisplaySafetyLabel.NOT_A_BACKTEST,
        ),
    ]
