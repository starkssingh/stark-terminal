from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.retail_trader_experience.cards import (
    default_retail_trader_experience_card_placeholders,
)
from stark_terminal_core.retail_trader_experience.interactions import (
    default_retail_trader_experience_forbidden_interactions,
)
from stark_terminal_core.retail_trader_experience.journeys import (
    default_retail_trader_journey_placeholders,
)
from stark_terminal_core.retail_trader_experience.personas import (
    default_retail_trader_persona_placeholders,
)
from stark_terminal_core.retail_trader_experience.sections import (
    default_retail_trader_experience_section_placeholders,
)


class RetailTraderExperienceHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    stage: str
    active_ui_allowed: bool
    frontend_components_allowed: bool
    desktop_components_allowed: bool
    recommendations_allowed: bool
    action_generation_allowed: bool
    confidence_scoring_allowed: bool
    decision_object_generation_allowed: bool
    readiness_to_trade_allowed: bool
    broker_controls_allowed: bool
    execution_allowed: bool = False
    approval_allowed: bool
    override_allowed: bool
    suitability_profiling_allowed: bool
    returns_unavailable_by_default: bool
    default_persona_count: int
    default_journey_count: int
    default_section_count: int
    default_card_count: int
    forbidden_interaction_count: int
    status: str
    error: str | None = None


def check_retail_trader_experience_health(settings: Settings | None = None) -> RetailTraderExperienceHealthStatus:
    resolved_settings = settings or get_settings()
    personas = default_retail_trader_persona_placeholders()
    journeys = default_retail_trader_journey_placeholders()
    sections = default_retail_trader_experience_section_placeholders()
    cards = default_retail_trader_experience_card_placeholders()
    forbidden_interactions = default_retail_trader_experience_forbidden_interactions()
    unsafe_flags: dict[str, Any] = {
        "active_ui_allowed": resolved_settings.retail_trader_experience_allow_active_ui,
        "frontend_components_allowed": resolved_settings.retail_trader_experience_allow_frontend_components,
        "desktop_components_allowed": resolved_settings.retail_trader_experience_allow_desktop_components,
        "recommendations_allowed": resolved_settings.retail_trader_experience_allow_recommendations,
        "action_generation_allowed": resolved_settings.retail_trader_experience_allow_action_generation,
        "confidence_scoring_allowed": resolved_settings.retail_trader_experience_allow_confidence_scoring,
        "decision_object_generation_allowed": (
            resolved_settings.retail_trader_experience_allow_decision_object_generation
        ),
        "readiness_to_trade_allowed": resolved_settings.retail_trader_experience_allow_readiness_to_trade,
        "broker_controls_allowed": resolved_settings.retail_trader_experience_allow_broker_controls,
        "execution_allowed": resolved_settings.retail_trader_experience_allow_execution,
        "approval_allowed": resolved_settings.retail_trader_experience_allow_approval,
        "override_allowed": resolved_settings.retail_trader_experience_allow_override,
    }
    error: str | None = None
    if any(bool(value) for value in unsafe_flags.values()):
        error = "Retail Trader Experience unsafe flags must remain false"
    elif not resolved_settings.retail_trader_experience_schema_version:
        error = "Retail Trader Experience schema version cannot be empty"
    elif not resolved_settings.retail_trader_experience_return_unavailable_by_default:
        error = "Retail Trader Experience must return unavailable by default"
    elif not personas or not journeys or not sections or not cards or not forbidden_interactions:
        error = "Retail Trader Experience default placeholders and forbidden interactions are required"
    return RetailTraderExperienceHealthStatus(
        enabled=resolved_settings.retail_trader_experience_enabled,
        schema_version=resolved_settings.retail_trader_experience_schema_version,
        stage=resolved_settings.retail_trader_experience_stage,
        active_ui_allowed=resolved_settings.retail_trader_experience_allow_active_ui,
        frontend_components_allowed=resolved_settings.retail_trader_experience_allow_frontend_components,
        desktop_components_allowed=resolved_settings.retail_trader_experience_allow_desktop_components,
        recommendations_allowed=resolved_settings.retail_trader_experience_allow_recommendations,
        action_generation_allowed=resolved_settings.retail_trader_experience_allow_action_generation,
        confidence_scoring_allowed=resolved_settings.retail_trader_experience_allow_confidence_scoring,
        decision_object_generation_allowed=(
            resolved_settings.retail_trader_experience_allow_decision_object_generation
        ),
        readiness_to_trade_allowed=resolved_settings.retail_trader_experience_allow_readiness_to_trade,
        broker_controls_allowed=resolved_settings.retail_trader_experience_allow_broker_controls,
        execution_allowed=False,
        approval_allowed=resolved_settings.retail_trader_experience_allow_approval,
        override_allowed=resolved_settings.retail_trader_experience_allow_override,
        suitability_profiling_allowed=False,
        returns_unavailable_by_default=resolved_settings.retail_trader_experience_return_unavailable_by_default,
        default_persona_count=len(personas),
        default_journey_count=len(journeys),
        default_section_count=len(sections),
        default_card_count=len(cards),
        forbidden_interaction_count=len(forbidden_interactions),
        status="healthy" if error is None else "blocked",
        error=error,
    )
