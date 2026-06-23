from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_boundary.endpoints import (
    DecisionEndpointBoundaryPolicy,
    default_decision_endpoint_boundary_policies,
    evaluate_decision_endpoint_boundary_policies,
)
from stark_terminal_core.decision_boundary.forbidden import (
    DecisionBoundarySafetyLabel,
    DecisionForbiddenBehaviorRegistry,
    default_decision_forbidden_behavior_registry,
    _non_empty_text,
    _utc_datetime,
)
from stark_terminal_core.decision_boundary.modules import (
    DecisionModuleBoundaryPolicy,
    default_decision_module_boundary_policies,
    evaluate_decision_module_boundary_policies,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class DecisionBoundaryInvariantResult(BaseModel):
    result_id: str
    passed: bool
    checked_families: list[str]
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    active_ui_allowed: bool = False
    active_workflow_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    safety_label: DecisionBoundarySafetyLabel = DecisionBoundarySafetyLabel.BOUNDARY_HARDENING_ONLY
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision boundary invariant result text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def invariant_result_must_fail_closed(self) -> DecisionBoundaryInvariantResult:
        if not self.checked_families:
            raise ValueError("boundary invariant result requires checked families")
        if self.recommendations_allowed:
            raise ValueError("boundary invariant cannot allow recommendations")
        if self.action_generation_allowed:
            raise ValueError("boundary invariant cannot allow action generation")
        if self.confidence_scoring_allowed:
            raise ValueError("boundary invariant cannot allow confidence scoring")
        if self.decision_object_generation_allowed:
            raise ValueError("boundary invariant cannot allow DecisionObject generation")
        if self.execution_allowed:
            raise ValueError("boundary invariant cannot allow execution")
        if self.approval_allowed:
            raise ValueError("boundary invariant cannot allow approval")
        if self.override_allowed:
            raise ValueError("boundary invariant cannot allow override")
        if self.active_ui_allowed:
            raise ValueError("boundary invariant cannot allow active UI")
        if self.active_workflow_allowed:
            raise ValueError("boundary invariant cannot allow active workflow")
        if self.readiness_to_trade_allowed:
            raise ValueError("boundary invariant cannot allow readiness-to-trade")
        if self.passed and self.blockers:
            raise ValueError("boundary invariant cannot pass with blockers")
        if self.safety_label == DecisionBoundarySafetyLabel.UNKNOWN:
            raise ValueError("UNKNOWN boundary safety label is not allowed")
        return self


def evaluate_decision_boundary_invariants(
    endpoint_policies: list[DecisionEndpointBoundaryPolicy] | None = None,
    module_policies: list[DecisionModuleBoundaryPolicy] | None = None,
    registry: DecisionForbiddenBehaviorRegistry | None = None,
) -> DecisionBoundaryInvariantResult:
    resolved_endpoint_policies = endpoint_policies or default_decision_endpoint_boundary_policies()
    resolved_module_policies = module_policies or default_decision_module_boundary_policies()
    resolved_registry = registry or default_decision_forbidden_behavior_registry()
    blockers = [
        *evaluate_decision_endpoint_boundary_policies(resolved_endpoint_policies),
        *evaluate_decision_module_boundary_policies(resolved_module_policies),
    ]
    checked_families = [
        *[policy.endpoint_family for policy in resolved_endpoint_policies],
        *[policy.module_family for policy in resolved_module_policies],
        resolved_registry.registry_id,
    ]
    return DecisionBoundaryInvariantResult(
        result_id="decision-boundary-invariant-result-v1",
        passed=not blockers,
        checked_families=checked_families,
        blockers=blockers,
        warnings=[],
    )


def _blocked_result(result_id: str, reason: str) -> DecisionBoundaryInvariantResult:
    return DecisionBoundaryInvariantResult(
        result_id=result_id,
        passed=False,
        checked_families=["decision_boundary"],
        blockers=[reason],
        safety_label=DecisionBoundarySafetyLabel.BLOCKED,
    )


def reject_recommendation_boundary_violation(reason: str = "recommendation boundary violation") -> DecisionBoundaryInvariantResult:
    return _blocked_result("decision-boundary-reject-recommendation-v1", reason)


def reject_execution_boundary_violation(reason: str = "execution boundary violation") -> DecisionBoundaryInvariantResult:
    return _blocked_result("decision-boundary-reject-execution-v1", reason)


def reject_approval_override_boundary_violation(
    reason: str = "approval or override boundary violation",
) -> DecisionBoundaryInvariantResult:
    return _blocked_result("decision-boundary-reject-approval-override-v1", reason)


def reject_active_ui_workflow_boundary_violation(
    reason: str = "active UI or workflow boundary violation",
) -> DecisionBoundaryInvariantResult:
    return _blocked_result("decision-boundary-reject-active-ui-workflow-v1", reason)


def reject_readiness_to_trade_boundary_violation(
    reason: str = "readiness-to-trade boundary violation",
) -> DecisionBoundaryInvariantResult:
    return _blocked_result("decision-boundary-reject-readiness-to-trade-v1", reason)
