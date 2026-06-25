from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.strategy_research_workspace_display.artifacts import (
    default_strategy_research_workspace_display_artifact_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.badges import (
    default_strategy_research_workspace_display_badges,
)
from stark_terminal_core.strategy_research_workspace_display.contracts import (
    default_strategy_research_workspace_display_contract_metadata,
)
from stark_terminal_core.strategy_research_workspace_display.datasets import (
    default_strategy_research_workspace_display_dataset_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.experiments import (
    default_strategy_research_workspace_display_experiment_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.health import (
    check_strategy_research_workspace_display_health,
)
from stark_terminal_core.strategy_research_workspace_display.hypotheses import (
    default_strategy_research_workspace_display_hypothesis_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.papers import (
    default_strategy_research_workspace_display_paper_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.unavailable import (
    default_strategy_research_workspace_display_unavailable_response,
)
from stark_terminal_core.strategy_research_workspace_display.workspaces import (
    default_strategy_research_workspace_display_workspace_placeholders,
)

router = APIRouter()


@router.get("/strategy-research-workspace-display/health")
def strategy_research_workspace_display_health() -> dict[str, Any]:
    status = check_strategy_research_workspace_display_health(get_settings())
    return {
        "service": "stark-terminal-strategy-research-workspace-display",
        **status.model_dump(),
    }


@router.get("/strategy-research-workspace-display/contracts")
def strategy_research_workspace_display_contracts() -> dict[str, Any]:
    settings = get_settings()
    metadata = default_strategy_research_workspace_display_contract_metadata()
    return {
        "service": "stark-terminal-strategy-research-workspace-display",
        "schema_version": settings.strategy_research_workspace_display_schema_version,
        "computation_scope": "display-contract-skeleton-only",
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
        "returns_unavailable_by_default": True,
        "workspace_kinds": [kind.value for kind in metadata.workspace_kinds],
        "artifact_kinds": [kind.value for kind in metadata.artifact_kinds],
        "paper_kinds": [kind.value for kind in metadata.paper_kinds],
        "hypothesis_kinds": [kind.value for kind in metadata.hypothesis_kinds],
        "dataset_kinds": [kind.value for kind in metadata.dataset_kinds],
        "experiment_kinds": [kind.value for kind in metadata.experiment_kinds],
        "badge_kinds": [kind.value for kind in metadata.badge_kinds],
        "forbidden_outputs": list(metadata.forbidden_outputs),
    }


@router.get("/strategy-research-workspace-display/unavailable-template")
def strategy_research_workspace_display_unavailable_template() -> dict[str, Any]:
    unavailable = default_strategy_research_workspace_display_unavailable_response()
    return {
        "service": "stark-terminal-strategy-research-workspace-display",
        "display_contract_skeleton_only": True,
        "unavailable_response": unavailable.model_dump(mode="json"),
        "no_active_ui": True,
        "no_frontend_components": True,
        "no_desktop_components": True,
        "no_paper_ingestion": True,
        "no_paper_parsing": True,
        "no_strategy_generation": True,
        "no_strategy_code_generation": True,
        "no_backtesting": True,
        "no_optimization": True,
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_readiness_to_trade": True,
        "no_broker_controls": True,
        "no_execution": True,
        "no_approval": True,
        "no_override": True,
    }


@router.get("/strategy-research-workspace-display/placeholder-workspace")
def strategy_research_workspace_display_placeholder_workspace() -> dict[str, Any]:
    return {
        "service": "stark-terminal-strategy-research-workspace-display",
        "display_contract_skeleton_only": True,
        "workspace_placeholders": [
            workspace.model_dump(mode="json")
            for workspace in default_strategy_research_workspace_display_workspace_placeholders()
        ],
        "artifact_placeholders": [
            artifact.model_dump(mode="json")
            for artifact in default_strategy_research_workspace_display_artifact_placeholders()
        ],
        "paper_placeholders": [
            paper.model_dump(mode="json")
            for paper in default_strategy_research_workspace_display_paper_placeholders()
        ],
        "hypothesis_placeholders": [
            hypothesis.model_dump(mode="json")
            for hypothesis in default_strategy_research_workspace_display_hypothesis_placeholders()
        ],
        "dataset_placeholders": [
            dataset.model_dump(mode="json")
            for dataset in default_strategy_research_workspace_display_dataset_placeholders()
        ],
        "experiment_placeholders": [
            experiment.model_dump(mode="json")
            for experiment in default_strategy_research_workspace_display_experiment_placeholders()
        ],
        "badges": [
            badge.model_dump(mode="json")
            for badge in default_strategy_research_workspace_display_badges()
        ],
        "unavailable_response": default_strategy_research_workspace_display_unavailable_response().model_dump(
            mode="json"
        ),
        "no_active_ui": True,
        "no_generated_outputs": True,
        "no_paper_parsing": True,
        "no_strategy_generation": True,
        "no_backtesting": True,
        "no_broker_controls": True,
        "no_execution": True,
        "active_ui_generated": False,
        "frontend_component_generated": False,
        "desktop_component_generated": False,
        "paper_ingested": False,
        "paper_parsed": False,
        "strategy_generated": False,
        "strategy_code_generated": False,
        "backtest_generated": False,
        "optimization_generated": False,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "readiness_to_trade_generated": False,
        "broker_control_generated": False,
        "execution_ready": False,
        "approval_granted": False,
        "override_granted": False,
    }
