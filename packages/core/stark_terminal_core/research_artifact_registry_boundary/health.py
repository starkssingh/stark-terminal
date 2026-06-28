from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.research_artifact_registry_boundary.endpoints import (
    default_research_artifact_endpoint_boundary_policies,
)
from stark_terminal_core.research_artifact_registry_boundary.forbidden import (
    default_research_artifact_forbidden_behavior_registry,
)
from stark_terminal_core.research_artifact_registry_boundary.invariants import (
    evaluate_research_artifact_boundary_invariants,
)
from stark_terminal_core.research_artifact_registry_boundary.modules import (
    default_research_artifact_module_boundary_policies,
)


class ResearchArtifactBoundaryHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    stage: str
    forbidden_behavior_count: int
    endpoint_policy_count: int
    module_policy_count: int
    invariant_passed: bool
    active_ingestion_allowed: bool
    persistent_storage_allowed: bool
    file_uploads_allowed: bool
    file_downloads_allowed: bool
    file_previews_allowed: bool
    active_ui_allowed: bool
    frontend_components_allowed: bool
    desktop_components_allowed: bool
    paper_parsing_allowed: bool
    pdf_parsing_allowed: bool
    arxiv_ingestion_allowed: bool
    llm_analysis_allowed: bool
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
    status: str
    error: str | None = None


def check_research_artifact_boundary_health(
    settings: Settings | None = None,
) -> ResearchArtifactBoundaryHealthStatus:
    resolved = settings or get_settings()
    registry = default_research_artifact_forbidden_behavior_registry()
    endpoint_policies = default_research_artifact_endpoint_boundary_policies()
    module_policies = default_research_artifact_module_boundary_policies()
    invariant = evaluate_research_artifact_boundary_invariants(
        endpoint_policies,
        module_policies,
        registry,
    )
    unsafe_flags: dict[str, Any] = {
        "active_ingestion_allowed": resolved.research_artifact_registry_boundary_allow_active_ingestion,
        "persistent_storage_allowed": (
            resolved.research_artifact_registry_boundary_allow_persistent_storage
        ),
        "file_uploads_allowed": resolved.research_artifact_registry_boundary_allow_file_uploads,
        "file_downloads_allowed": resolved.research_artifact_registry_boundary_allow_file_downloads,
        "file_previews_allowed": resolved.research_artifact_registry_boundary_allow_file_previews,
        "active_ui_allowed": resolved.research_artifact_registry_boundary_allow_active_ui,
        "frontend_components_allowed": (
            resolved.research_artifact_registry_boundary_allow_frontend_components
        ),
        "desktop_components_allowed": resolved.research_artifact_registry_boundary_allow_desktop_components,
        "paper_parsing_allowed": resolved.research_artifact_registry_boundary_allow_paper_parsing,
        "pdf_parsing_allowed": resolved.research_artifact_registry_boundary_allow_pdf_parsing,
        "arxiv_ingestion_allowed": resolved.research_artifact_registry_boundary_allow_arxiv_ingestion,
        "llm_analysis_allowed": resolved.research_artifact_registry_boundary_allow_llm_analysis,
        "strategy_generation_allowed": (
            resolved.research_artifact_registry_boundary_allow_strategy_generation
        ),
        "strategy_code_generation_allowed": (
            resolved.research_artifact_registry_boundary_allow_strategy_code_generation
        ),
        "backtesting_allowed": resolved.research_artifact_registry_boundary_allow_backtesting,
        "optimization_allowed": resolved.research_artifact_registry_boundary_allow_optimization,
        "recommendations_allowed": resolved.research_artifact_registry_boundary_allow_recommendations,
        "action_generation_allowed": resolved.research_artifact_registry_boundary_allow_action_generation,
        "confidence_scoring_allowed": (
            resolved.research_artifact_registry_boundary_allow_confidence_scoring
        ),
        "decision_object_generation_allowed": (
            resolved.research_artifact_registry_boundary_allow_decision_object_generation
        ),
        "readiness_to_trade_allowed": (
            resolved.research_artifact_registry_boundary_allow_readiness_to_trade
        ),
        "broker_controls_allowed": resolved.research_artifact_registry_boundary_allow_broker_controls,
        "execution_allowed": (
            resolved.research_artifact_registry_boundary_allow_execution
            or resolved.execution_apis_enabled
        ),
        "approval_allowed": resolved.research_artifact_registry_boundary_allow_approval,
        "override_allowed": resolved.research_artifact_registry_boundary_allow_override,
    }
    error: str | None = None
    if any(bool(value) for value in unsafe_flags.values()):
        error = "research artifact registry boundary unsafe flags must remain false"
    elif not resolved.research_artifact_registry_boundary_schema_version.strip():
        error = "research artifact registry boundary schema version cannot be empty"
    elif resolved.research_artifact_registry_boundary_stage != "boundary_hardening":
        error = "research artifact registry boundary stage must remain boundary_hardening"
    elif not invariant.passed:
        error = "research artifact registry boundary invariants must pass"
    elif not registry.behaviors or not endpoint_policies or not module_policies:
        error = "research artifact registry boundary registries and policies are required"
    return ResearchArtifactBoundaryHealthStatus(
        enabled=resolved.research_artifact_registry_boundary_enabled,
        schema_version=resolved.research_artifact_registry_boundary_schema_version,
        stage=resolved.research_artifact_registry_boundary_stage,
        forbidden_behavior_count=len(registry.behaviors),
        endpoint_policy_count=len(endpoint_policies),
        module_policy_count=len(module_policies),
        invariant_passed=invariant.passed,
        active_ingestion_allowed=resolved.research_artifact_registry_boundary_allow_active_ingestion,
        persistent_storage_allowed=(
            resolved.research_artifact_registry_boundary_allow_persistent_storage
        ),
        file_uploads_allowed=resolved.research_artifact_registry_boundary_allow_file_uploads,
        file_downloads_allowed=resolved.research_artifact_registry_boundary_allow_file_downloads,
        file_previews_allowed=resolved.research_artifact_registry_boundary_allow_file_previews,
        active_ui_allowed=resolved.research_artifact_registry_boundary_allow_active_ui,
        frontend_components_allowed=(
            resolved.research_artifact_registry_boundary_allow_frontend_components
        ),
        desktop_components_allowed=resolved.research_artifact_registry_boundary_allow_desktop_components,
        paper_parsing_allowed=resolved.research_artifact_registry_boundary_allow_paper_parsing,
        pdf_parsing_allowed=resolved.research_artifact_registry_boundary_allow_pdf_parsing,
        arxiv_ingestion_allowed=resolved.research_artifact_registry_boundary_allow_arxiv_ingestion,
        llm_analysis_allowed=resolved.research_artifact_registry_boundary_allow_llm_analysis,
        strategy_generation_allowed=(
            resolved.research_artifact_registry_boundary_allow_strategy_generation
        ),
        strategy_code_generation_allowed=(
            resolved.research_artifact_registry_boundary_allow_strategy_code_generation
        ),
        backtesting_allowed=resolved.research_artifact_registry_boundary_allow_backtesting,
        optimization_allowed=resolved.research_artifact_registry_boundary_allow_optimization,
        recommendations_allowed=resolved.research_artifact_registry_boundary_allow_recommendations,
        action_generation_allowed=resolved.research_artifact_registry_boundary_allow_action_generation,
        confidence_scoring_allowed=(
            resolved.research_artifact_registry_boundary_allow_confidence_scoring
        ),
        decision_object_generation_allowed=(
            resolved.research_artifact_registry_boundary_allow_decision_object_generation
        ),
        readiness_to_trade_allowed=resolved.research_artifact_registry_boundary_allow_readiness_to_trade,
        broker_controls_allowed=resolved.research_artifact_registry_boundary_allow_broker_controls,
        execution_allowed=False,
        approval_allowed=resolved.research_artifact_registry_boundary_allow_approval,
        override_allowed=resolved.research_artifact_registry_boundary_allow_override,
        status="healthy" if error is None else "blocked",
        error=error,
    )
