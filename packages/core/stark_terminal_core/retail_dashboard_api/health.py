from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings


class RetailDashboardAPIHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    stage: str
    active_ui_allowed: bool
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
    status: str
    error: str | None = None


def check_retail_dashboard_api_health(settings: Settings | None = None) -> RetailDashboardAPIHealthStatus:
    resolved = settings or get_settings()
    unsafe_flags = (
        resolved.retail_dashboard_api_allow_active_ui
        or resolved.retail_dashboard_api_allow_recommendations
        or resolved.retail_dashboard_api_allow_action_generation
        or resolved.retail_dashboard_api_allow_confidence_scoring
        or resolved.retail_dashboard_api_allow_decision_object_generation
        or resolved.retail_dashboard_api_allow_readiness_to_trade
        or resolved.retail_dashboard_api_allow_broker_controls
        or resolved.retail_dashboard_api_allow_execution
        or resolved.retail_dashboard_api_allow_approval
        or resolved.retail_dashboard_api_allow_override
        or resolved.execution_apis_enabled
    )
    has_required_configuration = (
        bool(resolved.retail_dashboard_api_schema_version.strip())
        and resolved.retail_dashboard_api_stage == "api_contract_skeleton"
        and resolved.retail_dashboard_api_return_unavailable_by_default
    )
    status = (
        "healthy"
        if resolved.retail_dashboard_api_enabled and not unsafe_flags and has_required_configuration
        else "blocked"
    )
    error = None if status == "healthy" else "Retail Dashboard API skeleton flags are not fail-closed"
    return RetailDashboardAPIHealthStatus(
        enabled=resolved.retail_dashboard_api_enabled,
        schema_version=resolved.retail_dashboard_api_schema_version,
        stage=resolved.retail_dashboard_api_stage,
        active_ui_allowed=resolved.retail_dashboard_api_allow_active_ui,
        recommendations_allowed=resolved.retail_dashboard_api_allow_recommendations,
        action_generation_allowed=resolved.retail_dashboard_api_allow_action_generation,
        confidence_scoring_allowed=resolved.retail_dashboard_api_allow_confidence_scoring,
        decision_object_generation_allowed=resolved.retail_dashboard_api_allow_decision_object_generation,
        readiness_to_trade_allowed=resolved.retail_dashboard_api_allow_readiness_to_trade,
        broker_controls_allowed=resolved.retail_dashboard_api_allow_broker_controls,
        execution_allowed=False,
        approval_allowed=resolved.retail_dashboard_api_allow_approval,
        override_allowed=resolved.retail_dashboard_api_allow_override,
        returns_unavailable_by_default=resolved.retail_dashboard_api_return_unavailable_by_default,
        status=status,
        error=error,
    )
