from __future__ import annotations

from datetime import datetime
from typing import Iterable

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.retail_dashboard_display.contracts import (
    RetailDashboardDisplayContractMetadata,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_dashboard_display_notes,
)
from stark_terminal_core.retail_dashboard_display.layouts import RetailDashboardLayoutPlaceholder
from stark_terminal_core.retail_dashboard_display.widgets import RetailDashboardWidgetPlaceholder


class RetailDashboardDisplaySafetyPolicy(BaseModel):
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
    require_display_contract_only: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard display safety policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_dashboard_display_notes(value)

    @model_validator(mode="after")
    def safety_policy_must_fail_closed(self) -> RetailDashboardDisplaySafetyPolicy:
        if self.allow_active_ui:
            raise ValueError("Retail Dashboard Display active UI is forbidden")
        if self.allow_recommendations:
            raise ValueError("Retail Dashboard Display recommendations are forbidden")
        if self.allow_action_generation:
            raise ValueError("Retail Dashboard Display action generation is forbidden")
        if self.allow_confidence_scoring:
            raise ValueError("Retail Dashboard Display confidence scoring is forbidden")
        if self.allow_decision_object_generation:
            raise ValueError("Retail Dashboard Display DecisionObject generation is forbidden")
        if self.allow_readiness_to_trade:
            raise ValueError("Retail Dashboard Display readiness-to-trade is forbidden")
        if self.allow_broker_controls:
            raise ValueError("Retail Dashboard Display broker controls are forbidden")
        if self.allow_execution:
            raise ValueError("Retail Dashboard Display execution is forbidden")
        if self.allow_approval:
            raise ValueError("Retail Dashboard Display approval is forbidden")
        if self.allow_override:
            raise ValueError("Retail Dashboard Display override is forbidden")
        if not self.require_display_contract_only:
            raise ValueError("Retail Dashboard Display must require display-contract-only mode")
        return self


class RetailDashboardDisplaySafetyResult(BaseModel):
    result_id: str
    policy_id: str
    safe: bool
    reasons: list[str]
    display_contract_only: bool = True
    active_ui_allowed: bool = False
    recommendations_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "policy_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard display safety result text fields")

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_non_empty(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_retail_dashboard_display_notes(value)
        if not sanitized:
            raise ValueError("retail dashboard display safety result reasons cannot be empty")
        return sanitized

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def safety_result_must_fail_closed(self) -> RetailDashboardDisplaySafetyResult:
        if not self.display_contract_only:
            raise ValueError("Retail Dashboard Display safety result must remain contract-only")
        if self.active_ui_allowed:
            raise ValueError("Retail Dashboard Display safety result cannot allow active UI")
        if self.recommendations_allowed:
            raise ValueError("Retail Dashboard Display safety result cannot allow recommendations")
        if self.broker_controls_allowed:
            raise ValueError("Retail Dashboard Display safety result cannot allow broker controls")
        if self.execution_allowed:
            raise ValueError("Retail Dashboard Display safety result cannot allow execution")
        return self


def default_retail_dashboard_display_safety_policy(
    settings: Settings | None = None,
) -> RetailDashboardDisplaySafetyPolicy:
    resolved = settings or get_settings()
    return RetailDashboardDisplaySafetyPolicy(
        policy_id="retail-dashboard-display-safety-policy-v1",
        name="Retail Dashboard Display Contract Skeleton Safety Policy",
        allow_active_ui=resolved.retail_dashboard_display_allow_active_ui,
        allow_recommendations=resolved.retail_dashboard_display_allow_recommendations,
        allow_action_generation=resolved.retail_dashboard_display_allow_action_generation,
        allow_confidence_scoring=resolved.retail_dashboard_display_allow_confidence_scoring,
        allow_decision_object_generation=resolved.retail_dashboard_display_allow_decision_object_generation,
        allow_readiness_to_trade=resolved.retail_dashboard_display_allow_readiness_to_trade,
        allow_broker_controls=resolved.retail_dashboard_display_allow_broker_controls,
        allow_execution=resolved.retail_dashboard_display_allow_execution,
        allow_approval=resolved.retail_dashboard_display_allow_approval,
        allow_override=resolved.retail_dashboard_display_allow_override,
        notes=["Prompt 51 display contract skeleton policy; no active UI, broker controls, or execution."],
    )


def _safety_result(policy: RetailDashboardDisplaySafetyPolicy, safe: bool, reasons: list[str]) -> RetailDashboardDisplaySafetyResult:
    return RetailDashboardDisplaySafetyResult(
        result_id="retail-dashboard-display-safety-result-v1",
        policy_id=policy.policy_id,
        safe=safe,
        reasons=reasons,
    )


def evaluate_retail_dashboard_display_contract_safety(
    contract: RetailDashboardDisplayContractMetadata,
    policy: RetailDashboardDisplaySafetyPolicy,
) -> RetailDashboardDisplaySafetyResult:
    reasons: list[str] = []
    if contract.active_ui_allowed or policy.allow_active_ui:
        reasons.append("active UI is forbidden")
    if contract.recommendations_allowed or policy.allow_recommendations:
        reasons.append("recommendations are forbidden")
    if contract.action_generation_allowed or policy.allow_action_generation:
        reasons.append("action generation is forbidden")
    if contract.confidence_scoring_allowed or policy.allow_confidence_scoring:
        reasons.append("confidence scoring is forbidden")
    if contract.decision_object_generation_allowed or policy.allow_decision_object_generation:
        reasons.append("DecisionObject generation or display is forbidden")
    if contract.readiness_to_trade_allowed or policy.allow_readiness_to_trade:
        reasons.append("readiness-to-trade is forbidden")
    if contract.broker_controls_allowed or policy.allow_broker_controls:
        reasons.append("broker controls are forbidden")
    if contract.execution_allowed or policy.allow_execution:
        reasons.append("execution is forbidden")
    if contract.approval_allowed or policy.allow_approval:
        reasons.append("approval is forbidden")
    if contract.override_allowed or policy.allow_override:
        reasons.append("override is forbidden")
    if not contract.returns_unavailable_by_default:
        reasons.append("display contract must return unavailable by default")
    return _safety_result(policy, not reasons, reasons or ["display contract remains fail-closed"])


def evaluate_retail_dashboard_layouts_safety(
    layouts: Iterable[RetailDashboardLayoutPlaceholder],
    policy: RetailDashboardDisplaySafetyPolicy,
) -> RetailDashboardDisplaySafetyResult:
    reasons: list[str] = []
    for layout in layouts:
        if layout.active_ui or layout.rendered_now:
            reasons.append(f"{layout.layout_id}: active or rendered layout is forbidden")
        if not layout.unavailable or not layout.display_contract_only:
            reasons.append(f"{layout.layout_id}: layout must remain unavailable and contract-only")
        if layout.recommendations_allowed or layout.readiness_to_trade_allowed:
            reasons.append(f"{layout.layout_id}: recommendation or readiness-to-trade display is forbidden")
        if layout.broker_controls_allowed or layout.execution_allowed:
            reasons.append(f"{layout.layout_id}: broker controls or execution are forbidden")
    if policy.allow_active_ui or policy.allow_execution:
        reasons.append("policy cannot allow active UI or execution")
    return _safety_result(policy, not reasons, reasons or ["layouts remain fail-closed placeholders"])


def evaluate_retail_dashboard_widgets_safety(
    widgets: Iterable[RetailDashboardWidgetPlaceholder],
    policy: RetailDashboardDisplaySafetyPolicy,
) -> RetailDashboardDisplaySafetyResult:
    reasons: list[str] = []
    for widget in widgets:
        if widget.active_ui or widget.rendered_now:
            reasons.append(f"{widget.widget_id}: active or rendered widget is forbidden")
        if not widget.unavailable or not widget.display_contract_only:
            reasons.append(f"{widget.widget_id}: widget must remain unavailable and contract-only")
        if widget.recommendation_widget or widget.action_widget or widget.confidence_widget:
            reasons.append(f"{widget.widget_id}: recommendation, action, or confidence widget is forbidden")
        if widget.decision_object_widget or widget.readiness_to_trade_widget:
            reasons.append(f"{widget.widget_id}: DecisionObject or readiness-to-trade widget is forbidden")
        if widget.broker_control_widget or widget.execution_widget:
            reasons.append(f"{widget.widget_id}: broker control or execution widget is forbidden")
        if widget.approval_widget or widget.override_widget:
            reasons.append(f"{widget.widget_id}: approval or override widget is forbidden")
    if policy.allow_recommendations or policy.allow_execution:
        reasons.append("policy cannot allow recommendations or execution")
    return _safety_result(policy, not reasons, reasons or ["widgets remain fail-closed placeholders"])


def reject_display_as_active_ui(reason: str = "Retail Dashboard Display active UI is forbidden") -> RetailDashboardDisplaySafetyResult:
    policy = RetailDashboardDisplaySafetyPolicy(
        policy_id="retail-dashboard-display-active-ui-rejection-policy-v1",
        name="Retail Dashboard Display Active UI Rejection",
    )
    return _safety_result(policy, False, [reason])


def reject_display_as_recommendation(
    reason: str = "Retail Dashboard Display cannot be interpreted as a recommendation",
) -> RetailDashboardDisplaySafetyResult:
    policy = RetailDashboardDisplaySafetyPolicy(
        policy_id="retail-dashboard-display-recommendation-rejection-policy-v1",
        name="Retail Dashboard Display Recommendation Rejection",
    )
    return _safety_result(policy, False, [reason])


def reject_display_as_execution_surface(
    reason: str = "Retail Dashboard Display cannot be interpreted as an execution surface",
) -> RetailDashboardDisplaySafetyResult:
    policy = RetailDashboardDisplaySafetyPolicy(
        policy_id="retail-dashboard-display-execution-rejection-policy-v1",
        name="Retail Dashboard Display Execution Rejection",
    )
    return _safety_result(policy, False, [reason])
