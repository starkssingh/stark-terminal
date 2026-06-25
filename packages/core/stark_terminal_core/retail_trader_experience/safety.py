from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience.cards import RetailTraderExperienceCardPlaceholder
from stark_terminal_core.retail_trader_experience.journeys import RetailTraderJourneyPlaceholder
from stark_terminal_core.retail_trader_experience.personas import RetailTraderPersonaPlaceholder
from stark_terminal_core.retail_trader_experience.planning import (
    RetailTraderExperiencePlanningContract,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_trader_experience_notes,
)


class RetailTraderExperienceSafetyPolicy(BaseModel):
    policy_id: str
    name: str
    allow_active_ui: bool = False
    allow_frontend_components: bool = False
    allow_desktop_components: bool = False
    allow_recommendations: bool = False
    allow_action_generation: bool = False
    allow_confidence_scoring: bool = False
    allow_decision_object_generation: bool = False
    allow_readiness_to_trade: bool = False
    allow_broker_controls: bool = False
    allow_execution: bool = False
    allow_approval: bool = False
    allow_override: bool = False
    allow_suitability_profiling: bool = False
    require_planning_only: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience safety policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_notes(value)

    @model_validator(mode="after")
    def policy_must_fail_closed(self) -> RetailTraderExperienceSafetyPolicy:
        if self.allow_active_ui:
            raise ValueError("Retail Trader Experience active UI is forbidden in Prompt 56")
        if self.allow_frontend_components:
            raise ValueError("Retail Trader Experience frontend components are forbidden in Prompt 56")
        if self.allow_desktop_components:
            raise ValueError("Retail Trader Experience desktop components are forbidden in Prompt 56")
        if self.allow_recommendations:
            raise ValueError("Retail Trader Experience recommendations are forbidden in Prompt 56")
        if self.allow_action_generation:
            raise ValueError("Retail Trader Experience action generation is forbidden in Prompt 56")
        if self.allow_confidence_scoring:
            raise ValueError("Retail Trader Experience confidence scoring is forbidden in Prompt 56")
        if self.allow_decision_object_generation:
            raise ValueError("Retail Trader Experience DecisionObject generation is forbidden in Prompt 56")
        if self.allow_readiness_to_trade:
            raise ValueError("Retail Trader Experience readiness-to-trade is forbidden in Prompt 56")
        if self.allow_broker_controls:
            raise ValueError("Retail Trader Experience broker controls are forbidden in Prompt 56")
        if self.allow_execution:
            raise ValueError("Retail Trader Experience execution is forbidden in Prompt 56")
        if self.allow_approval:
            raise ValueError("Retail Trader Experience approvals are forbidden in Prompt 56")
        if self.allow_override:
            raise ValueError("Retail Trader Experience overrides are forbidden in Prompt 56")
        if self.allow_suitability_profiling:
            raise ValueError("Retail Trader Experience suitability profiling is forbidden in Prompt 56")
        if not self.require_planning_only:
            raise ValueError("Retail Trader Experience must remain planning-only in Prompt 56")
        return self


class RetailTraderExperienceSafetyResult(BaseModel):
    result_id: str
    policy_id: str
    safe: bool
    reasons: list[str]
    planning_only: bool = True
    active_ui_allowed: bool = False
    recommendations_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    suitability_profiling_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "policy_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience safety result text fields")

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_retail_trader_experience_notes(value)
        if not sanitized:
            raise ValueError("retail trader experience safety reasons cannot be empty")
        return sanitized

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def result_must_fail_closed(self) -> RetailTraderExperienceSafetyResult:
        if not self.planning_only:
            raise ValueError("retail trader experience safety result must remain planning-only")
        if self.active_ui_allowed:
            raise ValueError("retail trader experience safety result cannot allow active UI")
        if self.recommendations_allowed:
            raise ValueError("retail trader experience safety result cannot allow recommendations")
        if self.broker_controls_allowed:
            raise ValueError("retail trader experience safety result cannot allow broker controls")
        if self.execution_allowed:
            raise ValueError("retail trader experience safety result cannot allow execution")
        if self.suitability_profiling_allowed:
            raise ValueError("retail trader experience safety result cannot allow suitability profiling")
        return self


def default_retail_trader_experience_safety_policy(
    settings: Any | None = None,
) -> RetailTraderExperienceSafetyPolicy:
    notes = ["Prompt 56 permits Retail Trader Experience planning and guardrails only."]
    if settings is not None:
        notes.append(f"stage={settings.retail_trader_experience_stage}")
    return RetailTraderExperienceSafetyPolicy(
        policy_id="retail-trader-experience-safety-policy-v1",
        name="Retail Trader Experience Safety Policy",
        notes=notes,
    )


def _safety_result(
    result_id: str,
    policy_id: str,
    reasons: list[str],
    safe: bool,
) -> RetailTraderExperienceSafetyResult:
    return RetailTraderExperienceSafetyResult(
        result_id=result_id,
        policy_id=policy_id,
        safe=safe,
        reasons=reasons,
    )


def evaluate_retail_trader_experience_plan_safety(
    plan: RetailTraderExperiencePlanningContract,
    policy: RetailTraderExperienceSafetyPolicy,
) -> RetailTraderExperienceSafetyResult:
    reasons: list[str] = []
    if plan.active_ui_allowed or policy.allow_active_ui:
        reasons.append("Retail Trader Experience plan cannot allow active UI")
    if plan.frontend_components_allowed or policy.allow_frontend_components:
        reasons.append("Retail Trader Experience plan cannot allow frontend components")
    if plan.desktop_components_allowed or policy.allow_desktop_components:
        reasons.append("Retail Trader Experience plan cannot allow desktop components")
    if plan.recommendations_allowed or policy.allow_recommendations:
        reasons.append("Retail Trader Experience plan cannot allow recommendations")
    if plan.action_generation_allowed or policy.allow_action_generation:
        reasons.append("Retail Trader Experience plan cannot allow action generation")
    if plan.confidence_scoring_allowed or policy.allow_confidence_scoring:
        reasons.append("Retail Trader Experience plan cannot allow confidence scoring")
    if plan.decision_object_generation_allowed or policy.allow_decision_object_generation:
        reasons.append("Retail Trader Experience plan cannot allow DecisionObject generation")
    if plan.readiness_to_trade_allowed or policy.allow_readiness_to_trade:
        reasons.append("Retail Trader Experience plan cannot allow readiness-to-trade")
    if plan.broker_controls_allowed or policy.allow_broker_controls:
        reasons.append("Retail Trader Experience plan cannot allow broker controls")
    if plan.execution_allowed or policy.allow_execution:
        reasons.append("Retail Trader Experience plan cannot allow execution")
    if plan.approval_allowed or policy.allow_approval:
        reasons.append("Retail Trader Experience plan cannot allow approvals")
    if plan.override_allowed or policy.allow_override:
        reasons.append("Retail Trader Experience plan cannot allow overrides")
    if plan.suitability_profiling_allowed or policy.allow_suitability_profiling:
        reasons.append("Retail Trader Experience plan cannot allow suitability profiling")
    if not plan.returns_unavailable_by_default:
        reasons.append("Retail Trader Experience plan must return unavailable by default")
    if reasons:
        return _safety_result("retail-trader-experience-plan-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "retail-trader-experience-plan-safety-safe",
        policy.policy_id,
        ["Retail Trader Experience plan remains planning-only with no active UI, suitability profiling, recommendations, broker controls, or execution"],
        True,
    )


def evaluate_retail_trader_experience_personas_safety(
    personas: Iterable[RetailTraderPersonaPlaceholder],
    policy: RetailTraderExperienceSafetyPolicy,
) -> RetailTraderExperienceSafetyResult:
    reasons: list[str] = []
    persona_list = list(personas)
    if not persona_list:
        reasons.append("Retail Trader Experience persona placeholders are required")
    for persona in persona_list:
        if not persona.planning_only:
            reasons.append(f"{persona.persona_id} must remain planning-only")
        if persona.active_profile or policy.allow_active_ui:
            reasons.append(f"{persona.persona_id} cannot be an active profile")
        if persona.suitability_profile or policy.allow_suitability_profiling:
            reasons.append(f"{persona.persona_id} cannot be suitability profiling")
        if persona.trading_permission_profile:
            reasons.append(f"{persona.persona_id} cannot be a trading permission profile")
        if persona.recommendations_allowed or policy.allow_recommendations:
            reasons.append(f"{persona.persona_id} cannot allow recommendations")
        if persona.action_generation_allowed or policy.allow_action_generation:
            reasons.append(f"{persona.persona_id} cannot allow action generation")
        if persona.confidence_scoring_allowed or policy.allow_confidence_scoring:
            reasons.append(f"{persona.persona_id} cannot allow confidence scoring")
        if persona.decision_object_generation_allowed or policy.allow_decision_object_generation:
            reasons.append(f"{persona.persona_id} cannot allow DecisionObject generation")
        if persona.readiness_to_trade_allowed or policy.allow_readiness_to_trade:
            reasons.append(f"{persona.persona_id} cannot allow readiness-to-trade")
        if persona.broker_controls_allowed or policy.allow_broker_controls:
            reasons.append(f"{persona.persona_id} cannot allow broker controls")
        if persona.execution_allowed or policy.allow_execution:
            reasons.append(f"{persona.persona_id} cannot allow execution")
    if reasons:
        return _safety_result("retail-trader-experience-persona-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "retail-trader-experience-persona-safety-safe",
        policy.policy_id,
        ["Retail Trader Experience personas remain planning placeholders with no suitability profiling"],
        True,
    )


def evaluate_retail_trader_experience_journeys_safety(
    journeys: Iterable[RetailTraderJourneyPlaceholder],
    policy: RetailTraderExperienceSafetyPolicy,
) -> RetailTraderExperienceSafetyResult:
    reasons: list[str] = []
    journey_list = list(journeys)
    if not journey_list:
        reasons.append("Retail Trader Experience journey placeholders are required")
    for journey in journey_list:
        if journey.active_ui or policy.allow_active_ui:
            reasons.append(f"{journey.journey_id} cannot be active UI")
        if not journey.unavailable or not journey.planning_only:
            reasons.append(f"{journey.journey_id} must remain unavailable and planning-only")
        if journey.recommendation_journey or policy.allow_recommendations:
            reasons.append(f"{journey.journey_id} cannot be a recommendation journey")
        if journey.trading_advice_journey:
            reasons.append(f"{journey.journey_id} cannot be a trading advice journey")
        if journey.broker_control_journey or policy.allow_broker_controls:
            reasons.append(f"{journey.journey_id} cannot be a broker control journey")
        if journey.execution_journey or policy.allow_execution:
            reasons.append(f"{journey.journey_id} cannot be an execution journey")
        if journey.readiness_to_trade_journey or policy.allow_readiness_to_trade:
            reasons.append(f"{journey.journey_id} cannot be readiness-to-trade")
        if journey.approval_journey or policy.allow_approval:
            reasons.append(f"{journey.journey_id} cannot be an approval journey")
        if journey.override_journey or policy.allow_override:
            reasons.append(f"{journey.journey_id} cannot be an override journey")
    if reasons:
        return _safety_result("retail-trader-experience-journey-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "retail-trader-experience-journey-safety-safe",
        policy.policy_id,
        ["Retail Trader Experience journeys remain unavailable planning placeholders"],
        True,
    )


def evaluate_retail_trader_experience_cards_safety(
    cards: Iterable[RetailTraderExperienceCardPlaceholder],
    policy: RetailTraderExperienceSafetyPolicy,
) -> RetailTraderExperienceSafetyResult:
    reasons: list[str] = []
    card_list = list(cards)
    if not card_list:
        reasons.append("Retail Trader Experience card placeholders are required")
    for card in card_list:
        if card.active_ui or policy.allow_active_ui:
            reasons.append(f"{card.card_id} cannot be active UI")
        if not card.unavailable or not card.planning_only:
            reasons.append(f"{card.card_id} must remain unavailable and planning-only")
        if card.recommendation_card or policy.allow_recommendations:
            reasons.append(f"{card.card_id} cannot be a recommendation card")
        if card.action_card or policy.allow_action_generation:
            reasons.append(f"{card.card_id} cannot be an action card")
        if card.confidence_display or policy.allow_confidence_scoring:
            reasons.append(f"{card.card_id} cannot display confidence")
        if card.decision_object_display or policy.allow_decision_object_generation:
            reasons.append(f"{card.card_id} cannot display DecisionObjects")
        if card.readiness_to_trade_display or policy.allow_readiness_to_trade:
            reasons.append(f"{card.card_id} cannot display readiness-to-trade")
        if card.broker_control or policy.allow_broker_controls:
            reasons.append(f"{card.card_id} cannot include broker controls")
        if card.execution_control or policy.allow_execution:
            reasons.append(f"{card.card_id} cannot include execution controls")
        if card.approval_control or policy.allow_approval:
            reasons.append(f"{card.card_id} cannot include approval controls")
        if card.override_control or policy.allow_override:
            reasons.append(f"{card.card_id} cannot include override controls")
        if card.suitability_profile_display or policy.allow_suitability_profiling:
            reasons.append(f"{card.card_id} cannot display suitability profiles")
    if reasons:
        return _safety_result("retail-trader-experience-card-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "retail-trader-experience-card-safety-safe",
        policy.policy_id,
        ["Retail Trader Experience cards remain unavailable planning placeholders"],
        True,
    )


def reject_experience_as_active_ui(
    reason: str = "Retail Trader Experience placeholders cannot be treated as active UI in Prompt 56",
) -> RetailTraderExperienceSafetyResult:
    return _safety_result("retail-trader-experience-reject-active-ui", "retail-trader-experience-safety-policy-v1", [reason], False)


def reject_experience_as_recommendation(
    reason: str = "Retail Trader Experience placeholders cannot be treated as recommendations in Prompt 56",
) -> RetailTraderExperienceSafetyResult:
    return _safety_result("retail-trader-experience-reject-recommendation", "retail-trader-experience-safety-policy-v1", [reason], False)


def reject_experience_as_execution_surface(
    reason: str = "Retail Trader Experience placeholders cannot be treated as execution surfaces in Prompt 56",
) -> RetailTraderExperienceSafetyResult:
    return _safety_result("retail-trader-experience-reject-execution", "retail-trader-experience-safety-policy-v1", [reason], False)


def reject_experience_as_suitability_profile(
    reason: str = "Retail Trader Experience placeholders cannot be treated as suitability profiles in Prompt 56",
) -> RetailTraderExperienceSafetyResult:
    return _safety_result("retail-trader-experience-reject-suitability", "retail-trader-experience-safety-policy-v1", [reason], False)
