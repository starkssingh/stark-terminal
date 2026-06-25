from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_api.references import (
    StrategyResearchWorkspaceAPIArtifactReference,
    StrategyResearchWorkspaceAPIDatasetReference,
    StrategyResearchWorkspaceAPIExperimentReference,
    StrategyResearchWorkspaceAPIHypothesisReference,
    StrategyResearchWorkspaceAPIPaperReference,
    StrategyResearchWorkspaceAPISafetyReference,
    StrategyResearchWorkspaceAPIWorkspaceReference,
    default_strategy_research_workspace_api_artifact_reference,
    default_strategy_research_workspace_api_dataset_reference,
    default_strategy_research_workspace_api_experiment_reference,
    default_strategy_research_workspace_api_hypothesis_reference,
    default_strategy_research_workspace_api_paper_reference,
    default_strategy_research_workspace_api_safety_reference,
    default_strategy_research_workspace_api_workspace_reference,
)
from stark_terminal_core.strategy_research_workspace_api.requests import (
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_workspace_api_notes,
)
from stark_terminal_core.strategy_research_workspace_api.unavailable import (
    StrategyResearchWorkspaceAPIUnavailableResponse,
    default_strategy_research_workspace_api_unavailable_response,
)


class StrategyResearchWorkspaceAPIResponsePlaceholder(BaseModel):
    response_id: str
    request_id: str | None = None
    workspace_reference: StrategyResearchWorkspaceAPIWorkspaceReference
    artifact_reference: StrategyResearchWorkspaceAPIArtifactReference
    paper_reference: StrategyResearchWorkspaceAPIPaperReference
    hypothesis_reference: StrategyResearchWorkspaceAPIHypothesisReference
    dataset_reference: StrategyResearchWorkspaceAPIDatasetReference
    experiment_reference: StrategyResearchWorkspaceAPIExperimentReference
    safety_reference: StrategyResearchWorkspaceAPISafetyReference
    unavailable_response: StrategyResearchWorkspaceAPIUnavailableResponse
    api_contract_skeleton_only: bool = True
    active_ui_generated: bool = False
    frontend_component_generated: bool = False
    desktop_component_generated: bool = False
    paper_ingested: bool = False
    paper_parsed: bool = False
    strategy_generated: bool = False
    strategy_code_generated: bool = False
    backtest_generated: bool = False
    optimization_generated: bool = False
    recommendation_generated: bool = False
    action_generated: bool = False
    confidence_generated: bool = False
    decision_object_generated: bool = False
    readiness_to_trade_generated: bool = False
    broker_control_generated: bool = False
    execution_ready: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace API response placeholder text fields")

    @field_validator("request_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_workspace_api_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def response_placeholder_must_fail_closed(self) -> StrategyResearchWorkspaceAPIResponsePlaceholder:
        if not self.api_contract_skeleton_only:
            raise ValueError("Strategy Research Workspace API response must remain contract-skeleton-only")
        dangerous_flags = {
            "active UI": self.active_ui_generated,
            "frontend component": self.frontend_component_generated,
            "desktop component": self.desktop_component_generated,
            "paper ingestion": self.paper_ingested,
            "paper parsing": self.paper_parsed,
            "strategy generation": self.strategy_generated,
            "strategy code generation": self.strategy_code_generated,
            "backtest generation": self.backtest_generated,
            "optimization generation": self.optimization_generated,
            "recommendation generation": self.recommendation_generated,
            "action generation": self.action_generated,
            "confidence generation": self.confidence_generated,
            "DecisionObject generation": self.decision_object_generated,
            "readiness-to-trade generation": self.readiness_to_trade_generated,
            "broker control": self.broker_control_generated,
            "execution readiness": self.execution_ready,
            "approval": self.approval_granted,
            "override": self.override_granted,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(
                "Strategy Research Workspace API response placeholder must fail closed: "
                + ", ".join(enabled)
            )
        return self


def default_strategy_research_workspace_api_response_placeholder(
    request_id: str | None = None,
    workspace_reference: StrategyResearchWorkspaceAPIWorkspaceReference | None = None,
    artifact_reference: StrategyResearchWorkspaceAPIArtifactReference | None = None,
    paper_reference: StrategyResearchWorkspaceAPIPaperReference | None = None,
    hypothesis_reference: StrategyResearchWorkspaceAPIHypothesisReference | None = None,
    dataset_reference: StrategyResearchWorkspaceAPIDatasetReference | None = None,
    experiment_reference: StrategyResearchWorkspaceAPIExperimentReference | None = None,
    safety_reference: StrategyResearchWorkspaceAPISafetyReference | None = None,
    unavailable_response: StrategyResearchWorkspaceAPIUnavailableResponse | None = None,
) -> StrategyResearchWorkspaceAPIResponsePlaceholder:
    return StrategyResearchWorkspaceAPIResponsePlaceholder(
        response_id="strategy-research-workspace-api-response-placeholder-v1",
        request_id=request_id,
        workspace_reference=workspace_reference or default_strategy_research_workspace_api_workspace_reference(),
        artifact_reference=artifact_reference or default_strategy_research_workspace_api_artifact_reference(),
        paper_reference=paper_reference or default_strategy_research_workspace_api_paper_reference(),
        hypothesis_reference=hypothesis_reference or default_strategy_research_workspace_api_hypothesis_reference(),
        dataset_reference=dataset_reference or default_strategy_research_workspace_api_dataset_reference(),
        experiment_reference=experiment_reference or default_strategy_research_workspace_api_experiment_reference(),
        safety_reference=safety_reference or default_strategy_research_workspace_api_safety_reference(),
        unavailable_response=unavailable_response or default_strategy_research_workspace_api_unavailable_response(),
        notes=["Response placeholder contains references only and no generated research outputs."],
    )
