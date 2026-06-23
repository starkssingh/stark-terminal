from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_desk.planning import (
    RetailEvidenceKind,
    _non_empty_text,
    sanitize_decision_notes,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class RetailDecisionEvidenceRequirement(BaseModel):
    requirement_id: str
    evidence_kind: RetailEvidenceKind
    description: str
    required: bool = True
    source_reference_required: bool = True
    validation_required: bool = True
    human_review_required: bool = True
    allowed_data_scope: str = "synthetic-local-until-approved"
    schema_version: str = "v1"

    @field_validator("requirement_id", "description", "allowed_data_scope", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail decision evidence requirement text fields")

    @model_validator(mode="after")
    def requirement_must_be_safe(self) -> RetailDecisionEvidenceRequirement:
        if self.evidence_kind == RetailEvidenceKind.UNKNOWN:
            raise ValueError("UNKNOWN retail evidence kind is not allowed")
        if not self.human_review_required:
            raise ValueError("human review is required for retail decision evidence in Prompt 36")
        return self


class RetailDecisionEvidenceChecklist(BaseModel):
    checklist_id: str
    requirements: list[RetailDecisionEvidenceRequirement]
    complete: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    decision_object_generation_allowed: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("checklist_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail decision evidence checklist text fields")

    @field_validator("requirements")
    @classmethod
    def requirements_must_be_present(
        cls,
        value: list[RetailDecisionEvidenceRequirement],
    ) -> list[RetailDecisionEvidenceRequirement]:
        if not value:
            raise ValueError("retail decision evidence requirements cannot be empty")
        return value

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def checklist_must_not_enable_outputs(self) -> RetailDecisionEvidenceChecklist:
        if self.recommendations_allowed:
            raise ValueError("retail decision evidence cannot allow recommendations in Prompt 36")
        if self.action_generation_allowed:
            raise ValueError("retail decision evidence cannot allow action generation in Prompt 36")
        if self.decision_object_generation_allowed:
            raise ValueError("retail decision evidence cannot allow DecisionObject generation in Prompt 36")
        if self.complete and self.blockers:
            raise ValueError("complete retail decision evidence checklist cannot have blockers")
        return self


def default_retail_decision_evidence_requirements() -> list[RetailDecisionEvidenceRequirement]:
    descriptions = {
        RetailEvidenceKind.INSTRUMENT_CONTEXT: "Validated instrument context and symbol metadata with source references.",
        RetailEvidenceKind.DATA_QUALITY: "Data quality report and validation status for any future decision context.",
        RetailEvidenceKind.RETURNS: "Descriptive returns evidence only; not a recommendation input in Prompt 36.",
        RetailEvidenceKind.VOLATILITY: "Descriptive volatility evidence only; not a recommendation input in Prompt 36.",
        RetailEvidenceKind.DRAWDOWN: "Descriptive drawdown evidence only; not a recommendation input in Prompt 36.",
        RetailEvidenceKind.CORRELATION_BETA: "Descriptive relationship metrics evidence only; not a recommendation input in Prompt 36.",
        RetailEvidenceKind.TIME_SERIES_DIAGNOSTICS: "Timestamp quality diagnostics evidence only.",
        RetailEvidenceKind.REGIME_CONTEXT: "Planning-only regime context; no regime classification exists.",
        RetailEvidenceKind.FEATURE_CONTEXT: "Feature context contracts only; no feature computation exists.",
        RetailEvidenceKind.RISK_CONTEXT: "Future risk context requirement before any retail decision surface.",
        RetailEvidenceKind.HUMAN_REVIEW: "Human review requirement before any future Decision Desk output.",
    }
    return [
        RetailDecisionEvidenceRequirement(
            requirement_id=f"retail-decision-evidence-{kind.value.lower().replace('_', '-')}",
            evidence_kind=kind,
            description=description,
        )
        for kind, description in descriptions.items()
    ]


def build_retail_decision_evidence_checklist(
    requirements: list[RetailDecisionEvidenceRequirement] | None = None,
    completed_requirement_ids: set[str] | None = None,
    warnings: list[str] | None = None,
) -> RetailDecisionEvidenceChecklist:
    resolved_requirements = requirements or default_retail_decision_evidence_requirements()
    completed = completed_requirement_ids or set()
    blockers = [
        f"missing required retail decision evidence: {requirement.requirement_id}"
        for requirement in resolved_requirements
        if requirement.required and requirement.requirement_id not in completed
    ]
    return RetailDecisionEvidenceChecklist(
        checklist_id="retail-decision-evidence-checklist-v1",
        requirements=resolved_requirements,
        complete=not blockers,
        blockers=blockers,
        warnings=warnings or [],
    )


def evaluate_retail_decision_evidence_checklist(
    checklist: RetailDecisionEvidenceChecklist,
) -> RetailDecisionEvidenceChecklist:
    if checklist.complete:
        return checklist
    blockers = checklist.blockers or ["required retail decision evidence remains incomplete"]
    return checklist.model_copy(update={"blockers": sanitize_decision_notes(blockers), "complete": False})
