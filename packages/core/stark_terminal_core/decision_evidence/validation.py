from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_evidence.items import (
    DecisionEvidenceItemKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_evidence_notes,
)


class DecisionEvidenceValidationRequirement(BaseModel):
    requirement_id: str
    item_kind: DecisionEvidenceItemKind
    description: str
    required: bool = True
    source_reference_required: bool = True
    data_quality_required: bool = True
    human_review_required: bool = True
    blocks_decision_object_generation: bool = True
    schema_version: str = "v1"

    @field_validator("requirement_id", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence validation requirement text fields")

    @model_validator(mode="after")
    def requirement_must_block_generation(self) -> DecisionEvidenceValidationRequirement:
        if self.item_kind == DecisionEvidenceItemKind.UNKNOWN:
            raise ValueError("UNKNOWN decision evidence item kind is not allowed")
        if not self.source_reference_required:
            raise ValueError("source reference checks are required for decision evidence in Prompt 38")
        if not self.data_quality_required:
            raise ValueError("data quality checks are required for decision evidence in Prompt 38")
        if not self.human_review_required:
            raise ValueError("human review checks are required for decision evidence in Prompt 38")
        if not self.blocks_decision_object_generation:
            raise ValueError("validation checks must block DecisionObject generation in Prompt 38")
        return self


class DecisionEvidenceValidationChecklist(BaseModel):
    checklist_id: str
    requirements: list[DecisionEvidenceValidationRequirement]
    complete: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("checklist_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence validation checklist text fields")

    @field_validator("requirements")
    @classmethod
    def requirements_must_be_present(
        cls,
        value: list[DecisionEvidenceValidationRequirement],
    ) -> list[DecisionEvidenceValidationRequirement]:
        if not value:
            raise ValueError("decision evidence validation requirements cannot be empty")
        return value

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_evidence_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def checklist_must_not_enable_outputs(self) -> DecisionEvidenceValidationChecklist:
        if self.recommendations_allowed:
            raise ValueError("decision evidence validation cannot allow recommendations in Prompt 38")
        if self.action_generation_allowed:
            raise ValueError("decision evidence validation cannot allow action generation in Prompt 38")
        if self.confidence_scoring_allowed:
            raise ValueError("decision evidence validation cannot allow confidence scoring in Prompt 38")
        if self.decision_object_generation_allowed:
            raise ValueError("decision evidence validation cannot allow DecisionObject generation in Prompt 38")
        if self.execution_allowed:
            raise ValueError("decision evidence validation cannot allow execution in Prompt 38")
        if self.complete and self.blockers:
            raise ValueError("complete decision evidence validation checklist cannot have blockers")
        return self


def default_decision_evidence_validation_requirements() -> list[DecisionEvidenceValidationRequirement]:
    return [
        DecisionEvidenceValidationRequirement(
            requirement_id=f"decision-evidence-validation-{kind.value.lower().replace('_', '-')}",
            item_kind=kind,
            description=f"Validate source reference, data quality, and human review for {kind.value}.",
        )
        for kind in DecisionEvidenceItemKind
        if kind != DecisionEvidenceItemKind.UNKNOWN
    ]


def build_decision_evidence_validation_checklist(
    requirements: list[DecisionEvidenceValidationRequirement] | None = None,
    completed_requirement_ids: set[str] | None = None,
    warnings: list[str] | None = None,
) -> DecisionEvidenceValidationChecklist:
    resolved_requirements = requirements or default_decision_evidence_validation_requirements()
    completed = completed_requirement_ids or set()
    blockers = [
        f"missing required decision evidence validation: {requirement.requirement_id}"
        for requirement in resolved_requirements
        if requirement.required and requirement.requirement_id not in completed
    ]
    return DecisionEvidenceValidationChecklist(
        checklist_id="decision-evidence-validation-checklist-v1",
        requirements=resolved_requirements,
        complete=not blockers,
        blockers=blockers,
        warnings=warnings or [],
    )


def evaluate_decision_evidence_validation_checklist(
    checklist: DecisionEvidenceValidationChecklist,
) -> DecisionEvidenceValidationChecklist:
    if checklist.complete:
        return checklist
    blockers = checklist.blockers or ["required decision evidence validation remains incomplete"]
    return checklist.model_copy(update={"blockers": sanitize_decision_evidence_notes(blockers), "complete": False})

