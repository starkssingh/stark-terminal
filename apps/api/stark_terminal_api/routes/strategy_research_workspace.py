from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.strategy_research_workspace.artifacts import (
    default_strategy_research_artifact_placeholders,
)
from stark_terminal_core.strategy_research_workspace.datasets import (
    default_strategy_research_dataset_reference_placeholders,
)
from stark_terminal_core.strategy_research_workspace.experiments import (
    default_strategy_research_experiment_placeholders,
)
from stark_terminal_core.strategy_research_workspace.health import (
    check_strategy_research_workspace_health,
)
from stark_terminal_core.strategy_research_workspace.interactions import (
    default_strategy_research_forbidden_interactions,
)
from stark_terminal_core.strategy_research_workspace.papers import (
    default_strategy_research_paper_reference_placeholders,
)
from stark_terminal_core.strategy_research_workspace.planning import (
    default_strategy_research_workspace_planning_contract,
)
from stark_terminal_core.strategy_research_workspace.readiness import (
    build_strategy_research_workspace_readiness_report,
)
from stark_terminal_core.strategy_research_workspace.safety import (
    default_strategy_research_safety_policy,
    evaluate_strategy_research_plan_safety,
)
from stark_terminal_core.strategy_research_workspace.strategies import (
    default_strategy_research_hypothesis_placeholders,
)
from stark_terminal_core.strategy_research_workspace.workspaces import (
    default_strategy_research_workspace_placeholders,
)

router = APIRouter()


@router.get("/strategy-research-workspace/health")
def strategy_research_workspace_health() -> dict[str, Any]:
    status = check_strategy_research_workspace_health(get_settings())
    return {
        "service": "stark-terminal-strategy-research-workspace",
        **status.model_dump(),
    }


@router.get("/strategy-research-workspace/contracts")
def strategy_research_workspace_contracts() -> dict[str, Any]:
    settings = get_settings()
    contract = default_strategy_research_workspace_planning_contract()
    return {
        "service": "stark-terminal-strategy-research-workspace",
        "schema_version": settings.strategy_research_workspace_schema_version,
        "computation_scope": "planning-and-guardrails-only",
        "active_ui_allowed_now": False,
        "frontend_components_allowed_now": False,
        "desktop_components_allowed_now": False,
        "paper_ingestion_allowed_now": False,
        "paper_parsing_allowed_now": False,
        "strategy_generation_allowed_now": False,
        "strategy_code_generation_allowed_now": False,
        "backtesting_allowed_now": False,
        "optimization_allowed_now": False,
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "readiness_to_trade_allowed_now": False,
        "broker_controls_allowed_now": False,
        "execution_allowed_now": False,
        "approval_allowed_now": False,
        "override_allowed_now": False,
        "planned_workspaces": [workspace.value for workspace in contract.planned_workspaces],
        "planned_artifacts": [artifact.value for artifact in contract.planned_artifacts],
        "planned_paper_references": [paper.value for paper in contract.planned_paper_references],
        "planned_hypotheses": [hypothesis.value for hypothesis in contract.planned_hypotheses],
        "planned_dataset_references": [dataset.value for dataset in contract.planned_dataset_references],
        "planned_experiments": [experiment.value for experiment in contract.planned_experiments],
        "forbidden_interactions": [interaction.value for interaction in contract.forbidden_interactions],
    }


@router.get("/strategy-research-workspace/placeholder-workspace")
def strategy_research_workspace_placeholder_workspace() -> dict[str, Any]:
    workspaces = default_strategy_research_workspace_placeholders()
    artifacts = default_strategy_research_artifact_placeholders()
    papers = default_strategy_research_paper_reference_placeholders()
    hypotheses = default_strategy_research_hypothesis_placeholders()
    datasets = default_strategy_research_dataset_reference_placeholders()
    experiments = default_strategy_research_experiment_placeholders()
    forbidden_interactions = default_strategy_research_forbidden_interactions()
    return {
        "service": "stark-terminal-strategy-research-workspace",
        "planning_only": True,
        "active_ui_allowed_now": False,
        "unavailable_by_default": True,
        "workspaces": [workspace.model_dump(mode="json") for workspace in workspaces],
        "artifacts": [artifact.model_dump(mode="json") for artifact in artifacts],
        "paper_references": [paper.model_dump(mode="json") for paper in papers],
        "hypotheses": [hypothesis.model_dump(mode="json") for hypothesis in hypotheses],
        "dataset_references": [dataset.model_dump(mode="json") for dataset in datasets],
        "experiments": [experiment.model_dump(mode="json") for experiment in experiments],
        "forbidden_interactions": [interaction.model_dump(mode="json") for interaction in forbidden_interactions],
        "no_active_ui": True,
        "no_paper_parsing": True,
        "no_strategy_generation": True,
        "no_backtesting": True,
        "no_recommendations": True,
        "no_broker_controls": True,
        "no_execution": True,
        "strategy_generated": False,
        "backtest_generated": False,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "readiness_to_trade": False,
        "broker_control_enabled": False,
        "execution_ready": False,
    }


@router.get("/strategy-research-workspace/readiness-template")
def strategy_research_workspace_readiness_template() -> dict[str, Any]:
    plan = default_strategy_research_workspace_planning_contract()
    workspaces = default_strategy_research_workspace_placeholders()
    artifacts = default_strategy_research_artifact_placeholders()
    papers = default_strategy_research_paper_reference_placeholders()
    hypotheses = default_strategy_research_hypothesis_placeholders()
    datasets = default_strategy_research_dataset_reference_placeholders()
    experiments = default_strategy_research_experiment_placeholders()
    forbidden_interactions = default_strategy_research_forbidden_interactions()
    policy = default_strategy_research_safety_policy(get_settings())
    safety_result = evaluate_strategy_research_plan_safety(plan, policy)
    report = build_strategy_research_workspace_readiness_report(
        plan,
        workspaces,
        artifacts,
        papers,
        hypotheses,
        datasets,
        experiments,
        forbidden_interactions,
        safety_result,
    )
    return {
        "service": "stark-terminal-strategy-research-workspace",
        "planning_only": True,
        "readiness_report": report.model_dump(mode="json"),
        "ready_for_active_ui": False,
        "ready_for_strategy_generation": False,
        "ready_for_backtesting": False,
        "ready_for_recommendations": False,
        "ready_for_broker_controls": False,
        "ready_for_execution": False,
        "no_readiness_to_trade": True,
        "strategy_generated": False,
        "backtest_generated": False,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "readiness_to_trade": False,
        "broker_control_enabled": False,
        "execution_ready": False,
    }
