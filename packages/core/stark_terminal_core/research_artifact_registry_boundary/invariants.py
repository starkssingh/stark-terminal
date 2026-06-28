from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry_boundary.endpoints import (
    ResearchArtifactEndpointBoundaryPolicy,
    default_research_artifact_endpoint_boundary_policies,
    evaluate_research_artifact_endpoint_boundary_policies,
)
from stark_terminal_core.research_artifact_registry_boundary.forbidden import (
    ResearchArtifactBoundarySafetyLabel,
    ResearchArtifactForbiddenBehaviorRegistry,
    _non_empty_text,
    _utc_datetime,
    default_research_artifact_forbidden_behavior_registry,
)
from stark_terminal_core.research_artifact_registry_boundary.modules import (
    ResearchArtifactModuleBoundaryPolicy,
    default_research_artifact_module_boundary_policies,
    evaluate_research_artifact_module_boundary_policies,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ResearchArtifactBoundaryInvariantResult(BaseModel):
    result_id: str
    passed: bool
    checked_families: list[str]
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    active_ingestion_allowed: bool = False
    persistent_storage_allowed: bool = False
    file_uploads_allowed: bool = False
    file_downloads_allowed: bool = False
    file_previews_allowed: bool = False
    active_ui_allowed: bool = False
    frontend_components_allowed: bool = False
    desktop_components_allowed: bool = False
    paper_parsing_allowed: bool = False
    pdf_parsing_allowed: bool = False
    arxiv_ingestion_allowed: bool = False
    llm_analysis_allowed: bool = False
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
    safety_label: ResearchArtifactBoundarySafetyLabel = (
        ResearchArtifactBoundarySafetyLabel.BOUNDARY_HARDENING_ONLY
    )
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "research artifact boundary invariant result text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def invariant_result_must_fail_closed(self) -> ResearchArtifactBoundaryInvariantResult:
        if not self.checked_families:
            raise ValueError("research artifact boundary invariant result requires checked families")
        dangerous_flags = {
            "active ingestion": self.active_ingestion_allowed,
            "persistent storage": self.persistent_storage_allowed,
            "file uploads": self.file_uploads_allowed,
            "file downloads": self.file_downloads_allowed,
            "file previews": self.file_previews_allowed,
            "active UI": self.active_ui_allowed,
            "frontend components": self.frontend_components_allowed,
            "desktop components": self.desktop_components_allowed,
            "paper parsing": self.paper_parsing_allowed,
            "PDF parsing": self.pdf_parsing_allowed,
            "arXiv ingestion": self.arxiv_ingestion_allowed,
            "LLM analysis": self.llm_analysis_allowed,
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
            raise ValueError(f"research artifact boundary invariant cannot allow: {', '.join(enabled)}")
        if self.passed and self.blockers:
            raise ValueError("research artifact boundary invariant cannot pass with blockers")
        if self.safety_label == ResearchArtifactBoundarySafetyLabel.UNKNOWN:
            raise ValueError("UNKNOWN research artifact boundary safety label is not allowed")
        return self


def evaluate_research_artifact_boundary_invariants(
    endpoint_policies: list[ResearchArtifactEndpointBoundaryPolicy] | None = None,
    module_policies: list[ResearchArtifactModuleBoundaryPolicy] | None = None,
    registry: ResearchArtifactForbiddenBehaviorRegistry | None = None,
) -> ResearchArtifactBoundaryInvariantResult:
    resolved_endpoint_policies = endpoint_policies or default_research_artifact_endpoint_boundary_policies()
    resolved_module_policies = module_policies or default_research_artifact_module_boundary_policies()
    resolved_registry = registry or default_research_artifact_forbidden_behavior_registry()
    blockers = [
        *evaluate_research_artifact_endpoint_boundary_policies(resolved_endpoint_policies),
        *evaluate_research_artifact_module_boundary_policies(resolved_module_policies),
    ]
    if not resolved_registry.complete:
        blockers.append("research artifact forbidden behavior registry is incomplete")
    checked_families = [
        *[policy.endpoint_family for policy in resolved_endpoint_policies],
        *[policy.module_family for policy in resolved_module_policies],
        resolved_registry.registry_id,
    ]
    return ResearchArtifactBoundaryInvariantResult(
        result_id="research-artifact-boundary-invariant-result-v1",
        passed=not blockers,
        checked_families=checked_families,
        blockers=blockers,
        warnings=[],
    )


def _blocked_result(result_id: str, reason: str) -> ResearchArtifactBoundaryInvariantResult:
    return ResearchArtifactBoundaryInvariantResult(
        result_id=result_id,
        passed=False,
        checked_families=["research_artifact_registry_boundary"],
        blockers=[reason],
        safety_label=ResearchArtifactBoundarySafetyLabel.BLOCKED,
    )


def reject_research_artifact_ingestion_boundary_violation(
    reason: str = "research artifact ingestion boundary violation",
) -> ResearchArtifactBoundaryInvariantResult:
    return _blocked_result("research-artifact-boundary-reject-ingestion-v1", reason)


def reject_research_artifact_storage_boundary_violation(
    reason: str = "research artifact storage boundary violation",
) -> ResearchArtifactBoundaryInvariantResult:
    return _blocked_result("research-artifact-boundary-reject-storage-v1", reason)


def reject_research_artifact_upload_download_boundary_violation(
    reason: str = "research artifact upload/download boundary violation",
) -> ResearchArtifactBoundaryInvariantResult:
    return _blocked_result("research-artifact-boundary-reject-upload-download-v1", reason)


def reject_research_artifact_active_ui_boundary_violation(
    reason: str = "research artifact active UI boundary violation",
) -> ResearchArtifactBoundaryInvariantResult:
    return _blocked_result("research-artifact-boundary-reject-active-ui-v1", reason)


def reject_research_artifact_paper_parsing_boundary_violation(
    reason: str = "research artifact paper parsing boundary violation",
) -> ResearchArtifactBoundaryInvariantResult:
    return _blocked_result("research-artifact-boundary-reject-paper-parsing-v1", reason)


def reject_research_artifact_strategy_generation_boundary_violation(
    reason: str = "research artifact strategy generation boundary violation",
) -> ResearchArtifactBoundaryInvariantResult:
    return _blocked_result("research-artifact-boundary-reject-strategy-generation-v1", reason)


def reject_research_artifact_backtesting_boundary_violation(
    reason: str = "research artifact backtesting boundary violation",
) -> ResearchArtifactBoundaryInvariantResult:
    return _blocked_result("research-artifact-boundary-reject-backtesting-v1", reason)


def reject_research_artifact_recommendation_boundary_violation(
    reason: str = "research artifact recommendation boundary violation",
) -> ResearchArtifactBoundaryInvariantResult:
    return _blocked_result("research-artifact-boundary-reject-recommendation-v1", reason)


def reject_research_artifact_execution_boundary_violation(
    reason: str = "research artifact execution boundary violation",
) -> ResearchArtifactBoundaryInvariantResult:
    return _blocked_result("research-artifact-boundary-reject-execution-v1", reason)


def reject_research_artifact_broker_control_boundary_violation(
    reason: str = "research artifact broker control boundary violation",
) -> ResearchArtifactBoundaryInvariantResult:
    return _blocked_result("research-artifact-boundary-reject-broker-control-v1", reason)


def reject_research_artifact_readiness_to_trade_boundary_violation(
    reason: str = "research artifact readiness-to-trade boundary violation",
) -> ResearchArtifactBoundaryInvariantResult:
    return _blocked_result("research-artifact-boundary-reject-readiness-to-trade-v1", reason)
