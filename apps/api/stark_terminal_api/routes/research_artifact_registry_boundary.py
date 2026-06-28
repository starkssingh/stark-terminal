from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.research_artifact_registry_boundary.endpoints import (
    default_research_artifact_endpoint_boundary_policies,
)
from stark_terminal_core.research_artifact_registry_boundary.forbidden import (
    default_research_artifact_forbidden_behavior_registry,
)
from stark_terminal_core.research_artifact_registry_boundary.health import (
    check_research_artifact_boundary_health,
)
from stark_terminal_core.research_artifact_registry_boundary.invariants import (
    evaluate_research_artifact_boundary_invariants,
)
from stark_terminal_core.research_artifact_registry_boundary.modules import (
    default_research_artifact_module_boundary_policies,
)

router = APIRouter()


def _public_forbidden_behavior_label(kind_value: str) -> str:
    if kind_value == "SECRET_OR_CREDENTIAL":
        return "SENSITIVE_MATERIAL"
    return kind_value


@router.get("/research-artifact-registry-boundary/health")
def research_artifact_registry_boundary_health() -> dict[str, Any]:
    status = check_research_artifact_boundary_health(get_settings())
    return {
        "service": "stark-terminal-research-artifact-registry-boundary",
        **status.model_dump(),
    }


@router.get("/research-artifact-registry-boundary/contracts")
def research_artifact_registry_boundary_contracts() -> dict[str, Any]:
    settings = get_settings()
    registry = default_research_artifact_forbidden_behavior_registry()
    endpoint_policies = default_research_artifact_endpoint_boundary_policies()
    module_policies = default_research_artifact_module_boundary_policies()
    return {
        "service": "stark-terminal-research-artifact-registry-boundary",
        "schema_version": settings.research_artifact_registry_boundary_schema_version,
        "computation_scope": "boundary-hardening-only",
        "boundary_hardening_only": True,
        "forbidden_behaviors": [
            _public_forbidden_behavior_label(behavior.kind.value)
            for behavior in registry.behaviors
        ],
        "endpoint_families": [policy.endpoint_family for policy in endpoint_policies],
        "module_families": [policy.module_family for policy in module_policies],
        "active_ingestion_allowed": False,
        "persistent_storage_allowed": False,
        "file_uploads_allowed": False,
        "file_downloads_allowed": False,
        "file_previews_allowed": False,
        "active_ui_allowed": False,
        "frontend_components_allowed": False,
        "desktop_components_allowed": False,
        "paper_parsing_allowed": False,
        "pdf_parsing_allowed": False,
        "arxiv_ingestion_allowed": False,
        "llm_analysis_allowed": False,
        "strategy_generation_allowed": False,
        "strategy_code_generation_allowed": False,
        "backtesting_allowed": False,
        "optimization_allowed": False,
        "recommendations_allowed": False,
        "action_generation_allowed": False,
        "confidence_scoring_allowed": False,
        "decision_object_generation_allowed": False,
        "readiness_to_trade_allowed": False,
        "broker_controls_allowed": False,
        "execution_allowed": False,
        "approval_allowed": False,
        "override_allowed": False,
    }


@router.get("/research-artifact-registry-boundary/invariants")
def research_artifact_registry_boundary_invariants() -> dict[str, Any]:
    result = evaluate_research_artifact_boundary_invariants()
    return {
        "service": "stark-terminal-research-artifact-registry-boundary",
        "computation_scope": "boundary-hardening-only",
        "boundary_hardening_only": True,
        "invariant_result": result.model_dump(mode="json"),
        "blockers": list(result.blockers),
        "warnings": list(result.warnings),
        "no_active_ingestion": True,
        "no_persistent_storage": True,
        "no_file_uploads": True,
        "no_file_downloads": True,
        "no_file_previews": True,
        "no_active_ui": True,
        "no_frontend_components": True,
        "no_desktop_components": True,
        "no_paper_parsing": True,
        "no_pdf_parsing": True,
        "no_arxiv_ingestion": True,
        "no_llm_analysis": True,
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
        "no_approval": True,
        "no_override": True,
        "no_execution": True,
        "active_ingestion_enabled": False,
        "persistent_storage_enabled": False,
        "file_upload_enabled": False,
        "file_download_enabled": False,
        "file_preview_enabled": False,
        "active_ui_generated": False,
        "frontend_component_generated": False,
        "desktop_component_generated": False,
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
        "broker_control_enabled": False,
        "approval_granted": False,
        "override_granted": False,
        "execution_ready": False,
    }
