from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.retail_decision_console.cards import (
    default_retail_decision_console_card_placeholders,
)
from stark_terminal_core.retail_decision_console.sections import (
    default_retail_decision_console_section_placeholders,
)


class RetailDecisionConsoleHealthStatus(BaseModel):
    service: str
    enabled: bool
    stage: str
    schema_version: str
    planning_only: bool
    productization_plan_only: bool
    read_only: bool
    unavailable_by_default: bool
    section_placeholder_count: int
    card_placeholder_count: int
    live_decisions_enabled: bool
    recommendations_enabled: bool
    action_generation_enabled: bool
    confidence_scoring_enabled: bool
    decision_object_generation_enabled: bool
    live_market_data_enabled: bool
    broker_controls_enabled: bool
    order_buttons_enabled: bool
    execution_enabled: bool
    status: str


def retail_decision_console_health(settings: object | None = None) -> RetailDecisionConsoleHealthStatus:
    enabled = getattr(settings, "retail_decision_console_enabled", True)
    schema_version = getattr(settings, "retail_decision_console_schema_version", "v1")
    stage = getattr(settings, "retail_decision_console_stage", "productization_plan")
    dangerous_flags = {
        "live_decisions_enabled": getattr(settings, "retail_decision_console_allow_live_decisions", False),
        "recommendations_enabled": getattr(settings, "retail_decision_console_allow_recommendations", False),
        "action_generation_enabled": getattr(settings, "retail_decision_console_allow_action_generation", False),
        "confidence_scoring_enabled": getattr(settings, "retail_decision_console_allow_confidence_scoring", False),
        "decision_object_generation_enabled": getattr(
            settings,
            "retail_decision_console_allow_decision_object_generation",
            False,
        ),
        "live_market_data_enabled": getattr(settings, "retail_decision_console_allow_live_market_data", False),
        "broker_controls_enabled": getattr(settings, "retail_decision_console_allow_broker_controls", False),
        "order_buttons_enabled": getattr(settings, "retail_decision_console_allow_order_buttons", False),
        "execution_enabled": getattr(settings, "retail_decision_console_allow_execution", False),
    }
    healthy = enabled and stage == "productization_plan" and not any(dangerous_flags.values())
    return RetailDecisionConsoleHealthStatus(
        service="stark-terminal-retail-decision-console",
        enabled=enabled,
        stage=stage,
        schema_version=schema_version,
        planning_only=True,
        productization_plan_only=True,
        read_only=True,
        unavailable_by_default=True,
        section_placeholder_count=len(default_retail_decision_console_section_placeholders()),
        card_placeholder_count=len(default_retail_decision_console_card_placeholders()),
        **dangerous_flags,
        status="healthy" if healthy else "blocked",
    )
