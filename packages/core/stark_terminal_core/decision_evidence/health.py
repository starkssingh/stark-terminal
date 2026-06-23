from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.decision_evidence.bundle import default_decision_object_evidence_bundle_contract
from stark_terminal_core.decision_evidence.items import default_decision_evidence_item_contracts


class DecisionEvidenceHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    planning_stage: str
    real_data_allowed: bool
    recommendations_allowed: bool
    action_generation_allowed: bool
    confidence_scoring_allowed: bool
    decision_object_generation_allowed: bool
    execution_allowed: bool = False
    source_reference_required: bool
    validation_checklist_required: bool
    human_review_attachment_required: bool
    default_evidence_item_count: int
    status: str
    error: str | None = None


def check_decision_evidence_health(settings: Settings | None = None) -> DecisionEvidenceHealthStatus:
    resolved = settings or get_settings()
    bundle = default_decision_object_evidence_bundle_contract()
    items = default_decision_evidence_item_contracts()
    unsafe_flags = (
        resolved.decision_evidence_allow_real_data
        or resolved.decision_evidence_allow_recommendations
        or resolved.decision_evidence_allow_action_generation
        or resolved.decision_evidence_allow_confidence_scoring
        or resolved.decision_evidence_allow_decision_object_generation
        or resolved.decision_evidence_allow_execution
        or resolved.execution_apis_enabled
    )
    has_required_configuration = (
        bool(resolved.decision_evidence_schema_version.strip())
        and resolved.decision_evidence_planning_stage == "contracts_only"
        and resolved.decision_evidence_require_source_reference
        and resolved.decision_evidence_require_validation_checklist
        and resolved.decision_evidence_require_human_review_attachment
        and bool(bundle.evidence_items)
        and bool(items)
    )
    status = "healthy" if resolved.decision_evidence_enabled and not unsafe_flags and has_required_configuration else "blocked"
    error = None if status == "healthy" else "Decision evidence safety flags are not fail-closed"
    return DecisionEvidenceHealthStatus(
        enabled=resolved.decision_evidence_enabled,
        schema_version=resolved.decision_evidence_schema_version,
        planning_stage=resolved.decision_evidence_planning_stage,
        real_data_allowed=resolved.decision_evidence_allow_real_data,
        recommendations_allowed=resolved.decision_evidence_allow_recommendations,
        action_generation_allowed=resolved.decision_evidence_allow_action_generation,
        confidence_scoring_allowed=resolved.decision_evidence_allow_confidence_scoring,
        decision_object_generation_allowed=resolved.decision_evidence_allow_decision_object_generation,
        execution_allowed=False,
        source_reference_required=resolved.decision_evidence_require_source_reference,
        validation_checklist_required=resolved.decision_evidence_require_validation_checklist,
        human_review_attachment_required=resolved.decision_evidence_require_human_review_attachment,
        default_evidence_item_count=len(items),
        status=status,
        error=error,
    )

