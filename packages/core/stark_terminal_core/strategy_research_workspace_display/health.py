from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.strategy_research_workspace_display.artifacts import (
    default_strategy_research_workspace_display_artifact_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.badges import (
    default_strategy_research_workspace_display_badges,
)
from stark_terminal_core.strategy_research_workspace_display.datasets import (
    default_strategy_research_workspace_display_dataset_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.experiments import (
    default_strategy_research_workspace_display_experiment_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.hypotheses import (
    default_strategy_research_workspace_display_hypothesis_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.papers import (
    default_strategy_research_workspace_display_paper_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.workspaces import (
    default_strategy_research_workspace_display_workspace_placeholders,
)


class StrategyResearchWorkspaceDisplayHealthStatus(BaseModel):
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
    workspace_count: int
    artifact_count: int
    paper_count: int
    hypothesis_count: int
    dataset_count: int
    experiment_count: int
    badge_count: int
    status: str
    error: str | None = None


def check_strategy_research_workspace_display_health(
    settings: Settings | None = None,
) -> StrategyResearchWorkspaceDisplayHealthStatus:
    resolved = settings or get_settings()
    workspaces = default_strategy_research_workspace_display_workspace_placeholders()
    artifacts = default_strategy_research_workspace_display_artifact_placeholders()
    papers = default_strategy_research_workspace_display_paper_placeholders()
    hypotheses = default_strategy_research_workspace_display_hypothesis_placeholders()
    datasets = default_strategy_research_workspace_display_dataset_placeholders()
    experiments = default_strategy_research_workspace_display_experiment_placeholders()
    badges = default_strategy_research_workspace_display_badges()
    unsafe_flags = (
        resolved.strategy_research_workspace_display_allow_active_ui
        or resolved.strategy_research_workspace_display_allow_frontend_components
        or resolved.strategy_research_workspace_display_allow_desktop_components
        or resolved.strategy_research_workspace_display_allow_paper_ingestion
        or resolved.strategy_research_workspace_display_allow_paper_parsing
        or resolved.strategy_research_workspace_display_allow_strategy_generation
        or resolved.strategy_research_workspace_display_allow_strategy_code_generation
        or resolved.strategy_research_workspace_display_allow_backtesting
        or resolved.strategy_research_workspace_display_allow_optimization
        or resolved.strategy_research_workspace_display_allow_recommendations
        or resolved.strategy_research_workspace_display_allow_action_generation
        or resolved.strategy_research_workspace_display_allow_confidence_scoring
        or resolved.strategy_research_workspace_display_allow_decision_object_generation
        or resolved.strategy_research_workspace_display_allow_readiness_to_trade
        or resolved.strategy_research_workspace_display_allow_broker_controls
        or resolved.strategy_research_workspace_display_allow_execution
        or resolved.strategy_research_workspace_display_allow_approval
        or resolved.strategy_research_workspace_display_allow_override
        or resolved.execution_apis_enabled
    )
    has_required_configuration = (
        bool(resolved.strategy_research_workspace_display_schema_version.strip())
        and resolved.strategy_research_workspace_display_stage == "display_contract_skeleton"
        and resolved.strategy_research_workspace_display_return_unavailable_by_default
        and bool(workspaces)
        and bool(artifacts)
        and bool(papers)
        and bool(hypotheses)
        and bool(datasets)
        and bool(experiments)
        and bool(badges)
    )
    status = (
        "healthy"
        if resolved.strategy_research_workspace_display_enabled and not unsafe_flags and has_required_configuration
        else "blocked"
    )
    error = None if status == "healthy" else "Strategy Research Workspace Display flags are not fail-closed"
    return StrategyResearchWorkspaceDisplayHealthStatus(
        enabled=resolved.strategy_research_workspace_display_enabled,
        schema_version=resolved.strategy_research_workspace_display_schema_version,
        stage=resolved.strategy_research_workspace_display_stage,
        active_ui_allowed=resolved.strategy_research_workspace_display_allow_active_ui,
        frontend_components_allowed=resolved.strategy_research_workspace_display_allow_frontend_components,
        desktop_components_allowed=resolved.strategy_research_workspace_display_allow_desktop_components,
        paper_ingestion_allowed=resolved.strategy_research_workspace_display_allow_paper_ingestion,
        paper_parsing_allowed=resolved.strategy_research_workspace_display_allow_paper_parsing,
        strategy_generation_allowed=resolved.strategy_research_workspace_display_allow_strategy_generation,
        strategy_code_generation_allowed=(
            resolved.strategy_research_workspace_display_allow_strategy_code_generation
        ),
        backtesting_allowed=resolved.strategy_research_workspace_display_allow_backtesting,
        optimization_allowed=resolved.strategy_research_workspace_display_allow_optimization,
        recommendations_allowed=resolved.strategy_research_workspace_display_allow_recommendations,
        action_generation_allowed=resolved.strategy_research_workspace_display_allow_action_generation,
        confidence_scoring_allowed=resolved.strategy_research_workspace_display_allow_confidence_scoring,
        decision_object_generation_allowed=(
            resolved.strategy_research_workspace_display_allow_decision_object_generation
        ),
        readiness_to_trade_allowed=resolved.strategy_research_workspace_display_allow_readiness_to_trade,
        broker_controls_allowed=resolved.strategy_research_workspace_display_allow_broker_controls,
        execution_allowed=False,
        approval_allowed=resolved.strategy_research_workspace_display_allow_approval,
        override_allowed=resolved.strategy_research_workspace_display_allow_override,
        returns_unavailable_by_default=(
            resolved.strategy_research_workspace_display_return_unavailable_by_default
        ),
        workspace_count=len(workspaces),
        artifact_count=len(artifacts),
        paper_count=len(papers),
        hypothesis_count=len(hypotheses),
        dataset_count=len(datasets),
        experiment_count=len(experiments),
        badge_count=len(badges),
        status=status,
        error=error,
    )
