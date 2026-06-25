from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.retail_trader_experience_display.badges import (
    default_retail_trader_experience_display_badges,
)
from stark_terminal_core.retail_trader_experience_display.journeys import (
    default_retail_trader_experience_display_journey_placeholders,
)
from stark_terminal_core.retail_trader_experience_display.personas import (
    default_retail_trader_experience_display_persona_placeholders,
)
from stark_terminal_core.retail_trader_experience_display.sections import (
    default_retail_trader_experience_display_section_placeholders,
)
from stark_terminal_core.retail_trader_experience_display.widgets import (
    default_retail_trader_experience_display_widget_placeholders,
)


class RetailTraderExperienceDisplayHealthStatus(BaseModel):
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
    persona_count: int
    journey_count: int
    section_count: int
    widget_count: int
    badge_count: int
    status: str
    error: str | None = None


def check_retail_trader_experience_display_health(
    settings: Settings | None = None,
) -> RetailTraderExperienceDisplayHealthStatus:
    resolved = settings or get_settings()
    persona_count = len(default_retail_trader_experience_display_persona_placeholders())
    journey_count = len(default_retail_trader_experience_display_journey_placeholders())
    section_count = len(default_retail_trader_experience_display_section_placeholders())
    widget_count = len(default_retail_trader_experience_display_widget_placeholders())
    badge_count = len(default_retail_trader_experience_display_badges())

    unsafe_flags = (
        resolved.retail_trader_experience_display_allow_active_ui
        or resolved.retail_trader_experience_display_allow_frontend_components
        or resolved.retail_trader_experience_display_allow_desktop_components
        or resolved.retail_trader_experience_display_allow_recommendations
        or resolved.retail_trader_experience_display_allow_action_generation
        or resolved.retail_trader_experience_display_allow_confidence_scoring
        or resolved.retail_trader_experience_display_allow_decision_object_generation
        or resolved.retail_trader_experience_display_allow_readiness_to_trade
        or resolved.retail_trader_experience_display_allow_broker_controls
        or resolved.retail_trader_experience_display_allow_execution
        or resolved.retail_trader_experience_display_allow_approval
        or resolved.retail_trader_experience_display_allow_override
        or resolved.retail_trader_experience_display_allow_suitability_profiling
        or resolved.execution_apis_enabled
    )
    has_required_configuration = (
        bool(resolved.retail_trader_experience_display_schema_version.strip())
        and resolved.retail_trader_experience_display_stage == "display_contract_skeleton"
        and resolved.retail_trader_experience_display_return_unavailable_by_default
        and persona_count > 0
        and journey_count > 0
        and section_count > 0
        and widget_count > 0
        and badge_count > 0
    )
    status = (
        "healthy"
        if resolved.retail_trader_experience_display_enabled and not unsafe_flags and has_required_configuration
        else "blocked"
    )
    error = None if status == "healthy" else "Retail Trader Experience Display skeleton flags are not fail-closed"
    return RetailTraderExperienceDisplayHealthStatus(
        enabled=resolved.retail_trader_experience_display_enabled,
        schema_version=resolved.retail_trader_experience_display_schema_version,
        stage=resolved.retail_trader_experience_display_stage,
        active_ui_allowed=resolved.retail_trader_experience_display_allow_active_ui,
        frontend_components_allowed=resolved.retail_trader_experience_display_allow_frontend_components,
        desktop_components_allowed=resolved.retail_trader_experience_display_allow_desktop_components,
        recommendations_allowed=resolved.retail_trader_experience_display_allow_recommendations,
        action_generation_allowed=resolved.retail_trader_experience_display_allow_action_generation,
        confidence_scoring_allowed=resolved.retail_trader_experience_display_allow_confidence_scoring,
        decision_object_generation_allowed=(
            resolved.retail_trader_experience_display_allow_decision_object_generation
        ),
        readiness_to_trade_allowed=resolved.retail_trader_experience_display_allow_readiness_to_trade,
        broker_controls_allowed=resolved.retail_trader_experience_display_allow_broker_controls,
        execution_allowed=False,
        approval_allowed=resolved.retail_trader_experience_display_allow_approval,
        override_allowed=resolved.retail_trader_experience_display_allow_override,
        suitability_profiling_allowed=(
            resolved.retail_trader_experience_display_allow_suitability_profiling
        ),
        returns_unavailable_by_default=(
            resolved.retail_trader_experience_display_return_unavailable_by_default
        ),
        persona_count=persona_count,
        journey_count=journey_count,
        section_count=section_count,
        widget_count=widget_count,
        badge_count=badge_count,
        status=status,
        error=error,
    )
