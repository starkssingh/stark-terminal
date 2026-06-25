from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_api.requests import (
    StrategyResearchWorkspaceAPIRequestKind,
    StrategyResearchWorkspaceAPIStage,
    StrategyResearchWorkspaceAPIUnavailableReason,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
)


class StrategyResearchWorkspaceAPIContractMetadata(BaseModel):
    contract_id: str
    service_name: str = "stark-terminal-strategy-research-workspace-api"
    stage: StrategyResearchWorkspaceAPIStage = StrategyResearchWorkspaceAPIStage.API_CONTRACT_SKELETON
    request_kinds: list[StrategyResearchWorkspaceAPIRequestKind]
    unavailable_reasons: list[StrategyResearchWorkspaceAPIUnavailableReason]
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
    approval_allowed: bool = False
    override_allowed: bool = False
    returns_unavailable_by_default: bool = True
    forbidden_outputs: list[str]
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("contract_id", "service_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace API contract metadata text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def contract_metadata_must_fail_closed(self) -> StrategyResearchWorkspaceAPIContractMetadata:
        if self.stage == StrategyResearchWorkspaceAPIStage.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research Workspace API stage is not allowed")
        if not self.request_kinds:
            raise ValueError("Strategy Research Workspace API metadata requires request kinds")
        if StrategyResearchWorkspaceAPIRequestKind.UNKNOWN in self.request_kinds:
            raise ValueError("UNKNOWN Strategy Research Workspace API request kind is not allowed")
        if not self.unavailable_reasons:
            raise ValueError("Strategy Research Workspace API metadata requires unavailable reasons")
        if StrategyResearchWorkspaceAPIUnavailableReason.UNKNOWN in self.unavailable_reasons:
            raise ValueError("UNKNOWN Strategy Research Workspace API unavailable reason is not allowed")
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
            "approval": self.approval_allowed,
            "override": self.override_allowed,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(
                "Strategy Research Workspace API contract metadata must fail closed: "
                + ", ".join(enabled)
            )
        if not self.returns_unavailable_by_default:
            raise ValueError("Strategy Research Workspace API skeleton must return unavailable by default")
        required_terms = [
            "active ui",
            "frontend",
            "desktop",
            "paper ingestion",
            "paper parsing",
            "strategy generation",
            "strategy code generation",
            "backtesting",
            "optimization",
            "recommendation",
            "action",
            "confidence",
            "decisionobject",
            "readiness-to-trade",
            "broker",
            "execution",
            "approval",
            "override",
        ]
        normalized_outputs = " ".join(self.forbidden_outputs).lower().replace("_", " ")
        missing = [term for term in required_terms if term not in normalized_outputs]
        if missing:
            raise ValueError(f"forbidden outputs missing required concepts: {', '.join(missing)}")
        return self


def default_strategy_research_workspace_api_contract_metadata() -> (
    StrategyResearchWorkspaceAPIContractMetadata
):
    return StrategyResearchWorkspaceAPIContractMetadata(
        contract_id="strategy-research-workspace-api-contract-metadata-v1",
        request_kinds=[
            StrategyResearchWorkspaceAPIRequestKind.WORKSPACE_OVERVIEW_REQUEST,
            StrategyResearchWorkspaceAPIRequestKind.ARTIFACT_CONTEXT_REQUEST,
            StrategyResearchWorkspaceAPIRequestKind.PAPER_REFERENCE_REQUEST,
            StrategyResearchWorkspaceAPIRequestKind.HYPOTHESIS_CONTEXT_REQUEST,
            StrategyResearchWorkspaceAPIRequestKind.DATASET_REFERENCE_REQUEST,
            StrategyResearchWorkspaceAPIRequestKind.EXPERIMENT_PLAN_REQUEST,
            StrategyResearchWorkspaceAPIRequestKind.READINESS_TEMPLATE_REQUEST,
        ],
        unavailable_reasons=[
            StrategyResearchWorkspaceAPIUnavailableReason.ACTIVE_UI_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.FRONTEND_COMPONENTS_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.DESKTOP_COMPONENTS_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.PAPER_INGESTION_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.PAPER_PARSING_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.STRATEGY_GENERATION_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.STRATEGY_CODE_GENERATION_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.BACKTESTING_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.OPTIMIZATION_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.RECOMMENDATIONS_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.ACTION_GENERATION_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.CONFIDENCE_SCORING_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.DECISION_OBJECT_GENERATION_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.READINESS_TO_TRADE_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.BROKER_CONTROLS_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.EXECUTION_DISABLED,
            StrategyResearchWorkspaceAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY,
        ],
        forbidden_outputs=[
            "active UI",
            "frontend_components",
            "desktop_components",
            "paper ingestion",
            "paper parsing",
            "strategy generation",
            "strategy code generation",
            "backtesting",
            "optimization",
            "recommendation_generation",
            "action_generation",
            "confidence_scoring",
            "DecisionObject_generation",
            "readiness-to-trade",
            "broker_controls",
            "execution_apis",
            "approval_controls",
            "override_controls",
        ],
    )
