from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience_boundary.endpoints import (
    RetailTraderExperienceEndpointBoundaryPolicy,
    default_retail_trader_experience_endpoint_boundary_policies,
    evaluate_retail_trader_experience_endpoint_boundary_policies,
)
from stark_terminal_core.retail_trader_experience_boundary.forbidden import (
    RetailTraderExperienceBoundarySafetyLabel,
    RetailTraderExperienceForbiddenBehaviorRegistry,
    default_retail_trader_experience_forbidden_behavior_registry,
    _non_empty_text,
    _utc_datetime,
)
from stark_terminal_core.retail_trader_experience_boundary.modules import (
    RetailTraderExperienceModuleBoundaryPolicy,
    default_retail_trader_experience_module_boundary_policies,
    evaluate_retail_trader_experience_module_boundary_policies,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RetailTraderExperienceBoundaryInvariantResult(BaseModel):
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
    suitability_profiling_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    safety_label: RetailTraderExperienceBoundarySafetyLabel = (
        RetailTraderExperienceBoundarySafetyLabel.BOUNDARY_HARDENING_ONLY
    )
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience boundary invariant result text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def invariant_result_must_fail_closed(self) -> RetailTraderExperienceBoundaryInvariantResult:
        if not self.checked_families:
            raise ValueError("retail trader experience boundary invariant result requires checked families")
        dangerous_flags = {
            "active UI": self.active_ui_allowed,
            "frontend components": self.frontend_components_allowed,
            "desktop components": self.desktop_components_allowed,
            "recommendations": self.recommendations_allowed,
            "action generation": self.action_generation_allowed,
            "confidence scoring": self.confidence_scoring_allowed,
            "DecisionObject generation": self.decision_object_generation_allowed,
            "readiness-to-trade": self.readiness_to_trade_allowed,
            "suitability profiling": self.suitability_profiling_allowed,
            "broker controls": self.broker_controls_allowed,
            "execution": self.execution_allowed,
            "approval": self.approval_allowed,
            "override": self.override_allowed,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"retail trader experience boundary invariant cannot allow: {', '.join(enabled)}")
        if self.passed and self.blockers:
            raise ValueError("retail trader experience boundary invariant cannot pass with blockers")
        if self.safety_label == RetailTraderExperienceBoundarySafetyLabel.UNKNOWN:
            raise ValueError("UNKNOWN retail trader experience boundary safety label is not allowed")
        return self


def evaluate_retail_trader_experience_boundary_invariants(
    endpoint_policies: list[RetailTraderExperienceEndpointBoundaryPolicy] | None = None,
    module_policies: list[RetailTraderExperienceModuleBoundaryPolicy] | None = None,
    registry: RetailTraderExperienceForbiddenBehaviorRegistry | None = None,
) -> RetailTraderExperienceBoundaryInvariantResult:
    resolved_endpoint_policies = endpoint_policies or default_retail_trader_experience_endpoint_boundary_policies()
    resolved_module_policies = module_policies or default_retail_trader_experience_module_boundary_policies()
    resolved_registry = registry or default_retail_trader_experience_forbidden_behavior_registry()
    blockers = [
        *evaluate_retail_trader_experience_endpoint_boundary_policies(resolved_endpoint_policies),
        *evaluate_retail_trader_experience_module_boundary_policies(resolved_module_policies),
    ]
    if not resolved_registry.complete:
        blockers.append("retail trader experience forbidden behavior registry is incomplete")
    checked_families = [
        *[policy.endpoint_family for policy in resolved_endpoint_policies],
        *[policy.module_family for policy in resolved_module_policies],
        resolved_registry.registry_id,
    ]
    return RetailTraderExperienceBoundaryInvariantResult(
        result_id="retail-trader-experience-boundary-invariant-result-v1",
        passed=not blockers,
        checked_families=checked_families,
        blockers=blockers,
        warnings=[],
    )


def _blocked_result(result_id: str, reason: str) -> RetailTraderExperienceBoundaryInvariantResult:
    return RetailTraderExperienceBoundaryInvariantResult(
        result_id=result_id,
        passed=False,
        checked_families=["retail_trader_experience_boundary"],
        blockers=[reason],
        safety_label=RetailTraderExperienceBoundarySafetyLabel.BLOCKED,
    )


def reject_experience_active_ui_boundary_violation(
    reason: str = "retail trader experience active UI boundary violation",
) -> RetailTraderExperienceBoundaryInvariantResult:
    return _blocked_result("retail-trader-experience-boundary-reject-active-ui-v1", reason)


def reject_experience_recommendation_boundary_violation(
    reason: str = "retail trader experience recommendation boundary violation",
) -> RetailTraderExperienceBoundaryInvariantResult:
    return _blocked_result("retail-trader-experience-boundary-reject-recommendation-v1", reason)


def reject_experience_execution_boundary_violation(
    reason: str = "retail trader experience execution boundary violation",
) -> RetailTraderExperienceBoundaryInvariantResult:
    return _blocked_result("retail-trader-experience-boundary-reject-execution-v1", reason)


def reject_experience_broker_control_boundary_violation(
    reason: str = "retail trader experience broker control boundary violation",
) -> RetailTraderExperienceBoundaryInvariantResult:
    return _blocked_result("retail-trader-experience-boundary-reject-broker-control-v1", reason)


def reject_experience_readiness_to_trade_boundary_violation(
    reason: str = "retail trader experience readiness-to-trade boundary violation",
) -> RetailTraderExperienceBoundaryInvariantResult:
    return _blocked_result("retail-trader-experience-boundary-reject-readiness-to-trade-v1", reason)


def reject_experience_suitability_profiling_boundary_violation(
    reason: str = "retail trader experience suitability profiling boundary violation",
) -> RetailTraderExperienceBoundaryInvariantResult:
    return _blocked_result("retail-trader-experience-boundary-reject-suitability-profiling-v1", reason)
