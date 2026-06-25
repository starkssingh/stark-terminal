from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class StrategyResearchWorkspaceStage(StrEnum):
    PLANNING_AND_GUARDRAILS = "PLANNING_AND_GUARDRAILS"
    UNAVAILABLE_ONLY = "UNAVAILABLE_ONLY"
    WORKSPACE_PLACEHOLDERS = "WORKSPACE_PLACEHOLDERS"
    RESEARCH_ARTIFACT_PLACEHOLDERS = "RESEARCH_ARTIFACT_PLACEHOLDERS"
    STRATEGY_PLACEHOLDERS = "STRATEGY_PLACEHOLDERS"
    ACTIVE_UI_PLANNED = "ACTIVE_UI_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class StrategyResearchWorkspaceKind(StrEnum):
    PAPER_RESEARCH_PLACEHOLDER = "PAPER_RESEARCH_PLACEHOLDER"
    STRATEGY_HYPOTHESIS_PLACEHOLDER = "STRATEGY_HYPOTHESIS_PLACEHOLDER"
    DATASET_CONTEXT_PLACEHOLDER = "DATASET_CONTEXT_PLACEHOLDER"
    EXPERIMENT_PLAN_PLACEHOLDER = "EXPERIMENT_PLAN_PLACEHOLDER"
    EVIDENCE_REVIEW_PLACEHOLDER = "EVIDENCE_REVIEW_PLACEHOLDER"
    SAFETY_REVIEW_PLACEHOLDER = "SAFETY_REVIEW_PLACEHOLDER"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class StrategyResearchArtifactKind(StrEnum):
    PAPER_REFERENCE = "PAPER_REFERENCE"
    STRATEGY_HYPOTHESIS = "STRATEGY_HYPOTHESIS"
    DATASET_REFERENCE = "DATASET_REFERENCE"
    EXPERIMENT_PLAN = "EXPERIMENT_PLAN"
    EVIDENCE_PLACEHOLDER = "EVIDENCE_PLACEHOLDER"
    SAFETY_NOTE = "SAFETY_NOTE"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class StrategyResearchPaperReferenceKind(StrEnum):
    ARXIV_REFERENCE_PLACEHOLDER = "ARXIV_REFERENCE_PLACEHOLDER"
    DOI_REFERENCE_PLACEHOLDER = "DOI_REFERENCE_PLACEHOLDER"
    LOCAL_DOCUMENT_REFERENCE_PLACEHOLDER = "LOCAL_DOCUMENT_REFERENCE_PLACEHOLDER"
    ABSTRACT_PLACEHOLDER = "ABSTRACT_PLACEHOLDER"
    METHOD_SUMMARY_PLACEHOLDER = "METHOD_SUMMARY_PLACEHOLDER"
    UNKNOWN = "UNKNOWN"


class StrategyResearchHypothesisKind(StrEnum):
    STRATEGY_HYPOTHESIS_PLACEHOLDER = "STRATEGY_HYPOTHESIS_PLACEHOLDER"
    SIGNAL_HYPOTHESIS_PLACEHOLDER = "SIGNAL_HYPOTHESIS_PLACEHOLDER"
    FACTOR_HYPOTHESIS_PLACEHOLDER = "FACTOR_HYPOTHESIS_PLACEHOLDER"
    RISK_HYPOTHESIS_PLACEHOLDER = "RISK_HYPOTHESIS_PLACEHOLDER"
    EXECUTION_HYPOTHESIS_PLACEHOLDER = "EXECUTION_HYPOTHESIS_PLACEHOLDER"
    UNKNOWN = "UNKNOWN"


class StrategyResearchDatasetReferenceKind(StrEnum):
    SYNTHETIC_DATASET_REFERENCE = "SYNTHETIC_DATASET_REFERENCE"
    LOCAL_FILE_REFERENCE = "LOCAL_FILE_REFERENCE"
    RESEARCH_LAKE_REFERENCE = "RESEARCH_LAKE_REFERENCE"
    METADATA_REFERENCE = "METADATA_REFERENCE"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class StrategyResearchExperimentKind(StrEnum):
    EXPERIMENT_PLAN_PLACEHOLDER = "EXPERIMENT_PLAN_PLACEHOLDER"
    VALIDATION_PLAN_PLACEHOLDER = "VALIDATION_PLAN_PLACEHOLDER"
    BACKTEST_PLAN_PLACEHOLDER = "BACKTEST_PLAN_PLACEHOLDER"
    WALK_FORWARD_PLAN_PLACEHOLDER = "WALK_FORWARD_PLAN_PLACEHOLDER"
    SAFETY_REVIEW_PLAN_PLACEHOLDER = "SAFETY_REVIEW_PLAN_PLACEHOLDER"
    UNKNOWN = "UNKNOWN"


class StrategyResearchForbiddenInteractionKind(StrEnum):
    ACTIVE_UI = "ACTIVE_UI"
    FRONTEND_COMPONENT = "FRONTEND_COMPONENT"
    DESKTOP_COMPONENT = "DESKTOP_COMPONENT"
    PAPER_INGESTION = "PAPER_INGESTION"
    PAPER_PARSING = "PAPER_PARSING"
    STRATEGY_GENERATION = "STRATEGY_GENERATION"
    STRATEGY_CODE_GENERATION = "STRATEGY_CODE_GENERATION"
    BACKTESTING = "BACKTESTING"
    OPTIMIZATION = "OPTIMIZATION"
    RECOMMENDATION_GENERATION = "RECOMMENDATION_GENERATION"
    ACTION_GENERATION = "ACTION_GENERATION"
    CONFIDENCE_SCORING = "CONFIDENCE_SCORING"
    DECISION_OBJECT_GENERATION = "DECISION_OBJECT_GENERATION"
    READINESS_TO_TRADE = "READINESS_TO_TRADE"
    BROKER_CONTROL = "BROKER_CONTROL"
    ORDER_BUTTON = "ORDER_BUTTON"
    EXECUTION = "EXECUTION"
    APPROVAL_CONTROL = "APPROVAL_CONTROL"
    OVERRIDE_CONTROL = "OVERRIDE_CONTROL"
    LIVE_DATA_CONTROL = "LIVE_DATA_CONTROL"
    UNKNOWN = "UNKNOWN"


class StrategyResearchSafetyLabel(StrEnum):
    PLANNING_ONLY = "PLANNING_ONLY"
    NOT_ACTIVE_UI = "NOT_ACTIVE_UI"
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


def sanitize_strategy_research_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


REQUIRED_STRATEGY_RESEARCH_FORBIDDEN_INTERACTIONS = {
    StrategyResearchForbiddenInteractionKind.PAPER_INGESTION,
    StrategyResearchForbiddenInteractionKind.PAPER_PARSING,
    StrategyResearchForbiddenInteractionKind.STRATEGY_GENERATION,
    StrategyResearchForbiddenInteractionKind.STRATEGY_CODE_GENERATION,
    StrategyResearchForbiddenInteractionKind.BACKTESTING,
    StrategyResearchForbiddenInteractionKind.OPTIMIZATION,
    StrategyResearchForbiddenInteractionKind.RECOMMENDATION_GENERATION,
    StrategyResearchForbiddenInteractionKind.ACTION_GENERATION,
    StrategyResearchForbiddenInteractionKind.CONFIDENCE_SCORING,
    StrategyResearchForbiddenInteractionKind.DECISION_OBJECT_GENERATION,
    StrategyResearchForbiddenInteractionKind.READINESS_TO_TRADE,
    StrategyResearchForbiddenInteractionKind.BROKER_CONTROL,
    StrategyResearchForbiddenInteractionKind.EXECUTION,
}


class StrategyResearchWorkspacePlanningContract(BaseModel):
    plan_id: str
    name: str
    stage: StrategyResearchWorkspaceStage = StrategyResearchWorkspaceStage.PLANNING_AND_GUARDRAILS
    purpose: str
    planned_workspaces: list[StrategyResearchWorkspaceKind]
    planned_artifacts: list[StrategyResearchArtifactKind]
    planned_paper_references: list[StrategyResearchPaperReferenceKind]
    planned_hypotheses: list[StrategyResearchHypothesisKind]
    planned_dataset_references: list[StrategyResearchDatasetReferenceKind]
    planned_experiments: list[StrategyResearchExperimentKind]
    forbidden_interactions: list[StrategyResearchForbiddenInteractionKind]
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
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("plan_id", "name", "purpose", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace planning text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def planning_contract_must_fail_closed(self) -> StrategyResearchWorkspacePlanningContract:
        if self.stage == StrategyResearchWorkspaceStage.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research Workspace stage is not allowed")
        if not self.planned_workspaces or StrategyResearchWorkspaceKind.UNKNOWN in self.planned_workspaces:
            raise ValueError("Strategy Research Workspace planning requires known workspace kinds")
        if not self.planned_artifacts or StrategyResearchArtifactKind.UNKNOWN in self.planned_artifacts:
            raise ValueError("Strategy Research Workspace planning requires known artifact kinds")
        if (
            not self.planned_paper_references
            or StrategyResearchPaperReferenceKind.UNKNOWN in self.planned_paper_references
        ):
            raise ValueError("Strategy Research Workspace planning requires known paper reference kinds")
        if not self.planned_hypotheses or StrategyResearchHypothesisKind.UNKNOWN in self.planned_hypotheses:
            raise ValueError("Strategy Research Workspace planning requires known hypothesis kinds")
        if (
            not self.planned_dataset_references
            or StrategyResearchDatasetReferenceKind.UNKNOWN in self.planned_dataset_references
        ):
            raise ValueError("Strategy Research Workspace planning requires known dataset reference kinds")
        if not self.planned_experiments or StrategyResearchExperimentKind.UNKNOWN in self.planned_experiments:
            raise ValueError("Strategy Research Workspace planning requires known experiment kinds")
        if (
            not self.forbidden_interactions
            or StrategyResearchForbiddenInteractionKind.UNKNOWN in self.forbidden_interactions
        ):
            raise ValueError("Strategy Research Workspace planning requires known forbidden interactions")
        missing = sorted(
            kind.value for kind in REQUIRED_STRATEGY_RESEARCH_FORBIDDEN_INTERACTIONS - set(self.forbidden_interactions)
        )
        if missing:
            raise ValueError("Strategy Research Workspace missing forbidden interactions: " + ", ".join(missing))
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
            raise ValueError("Strategy Research Workspace cannot allow: " + ", ".join(enabled))
        if not self.returns_unavailable_by_default:
            raise ValueError("Strategy Research Workspace must return unavailable by default in Prompt 63")
        return self


def default_strategy_research_workspace_planning_contract() -> StrategyResearchWorkspacePlanningContract:
    return StrategyResearchWorkspacePlanningContract(
        plan_id="strategy-research-workspace-planning-guardrails-v1",
        name="Strategy Research Workspace Planning and Guardrails",
        purpose=(
            "Define planning-only research workspace, artifact, paper reference, strategy hypothesis, dataset, "
            "experiment, safety, and forbidden interaction contracts without paper ingestion, strategy generation, "
            "backtesting, recommendations, broker controls, or execution."
        ),
        planned_workspaces=[
            StrategyResearchWorkspaceKind.PAPER_RESEARCH_PLACEHOLDER,
            StrategyResearchWorkspaceKind.STRATEGY_HYPOTHESIS_PLACEHOLDER,
            StrategyResearchWorkspaceKind.DATASET_CONTEXT_PLACEHOLDER,
            StrategyResearchWorkspaceKind.EXPERIMENT_PLAN_PLACEHOLDER,
            StrategyResearchWorkspaceKind.EVIDENCE_REVIEW_PLACEHOLDER,
            StrategyResearchWorkspaceKind.SAFETY_REVIEW_PLACEHOLDER,
        ],
        planned_artifacts=[
            StrategyResearchArtifactKind.PAPER_REFERENCE,
            StrategyResearchArtifactKind.STRATEGY_HYPOTHESIS,
            StrategyResearchArtifactKind.DATASET_REFERENCE,
            StrategyResearchArtifactKind.EXPERIMENT_PLAN,
            StrategyResearchArtifactKind.EVIDENCE_PLACEHOLDER,
            StrategyResearchArtifactKind.SAFETY_NOTE,
        ],
        planned_paper_references=[
            StrategyResearchPaperReferenceKind.ARXIV_REFERENCE_PLACEHOLDER,
            StrategyResearchPaperReferenceKind.DOI_REFERENCE_PLACEHOLDER,
            StrategyResearchPaperReferenceKind.LOCAL_DOCUMENT_REFERENCE_PLACEHOLDER,
            StrategyResearchPaperReferenceKind.ABSTRACT_PLACEHOLDER,
            StrategyResearchPaperReferenceKind.METHOD_SUMMARY_PLACEHOLDER,
        ],
        planned_hypotheses=[
            StrategyResearchHypothesisKind.STRATEGY_HYPOTHESIS_PLACEHOLDER,
            StrategyResearchHypothesisKind.SIGNAL_HYPOTHESIS_PLACEHOLDER,
            StrategyResearchHypothesisKind.FACTOR_HYPOTHESIS_PLACEHOLDER,
            StrategyResearchHypothesisKind.RISK_HYPOTHESIS_PLACEHOLDER,
            StrategyResearchHypothesisKind.EXECUTION_HYPOTHESIS_PLACEHOLDER,
        ],
        planned_dataset_references=[
            StrategyResearchDatasetReferenceKind.SYNTHETIC_DATASET_REFERENCE,
            StrategyResearchDatasetReferenceKind.LOCAL_FILE_REFERENCE,
            StrategyResearchDatasetReferenceKind.RESEARCH_LAKE_REFERENCE,
            StrategyResearchDatasetReferenceKind.METADATA_REFERENCE,
        ],
        planned_experiments=[
            StrategyResearchExperimentKind.EXPERIMENT_PLAN_PLACEHOLDER,
            StrategyResearchExperimentKind.VALIDATION_PLAN_PLACEHOLDER,
            StrategyResearchExperimentKind.BACKTEST_PLAN_PLACEHOLDER,
            StrategyResearchExperimentKind.WALK_FORWARD_PLAN_PLACEHOLDER,
            StrategyResearchExperimentKind.SAFETY_REVIEW_PLAN_PLACEHOLDER,
        ],
        forbidden_interactions=[kind for kind in StrategyResearchForbiddenInteractionKind if kind != StrategyResearchForbiddenInteractionKind.UNKNOWN],
        notes=[
            "Prompt 63 creates planning and guardrails only.",
            "No active UI, paper parsing, strategy generation, backtesting, recommendations, broker controls, or execution are implemented.",
        ],
    )
