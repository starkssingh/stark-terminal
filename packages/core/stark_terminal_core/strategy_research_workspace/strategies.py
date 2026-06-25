from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace.planning import (
    StrategyResearchHypothesisKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_notes,
)


class StrategyResearchHypothesisPlaceholder(BaseModel):
    hypothesis_id: str
    hypothesis_kind: StrategyResearchHypothesisKind
    title: str
    description: str
    planning_only: bool = True
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
        return _non_empty_text(value, "strategy research hypothesis placeholder text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def hypothesis_must_remain_placeholder(self) -> StrategyResearchHypothesisPlaceholder:
        if self.hypothesis_kind == StrategyResearchHypothesisKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research hypothesis kind is not allowed")
        if not self.planning_only:
            raise ValueError("Strategy Research hypothesis must remain planning-only")
        forbidden = {
            "generated strategy": self.generated_strategy,
            "generated signal": self.generated_signal,
            "generated factor": self.generated_factor,
            "generated code": self.generated_code,
            "backtest ready": self.backtest_ready,
            "recommendation ready": self.recommendation_ready,
            "execution ready": self.execution_ready,
        }
        enabled = [name for name, value in forbidden.items() if value]
        if enabled:
            raise ValueError("Strategy Research hypothesis cannot be: " + ", ".join(enabled))
        return self


def default_strategy_research_hypothesis_placeholders() -> list[StrategyResearchHypothesisPlaceholder]:
    return [
        StrategyResearchHypothesisPlaceholder(
            hypothesis_id="strategy-research-strategy-hypothesis-placeholder-v1",
            hypothesis_kind=StrategyResearchHypothesisKind.STRATEGY_HYPOTHESIS_PLACEHOLDER,
            title="Strategy Hypothesis Placeholder",
            description="Planning-only hypothesis metadata; no strategy is generated.",
        ),
        StrategyResearchHypothesisPlaceholder(
            hypothesis_id="strategy-research-signal-hypothesis-placeholder-v1",
            hypothesis_kind=StrategyResearchHypothesisKind.SIGNAL_HYPOTHESIS_PLACEHOLDER,
            title="Signal Hypothesis Placeholder",
            description="Planning-only signal hypothesis metadata; no signal is computed or emitted.",
        ),
        StrategyResearchHypothesisPlaceholder(
            hypothesis_id="strategy-research-risk-hypothesis-placeholder-v1",
            hypothesis_kind=StrategyResearchHypothesisKind.RISK_HYPOTHESIS_PLACEHOLDER,
            title="Risk Hypothesis Placeholder",
            description="Planning-only risk hypothesis metadata; no recommendation or execution readiness is created.",
        ),
    ]
