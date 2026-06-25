from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.strategy_research_workspace.artifacts import default_strategy_research_artifact_placeholders
from stark_terminal_core.strategy_research_workspace.datasets import (
    default_strategy_research_dataset_reference_placeholders,
)
from stark_terminal_core.strategy_research_workspace.experiments import default_strategy_research_experiment_placeholders
from stark_terminal_core.strategy_research_workspace.interactions import default_strategy_research_forbidden_interactions
from stark_terminal_core.strategy_research_workspace.papers import (
    default_strategy_research_paper_reference_placeholders,
)
from stark_terminal_core.strategy_research_workspace.strategies import (
    default_strategy_research_hypothesis_placeholders,
)
from stark_terminal_core.strategy_research_workspace.workspaces import (
    default_strategy_research_workspace_placeholders,
)


class StrategyResearchWorkspaceHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    stage: str
    active_ui_allowed: bool
    frontend_components_allowed: bool
    desktop_components_allowed: bool
    paper_ingestion_allowed: bool
    paper_parsing_allowed: bool
    strategy_generation_allowed: bool
    strategy_code_generation_allowed: bool
    backtesting_allowed: bool
    optimization_allowed: bool
    recommendations_allowed: bool
    action_generation_allowed: bool
    confidence_scoring_allowed: bool
    decision_object_generation_allowed: bool
    readiness_to_trade_allowed: bool
    broker_controls_allowed: bool
    execution_allowed: bool = False
    approval_allowed: bool
    override_allowed: bool
    returns_unavailable_by_default: bool
    default_workspace_count: int
    default_artifact_count: int
    default_paper_reference_count: int
    default_hypothesis_count: int
    default_dataset_reference_count: int
    default_experiment_count: int
    forbidden_interaction_count: int
    status: str
    error: str | None = None


def check_strategy_research_workspace_health(
    settings: Settings | None = None,
) -> StrategyResearchWorkspaceHealthStatus:
    resolved_settings = settings or get_settings()
    workspaces = default_strategy_research_workspace_placeholders()
    artifacts = default_strategy_research_artifact_placeholders()
    papers = default_strategy_research_paper_reference_placeholders()
    hypotheses = default_strategy_research_hypothesis_placeholders()
    datasets = default_strategy_research_dataset_reference_placeholders()
    experiments = default_strategy_research_experiment_placeholders()
    forbidden_interactions = default_strategy_research_forbidden_interactions()
    unsafe_flags: dict[str, Any] = {
        "active_ui_allowed": resolved_settings.strategy_research_workspace_allow_active_ui,
        "frontend_components_allowed": resolved_settings.strategy_research_workspace_allow_frontend_components,
        "desktop_components_allowed": resolved_settings.strategy_research_workspace_allow_desktop_components,
        "paper_ingestion_allowed": resolved_settings.strategy_research_workspace_allow_paper_ingestion,
        "paper_parsing_allowed": resolved_settings.strategy_research_workspace_allow_paper_parsing,
        "strategy_generation_allowed": resolved_settings.strategy_research_workspace_allow_strategy_generation,
        "strategy_code_generation_allowed": (
            resolved_settings.strategy_research_workspace_allow_strategy_code_generation
        ),
        "backtesting_allowed": resolved_settings.strategy_research_workspace_allow_backtesting,
        "optimization_allowed": resolved_settings.strategy_research_workspace_allow_optimization,
        "recommendations_allowed": resolved_settings.strategy_research_workspace_allow_recommendations,
        "action_generation_allowed": resolved_settings.strategy_research_workspace_allow_action_generation,
        "confidence_scoring_allowed": resolved_settings.strategy_research_workspace_allow_confidence_scoring,
        "decision_object_generation_allowed": (
            resolved_settings.strategy_research_workspace_allow_decision_object_generation
        ),
        "readiness_to_trade_allowed": resolved_settings.strategy_research_workspace_allow_readiness_to_trade,
        "broker_controls_allowed": resolved_settings.strategy_research_workspace_allow_broker_controls,
        "execution_allowed": resolved_settings.strategy_research_workspace_allow_execution,
        "approval_allowed": resolved_settings.strategy_research_workspace_allow_approval,
        "override_allowed": resolved_settings.strategy_research_workspace_allow_override,
    }
    error: str | None = None
    if any(bool(value) for value in unsafe_flags.values()):
        error = "Strategy Research Workspace unsafe flags must remain false"
    elif not resolved_settings.strategy_research_workspace_schema_version:
        error = "Strategy Research Workspace schema version cannot be empty"
    elif not resolved_settings.strategy_research_workspace_return_unavailable_by_default:
        error = "Strategy Research Workspace must return unavailable by default"
    elif not all([workspaces, artifacts, papers, hypotheses, datasets, experiments, forbidden_interactions]):
        error = "Strategy Research Workspace default placeholders and forbidden interactions are required"
    return StrategyResearchWorkspaceHealthStatus(
        enabled=resolved_settings.strategy_research_workspace_enabled,
        schema_version=resolved_settings.strategy_research_workspace_schema_version,
        stage=resolved_settings.strategy_research_workspace_stage,
        active_ui_allowed=resolved_settings.strategy_research_workspace_allow_active_ui,
        frontend_components_allowed=resolved_settings.strategy_research_workspace_allow_frontend_components,
        desktop_components_allowed=resolved_settings.strategy_research_workspace_allow_desktop_components,
        paper_ingestion_allowed=resolved_settings.strategy_research_workspace_allow_paper_ingestion,
        paper_parsing_allowed=resolved_settings.strategy_research_workspace_allow_paper_parsing,
        strategy_generation_allowed=resolved_settings.strategy_research_workspace_allow_strategy_generation,
        strategy_code_generation_allowed=(
            resolved_settings.strategy_research_workspace_allow_strategy_code_generation
        ),
        backtesting_allowed=resolved_settings.strategy_research_workspace_allow_backtesting,
        optimization_allowed=resolved_settings.strategy_research_workspace_allow_optimization,
        recommendations_allowed=resolved_settings.strategy_research_workspace_allow_recommendations,
        action_generation_allowed=resolved_settings.strategy_research_workspace_allow_action_generation,
        confidence_scoring_allowed=resolved_settings.strategy_research_workspace_allow_confidence_scoring,
        decision_object_generation_allowed=(
            resolved_settings.strategy_research_workspace_allow_decision_object_generation
        ),
        readiness_to_trade_allowed=resolved_settings.strategy_research_workspace_allow_readiness_to_trade,
        broker_controls_allowed=resolved_settings.strategy_research_workspace_allow_broker_controls,
        execution_allowed=False,
        approval_allowed=resolved_settings.strategy_research_workspace_allow_approval,
        override_allowed=resolved_settings.strategy_research_workspace_allow_override,
        returns_unavailable_by_default=resolved_settings.strategy_research_workspace_return_unavailable_by_default,
        default_workspace_count=len(workspaces),
        default_artifact_count=len(artifacts),
        default_paper_reference_count=len(papers),
        default_hypothesis_count=len(hypotheses),
        default_dataset_reference_count=len(datasets),
        default_experiment_count=len(experiments),
        forbidden_interaction_count=len(forbidden_interactions),
        status="healthy" if error is None else "blocked",
        error=error,
    )
