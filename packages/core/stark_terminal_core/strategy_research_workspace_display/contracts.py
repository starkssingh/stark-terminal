from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class StrategyResearchWorkspaceDisplayStage(StrEnum):
    DISPLAY_CONTRACT_SKELETON = "DISPLAY_CONTRACT_SKELETON"
    UNAVAILABLE_ONLY = "UNAVAILABLE_ONLY"
    WORKSPACE_PLACEHOLDERS = "WORKSPACE_PLACEHOLDERS"
    ARTIFACT_PLACEHOLDERS = "ARTIFACT_PLACEHOLDERS"
    STRATEGY_PLACEHOLDERS = "STRATEGY_PLACEHOLDERS"
    ACTIVE_UI_PLANNED = "ACTIVE_UI_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class StrategyResearchWorkspaceDisplayWorkspaceKind(StrEnum):
    PAPER_RESEARCH_VISUAL_PLACEHOLDER = "PAPER_RESEARCH_VISUAL_PLACEHOLDER"
    STRATEGY_HYPOTHESIS_VISUAL_PLACEHOLDER = "STRATEGY_HYPOTHESIS_VISUAL_PLACEHOLDER"
    DATASET_CONTEXT_VISUAL_PLACEHOLDER = "DATASET_CONTEXT_VISUAL_PLACEHOLDER"
    EXPERIMENT_PLAN_VISUAL_PLACEHOLDER = "EXPERIMENT_PLAN_VISUAL_PLACEHOLDER"
    EVIDENCE_REVIEW_VISUAL_PLACEHOLDER = "EVIDENCE_REVIEW_VISUAL_PLACEHOLDER"
    SAFETY_REVIEW_VISUAL_PLACEHOLDER = "SAFETY_REVIEW_VISUAL_PLACEHOLDER"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class StrategyResearchWorkspaceDisplayArtifactKind(StrEnum):
    PAPER_REFERENCE_VISUAL_PLACEHOLDER = "PAPER_REFERENCE_VISUAL_PLACEHOLDER"
    STRATEGY_HYPOTHESIS_VISUAL_PLACEHOLDER = "STRATEGY_HYPOTHESIS_VISUAL_PLACEHOLDER"
    DATASET_REFERENCE_VISUAL_PLACEHOLDER = "DATASET_REFERENCE_VISUAL_PLACEHOLDER"
    EXPERIMENT_PLAN_VISUAL_PLACEHOLDER = "EXPERIMENT_PLAN_VISUAL_PLACEHOLDER"
    EVIDENCE_VISUAL_PLACEHOLDER = "EVIDENCE_VISUAL_PLACEHOLDER"
    SAFETY_NOTE_VISUAL_PLACEHOLDER = "SAFETY_NOTE_VISUAL_PLACEHOLDER"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class StrategyResearchWorkspaceDisplayPaperKind(StrEnum):
    ARXIV_REFERENCE_VISUAL_PLACEHOLDER = "ARXIV_REFERENCE_VISUAL_PLACEHOLDER"
    DOI_REFERENCE_VISUAL_PLACEHOLDER = "DOI_REFERENCE_VISUAL_PLACEHOLDER"
    LOCAL_DOCUMENT_REFERENCE_VISUAL_PLACEHOLDER = "LOCAL_DOCUMENT_REFERENCE_VISUAL_PLACEHOLDER"
    ABSTRACT_VISUAL_PLACEHOLDER = "ABSTRACT_VISUAL_PLACEHOLDER"
    METHOD_SUMMARY_VISUAL_PLACEHOLDER = "METHOD_SUMMARY_VISUAL_PLACEHOLDER"
    UNKNOWN = "UNKNOWN"


class StrategyResearchWorkspaceDisplayHypothesisKind(StrEnum):
    STRATEGY_HYPOTHESIS_VISUAL_PLACEHOLDER = "STRATEGY_HYPOTHESIS_VISUAL_PLACEHOLDER"
    SIGNAL_HYPOTHESIS_VISUAL_PLACEHOLDER = "SIGNAL_HYPOTHESIS_VISUAL_PLACEHOLDER"
    FACTOR_HYPOTHESIS_VISUAL_PLACEHOLDER = "FACTOR_HYPOTHESIS_VISUAL_PLACEHOLDER"
    RISK_HYPOTHESIS_VISUAL_PLACEHOLDER = "RISK_HYPOTHESIS_VISUAL_PLACEHOLDER"
    EXECUTION_HYPOTHESIS_VISUAL_PLACEHOLDER = "EXECUTION_HYPOTHESIS_VISUAL_PLACEHOLDER"
    UNKNOWN = "UNKNOWN"


class StrategyResearchWorkspaceDisplayDatasetKind(StrEnum):
    SYNTHETIC_DATASET_VISUAL_PLACEHOLDER = "SYNTHETIC_DATASET_VISUAL_PLACEHOLDER"
    LOCAL_FILE_VISUAL_PLACEHOLDER = "LOCAL_FILE_VISUAL_PLACEHOLDER"
    RESEARCH_LAKE_VISUAL_PLACEHOLDER = "RESEARCH_LAKE_VISUAL_PLACEHOLDER"
    METADATA_VISUAL_PLACEHOLDER = "METADATA_VISUAL_PLACEHOLDER"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class StrategyResearchWorkspaceDisplayExperimentKind(StrEnum):
    EXPERIMENT_PLAN_VISUAL_PLACEHOLDER = "EXPERIMENT_PLAN_VISUAL_PLACEHOLDER"
    VALIDATION_PLAN_VISUAL_PLACEHOLDER = "VALIDATION_PLAN_VISUAL_PLACEHOLDER"
    BACKTEST_PLAN_VISUAL_PLACEHOLDER = "BACKTEST_PLAN_VISUAL_PLACEHOLDER"
    WALK_FORWARD_PLAN_VISUAL_PLACEHOLDER = "WALK_FORWARD_PLAN_VISUAL_PLACEHOLDER"
    SAFETY_REVIEW_PLAN_VISUAL_PLACEHOLDER = "SAFETY_REVIEW_PLAN_VISUAL_PLACEHOLDER"
    UNKNOWN = "UNKNOWN"


class StrategyResearchWorkspaceDisplayBadgeKind(StrEnum):
    PLANNING_ONLY = "PLANNING_ONLY"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_ACTIVE_UI = "NOT_ACTIVE_UI"
    NOT_A_PAPER_PARSER = "NOT_A_PAPER_PARSER"
    NOT_A_STRATEGY = "NOT_A_STRATEGY"
    NOT_A_BACKTEST = "NOT_A_BACKTEST"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    NOT_READINESS_TO_TRADE = "NOT_READINESS_TO_TRADE"
    NO_BROKER_CONTROL = "NO_BROKER_CONTROL"
    NO_EXECUTION = "NO_EXECUTION"
    UNKNOWN = "UNKNOWN"


class StrategyResearchWorkspaceDisplaySafetyLabel(StrEnum):
    DISPLAY_CONTRACT_ONLY = "DISPLAY_CONTRACT_ONLY"
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


def sanitize_strategy_research_workspace_display_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


STRATEGY_RESEARCH_WORKSPACE_DISPLAY_FORBIDDEN_OUTPUTS = [
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
]


class StrategyResearchWorkspaceDisplayContractMetadata(BaseModel):
    contract_id: str
    service_name: str = "stark-terminal-strategy-research-workspace-display"
    stage: StrategyResearchWorkspaceDisplayStage = (
        StrategyResearchWorkspaceDisplayStage.DISPLAY_CONTRACT_SKELETON
    )
    workspace_kinds: list[StrategyResearchWorkspaceDisplayWorkspaceKind]
    artifact_kinds: list[StrategyResearchWorkspaceDisplayArtifactKind]
    paper_kinds: list[StrategyResearchWorkspaceDisplayPaperKind]
    hypothesis_kinds: list[StrategyResearchWorkspaceDisplayHypothesisKind]
    dataset_kinds: list[StrategyResearchWorkspaceDisplayDatasetKind]
    experiment_kinds: list[StrategyResearchWorkspaceDisplayExperimentKind]
    badge_kinds: list[StrategyResearchWorkspaceDisplayBadgeKind]
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
        return _non_empty_text(value, "strategy research workspace display contract text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def contract_metadata_must_fail_closed(self) -> StrategyResearchWorkspaceDisplayContractMetadata:
        if self.stage == StrategyResearchWorkspaceDisplayStage.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research Workspace Display stage is not allowed")
        kind_checks = [
            (self.workspace_kinds, StrategyResearchWorkspaceDisplayWorkspaceKind.UNKNOWN, "workspace"),
            (self.artifact_kinds, StrategyResearchWorkspaceDisplayArtifactKind.UNKNOWN, "artifact"),
            (self.paper_kinds, StrategyResearchWorkspaceDisplayPaperKind.UNKNOWN, "paper"),
            (self.hypothesis_kinds, StrategyResearchWorkspaceDisplayHypothesisKind.UNKNOWN, "hypothesis"),
            (self.dataset_kinds, StrategyResearchWorkspaceDisplayDatasetKind.UNKNOWN, "dataset"),
            (self.experiment_kinds, StrategyResearchWorkspaceDisplayExperimentKind.UNKNOWN, "experiment"),
            (self.badge_kinds, StrategyResearchWorkspaceDisplayBadgeKind.UNKNOWN, "badge"),
        ]
        for values, unknown, label in kind_checks:
            if not values or unknown in values:
                raise ValueError(f"Strategy Research Workspace Display metadata requires known {label} kinds")
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
            raise ValueError("Strategy Research Workspace Display forbids: " + ", ".join(enabled))
        if not self.returns_unavailable_by_default:
            raise ValueError("Strategy Research Workspace Display must return unavailable by default")
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


def default_strategy_research_workspace_display_contract_metadata() -> (
    StrategyResearchWorkspaceDisplayContractMetadata
):
    return StrategyResearchWorkspaceDisplayContractMetadata(
        contract_id="strategy-research-workspace-display-contract-metadata-v1",
        workspace_kinds=[
            StrategyResearchWorkspaceDisplayWorkspaceKind.PAPER_RESEARCH_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayWorkspaceKind.STRATEGY_HYPOTHESIS_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayWorkspaceKind.DATASET_CONTEXT_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayWorkspaceKind.EXPERIMENT_PLAN_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayWorkspaceKind.EVIDENCE_REVIEW_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayWorkspaceKind.SAFETY_REVIEW_VISUAL_PLACEHOLDER,
        ],
        artifact_kinds=[
            StrategyResearchWorkspaceDisplayArtifactKind.PAPER_REFERENCE_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayArtifactKind.STRATEGY_HYPOTHESIS_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayArtifactKind.DATASET_REFERENCE_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayArtifactKind.EXPERIMENT_PLAN_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayArtifactKind.EVIDENCE_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayArtifactKind.SAFETY_NOTE_VISUAL_PLACEHOLDER,
        ],
        paper_kinds=[
            StrategyResearchWorkspaceDisplayPaperKind.ARXIV_REFERENCE_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayPaperKind.DOI_REFERENCE_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayPaperKind.LOCAL_DOCUMENT_REFERENCE_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayPaperKind.ABSTRACT_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayPaperKind.METHOD_SUMMARY_VISUAL_PLACEHOLDER,
        ],
        hypothesis_kinds=[
            StrategyResearchWorkspaceDisplayHypothesisKind.STRATEGY_HYPOTHESIS_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayHypothesisKind.SIGNAL_HYPOTHESIS_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayHypothesisKind.FACTOR_HYPOTHESIS_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayHypothesisKind.RISK_HYPOTHESIS_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayHypothesisKind.EXECUTION_HYPOTHESIS_VISUAL_PLACEHOLDER,
        ],
        dataset_kinds=[
            StrategyResearchWorkspaceDisplayDatasetKind.SYNTHETIC_DATASET_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayDatasetKind.LOCAL_FILE_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayDatasetKind.RESEARCH_LAKE_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayDatasetKind.METADATA_VISUAL_PLACEHOLDER,
        ],
        experiment_kinds=[
            StrategyResearchWorkspaceDisplayExperimentKind.EXPERIMENT_PLAN_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayExperimentKind.VALIDATION_PLAN_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayExperimentKind.BACKTEST_PLAN_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayExperimentKind.WALK_FORWARD_PLAN_VISUAL_PLACEHOLDER,
            StrategyResearchWorkspaceDisplayExperimentKind.SAFETY_REVIEW_PLAN_VISUAL_PLACEHOLDER,
        ],
        badge_kinds=[
            StrategyResearchWorkspaceDisplayBadgeKind.PLANNING_ONLY,
            StrategyResearchWorkspaceDisplayBadgeKind.UNAVAILABLE,
            StrategyResearchWorkspaceDisplayBadgeKind.NOT_ACTIVE_UI,
            StrategyResearchWorkspaceDisplayBadgeKind.NOT_A_PAPER_PARSER,
            StrategyResearchWorkspaceDisplayBadgeKind.NOT_A_STRATEGY,
            StrategyResearchWorkspaceDisplayBadgeKind.NOT_A_BACKTEST,
            StrategyResearchWorkspaceDisplayBadgeKind.NOT_A_RECOMMENDATION,
            StrategyResearchWorkspaceDisplayBadgeKind.NOT_READINESS_TO_TRADE,
            StrategyResearchWorkspaceDisplayBadgeKind.NO_BROKER_CONTROL,
            StrategyResearchWorkspaceDisplayBadgeKind.NO_EXECUTION,
        ],
        forbidden_outputs=list(STRATEGY_RESEARCH_WORKSPACE_DISPLAY_FORBIDDEN_OUTPUTS),
    )
