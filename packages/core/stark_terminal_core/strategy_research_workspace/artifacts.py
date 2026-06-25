from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace.planning import (
    StrategyResearchArtifactKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_notes,
)


class StrategyResearchArtifactPlaceholder(BaseModel):
    artifact_id: str
    artifact_kind: StrategyResearchArtifactKind
    title: str
    description: str
    planning_only: bool = True
    validated: bool = False
    strategy_ready: bool = False
    recommendation_ready: bool = False
    execution_ready: bool = False
    paper_parsed: bool = False
    backtest_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("artifact_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research artifact placeholder text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def artifact_must_remain_placeholder(self) -> StrategyResearchArtifactPlaceholder:
        if self.artifact_kind == StrategyResearchArtifactKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research artifact kind is not allowed")
        if not self.planning_only:
            raise ValueError("Strategy Research artifact must remain planning-only")
        forbidden = {
            "validated": self.validated,
            "strategy ready": self.strategy_ready,
            "recommendation ready": self.recommendation_ready,
            "execution ready": self.execution_ready,
            "paper parsed": self.paper_parsed,
            "backtest ready": self.backtest_ready,
        }
        enabled = [name for name, value in forbidden.items() if value]
        if enabled:
            raise ValueError("Strategy Research artifact cannot be: " + ", ".join(enabled))
        return self


def default_strategy_research_artifact_placeholders() -> list[StrategyResearchArtifactPlaceholder]:
    return [
        StrategyResearchArtifactPlaceholder(
            artifact_id="strategy-research-paper-reference-artifact-placeholder-v1",
            artifact_kind=StrategyResearchArtifactKind.PAPER_REFERENCE,
            title="Paper Reference Artifact Placeholder",
            description="Planning-only paper reference metadata; no paper is ingested, parsed, or validated.",
        ),
        StrategyResearchArtifactPlaceholder(
            artifact_id="strategy-research-hypothesis-artifact-placeholder-v1",
            artifact_kind=StrategyResearchArtifactKind.STRATEGY_HYPOTHESIS,
            title="Strategy Hypothesis Artifact Placeholder",
            description="Planning-only strategy hypothesis metadata; no strategy, signal, factor, or code is generated.",
        ),
        StrategyResearchArtifactPlaceholder(
            artifact_id="strategy-research-experiment-artifact-placeholder-v1",
            artifact_kind=StrategyResearchArtifactKind.EXPERIMENT_PLAN,
            title="Experiment Plan Artifact Placeholder",
            description="Planning-only experiment metadata; no backtest-ready, recommendation-ready, or execution-ready state.",
        ),
    ]
