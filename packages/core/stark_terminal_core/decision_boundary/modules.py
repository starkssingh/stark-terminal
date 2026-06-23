from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_boundary.forbidden import (
    DecisionForbiddenBehaviorKind,
    _non_empty_text,
    _utc_datetime,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


DEFAULT_FORBIDDEN_MODULE_BEHAVIORS = [
    DecisionForbiddenBehaviorKind.RECOMMENDATION,
    DecisionForbiddenBehaviorKind.ACTION_GENERATION,
    DecisionForbiddenBehaviorKind.CONFIDENCE_SCORING,
    DecisionForbiddenBehaviorKind.DECISION_OBJECT_GENERATION,
    DecisionForbiddenBehaviorKind.EXECUTION,
    DecisionForbiddenBehaviorKind.APPROVAL,
    DecisionForbiddenBehaviorKind.OVERRIDE,
    DecisionForbiddenBehaviorKind.ACTIVE_UI,
    DecisionForbiddenBehaviorKind.ACTIVE_WORKFLOW,
    DecisionForbiddenBehaviorKind.TASK_ASSIGNMENT,
    DecisionForbiddenBehaviorKind.REVIEWER_AUTH,
    DecisionForbiddenBehaviorKind.NOTIFICATION,
    DecisionForbiddenBehaviorKind.READINESS_TO_TRADE,
    DecisionForbiddenBehaviorKind.BROKER_BEHAVIOR,
    DecisionForbiddenBehaviorKind.REAL_INGESTION,
    DecisionForbiddenBehaviorKind.EXTERNAL_CALL,
    DecisionForbiddenBehaviorKind.SECRET_OR_CREDENTIAL,
    DecisionForbiddenBehaviorKind.PROVIDER_SDK,
    DecisionForbiddenBehaviorKind.SCRAPING,
]


class DecisionModuleBoundaryPolicy(BaseModel):
    policy_id: str
    module_family: str
    allowed_purpose: str
    forbidden_behaviors: list[DecisionForbiddenBehaviorKind]
    may_generate_recommendations: bool = False
    may_generate_actions: bool = False
    may_score_confidence: bool = False
    may_generate_decision_objects: bool = False
    may_grant_approval: bool = False
    may_grant_override: bool = False
    may_execute: bool = False
    may_create_active_ui: bool = False
    may_create_active_workflow: bool = False
    may_generate_readiness_to_trade: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("policy_id", "module_family", "allowed_purpose", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision module boundary policy text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def module_policy_must_fail_closed(self) -> DecisionModuleBoundaryPolicy:
        if not self.forbidden_behaviors:
            raise ValueError("module boundary policy requires forbidden behaviors")
        if DecisionForbiddenBehaviorKind.UNKNOWN in self.forbidden_behaviors:
            raise ValueError("UNKNOWN forbidden behavior is not allowed")
        if self.may_generate_recommendations:
            raise ValueError("module may not generate recommendations in Prompt 47")
        if self.may_generate_actions:
            raise ValueError("module may not generate actions in Prompt 47")
        if self.may_score_confidence:
            raise ValueError("module may not score confidence in Prompt 47")
        if self.may_generate_decision_objects:
            raise ValueError("module may not generate DecisionObjects in Prompt 47")
        if self.may_grant_approval:
            raise ValueError("module may not grant approval in Prompt 47")
        if self.may_grant_override:
            raise ValueError("module may not grant override in Prompt 47")
        if self.may_execute:
            raise ValueError("module may not execute in Prompt 47")
        if self.may_create_active_ui:
            raise ValueError("module may not create active UI in Prompt 47")
        if self.may_create_active_workflow:
            raise ValueError("module may not create active workflow in Prompt 47")
        if self.may_generate_readiness_to_trade:
            raise ValueError("module may not generate readiness-to-trade in Prompt 47")
        return self


def _module_policy(module_family: str, allowed_purpose: str) -> DecisionModuleBoundaryPolicy:
    return DecisionModuleBoundaryPolicy(
        policy_id=f"{module_family.replace('_', '-')}-module-boundary-policy-v1",
        module_family=module_family,
        allowed_purpose=allowed_purpose,
        forbidden_behaviors=list(DEFAULT_FORBIDDEN_MODULE_BEHAVIORS),
    )


def default_decision_module_boundary_policies() -> list[DecisionModuleBoundaryPolicy]:
    return [
        _module_policy("decision_desk", "planning contracts and readiness templates only"),
        _module_policy("decision_evidence", "evidence bundle contracts only"),
        _module_policy("decision_safety", "guardrails and blocked-output contracts only"),
        _module_policy("decision_api", "read-only API contract skeleton only"),
        _module_policy("decision_readiness_api", "readiness API skeleton placeholders only"),
        _module_policy("decision_display", "display contract skeleton placeholders only"),
        _module_policy("decision_evidence_validation", "validation-only contract inspection only"),
        _module_policy("decision_human_review", "human-review workflow skeleton placeholders only"),
        _module_policy("decision_boundary", "boundary-hardening contracts and invariant helpers only"),
        _module_policy("retail_dashboard", "retail dashboard planning and guardrail placeholders only"),
        _module_policy("retail_dashboard_api", "retail dashboard API contract skeleton placeholders only"),
        _module_policy("retail_dashboard_display", "retail dashboard display contract skeleton placeholders only"),
    ]


def evaluate_decision_module_boundary_policies(
    policies: list[DecisionModuleBoundaryPolicy] | None = None,
) -> list[str]:
    resolved_policies = policies or default_decision_module_boundary_policies()
    blockers: list[str] = []
    for policy in resolved_policies:
        if policy.may_generate_recommendations:
            blockers.append(f"{policy.module_family}: may generate recommendations")
        if policy.may_generate_actions:
            blockers.append(f"{policy.module_family}: may generate actions")
        if policy.may_score_confidence:
            blockers.append(f"{policy.module_family}: may score confidence")
        if policy.may_generate_decision_objects:
            blockers.append(f"{policy.module_family}: may generate DecisionObjects")
        if policy.may_grant_approval:
            blockers.append(f"{policy.module_family}: may grant approval")
        if policy.may_grant_override:
            blockers.append(f"{policy.module_family}: may grant override")
        if policy.may_execute:
            blockers.append(f"{policy.module_family}: may execute")
        if policy.may_create_active_ui:
            blockers.append(f"{policy.module_family}: may create active UI")
        if policy.may_create_active_workflow:
            blockers.append(f"{policy.module_family}: may create active workflow")
        if policy.may_generate_readiness_to_trade:
            blockers.append(f"{policy.module_family}: may generate readiness-to-trade")
    return blockers
