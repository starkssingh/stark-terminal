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


DEFAULT_FORBIDDEN_ENDPOINT_OUTPUTS = [
    DecisionForbiddenBehaviorKind.RECOMMENDATION,
    DecisionForbiddenBehaviorKind.ACTION_GENERATION,
    DecisionForbiddenBehaviorKind.CONFIDENCE_SCORING,
    DecisionForbiddenBehaviorKind.DECISION_OBJECT_GENERATION,
    DecisionForbiddenBehaviorKind.EXECUTION,
    DecisionForbiddenBehaviorKind.APPROVAL,
    DecisionForbiddenBehaviorKind.OVERRIDE,
    DecisionForbiddenBehaviorKind.ACTIVE_UI,
    DecisionForbiddenBehaviorKind.ACTIVE_WORKFLOW,
    DecisionForbiddenBehaviorKind.READINESS_TO_TRADE,
    DecisionForbiddenBehaviorKind.BROKER_BEHAVIOR,
    DecisionForbiddenBehaviorKind.REAL_INGESTION,
    DecisionForbiddenBehaviorKind.EXTERNAL_CALL,
    DecisionForbiddenBehaviorKind.SECRET_OR_CREDENTIAL,
]


class DecisionEndpointBoundaryPolicy(BaseModel):
    policy_id: str
    endpoint_family: str
    allowed_methods: list[str]
    forbidden_methods: list[str]
    forbidden_outputs: list[DecisionForbiddenBehaviorKind]
    read_only: bool = True
    unavailable_by_default: bool = True
    accepts_market_data_for_decision: bool = False
    generates_recommendation: bool = False
    generates_decision_object: bool = False
    grants_approval: bool = False
    grants_override: bool = False
    executes_trade: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("policy_id", "endpoint_family", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision endpoint boundary policy text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def endpoint_policy_must_fail_closed(self) -> DecisionEndpointBoundaryPolicy:
        if not self.allowed_methods:
            raise ValueError("endpoint boundary policy requires allowed methods")
        if any(not method.strip() for method in self.allowed_methods):
            raise ValueError("endpoint boundary allowed methods cannot be empty")
        if not self.forbidden_outputs:
            raise ValueError("endpoint boundary policy requires forbidden outputs")
        if DecisionForbiddenBehaviorKind.UNKNOWN in self.forbidden_outputs:
            raise ValueError("UNKNOWN forbidden output is not allowed")
        if not self.read_only:
            raise ValueError("decision endpoint boundary policies must be read-only")
        if not self.unavailable_by_default:
            raise ValueError("decision endpoint boundary policies must be unavailable by default")
        if self.accepts_market_data_for_decision:
            raise ValueError("market-data-to-decision endpoints are forbidden")
        if self.generates_recommendation:
            raise ValueError("recommendation endpoints are forbidden")
        if self.generates_decision_object:
            raise ValueError("DecisionObject endpoints are forbidden")
        if self.grants_approval:
            raise ValueError("approval endpoints are forbidden")
        if self.grants_override:
            raise ValueError("override endpoints are forbidden")
        if self.executes_trade:
            raise ValueError("execution endpoints are forbidden")
        return self


def _endpoint_policy(endpoint_family: str) -> DecisionEndpointBoundaryPolicy:
    return DecisionEndpointBoundaryPolicy(
        policy_id=f"{endpoint_family}-endpoint-boundary-policy-v1",
        endpoint_family=endpoint_family,
        allowed_methods=["GET"],
        forbidden_methods=["POST", "PUT", "PATCH", "DELETE"],
        forbidden_outputs=list(DEFAULT_FORBIDDEN_ENDPOINT_OUTPUTS),
    )


def default_decision_endpoint_boundary_policies() -> list[DecisionEndpointBoundaryPolicy]:
    return [
        _endpoint_policy("decision-desk"),
        _endpoint_policy("decision-evidence"),
        _endpoint_policy("decision-safety"),
        _endpoint_policy("decision-desk-api"),
        _endpoint_policy("decision-readiness-api"),
        _endpoint_policy("decision-display"),
        _endpoint_policy("decision-evidence-validation"),
        _endpoint_policy("decision-human-review"),
        _endpoint_policy("decision-boundary"),
        _endpoint_policy("retail-dashboard"),
        _endpoint_policy("retail-dashboard-api"),
        _endpoint_policy("retail-dashboard-display"),
    ]


def evaluate_decision_endpoint_boundary_policies(
    policies: list[DecisionEndpointBoundaryPolicy] | None = None,
) -> list[str]:
    resolved_policies = policies or default_decision_endpoint_boundary_policies()
    blockers: list[str] = []
    for policy in resolved_policies:
        if not policy.read_only:
            blockers.append(f"{policy.endpoint_family}: endpoint policy is not read-only")
        if not policy.unavailable_by_default:
            blockers.append(f"{policy.endpoint_family}: endpoint policy is not unavailable by default")
        if policy.accepts_market_data_for_decision:
            blockers.append(f"{policy.endpoint_family}: accepts market data for decision")
        if policy.generates_recommendation:
            blockers.append(f"{policy.endpoint_family}: generates recommendations")
        if policy.generates_decision_object:
            blockers.append(f"{policy.endpoint_family}: generates DecisionObjects")
        if policy.grants_approval:
            blockers.append(f"{policy.endpoint_family}: grants approval")
        if policy.grants_override:
            blockers.append(f"{policy.endpoint_family}: grants override")
        if policy.executes_trade:
            blockers.append(f"{policy.endpoint_family}: executes trade")
    return blockers
