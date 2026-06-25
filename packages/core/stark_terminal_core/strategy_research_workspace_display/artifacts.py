from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplayArtifactKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_workspace_display_notes,
)


class StrategyResearchWorkspaceDisplayArtifactPlaceholder(BaseModel):
    artifact_id: str
    artifact_kind: StrategyResearchWorkspaceDisplayArtifactKind
    title: str
    description: str
    display_contract_only: bool = True
    rendered_now: bool = False
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
        return _non_empty_text(value, "strategy research workspace display artifact text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_workspace_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def artifact_placeholder_must_fail_closed(self) -> StrategyResearchWorkspaceDisplayArtifactPlaceholder:
        if self.artifact_kind == StrategyResearchWorkspaceDisplayArtifactKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research Workspace Display artifact kind is not allowed")
        if not self.display_contract_only:
            raise ValueError("Strategy Research Workspace Display artifact must remain display-contract-only")
        forbidden = {
            "rendered now": self.rendered_now,
            "validated": self.validated,
            "strategy ready": self.strategy_ready,
            "recommendation ready": self.recommendation_ready,
            "execution ready": self.execution_ready,
            "paper parsed": self.paper_parsed,
            "backtest ready": self.backtest_ready,
        }
        enabled = [name for name, value in forbidden.items() if value]
        if enabled:
            raise ValueError("Strategy Research Workspace Display artifact cannot be: " + ", ".join(enabled))
        return self


def default_strategy_research_workspace_display_artifact_placeholders() -> list[
    StrategyResearchWorkspaceDisplayArtifactPlaceholder
]:
    return [
        StrategyResearchWorkspaceDisplayArtifactPlaceholder(
            artifact_id="strategy-research-display-paper-artifact-placeholder-v1",
            artifact_kind=StrategyResearchWorkspaceDisplayArtifactKind.PAPER_REFERENCE_VISUAL_PLACEHOLDER,
            title="Paper Reference Visual Placeholder",
            description="Display contract paper reference placeholder; no paper is parsed or validated.",
        ),
        StrategyResearchWorkspaceDisplayArtifactPlaceholder(
            artifact_id="strategy-research-display-hypothesis-artifact-placeholder-v1",
            artifact_kind=StrategyResearchWorkspaceDisplayArtifactKind.STRATEGY_HYPOTHESIS_VISUAL_PLACEHOLDER,
            title="Strategy Hypothesis Visual Placeholder",
            description="Display contract hypothesis placeholder; no strategy, signal, factor, or code is generated.",
        ),
        StrategyResearchWorkspaceDisplayArtifactPlaceholder(
            artifact_id="strategy-research-display-experiment-artifact-placeholder-v1",
            artifact_kind=StrategyResearchWorkspaceDisplayArtifactKind.EXPERIMENT_PLAN_VISUAL_PLACEHOLDER,
            title="Experiment Plan Visual Placeholder",
            description="Display contract experiment placeholder; no backtest-ready or execution-ready state.",
        ),
    ]
