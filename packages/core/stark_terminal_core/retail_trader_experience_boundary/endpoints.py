from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience_boundary.forbidden import (
    RetailTraderExperienceForbiddenBehaviorKind,
    _non_empty_text,
    _utc_datetime,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


DEFAULT_RETAIL_TRADER_EXPERIENCE_FORBIDDEN_ENDPOINT_OUTPUTS = [
    RetailTraderExperienceForbiddenBehaviorKind.ACTIVE_UI,
    RetailTraderExperienceForbiddenBehaviorKind.FRONTEND_COMPONENT,
    RetailTraderExperienceForbiddenBehaviorKind.DESKTOP_COMPONENT,
    RetailTraderExperienceForbiddenBehaviorKind.RECOMMENDATION_CARD,
    RetailTraderExperienceForbiddenBehaviorKind.ACTION_BUTTON,
    RetailTraderExperienceForbiddenBehaviorKind.CONFIDENCE_SCORE,
    RetailTraderExperienceForbiddenBehaviorKind.DECISION_OBJECT_DISPLAY,
    RetailTraderExperienceForbiddenBehaviorKind.READINESS_TO_TRADE,
    RetailTraderExperienceForbiddenBehaviorKind.SUITABILITY_PROFILING,
    RetailTraderExperienceForbiddenBehaviorKind.TRADING_PERMISSION_PROFILE,
    RetailTraderExperienceForbiddenBehaviorKind.PERSONA_TO_SUITABILITY_PROFILE,
    RetailTraderExperienceForbiddenBehaviorKind.JOURNEY_TO_TRADING_ADVICE,
    RetailTraderExperienceForbiddenBehaviorKind.BROKER_CONTROL,
    RetailTraderExperienceForbiddenBehaviorKind.ORDER_BUTTON,
    RetailTraderExperienceForbiddenBehaviorKind.EXECUTION,
    RetailTraderExperienceForbiddenBehaviorKind.APPROVAL_CONTROL,
    RetailTraderExperienceForbiddenBehaviorKind.OVERRIDE_CONTROL,
    RetailTraderExperienceForbiddenBehaviorKind.REAL_DATA_DISPLAY,
    RetailTraderExperienceForbiddenBehaviorKind.EXTERNAL_CALL,
    RetailTraderExperienceForbiddenBehaviorKind.SECRET_OR_CREDENTIAL,
]


class RetailTraderExperienceEndpointBoundaryPolicy(BaseModel):
    policy_id: str
    endpoint_family: str
    allowed_methods: list[str]
    forbidden_methods: list[str]
    forbidden_outputs: list[RetailTraderExperienceForbiddenBehaviorKind]
    read_only: bool = True
    unavailable_by_default: bool = True
    accepts_market_data_for_trader_decision: bool = False
    generates_recommendation: bool = False
    generates_active_ui: bool = False
    generates_decision_object: bool = False
    generates_suitability_profile: bool = False
    exposes_broker_controls: bool = False
    executes_trade: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("policy_id", "endpoint_family", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience endpoint boundary policy text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def endpoint_policy_must_fail_closed(self) -> RetailTraderExperienceEndpointBoundaryPolicy:
        if not self.allowed_methods:
            raise ValueError("retail trader experience endpoint boundary policy requires allowed methods")
        if any(not method.strip() for method in self.allowed_methods):
            raise ValueError("retail trader experience endpoint allowed methods cannot be empty")
        if not self.forbidden_outputs:
            raise ValueError("retail trader experience endpoint boundary policy requires forbidden outputs")
        if RetailTraderExperienceForbiddenBehaviorKind.UNKNOWN in self.forbidden_outputs:
            raise ValueError("UNKNOWN retail trader experience forbidden endpoint output is not allowed")
        if not self.read_only:
            raise ValueError("retail trader experience endpoint boundary policies must be read-only")
        if not self.unavailable_by_default:
            raise ValueError("retail trader experience endpoint boundary policies must be unavailable by default")
        if self.accepts_market_data_for_trader_decision:
            raise ValueError("market-data-to-trader-decision endpoints are forbidden")
        if self.generates_recommendation:
            raise ValueError("retail trader experience recommendation endpoints are forbidden")
        if self.generates_active_ui:
            raise ValueError("retail trader experience active UI endpoints are forbidden")
        if self.generates_decision_object:
            raise ValueError("retail trader experience DecisionObject endpoints are forbidden")
        if self.generates_suitability_profile:
            raise ValueError("retail trader experience suitability profiling endpoints are forbidden")
        if self.exposes_broker_controls:
            raise ValueError("retail trader experience broker-control endpoints are forbidden")
        if self.executes_trade:
            raise ValueError("retail trader experience execution endpoints are forbidden")
        return self


def _endpoint_policy(endpoint_family: str) -> RetailTraderExperienceEndpointBoundaryPolicy:
    return RetailTraderExperienceEndpointBoundaryPolicy(
        policy_id=f"{endpoint_family}-boundary-policy-v1",
        endpoint_family=endpoint_family,
        allowed_methods=["GET"],
        forbidden_methods=["POST", "PUT", "PATCH", "DELETE"],
        forbidden_outputs=list(DEFAULT_RETAIL_TRADER_EXPERIENCE_FORBIDDEN_ENDPOINT_OUTPUTS),
    )


def default_retail_trader_experience_endpoint_boundary_policies() -> list[
    RetailTraderExperienceEndpointBoundaryPolicy
]:
    return [
        _endpoint_policy("retail-trader-experience"),
        _endpoint_policy("retail-trader-experience-api"),
        _endpoint_policy("retail-trader-experience-display"),
        _endpoint_policy("retail-trader-experience-boundary"),
    ]


def evaluate_retail_trader_experience_endpoint_boundary_policies(
    policies: list[RetailTraderExperienceEndpointBoundaryPolicy] | None = None,
) -> list[str]:
    resolved_policies = policies or default_retail_trader_experience_endpoint_boundary_policies()
    blockers: list[str] = []
    for policy in resolved_policies:
        if not policy.read_only:
            blockers.append(f"{policy.endpoint_family}: endpoint policy is not read-only")
        if not policy.unavailable_by_default:
            blockers.append(f"{policy.endpoint_family}: endpoint policy is not unavailable by default")
        if policy.accepts_market_data_for_trader_decision:
            blockers.append(f"{policy.endpoint_family}: accepts market data for trader decision")
        if policy.generates_recommendation:
            blockers.append(f"{policy.endpoint_family}: generates recommendations")
        if policy.generates_active_ui:
            blockers.append(f"{policy.endpoint_family}: generates active UI")
        if policy.generates_decision_object:
            blockers.append(f"{policy.endpoint_family}: generates DecisionObjects")
        if policy.generates_suitability_profile:
            blockers.append(f"{policy.endpoint_family}: generates suitability profiles")
        if policy.exposes_broker_controls:
            blockers.append(f"{policy.endpoint_family}: exposes broker controls")
        if policy.executes_trade:
            blockers.append(f"{policy.endpoint_family}: executes trade")
    return blockers
