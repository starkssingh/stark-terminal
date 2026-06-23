from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard_boundary.endpoints import (
    RetailDashboardEndpointBoundaryPolicy,
    default_retail_dashboard_endpoint_boundary_policies,
    evaluate_retail_dashboard_endpoint_boundary_policies,
)
from stark_terminal_core.retail_dashboard_boundary.forbidden import (
    RetailDashboardBoundarySafetyLabel,
    RetailDashboardForbiddenBehaviorRegistry,
    default_retail_dashboard_forbidden_behavior_registry,
    _non_empty_text,
    _utc_datetime,
)
from stark_terminal_core.retail_dashboard_boundary.modules import (
    RetailDashboardModuleBoundaryPolicy,
    default_retail_dashboard_module_boundary_policies,
    evaluate_retail_dashboard_module_boundary_policies,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RetailDashboardBoundaryInvariantResult(BaseModel):
    result_id: str
    passed: bool
    checked_families: list[str]
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    active_ui_allowed: bool = False
    frontend_components_allowed: bool = False
    desktop_components_allowed: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    safety_label: RetailDashboardBoundarySafetyLabel = (
        RetailDashboardBoundarySafetyLabel.BOUNDARY_HARDENING_ONLY
    )
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard boundary invariant result text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def invariant_result_must_fail_closed(self) -> RetailDashboardBoundaryInvariantResult:
        if not self.checked_families:
            raise ValueError("retail dashboard boundary invariant result requires checked families")
        dangerous_flags = {
            "active UI": self.active_ui_allowed,
            "frontend components": self.frontend_components_allowed,
            "desktop components": self.desktop_components_allowed,
            "recommendations": self.recommendations_allowed,
            "action generation": self.action_generation_allowed,
            "confidence scoring": self.confidence_scoring_allowed,
            "DecisionObject generation": self.decision_object_generation_allowed,
            "readiness-to-trade": self.readiness_to_trade_allowed,
            "broker controls": self.broker_controls_allowed,
            "execution": self.execution_allowed,
            "approval": self.approval_allowed,
            "override": self.override_allowed,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"retail dashboard boundary invariant cannot allow: {', '.join(enabled)}")
        if self.passed and self.blockers:
            raise ValueError("retail dashboard boundary invariant cannot pass with blockers")
        if self.safety_label == RetailDashboardBoundarySafetyLabel.UNKNOWN:
            raise ValueError("UNKNOWN retail dashboard boundary safety label is not allowed")
        return self


def evaluate_retail_dashboard_boundary_invariants(
    endpoint_policies: list[RetailDashboardEndpointBoundaryPolicy] | None = None,
    module_policies: list[RetailDashboardModuleBoundaryPolicy] | None = None,
    registry: RetailDashboardForbiddenBehaviorRegistry | None = None,
) -> RetailDashboardBoundaryInvariantResult:
    resolved_endpoint_policies = endpoint_policies or default_retail_dashboard_endpoint_boundary_policies()
    resolved_module_policies = module_policies or default_retail_dashboard_module_boundary_policies()
    resolved_registry = registry or default_retail_dashboard_forbidden_behavior_registry()
    blockers = [
        *evaluate_retail_dashboard_endpoint_boundary_policies(resolved_endpoint_policies),
        *evaluate_retail_dashboard_module_boundary_policies(resolved_module_policies),
    ]
    if not resolved_registry.complete:
        blockers.append("retail dashboard forbidden behavior registry is incomplete")
    checked_families = [
        *[policy.endpoint_family for policy in resolved_endpoint_policies],
        *[policy.module_family for policy in resolved_module_policies],
        resolved_registry.registry_id,
    ]
    return RetailDashboardBoundaryInvariantResult(
        result_id="retail-dashboard-boundary-invariant-result-v1",
        passed=not blockers,
        checked_families=checked_families,
        blockers=blockers,
        warnings=[],
    )


def _blocked_result(result_id: str, reason: str) -> RetailDashboardBoundaryInvariantResult:
    return RetailDashboardBoundaryInvariantResult(
        result_id=result_id,
        passed=False,
        checked_families=["retail_dashboard_boundary"],
        blockers=[reason],
        safety_label=RetailDashboardBoundarySafetyLabel.BLOCKED,
    )


def reject_dashboard_active_ui_boundary_violation(
    reason: str = "retail dashboard active UI boundary violation",
) -> RetailDashboardBoundaryInvariantResult:
    return _blocked_result("retail-dashboard-boundary-reject-active-ui-v1", reason)


def reject_dashboard_recommendation_boundary_violation(
    reason: str = "retail dashboard recommendation boundary violation",
) -> RetailDashboardBoundaryInvariantResult:
    return _blocked_result("retail-dashboard-boundary-reject-recommendation-v1", reason)


def reject_dashboard_execution_boundary_violation(
    reason: str = "retail dashboard execution boundary violation",
) -> RetailDashboardBoundaryInvariantResult:
    return _blocked_result("retail-dashboard-boundary-reject-execution-v1", reason)


def reject_dashboard_broker_control_boundary_violation(
    reason: str = "retail dashboard broker control boundary violation",
) -> RetailDashboardBoundaryInvariantResult:
    return _blocked_result("retail-dashboard-boundary-reject-broker-control-v1", reason)


def reject_dashboard_readiness_to_trade_boundary_violation(
    reason: str = "retail dashboard readiness-to-trade boundary violation",
) -> RetailDashboardBoundaryInvariantResult:
    return _blocked_result("retail-dashboard-boundary-reject-readiness-to-trade-v1", reason)
