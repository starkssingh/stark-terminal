from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard.cards import RetailDashboardCardPlaceholder
from stark_terminal_core.retail_dashboard.planning import (
    RetailDashboardPlanningContract,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_dashboard_notes,
)
from stark_terminal_core.retail_dashboard.sections import RetailDashboardSectionPlaceholder


class RetailDashboardSafetyPolicy(BaseModel):
    policy_id: str
    name: str
    allow_active_ui: bool = False
    allow_recommendations: bool = False
    allow_action_generation: bool = False
    allow_confidence_scoring: bool = False
    allow_decision_object_generation: bool = False
    allow_readiness_to_trade: bool = False
    allow_broker_controls: bool = False
    allow_execution: bool = False
    allow_approval: bool = False
    allow_override: bool = False
    require_planning_only: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard safety policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_dashboard_notes(value)

    @model_validator(mode="after")
    def policy_must_fail_closed(self) -> RetailDashboardSafetyPolicy:
        if self.allow_active_ui:
            raise ValueError("Retail Dashboard active UI is forbidden in Prompt 49")
        if self.allow_recommendations:
            raise ValueError("Retail Dashboard recommendations are forbidden in Prompt 49")
        if self.allow_action_generation:
            raise ValueError("Retail Dashboard action generation is forbidden in Prompt 49")
        if self.allow_confidence_scoring:
            raise ValueError("Retail Dashboard confidence scoring is forbidden in Prompt 49")
        if self.allow_decision_object_generation:
            raise ValueError("Retail Dashboard DecisionObject generation is forbidden in Prompt 49")
        if self.allow_readiness_to_trade:
            raise ValueError("Retail Dashboard readiness-to-trade is forbidden in Prompt 49")
        if self.allow_broker_controls:
            raise ValueError("Retail Dashboard broker controls are forbidden in Prompt 49")
        if self.allow_execution:
            raise ValueError("Retail Dashboard execution is forbidden in Prompt 49")
        if self.allow_approval:
            raise ValueError("Retail Dashboard approvals are forbidden in Prompt 49")
        if self.allow_override:
            raise ValueError("Retail Dashboard overrides are forbidden in Prompt 49")
        if not self.require_planning_only:
            raise ValueError("Retail Dashboard must remain planning-only in Prompt 49")
        return self


class RetailDashboardSafetyResult(BaseModel):
    result_id: str
    policy_id: str
    safe: bool
    reasons: list[str]
    planning_only: bool = True
    active_ui_allowed: bool = False
    recommendations_allowed: bool = False
    execution_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "policy_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard safety result text fields")

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_retail_dashboard_notes(value)
        if not sanitized:
            raise ValueError("retail dashboard safety reasons cannot be empty")
        return sanitized

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def result_must_fail_closed(self) -> RetailDashboardSafetyResult:
        if not self.planning_only:
            raise ValueError("retail dashboard safety result must remain planning-only")
        if self.active_ui_allowed:
            raise ValueError("retail dashboard safety result cannot allow active UI")
        if self.recommendations_allowed:
            raise ValueError("retail dashboard safety result cannot allow recommendations")
        if self.execution_allowed:
            raise ValueError("retail dashboard safety result cannot allow execution")
        return self


def default_retail_dashboard_safety_policy(settings: Any | None = None) -> RetailDashboardSafetyPolicy:
    notes = ["Prompt 49 permits Retail Dashboard planning and guardrails only."]
    if settings is not None:
        notes.append(f"stage={settings.retail_dashboard_stage}")
    return RetailDashboardSafetyPolicy(
        policy_id="retail-dashboard-safety-policy-v1",
        name="Retail Dashboard Safety Policy",
        notes=notes,
    )


def _safety_result(result_id: str, policy_id: str, reasons: list[str], safe: bool) -> RetailDashboardSafetyResult:
    return RetailDashboardSafetyResult(
        result_id=result_id,
        policy_id=policy_id,
        safe=safe,
        reasons=reasons,
    )


def evaluate_retail_dashboard_plan_safety(
    plan: RetailDashboardPlanningContract,
    policy: RetailDashboardSafetyPolicy,
) -> RetailDashboardSafetyResult:
    reasons: list[str] = []
    if plan.active_ui_allowed or policy.allow_active_ui:
        reasons.append("Retail Dashboard plan cannot allow active UI")
    if plan.recommendations_allowed or policy.allow_recommendations:
        reasons.append("Retail Dashboard plan cannot allow recommendations")
    if plan.action_generation_allowed or policy.allow_action_generation:
        reasons.append("Retail Dashboard plan cannot allow action generation")
    if plan.confidence_scoring_allowed or policy.allow_confidence_scoring:
        reasons.append("Retail Dashboard plan cannot allow confidence scoring")
    if plan.decision_object_generation_allowed or policy.allow_decision_object_generation:
        reasons.append("Retail Dashboard plan cannot allow DecisionObject generation")
    if plan.readiness_to_trade_allowed or policy.allow_readiness_to_trade:
        reasons.append("Retail Dashboard plan cannot allow readiness-to-trade")
    if plan.broker_controls_allowed or policy.allow_broker_controls:
        reasons.append("Retail Dashboard plan cannot allow broker controls")
    if plan.execution_allowed or policy.allow_execution:
        reasons.append("Retail Dashboard plan cannot allow execution")
    if plan.approval_allowed or policy.allow_approval:
        reasons.append("Retail Dashboard plan cannot allow approvals")
    if plan.override_allowed or policy.allow_override:
        reasons.append("Retail Dashboard plan cannot allow overrides")
    if not plan.returns_unavailable_by_default:
        reasons.append("Retail Dashboard plan must return unavailable by default")
    if reasons:
        return _safety_result("retail-dashboard-plan-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "retail-dashboard-plan-safety-safe",
        policy.policy_id,
        ["Retail Dashboard plan remains planning-only with no active UI, recommendations, broker controls, or execution"],
        True,
    )


def evaluate_retail_dashboard_sections_safety(
    sections: Iterable[RetailDashboardSectionPlaceholder],
    policy: RetailDashboardSafetyPolicy,
) -> RetailDashboardSafetyResult:
    reasons: list[str] = []
    section_list = list(sections)
    if not section_list:
        reasons.append("Retail Dashboard section placeholders are required")
    for section in section_list:
        if section.active_ui or policy.allow_active_ui:
            reasons.append(f"{section.section_id} cannot be active UI")
        if not section.unavailable or not section.planning_only:
            reasons.append(f"{section.section_id} must remain unavailable and planning-only")
        if section.recommendations_allowed or policy.allow_recommendations:
            reasons.append(f"{section.section_id} cannot allow recommendations")
        if section.action_generation_allowed or policy.allow_action_generation:
            reasons.append(f"{section.section_id} cannot allow action generation")
        if section.confidence_scoring_allowed or policy.allow_confidence_scoring:
            reasons.append(f"{section.section_id} cannot allow confidence scoring")
        if section.decision_object_generation_allowed or policy.allow_decision_object_generation:
            reasons.append(f"{section.section_id} cannot allow DecisionObject generation")
        if section.readiness_to_trade_allowed or policy.allow_readiness_to_trade:
            reasons.append(f"{section.section_id} cannot allow readiness-to-trade")
        if section.broker_controls_allowed or policy.allow_broker_controls:
            reasons.append(f"{section.section_id} cannot allow broker controls")
        if section.execution_allowed or policy.allow_execution:
            reasons.append(f"{section.section_id} cannot allow execution")
    if reasons:
        return _safety_result("retail-dashboard-section-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "retail-dashboard-section-safety-safe",
        policy.policy_id,
        ["Retail Dashboard sections remain unavailable planning placeholders"],
        True,
    )


def evaluate_retail_dashboard_cards_safety(
    cards: Iterable[RetailDashboardCardPlaceholder],
    policy: RetailDashboardSafetyPolicy,
) -> RetailDashboardSafetyResult:
    reasons: list[str] = []
    card_list = list(cards)
    if not card_list:
        reasons.append("Retail Dashboard card placeholders are required")
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
    if reasons:
        return _safety_result("retail-dashboard-card-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "retail-dashboard-card-safety-safe",
        policy.policy_id,
        ["Retail Dashboard cards remain unavailable planning placeholders"],
        True,
    )


def reject_dashboard_as_recommendation(
    reason: str = "Retail Dashboard placeholders cannot be treated as recommendations in Prompt 49",
) -> RetailDashboardSafetyResult:
    return _safety_result("retail-dashboard-reject-recommendation", "retail-dashboard-safety-policy-v1", [reason], False)


def reject_dashboard_as_execution_surface(
    reason: str = "Retail Dashboard placeholders cannot be treated as execution surfaces in Prompt 49",
) -> RetailDashboardSafetyResult:
    return _safety_result("retail-dashboard-reject-execution", "retail-dashboard-safety-policy-v1", [reason], False)


def reject_dashboard_as_active_ui(
    reason: str = "Retail Dashboard placeholders cannot be treated as active UI in Prompt 49",
) -> RetailDashboardSafetyResult:
    return _safety_result("retail-dashboard-reject-active-ui", "retail-dashboard-safety-policy-v1", [reason], False)
