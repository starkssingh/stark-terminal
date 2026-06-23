from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_evidence.bundle import DecisionObjectEvidenceBundleContract
from stark_terminal_core.decision_evidence.human_review import DecisionEvidenceHumanReviewAttachmentSet
from stark_terminal_core.decision_evidence.items import (
    DecisionEvidenceStage,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_evidence_notes,
)
from stark_terminal_core.decision_evidence.provenance import DecisionEvidenceProvenanceMap
from stark_terminal_core.decision_evidence.safety import DecisionEvidenceSafetyResult
from stark_terminal_core.decision_evidence.validation import DecisionEvidenceValidationChecklist


class DecisionEvidenceBundleReadinessReport(BaseModel):
    report_id: str
    bundle_id: str
    planning_stage: DecisionEvidenceStage
    evidence_item_count: int = Field(ge=0)
    provenance_complete: bool
    validation_checklist_complete: bool
    human_review_attachments_complete: bool
    safety_decision: str
    ready_for_bundle_validation: bool = False
    ready_for_decision_object_generation: bool = False
    ready_for_recommendations: bool = False
    ready_for_action_generation: bool = False
    ready_for_confidence_scoring: bool = False
    ready_for_execution: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    generated_at: datetime = Field(default_factory=_utc_now)

    @field_validator("report_id", "bundle_id", "safety_decision", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence readiness report text fields")

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_evidence_notes(value)

    @field_validator("generated_at")
    @classmethod
    def generated_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def report_must_not_enable_generation(self) -> DecisionEvidenceBundleReadinessReport:
        if self.ready_for_decision_object_generation:
            raise ValueError("DecisionObject generation is forbidden in Prompt 38")
        if self.ready_for_recommendations:
            raise ValueError("recommendations are forbidden in Prompt 38")
        if self.ready_for_action_generation:
            raise ValueError("action generation is forbidden in Prompt 38")
        if self.ready_for_confidence_scoring:
            raise ValueError("confidence scoring is forbidden in Prompt 38")
        if self.ready_for_execution:
            raise ValueError("execution is forbidden in Prompt 38")
        if self.ready_for_bundle_validation and self.blockers:
            raise ValueError("bundle validation readiness requires no blockers")
        return self


def build_decision_evidence_bundle_readiness_report(
    bundle: DecisionObjectEvidenceBundleContract,
    provenance_map: DecisionEvidenceProvenanceMap,
    validation_checklist: DecisionEvidenceValidationChecklist,
    human_review_attachment_set: DecisionEvidenceHumanReviewAttachmentSet,
    safety_result: DecisionEvidenceSafetyResult,
) -> DecisionEvidenceBundleReadinessReport:
    blockers = [
        *provenance_map.blockers,
        *validation_checklist.blockers,
        *human_review_attachment_set.blockers,
    ]
    warnings = [
        *provenance_map.warnings,
        *validation_checklist.warnings,
        *human_review_attachment_set.warnings,
    ]
    if safety_result.decision == "blocked":
        blockers.extend(safety_result.reasons)
    else:
        warnings.extend(safety_result.reasons)
    ready_for_bundle_validation = (
        provenance_map.complete
        and validation_checklist.complete
        and human_review_attachment_set.complete
        and safety_result.decision != "blocked"
        and not blockers
    )
    return DecisionEvidenceBundleReadinessReport(
        report_id="decision-evidence-bundle-readiness-report-v1",
        bundle_id=bundle.bundle_id,
        planning_stage=bundle.planning_stage,
        evidence_item_count=len(bundle.evidence_items),
        provenance_complete=provenance_map.complete,
        validation_checklist_complete=validation_checklist.complete,
        human_review_attachments_complete=human_review_attachment_set.complete,
        safety_decision=safety_result.decision,
        ready_for_bundle_validation=ready_for_bundle_validation,
        ready_for_decision_object_generation=False,
        ready_for_recommendations=False,
        ready_for_action_generation=False,
        ready_for_confidence_scoring=False,
        ready_for_execution=False,
        blockers=blockers,
        warnings=warnings,
    )


def decision_evidence_ready_for_bundle_validation(report: DecisionEvidenceBundleReadinessReport) -> bool:
    return report.ready_for_bundle_validation and not report.blockers


def decision_evidence_ready_for_decision_object_generation(report: DecisionEvidenceBundleReadinessReport) -> bool:
    return False


def decision_evidence_ready_for_recommendations(report: DecisionEvidenceBundleReadinessReport) -> bool:
    return False


def decision_evidence_ready_for_execution(report: DecisionEvidenceBundleReadinessReport) -> bool:
    return False

