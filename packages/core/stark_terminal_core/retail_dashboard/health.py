from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.retail_dashboard.cards import default_retail_dashboard_card_placeholders
from stark_terminal_core.retail_dashboard.interactions import default_retail_dashboard_forbidden_interactions
from stark_terminal_core.retail_dashboard.sections import default_retail_dashboard_section_placeholders


class RetailDashboardHealthStatus(BaseModel):
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
    default_section_count: int
    default_card_count: int
    forbidden_interaction_count: int
    status: str
    error: str | None = None


def check_retail_dashboard_health(settings: Settings | None = None) -> RetailDashboardHealthStatus:
    resolved_settings = settings or get_settings()
    sections = default_retail_dashboard_section_placeholders()
    cards = default_retail_dashboard_card_placeholders()
    forbidden_interactions = default_retail_dashboard_forbidden_interactions()
    unsafe_flags: dict[str, Any] = {
        "active_ui_allowed": resolved_settings.retail_dashboard_allow_active_ui,
        "recommendations_allowed": resolved_settings.retail_dashboard_allow_recommendations,
        "action_generation_allowed": resolved_settings.retail_dashboard_allow_action_generation,
        "confidence_scoring_allowed": resolved_settings.retail_dashboard_allow_confidence_scoring,
        "decision_object_generation_allowed": resolved_settings.retail_dashboard_allow_decision_object_generation,
        "readiness_to_trade_allowed": resolved_settings.retail_dashboard_allow_readiness_to_trade,
        "broker_controls_allowed": resolved_settings.retail_dashboard_allow_broker_controls,
        "execution_allowed": resolved_settings.retail_dashboard_allow_execution,
        "approval_allowed": resolved_settings.retail_dashboard_allow_approval,
        "override_allowed": resolved_settings.retail_dashboard_allow_override,
    }
    error: str | None = None
    if any(bool(value) for value in unsafe_flags.values()):
        error = "Retail Dashboard unsafe flags must remain false"
    elif not resolved_settings.retail_dashboard_schema_version:
        error = "Retail Dashboard schema version cannot be empty"
    elif not resolved_settings.retail_dashboard_return_unavailable_by_default:
        error = "Retail Dashboard must return unavailable by default"
    elif not sections or not cards or not forbidden_interactions:
        error = "Retail Dashboard default placeholders and forbidden interactions are required"
    return RetailDashboardHealthStatus(
        enabled=resolved_settings.retail_dashboard_enabled,
        schema_version=resolved_settings.retail_dashboard_schema_version,
        stage=resolved_settings.retail_dashboard_stage,
        active_ui_allowed=resolved_settings.retail_dashboard_allow_active_ui,
        recommendations_allowed=resolved_settings.retail_dashboard_allow_recommendations,
        action_generation_allowed=resolved_settings.retail_dashboard_allow_action_generation,
        confidence_scoring_allowed=resolved_settings.retail_dashboard_allow_confidence_scoring,
        decision_object_generation_allowed=resolved_settings.retail_dashboard_allow_decision_object_generation,
        readiness_to_trade_allowed=resolved_settings.retail_dashboard_allow_readiness_to_trade,
        broker_controls_allowed=resolved_settings.retail_dashboard_allow_broker_controls,
        execution_allowed=False,
        approval_allowed=resolved_settings.retail_dashboard_allow_approval,
        override_allowed=resolved_settings.retail_dashboard_allow_override,
        returns_unavailable_by_default=resolved_settings.retail_dashboard_return_unavailable_by_default,
        default_section_count=len(sections),
        default_card_count=len(cards),
        forbidden_interaction_count=len(forbidden_interactions),
        status="healthy" if error is None else "blocked",
        error=error,
    )
