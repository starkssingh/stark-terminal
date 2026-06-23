from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.decision_display.cards import default_decision_display_card_placeholders
from stark_terminal_core.decision_display.sections import default_decision_display_section_placeholders


class DecisionDisplayHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    stage: str
    recommendations_allowed: bool
    action_generation_allowed: bool
    confidence_scoring_allowed: bool
    decision_object_generation_allowed: bool
    readiness_to_trade_allowed: bool
    execution_allowed: bool = False
    approval_allowed: bool
    override_allowed: bool
    returns_unavailable_by_default: bool
    default_section_count: int
    default_card_count: int
    status: str
    error: str | None = None


def check_decision_display_health(settings: Settings | None = None) -> DecisionDisplayHealthStatus:
    resolved = settings or get_settings()
    cards = default_decision_display_card_placeholders()
    sections = default_decision_display_section_placeholders()
    unsafe_flags = (
        resolved.decision_display_allow_recommendations
        or resolved.decision_display_allow_action_generation
        or resolved.decision_display_allow_confidence_scoring
        or resolved.decision_display_allow_decision_object_generation
        or resolved.decision_display_allow_execution
        or resolved.decision_display_allow_approval
        or resolved.decision_display_allow_override
        or resolved.decision_display_allow_readiness_to_trade
        or resolved.execution_apis_enabled
    )
    has_required_configuration = (
        bool(resolved.decision_display_schema_version.strip())
        and resolved.decision_display_stage == "display_contract_skeleton"
        and resolved.decision_display_return_unavailable_by_default
        and bool(cards)
        and bool(sections)
    )
    status = "healthy" if resolved.decision_display_enabled and not unsafe_flags and has_required_configuration else "blocked"
    error = None if status == "healthy" else "Decision display skeleton flags are not fail-closed"
    return DecisionDisplayHealthStatus(
        enabled=resolved.decision_display_enabled,
        schema_version=resolved.decision_display_schema_version,
        stage=resolved.decision_display_stage,
        recommendations_allowed=resolved.decision_display_allow_recommendations,
        action_generation_allowed=resolved.decision_display_allow_action_generation,
        confidence_scoring_allowed=resolved.decision_display_allow_confidence_scoring,
        decision_object_generation_allowed=resolved.decision_display_allow_decision_object_generation,
        readiness_to_trade_allowed=resolved.decision_display_allow_readiness_to_trade,
        execution_allowed=False,
        approval_allowed=resolved.decision_display_allow_approval,
        override_allowed=resolved.decision_display_allow_override,
        returns_unavailable_by_default=resolved.decision_display_return_unavailable_by_default,
        default_section_count=len(sections),
        default_card_count=len(cards),
        status=status,
        error=error,
    )

