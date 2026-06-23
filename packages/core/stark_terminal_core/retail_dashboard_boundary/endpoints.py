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


DEFAULT_RETAIL_DASHBOARD_FORBIDDEN_ENDPOINT_OUTPUTS = [
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
]


class RetailDashboardEndpointBoundaryPolicy(BaseModel):
    policy_id: str
    endpoint_family: str
    allowed_methods: list[str]
    forbidden_methods: list[str]
    forbidden_outputs: list[RetailDashboardForbiddenBehaviorKind]
    read_only: bool = True
    unavailable_by_default: bool = True
    accepts_market_data_for_dashboard_decision: bool = False
    generates_recommendation: bool = False
    generates_active_ui: bool = False
    generates_decision_object: bool = False
    exposes_broker_controls: bool = False
    executes_trade: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("policy_id", "endpoint_family", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard endpoint boundary policy text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def endpoint_policy_must_fail_closed(self) -> RetailDashboardEndpointBoundaryPolicy:
        if not self.allowed_methods:
            raise ValueError("retail dashboard endpoint boundary policy requires allowed methods")
        if any(not method.strip() for method in self.allowed_methods):
            raise ValueError("retail dashboard endpoint allowed methods cannot be empty")
        if not self.forbidden_outputs:
            raise ValueError("retail dashboard endpoint boundary policy requires forbidden outputs")
        if RetailDashboardForbiddenBehaviorKind.UNKNOWN in self.forbidden_outputs:
            raise ValueError("UNKNOWN retail dashboard forbidden endpoint output is not allowed")
        if not self.read_only:
            raise ValueError("retail dashboard endpoint boundary policies must be read-only")
        if not self.unavailable_by_default:
            raise ValueError("retail dashboard endpoint boundary policies must be unavailable by default")
        if self.accepts_market_data_for_dashboard_decision:
            raise ValueError("market-data-to-dashboard-decision endpoints are forbidden")
        if self.generates_recommendation:
            raise ValueError("retail dashboard recommendation endpoints are forbidden")
        if self.generates_active_ui:
            raise ValueError("retail dashboard active UI endpoints are forbidden")
        if self.generates_decision_object:
            raise ValueError("retail dashboard DecisionObject endpoints are forbidden")
        if self.exposes_broker_controls:
            raise ValueError("retail dashboard broker-control endpoints are forbidden")
        if self.executes_trade:
            raise ValueError("retail dashboard execution endpoints are forbidden")
        return self


def _endpoint_policy(endpoint_family: str) -> RetailDashboardEndpointBoundaryPolicy:
    return RetailDashboardEndpointBoundaryPolicy(
        policy_id=f"{endpoint_family}-boundary-policy-v1",
        endpoint_family=endpoint_family,
        allowed_methods=["GET"],
        forbidden_methods=["POST", "PUT", "PATCH", "DELETE"],
        forbidden_outputs=list(DEFAULT_RETAIL_DASHBOARD_FORBIDDEN_ENDPOINT_OUTPUTS),
    )


def default_retail_dashboard_endpoint_boundary_policies() -> list[RetailDashboardEndpointBoundaryPolicy]:
    return [
        _endpoint_policy("retail-dashboard"),
        _endpoint_policy("retail-dashboard-api"),
        _endpoint_policy("retail-dashboard-display"),
        _endpoint_policy("retail-dashboard-boundary"),
    ]


def evaluate_retail_dashboard_endpoint_boundary_policies(
    policies: list[RetailDashboardEndpointBoundaryPolicy] | None = None,
) -> list[str]:
    resolved_policies = policies or default_retail_dashboard_endpoint_boundary_policies()
    blockers: list[str] = []
    for policy in resolved_policies:
        if not policy.read_only:
            blockers.append(f"{policy.endpoint_family}: endpoint policy is not read-only")
        if not policy.unavailable_by_default:
            blockers.append(f"{policy.endpoint_family}: endpoint policy is not unavailable by default")
        if policy.accepts_market_data_for_dashboard_decision:
            blockers.append(f"{policy.endpoint_family}: accepts market data for dashboard decision")
        if policy.generates_recommendation:
            blockers.append(f"{policy.endpoint_family}: generates recommendations")
        if policy.generates_active_ui:
            blockers.append(f"{policy.endpoint_family}: generates active UI")
        if policy.generates_decision_object:
            blockers.append(f"{policy.endpoint_family}: generates DecisionObjects")
        if policy.exposes_broker_controls:
            blockers.append(f"{policy.endpoint_family}: exposes broker controls")
        if policy.executes_trade:
            blockers.append(f"{policy.endpoint_family}: executes trade")
    return blockers
