from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplayBadgeKind,
    StrategyResearchWorkspaceDisplaySafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_workspace_display_notes,
)


class StrategyResearchWorkspaceDisplayBadgePlaceholder(BaseModel):
    badge_id: str
    badge_kind: StrategyResearchWorkspaceDisplayBadgeKind
    label: str
    description: str
    visible: bool = True
    active_ui: bool = False
    unavailable: bool = True
    paper_parsed: bool = False
    strategy_generated: bool = False
    backtest_generated: bool = False
    recommendation: bool = False
    action_signal: bool = False
    confidence_signal: bool = False
    decision_object_signal: bool = False
    readiness_to_trade: bool = False
    broker_control: bool = False
    execution_ready: bool = False
    safety_label: StrategyResearchWorkspaceDisplaySafetyLabel = (
        StrategyResearchWorkspaceDisplaySafetyLabel.NOT_A_RECOMMENDATION
    )
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("badge_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace display badge text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_workspace_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def badge_placeholder_must_fail_closed(self) -> StrategyResearchWorkspaceDisplayBadgePlaceholder:
        if self.badge_kind == StrategyResearchWorkspaceDisplayBadgeKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research Workspace Display badge kind is not allowed")
        if self.active_ui:
            raise ValueError("Strategy Research Workspace Display badge cannot be active UI")
        if not self.unavailable:
            raise ValueError("Strategy Research Workspace Display badge must remain unavailable")
        if (
            self.paper_parsed
            or self.strategy_generated
            or self.backtest_generated
            or self.recommendation
            or self.action_signal
            or self.confidence_signal
            or self.decision_object_signal
            or self.readiness_to_trade
            or self.broker_control
            or self.execution_ready
        ):
            raise ValueError("Strategy Research Workspace Display badge dangerous flags must be false")
        if self.safety_label == StrategyResearchWorkspaceDisplaySafetyLabel.UNKNOWN:
            raise ValueError("Strategy Research Workspace Display badge safety label cannot be UNKNOWN")
        return self


def default_strategy_research_workspace_display_badges() -> list[
    StrategyResearchWorkspaceDisplayBadgePlaceholder
]:
    return [
        StrategyResearchWorkspaceDisplayBadgePlaceholder(
            badge_id="strategy-research-display-planning-only-badge",
            badge_kind=StrategyResearchWorkspaceDisplayBadgeKind.PLANNING_ONLY,
            label="Planning only",
            description="Display contract badge placeholder; not active UI and not a recommendation.",
            safety_label=StrategyResearchWorkspaceDisplaySafetyLabel.DISPLAY_CONTRACT_ONLY,
        ),
        StrategyResearchWorkspaceDisplayBadgePlaceholder(
            badge_id="strategy-research-display-unavailable-badge",
            badge_kind=StrategyResearchWorkspaceDisplayBadgeKind.UNAVAILABLE,
            label="Unavailable",
            description="Fail-closed badge placeholder expected during Prompt 65.",
            safety_label=StrategyResearchWorkspaceDisplaySafetyLabel.DISPLAY_CONTRACT_ONLY,
        ),
        StrategyResearchWorkspaceDisplayBadgePlaceholder(
            badge_id="strategy-research-display-not-active-ui-badge",
            badge_kind=StrategyResearchWorkspaceDisplayBadgeKind.NOT_ACTIVE_UI,
            label="Not active UI",
            description="Badge placeholder marks that no frontend or desktop component is rendered.",
            safety_label=StrategyResearchWorkspaceDisplaySafetyLabel.NOT_ACTIVE_UI,
        ),
        StrategyResearchWorkspaceDisplayBadgePlaceholder(
            badge_id="strategy-research-display-not-paper-parser-badge",
            badge_kind=StrategyResearchWorkspaceDisplayBadgeKind.NOT_A_PAPER_PARSER,
            label="Not a paper parser",
            description="Badge placeholder cannot parse PDFs, arXiv records, or methods.",
            safety_label=StrategyResearchWorkspaceDisplaySafetyLabel.NOT_A_PAPER_PARSER,
        ),
        StrategyResearchWorkspaceDisplayBadgePlaceholder(
            badge_id="strategy-research-display-not-strategy-badge",
            badge_kind=StrategyResearchWorkspaceDisplayBadgeKind.NOT_A_STRATEGY,
            label="Not a strategy",
            description="Badge placeholder cannot be interpreted as generated strategy code.",
            safety_label=StrategyResearchWorkspaceDisplaySafetyLabel.NOT_A_STRATEGY,
        ),
        StrategyResearchWorkspaceDisplayBadgePlaceholder(
            badge_id="strategy-research-display-not-backtest-badge",
            badge_kind=StrategyResearchWorkspaceDisplayBadgeKind.NOT_A_BACKTEST,
            label="Not a backtest",
            description="Badge placeholder cannot be interpreted as a backtest result.",
            safety_label=StrategyResearchWorkspaceDisplaySafetyLabel.NOT_A_BACKTEST,
        ),
        StrategyResearchWorkspaceDisplayBadgePlaceholder(
            badge_id="strategy-research-display-not-recommendation-badge",
            badge_kind=StrategyResearchWorkspaceDisplayBadgeKind.NOT_A_RECOMMENDATION,
            label="Not a recommendation",
            description="Badge placeholder cannot be interpreted as buy, sell, hold, watch, or avoid output.",
            safety_label=StrategyResearchWorkspaceDisplaySafetyLabel.NOT_A_RECOMMENDATION,
        ),
        StrategyResearchWorkspaceDisplayBadgePlaceholder(
            badge_id="strategy-research-display-no-execution-badge",
            badge_kind=StrategyResearchWorkspaceDisplayBadgeKind.NO_EXECUTION,
            label="No execution",
            description="Badge placeholder cannot execute, route, approve, or override trades.",
            safety_label=StrategyResearchWorkspaceDisplaySafetyLabel.NO_EXECUTION,
        ),
    ]
