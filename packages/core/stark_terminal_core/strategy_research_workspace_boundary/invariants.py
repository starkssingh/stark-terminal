from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_boundary.endpoints import (
    StrategyResearchEndpointBoundaryPolicy,
    default_strategy_research_endpoint_boundary_policies,
    evaluate_strategy_research_endpoint_boundary_policies,
)
from stark_terminal_core.strategy_research_workspace_boundary.forbidden import (
    StrategyResearchBoundarySafetyLabel,
    StrategyResearchForbiddenBehaviorRegistry,
    _non_empty_text,
    _utc_datetime,
    default_strategy_research_forbidden_behavior_registry,
)
from stark_terminal_core.strategy_research_workspace_boundary.modules import (
    StrategyResearchModuleBoundaryPolicy,
    default_strategy_research_module_boundary_policies,
    evaluate_strategy_research_module_boundary_policies,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class StrategyResearchBoundaryInvariantResult(BaseModel):
    result_id: str
    passed: bool
    checked_families: list[str]
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    active_ui_allowed: bool = False
    frontend_components_allowed: bool = False
    desktop_components_allowed: bool = False
    paper_ingestion_allowed: bool = False
    paper_parsing_allowed: bool = False
    strategy_generation_allowed: bool = False
    strategy_code_generation_allowed: bool = False
    backtesting_allowed: bool = False
    optimization_allowed: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    safety_label: StrategyResearchBoundarySafetyLabel = (
        StrategyResearchBoundarySafetyLabel.BOUNDARY_HARDENING_ONLY
    )
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research boundary invariant result text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def invariant_result_must_fail_closed(self) -> StrategyResearchBoundaryInvariantResult:
        if not self.checked_families:
            raise ValueError("strategy research boundary invariant result requires checked families")
        dangerous_flags = {
            "active UI": self.active_ui_allowed,
            "frontend components": self.frontend_components_allowed,
            "desktop components": self.desktop_components_allowed,
            "paper ingestion": self.paper_ingestion_allowed,
            "paper parsing": self.paper_parsing_allowed,
            "strategy generation": self.strategy_generation_allowed,
            "strategy code generation": self.strategy_code_generation_allowed,
            "backtesting": self.backtesting_allowed,
            "optimization": self.optimization_allowed,
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
            raise ValueError(f"strategy research boundary invariant cannot allow: {', '.join(enabled)}")
        if self.passed and self.blockers:
            raise ValueError("strategy research boundary invariant cannot pass with blockers")
        if self.safety_label == StrategyResearchBoundarySafetyLabel.UNKNOWN:
            raise ValueError("UNKNOWN strategy research boundary safety label is not allowed")
        return self


def evaluate_strategy_research_boundary_invariants(
    endpoint_policies: list[StrategyResearchEndpointBoundaryPolicy] | None = None,
    module_policies: list[StrategyResearchModuleBoundaryPolicy] | None = None,
    registry: StrategyResearchForbiddenBehaviorRegistry | None = None,
) -> StrategyResearchBoundaryInvariantResult:
    resolved_endpoint_policies = endpoint_policies or default_strategy_research_endpoint_boundary_policies()
    resolved_module_policies = module_policies or default_strategy_research_module_boundary_policies()
    resolved_registry = registry or default_strategy_research_forbidden_behavior_registry()
    blockers = [
        *evaluate_strategy_research_endpoint_boundary_policies(resolved_endpoint_policies),
        *evaluate_strategy_research_module_boundary_policies(resolved_module_policies),
    ]
    if not resolved_registry.complete:
        blockers.append("strategy research forbidden behavior registry is incomplete")
    checked_families = [
        *[policy.endpoint_family for policy in resolved_endpoint_policies],
        *[policy.module_family for policy in resolved_module_policies],
        resolved_registry.registry_id,
    ]
    return StrategyResearchBoundaryInvariantResult(
        result_id="strategy-research-boundary-invariant-result-v1",
        passed=not blockers,
        checked_families=checked_families,
        blockers=blockers,
        warnings=[],
    )


def _blocked_result(result_id: str, reason: str) -> StrategyResearchBoundaryInvariantResult:
    return StrategyResearchBoundaryInvariantResult(
        result_id=result_id,
        passed=False,
        checked_families=["strategy_research_workspace_boundary"],
        blockers=[reason],
        safety_label=StrategyResearchBoundarySafetyLabel.BLOCKED,
    )


def reject_strategy_research_active_ui_boundary_violation(
    reason: str = "strategy research active UI boundary violation",
) -> StrategyResearchBoundaryInvariantResult:
    return _blocked_result("strategy-research-boundary-reject-active-ui-v1", reason)


def reject_strategy_research_paper_parsing_boundary_violation(
    reason: str = "strategy research paper parsing boundary violation",
) -> StrategyResearchBoundaryInvariantResult:
    return _blocked_result("strategy-research-boundary-reject-paper-parsing-v1", reason)


def reject_strategy_research_strategy_generation_boundary_violation(
    reason: str = "strategy research strategy generation boundary violation",
) -> StrategyResearchBoundaryInvariantResult:
    return _blocked_result("strategy-research-boundary-reject-strategy-generation-v1", reason)


def reject_strategy_research_backtesting_boundary_violation(
    reason: str = "strategy research backtesting boundary violation",
) -> StrategyResearchBoundaryInvariantResult:
    return _blocked_result("strategy-research-boundary-reject-backtesting-v1", reason)


def reject_strategy_research_recommendation_boundary_violation(
    reason: str = "strategy research recommendation boundary violation",
) -> StrategyResearchBoundaryInvariantResult:
    return _blocked_result("strategy-research-boundary-reject-recommendation-v1", reason)


def reject_strategy_research_execution_boundary_violation(
    reason: str = "strategy research execution boundary violation",
) -> StrategyResearchBoundaryInvariantResult:
    return _blocked_result("strategy-research-boundary-reject-execution-v1", reason)


def reject_strategy_research_broker_control_boundary_violation(
    reason: str = "strategy research broker control boundary violation",
) -> StrategyResearchBoundaryInvariantResult:
    return _blocked_result("strategy-research-boundary-reject-broker-control-v1", reason)


def reject_strategy_research_readiness_to_trade_boundary_violation(
    reason: str = "strategy research readiness-to-trade boundary violation",
) -> StrategyResearchBoundaryInvariantResult:
    return _blocked_result("strategy-research-boundary-reject-readiness-to-trade-v1", reason)
