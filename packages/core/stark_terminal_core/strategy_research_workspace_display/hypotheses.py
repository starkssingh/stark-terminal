from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplayHypothesisKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_workspace_display_notes,
)


class StrategyResearchWorkspaceDisplayHypothesisPlaceholder(BaseModel):
    hypothesis_id: str
    hypothesis_kind: StrategyResearchWorkspaceDisplayHypothesisKind
    title: str
    description: str
    display_contract_only: bool = True
    rendered_now: bool = False
    generated_strategy: bool = False
    generated_signal: bool = False
    generated_factor: bool = False
    generated_code: bool = False
    backtest_ready: bool = False
    recommendation_ready: bool = False
    execution_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("hypothesis_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace display hypothesis text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_workspace_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def hypothesis_placeholder_must_fail_closed(self) -> StrategyResearchWorkspaceDisplayHypothesisPlaceholder:
        if self.hypothesis_kind == StrategyResearchWorkspaceDisplayHypothesisKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research Workspace Display hypothesis kind is not allowed")
        if not self.display_contract_only:
            raise ValueError("Strategy Research Workspace Display hypothesis must remain display-contract-only")
        if (
            self.rendered_now
            or self.generated_strategy
            or self.generated_signal
            or self.generated_factor
            or self.generated_code
            or self.backtest_ready
            or self.recommendation_ready
            or self.execution_ready
        ):
            raise ValueError("Strategy Research Workspace Display hypothesis dangerous flags must be false")
        return self


def default_strategy_research_workspace_display_hypothesis_placeholders() -> list[
    StrategyResearchWorkspaceDisplayHypothesisPlaceholder
]:
    return [
        StrategyResearchWorkspaceDisplayHypothesisPlaceholder(
            hypothesis_id="strategy-research-display-strategy-hypothesis-placeholder-v1",
            hypothesis_kind=StrategyResearchWorkspaceDisplayHypothesisKind.STRATEGY_HYPOTHESIS_VISUAL_PLACEHOLDER,
            title="Strategy Hypothesis Visual Placeholder",
            description="Visual placeholder only; no generated strategy, signal, factor, code, or backtest.",
        ),
        StrategyResearchWorkspaceDisplayHypothesisPlaceholder(
            hypothesis_id="strategy-research-display-signal-hypothesis-placeholder-v1",
            hypothesis_kind=StrategyResearchWorkspaceDisplayHypothesisKind.SIGNAL_HYPOTHESIS_VISUAL_PLACEHOLDER,
            title="Signal Hypothesis Visual Placeholder",
            description="Visual placeholder only; no signal generation or recommendation readiness.",
        ),
        StrategyResearchWorkspaceDisplayHypothesisPlaceholder(
            hypothesis_id="strategy-research-display-risk-hypothesis-placeholder-v1",
            hypothesis_kind=StrategyResearchWorkspaceDisplayHypothesisKind.RISK_HYPOTHESIS_VISUAL_PLACEHOLDER,
            title="Risk Hypothesis Visual Placeholder",
            description="Visual placeholder only; no risk model, execution readiness, or broker control.",
        ),
    ]
