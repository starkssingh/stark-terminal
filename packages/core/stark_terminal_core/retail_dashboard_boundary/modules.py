from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard_boundary.forbidden import (
    RetailDashboardForbiddenBehaviorKind,
    _non_empty_text,
    _utc_datetime,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


DEFAULT_RETAIL_DASHBOARD_FORBIDDEN_MODULE_BEHAVIORS = [
    RetailDashboardForbiddenBehaviorKind.ACTIVE_UI,
    RetailDashboardForbiddenBehaviorKind.FRONTEND_COMPONENT,
    RetailDashboardForbiddenBehaviorKind.DESKTOP_COMPONENT,
    RetailDashboardForbiddenBehaviorKind.RECOMMENDATION_CARD,
    RetailDashboardForbiddenBehaviorKind.ACTION_BUTTON,
    RetailDashboardForbiddenBehaviorKind.CONFIDENCE_SCORE,
    RetailDashboardForbiddenBehaviorKind.DECISION_OBJECT_DISPLAY,
    RetailDashboardForbiddenBehaviorKind.READINESS_TO_TRADE,
    RetailDashboardForbiddenBehaviorKind.BROKER_CONTROL,
    RetailDashboardForbiddenBehaviorKind.ORDER_BUTTON,
    RetailDashboardForbiddenBehaviorKind.EXECUTION,
    RetailDashboardForbiddenBehaviorKind.APPROVAL_CONTROL,
    RetailDashboardForbiddenBehaviorKind.OVERRIDE_CONTROL,
    RetailDashboardForbiddenBehaviorKind.REAL_DATA_DISPLAY,
    RetailDashboardForbiddenBehaviorKind.EXTERNAL_CALL,
    RetailDashboardForbiddenBehaviorKind.SECRET_OR_CREDENTIAL,
    RetailDashboardForbiddenBehaviorKind.PROVIDER_SDK,
    RetailDashboardForbiddenBehaviorKind.SCRAPING,
]


class RetailDashboardModuleBoundaryPolicy(BaseModel):
    policy_id: str
    module_family: str
    allowed_purpose: str
    forbidden_behaviors: list[RetailDashboardForbiddenBehaviorKind]
    may_create_active_ui: bool = False
    may_create_frontend_components: bool = False
    may_create_desktop_components: bool = False
    may_generate_recommendations: bool = False
    may_generate_actions: bool = False
    may_score_confidence: bool = False
    may_generate_decision_objects: bool = False
    may_generate_readiness_to_trade: bool = False
    may_expose_broker_controls: bool = False
    may_execute: bool = False
    may_grant_approval: bool = False
    may_grant_override: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("policy_id", "module_family", "allowed_purpose", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard module boundary policy text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def module_policy_must_fail_closed(self) -> RetailDashboardModuleBoundaryPolicy:
        if not self.forbidden_behaviors:
            raise ValueError("retail dashboard module boundary policy requires forbidden behaviors")
        if RetailDashboardForbiddenBehaviorKind.UNKNOWN in self.forbidden_behaviors:
            raise ValueError("UNKNOWN retail dashboard forbidden behavior is not allowed")
        if self.may_create_active_ui:
            raise ValueError("retail dashboard modules may not create active UI in Prompt 54")
        if self.may_create_frontend_components:
            raise ValueError("retail dashboard modules may not create frontend components in Prompt 54")
        if self.may_create_desktop_components:
            raise ValueError("retail dashboard modules may not create desktop components in Prompt 54")
        if self.may_generate_recommendations:
            raise ValueError("retail dashboard modules may not generate recommendations in Prompt 54")
        if self.may_generate_actions:
            raise ValueError("retail dashboard modules may not generate actions in Prompt 54")
        if self.may_score_confidence:
            raise ValueError("retail dashboard modules may not score confidence in Prompt 54")
        if self.may_generate_decision_objects:
            raise ValueError("retail dashboard modules may not generate DecisionObjects in Prompt 54")
        if self.may_generate_readiness_to_trade:
            raise ValueError("retail dashboard modules may not generate readiness-to-trade in Prompt 54")
        if self.may_expose_broker_controls:
            raise ValueError("retail dashboard modules may not expose broker controls in Prompt 54")
        if self.may_execute:
            raise ValueError("retail dashboard modules may not execute in Prompt 54")
        if self.may_grant_approval:
            raise ValueError("retail dashboard modules may not grant approval in Prompt 54")
        if self.may_grant_override:
            raise ValueError("retail dashboard modules may not grant override in Prompt 54")
        return self


def _module_policy(module_family: str, allowed_purpose: str) -> RetailDashboardModuleBoundaryPolicy:
    return RetailDashboardModuleBoundaryPolicy(
        policy_id=f"{module_family.replace('_', '-')}-boundary-policy-v1",
        module_family=module_family,
        allowed_purpose=allowed_purpose,
        forbidden_behaviors=list(DEFAULT_RETAIL_DASHBOARD_FORBIDDEN_MODULE_BEHAVIORS),
    )


def default_retail_dashboard_module_boundary_policies() -> list[RetailDashboardModuleBoundaryPolicy]:
    return [
        _module_policy("retail_dashboard", "planning and guardrail placeholders only"),
        _module_policy("retail_dashboard_api", "API contract skeleton placeholders only"),
        _module_policy("retail_dashboard_display", "display contract skeleton placeholders only"),
        _module_policy("retail_dashboard_boundary", "boundary-hardening contracts and invariant helpers only"),
    ]


def evaluate_retail_dashboard_module_boundary_policies(
    policies: list[RetailDashboardModuleBoundaryPolicy] | None = None,
) -> list[str]:
    resolved_policies = policies or default_retail_dashboard_module_boundary_policies()
    blockers: list[str] = []
    for policy in resolved_policies:
        if policy.may_create_active_ui:
            blockers.append(f"{policy.module_family}: may create active UI")
        if policy.may_create_frontend_components:
            blockers.append(f"{policy.module_family}: may create frontend components")
        if policy.may_create_desktop_components:
            blockers.append(f"{policy.module_family}: may create desktop components")
        if policy.may_generate_recommendations:
            blockers.append(f"{policy.module_family}: may generate recommendations")
        if policy.may_generate_actions:
            blockers.append(f"{policy.module_family}: may generate actions")
        if policy.may_score_confidence:
            blockers.append(f"{policy.module_family}: may score confidence")
        if policy.may_generate_decision_objects:
            blockers.append(f"{policy.module_family}: may generate DecisionObjects")
        if policy.may_generate_readiness_to_trade:
            blockers.append(f"{policy.module_family}: may generate readiness-to-trade")
        if policy.may_expose_broker_controls:
            blockers.append(f"{policy.module_family}: may expose broker controls")
        if policy.may_execute:
            blockers.append(f"{policy.module_family}: may execute")
        if policy.may_grant_approval:
            blockers.append(f"{policy.module_family}: may grant approval")
        if policy.may_grant_override:
            blockers.append(f"{policy.module_family}: may grant override")
    return blockers
