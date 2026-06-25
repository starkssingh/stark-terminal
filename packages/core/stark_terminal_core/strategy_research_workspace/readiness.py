from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace.artifacts import StrategyResearchArtifactPlaceholder
from stark_terminal_core.strategy_research_workspace.datasets import StrategyResearchDatasetReferencePlaceholder
from stark_terminal_core.strategy_research_workspace.experiments import StrategyResearchExperimentPlaceholder
from stark_terminal_core.strategy_research_workspace.interactions import StrategyResearchForbiddenInteraction
from stark_terminal_core.strategy_research_workspace.papers import StrategyResearchPaperReferencePlaceholder
from stark_terminal_core.strategy_research_workspace.planning import (
    StrategyResearchWorkspacePlanningContract,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
)
from stark_terminal_core.strategy_research_workspace.safety import StrategyResearchSafetyResult
from stark_terminal_core.strategy_research_workspace.strategies import StrategyResearchHypothesisPlaceholder
from stark_terminal_core.strategy_research_workspace.workspaces import StrategyResearchWorkspacePlaceholder


class StrategyResearchWorkspaceReadinessReport(BaseModel):
    report_id: str
    plan_id: str
    workspace_count: int = Field(ge=0)
    artifact_count: int = Field(ge=0)
    paper_reference_count: int = Field(ge=0)
    hypothesis_count: int = Field(ge=0)
    dataset_reference_count: int = Field(ge=0)
    experiment_count: int = Field(ge=0)
    forbidden_interaction_count: int = Field(ge=0)
    safety_result_safe: bool
    ready_for_api_contract_skeleton: bool = False
    ready_for_display_contract_skeleton: bool = False
    ready_for_active_ui: bool = False
    ready_for_paper_ingestion: bool = False
    ready_for_paper_parsing: bool = False
    ready_for_strategy_generation: bool = False
    ready_for_strategy_code_generation: bool = False
    ready_for_backtesting: bool = False
    ready_for_optimization: bool = False
    ready_for_recommendations: bool = False
    ready_for_action_generation: bool = False
    ready_for_confidence_scoring: bool = False
    ready_for_decision_objects: bool = False
    ready_for_readiness_to_trade: bool = False
    ready_for_broker_controls: bool = False
    ready_for_execution: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("report_id", "plan_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research readiness report text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def readiness_report_must_fail_closed(self) -> StrategyResearchWorkspaceReadinessReport:
        dangerous_flags = {
            "active UI": self.ready_for_active_ui,
            "paper ingestion": self.ready_for_paper_ingestion,
            "paper parsing": self.ready_for_paper_parsing,
            "strategy generation": self.ready_for_strategy_generation,
            "strategy code generation": self.ready_for_strategy_code_generation,
            "backtesting": self.ready_for_backtesting,
            "optimization": self.ready_for_optimization,
            "recommendations": self.ready_for_recommendations,
            "action generation": self.ready_for_action_generation,
            "confidence scoring": self.ready_for_confidence_scoring,
            "DecisionObjects": self.ready_for_decision_objects,
            "readiness-to-trade": self.ready_for_readiness_to_trade,
            "broker controls": self.ready_for_broker_controls,
            "execution": self.ready_for_execution,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Strategy Research readiness cannot allow: " + ", ".join(enabled))
        return self


def build_strategy_research_workspace_readiness_report(
    plan: StrategyResearchWorkspacePlanningContract,
    workspaces: list[StrategyResearchWorkspacePlaceholder],
    artifacts: list[StrategyResearchArtifactPlaceholder],
    papers: list[StrategyResearchPaperReferencePlaceholder],
    hypotheses: list[StrategyResearchHypothesisPlaceholder],
    datasets: list[StrategyResearchDatasetReferencePlaceholder],
    experiments: list[StrategyResearchExperimentPlaceholder],
    forbidden_interactions: list[StrategyResearchForbiddenInteraction],
    safety_result: StrategyResearchSafetyResult,
) -> StrategyResearchWorkspaceReadinessReport:
    blockers = [] if safety_result.safe else list(safety_result.reasons)
    warnings = [
        "Strategy Research Workspace is ready for API/display contract skeleton planning only.",
        "No paper ingestion, paper parsing, strategy generation, backtesting, recommendations, broker controls, or execution are allowed.",
    ]
    return StrategyResearchWorkspaceReadinessReport(
        report_id="strategy-research-workspace-readiness-report-v1",
        plan_id=plan.plan_id,
        workspace_count=len(workspaces),
        artifact_count=len(artifacts),
        paper_reference_count=len(papers),
        hypothesis_count=len(hypotheses),
        dataset_reference_count=len(datasets),
        experiment_count=len(experiments),
        forbidden_interaction_count=len(forbidden_interactions),
        safety_result_safe=safety_result.safe,
        ready_for_api_contract_skeleton=safety_result.safe and not blockers,
        ready_for_display_contract_skeleton=safety_result.safe and not blockers,
        blockers=blockers,
        warnings=warnings,
    )


def strategy_research_ready_for_active_ui(report: StrategyResearchWorkspaceReadinessReport) -> bool:
    return False


def strategy_research_ready_for_strategy_generation(report: StrategyResearchWorkspaceReadinessReport) -> bool:
    return False


def strategy_research_ready_for_backtesting(report: StrategyResearchWorkspaceReadinessReport) -> bool:
    return False


def strategy_research_ready_for_recommendations(report: StrategyResearchWorkspaceReadinessReport) -> bool:
    return False


def strategy_research_ready_for_execution(report: StrategyResearchWorkspaceReadinessReport) -> bool:
    return False
