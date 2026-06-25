from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplaySafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_workspace_display_notes,
)


class StrategyResearchWorkspaceDisplayUnavailableResponse(BaseModel):
    response_id: str
    unavailable: bool = True
    message: str
    display_contract_only: bool = True
    active_ui_allowed: bool = False
    frontend_components_allowed: bool = False
    desktop_components_allowed: bool = False
    paper_ingestion_allowed: bool = False
    paper_parsing_allowed: bool = False
    strategy_generation_allowed: bool = False
    strategy_code_generation_allowed: bool = False
    backtesting_allowed: bool = False
    optimization_allowed: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    safety_label: StrategyResearchWorkspaceDisplaySafetyLabel = (
        StrategyResearchWorkspaceDisplaySafetyLabel.DISPLAY_CONTRACT_ONLY
    )
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "message", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace display unavailable response text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_workspace_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def unavailable_response_must_fail_closed(self) -> StrategyResearchWorkspaceDisplayUnavailableResponse:
        if not self.unavailable:
            raise ValueError("Strategy Research Workspace Display response must be unavailable")
        if not self.display_contract_only:
            raise ValueError("Strategy Research Workspace Display response must be display-contract-only")
        if (
            self.active_ui_allowed
            or self.frontend_components_allowed
            or self.desktop_components_allowed
            or self.paper_ingestion_allowed
            or self.paper_parsing_allowed
            or self.strategy_generation_allowed
            or self.strategy_code_generation_allowed
            or self.backtesting_allowed
            or self.optimization_allowed
            or self.recommendations_allowed
            or self.action_generation_allowed
            or self.confidence_scoring_allowed
            or self.decision_object_generation_allowed
            or self.readiness_to_trade_allowed
            or self.broker_controls_allowed
            or self.execution_allowed
            or self.approval_granted
            or self.override_granted
        ):
            raise ValueError("Strategy Research Workspace Display unavailable response dangerous flags must be false")
        if self.safety_label == StrategyResearchWorkspaceDisplaySafetyLabel.UNKNOWN:
            raise ValueError("Strategy Research Workspace Display unavailable response safety label cannot be UNKNOWN")
        return self


def default_strategy_research_workspace_display_unavailable_response() -> (
    StrategyResearchWorkspaceDisplayUnavailableResponse
):
    return StrategyResearchWorkspaceDisplayUnavailableResponse(
        response_id="strategy-research-workspace-display-unavailable-response-v1",
        message=(
            "Strategy Research Workspace Display is a display contract skeleton only and returns "
            "unavailable placeholder responses in Prompt 65."
        ),
        notes=[
            (
                "Unavailable by default; not active UI, not a paper parser, not a strategy, "
                "not a backtest, not a recommendation, not readiness-to-trade, and no execution."
            ),
        ],
    )
