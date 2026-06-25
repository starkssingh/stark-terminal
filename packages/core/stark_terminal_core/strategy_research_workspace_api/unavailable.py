from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_api.requests import (
    StrategyResearchWorkspaceAPISafetyLabel,
    StrategyResearchWorkspaceAPIUnavailableReason,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_workspace_api_notes,
)


class StrategyResearchWorkspaceAPIUnavailableResponse(BaseModel):
    response_id: str
    unavailable: bool = True
    reason: StrategyResearchWorkspaceAPIUnavailableReason
    message: str
    api_contract_skeleton_only: bool = True
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
    safety_label: StrategyResearchWorkspaceAPISafetyLabel = StrategyResearchWorkspaceAPISafetyLabel.UNAVAILABLE
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "message", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace API unavailable response text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_workspace_api_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def unavailable_response_must_fail_closed(self) -> StrategyResearchWorkspaceAPIUnavailableResponse:
        if not self.unavailable:
            raise ValueError("Strategy Research Workspace API skeleton responses must be unavailable")
        if self.reason == StrategyResearchWorkspaceAPIUnavailableReason.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research Workspace API unavailable reason is not allowed")
        if not self.api_contract_skeleton_only:
            raise ValueError("Strategy Research Workspace API responses must remain contract-skeleton-only")
        dangerous_flags = {
            "active UI": self.active_ui_allowed,
            "frontend components": self.frontend_components_allowed,
            "desktop components": self.desktop_components_allowed,
            "paper ingestion": self.paper_ingestion_allowed,
            "paper parsing": self.paper_parsing_allowed,
            "strategy generation": self.strategy_generation_allowed,
            "strategy code generation": self.strategy_code_generation_allowed,
            "backtesting": self.backtesting_allowed,
            "optimization": self.optimization_allowed,
            "recommendations": self.recommendations_allowed,
            "action generation": self.action_generation_allowed,
            "confidence scoring": self.confidence_scoring_allowed,
            "DecisionObject generation": self.decision_object_generation_allowed,
            "readiness-to-trade": self.readiness_to_trade_allowed,
            "broker controls": self.broker_controls_allowed,
            "execution": self.execution_allowed,
            "approval": self.approval_granted,
            "override": self.override_granted,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(
                "Strategy Research Workspace API unavailable response must fail closed: "
                + ", ".join(enabled)
            )
        if self.safety_label == StrategyResearchWorkspaceAPISafetyLabel.UNKNOWN:
            raise ValueError("Strategy Research Workspace API safety label cannot be UNKNOWN")
        return self


def default_strategy_research_workspace_api_unavailable_response(
    reason: StrategyResearchWorkspaceAPIUnavailableReason = (
        StrategyResearchWorkspaceAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY
    ),
) -> StrategyResearchWorkspaceAPIUnavailableResponse:
    return StrategyResearchWorkspaceAPIUnavailableResponse(
        response_id="strategy-research-workspace-api-unavailable-response-v1",
        reason=reason,
        message=(
            "Strategy Research Workspace API is an API contract skeleton only and returns unavailable "
            "responses in Prompt 64."
        ),
        notes=[
            (
                "Unavailable by default; not active UI, not a paper parser, not a strategy, "
                "not a backtest, not a recommendation, not readiness-to-trade, and no execution."
            ),
        ],
    )
