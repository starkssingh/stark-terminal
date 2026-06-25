from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class StrategyResearchWorkspaceAPIStage(StrEnum):
    API_CONTRACT_SKELETON = "API_CONTRACT_SKELETON"
    UNAVAILABLE_ONLY = "UNAVAILABLE_ONLY"
    REFERENCE_PLACEHOLDERS = "REFERENCE_PLACEHOLDERS"
    ACTIVE_UI_PLANNED = "ACTIVE_UI_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class StrategyResearchWorkspaceAPIRequestKind(StrEnum):
    WORKSPACE_OVERVIEW_REQUEST = "WORKSPACE_OVERVIEW_REQUEST"
    ARTIFACT_CONTEXT_REQUEST = "ARTIFACT_CONTEXT_REQUEST"
    PAPER_REFERENCE_REQUEST = "PAPER_REFERENCE_REQUEST"
    HYPOTHESIS_CONTEXT_REQUEST = "HYPOTHESIS_CONTEXT_REQUEST"
    DATASET_REFERENCE_REQUEST = "DATASET_REFERENCE_REQUEST"
    EXPERIMENT_PLAN_REQUEST = "EXPERIMENT_PLAN_REQUEST"
    READINESS_TEMPLATE_REQUEST = "READINESS_TEMPLATE_REQUEST"
    UNKNOWN = "UNKNOWN"


class StrategyResearchWorkspaceAPIUnavailableReason(StrEnum):
    ACTIVE_UI_DISABLED = "ACTIVE_UI_DISABLED"
    FRONTEND_COMPONENTS_DISABLED = "FRONTEND_COMPONENTS_DISABLED"
    DESKTOP_COMPONENTS_DISABLED = "DESKTOP_COMPONENTS_DISABLED"
    PAPER_INGESTION_DISABLED = "PAPER_INGESTION_DISABLED"
    PAPER_PARSING_DISABLED = "PAPER_PARSING_DISABLED"
    STRATEGY_GENERATION_DISABLED = "STRATEGY_GENERATION_DISABLED"
    STRATEGY_CODE_GENERATION_DISABLED = "STRATEGY_CODE_GENERATION_DISABLED"
    BACKTESTING_DISABLED = "BACKTESTING_DISABLED"
    OPTIMIZATION_DISABLED = "OPTIMIZATION_DISABLED"
    RECOMMENDATIONS_DISABLED = "RECOMMENDATIONS_DISABLED"
    ACTION_GENERATION_DISABLED = "ACTION_GENERATION_DISABLED"
    CONFIDENCE_SCORING_DISABLED = "CONFIDENCE_SCORING_DISABLED"
    DECISION_OBJECT_GENERATION_DISABLED = "DECISION_OBJECT_GENERATION_DISABLED"
    READINESS_TO_TRADE_DISABLED = "READINESS_TO_TRADE_DISABLED"
    BROKER_CONTROLS_DISABLED = "BROKER_CONTROLS_DISABLED"
    EXECUTION_DISABLED = "EXECUTION_DISABLED"
    API_CONTRACT_SKELETON_ONLY = "API_CONTRACT_SKELETON_ONLY"
    UNKNOWN = "UNKNOWN"


class StrategyResearchWorkspaceAPISafetyLabel(StrEnum):
    API_CONTRACT_SKELETON_ONLY = "API_CONTRACT_SKELETON_ONLY"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_ACTIVE_UI = "NOT_ACTIVE_UI"
    NOT_A_PAPER_PARSER = "NOT_A_PAPER_PARSER"
    NOT_A_STRATEGY = "NOT_A_STRATEGY"
    NOT_A_BACKTEST = "NOT_A_BACKTEST"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    NOT_READINESS_TO_TRADE = "NOT_READINESS_TO_TRADE"
    NO_BROKER_CONTROL = "NO_BROKER_CONTROL"
    NO_EXECUTION = "NO_EXECUTION"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _non_empty_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


def sanitize_strategy_research_workspace_api_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


class StrategyResearchWorkspaceAPIRequestPlaceholder(BaseModel):
    request_id: str
    request_kind: StrategyResearchWorkspaceAPIRequestKind
    requested_workspaces: list[str] = Field(default_factory=list)
    requested_artifacts: list[str] = Field(default_factory=list)
    requested_paper_references: list[str] = Field(default_factory=list)
    requested_hypotheses: list[str] = Field(default_factory=list)
    requested_dataset_references: list[str] = Field(default_factory=list)
    requested_experiments: list[str] = Field(default_factory=list)
    safety_reference_required: bool = True
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
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("request_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace API request placeholder text fields")

    @field_validator(
        "requested_workspaces",
        "requested_artifacts",
        "requested_paper_references",
        "requested_hypotheses",
        "requested_dataset_references",
        "requested_experiments",
        "notes",
    )
    @classmethod
    def list_fields_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_workspace_api_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def request_placeholder_must_fail_closed(self) -> StrategyResearchWorkspaceAPIRequestPlaceholder:
        if self.request_kind == StrategyResearchWorkspaceAPIRequestKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research Workspace API request kind is not allowed")
        if not self.safety_reference_required:
            raise ValueError("Strategy Research Workspace API safety references are required in Prompt 64")
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
                "Strategy Research Workspace API request placeholder must fail closed: "
                + ", ".join(enabled)
            )
        return self


def create_strategy_research_workspace_api_request_placeholder(
    request_id: str,
    request_kind: StrategyResearchWorkspaceAPIRequestKind = (
        StrategyResearchWorkspaceAPIRequestKind.WORKSPACE_OVERVIEW_REQUEST
    ),
    requested_workspaces: list[str] | None = None,
    requested_artifacts: list[str] | None = None,
    requested_paper_references: list[str] | None = None,
    requested_hypotheses: list[str] | None = None,
    requested_dataset_references: list[str] | None = None,
    requested_experiments: list[str] | None = None,
    notes: list[str] | None = None,
) -> StrategyResearchWorkspaceAPIRequestPlaceholder:
    return StrategyResearchWorkspaceAPIRequestPlaceholder(
        request_id=request_id,
        request_kind=request_kind,
        requested_workspaces=list(requested_workspaces or []),
        requested_artifacts=list(requested_artifacts or []),
        requested_paper_references=list(requested_paper_references or []),
        requested_hypotheses=list(requested_hypotheses or []),
        requested_dataset_references=list(requested_dataset_references or []),
        requested_experiments=list(requested_experiments or []),
        notes=list(notes or ["API contract skeleton request placeholder; not active research behavior."]),
    )


def default_strategy_research_workspace_api_request_placeholder() -> (
    StrategyResearchWorkspaceAPIRequestPlaceholder
):
    return create_strategy_research_workspace_api_request_placeholder(
        request_id="strategy-research-workspace-api-request-placeholder-v1",
        request_kind=StrategyResearchWorkspaceAPIRequestKind.WORKSPACE_OVERVIEW_REQUEST,
        requested_workspaces=[
            "paper_research_placeholder",
            "strategy_hypothesis_placeholder",
            "experiment_plan_placeholder",
        ],
        requested_artifacts=[
            "paper_reference_placeholder",
            "strategy_hypothesis_placeholder",
            "safety_note_placeholder",
        ],
        requested_paper_references=[
            "arxiv_reference_placeholder",
            "doi_reference_placeholder",
            "local_document_reference_placeholder",
        ],
        requested_hypotheses=[
            "strategy_hypothesis_placeholder",
            "signal_hypothesis_placeholder",
            "factor_hypothesis_placeholder",
        ],
        requested_dataset_references=[
            "synthetic_dataset_reference",
            "local_file_reference",
            "metadata_reference",
        ],
        requested_experiments=[
            "experiment_plan_placeholder",
            "validation_plan_placeholder",
            "backtest_plan_placeholder",
        ],
    )
