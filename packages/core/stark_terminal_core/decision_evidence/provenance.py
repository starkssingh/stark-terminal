from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_evidence.items import (
    DecisionEvidenceItemContract,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    default_decision_evidence_item_contracts,
    sanitize_decision_evidence_notes,
)


class DecisionEvidenceSourceReference(BaseModel):
    source_id: str
    source_type: str
    source_data_reference: str
    synthetic_or_local_only_until_approved: bool = True
    real_market_data: bool = False
    dataset_manifest_id: str | None = None
    validation_report_id: str | None = None
    analytics_family: str | None = None
    provider_name: str | None = None
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("source_id", "source_type", "source_data_reference", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence source reference text fields")

    @field_validator("dataset_manifest_id", "validation_report_id", "analytics_family", "provider_name")
    @classmethod
    def optional_text_fields_must_be_sanitized(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_evidence_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def source_must_remain_local_or_synthetic(self) -> DecisionEvidenceSourceReference:
        if self.real_market_data:
            raise ValueError("real market data is forbidden for decision evidence in Prompt 38")
        return self


class DecisionEvidenceProvenanceRequirement(BaseModel):
    provenance_id: str
    item_id: str
    required_source_types: list[str]
    source_reference_required: bool = True
    validation_report_required: bool = True
    dataset_manifest_required: bool = False
    human_review_required: bool = True
    schema_version: str = "v1"

    @field_validator("provenance_id", "item_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence provenance requirement text fields")

    @field_validator("required_source_types")
    @classmethod
    def source_types_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_decision_evidence_notes(value)
        if not sanitized:
            raise ValueError("decision evidence required_source_types cannot be empty")
        return sanitized

    @model_validator(mode="after")
    def provenance_requirement_must_be_strict(self) -> DecisionEvidenceProvenanceRequirement:
        if not self.source_reference_required:
            raise ValueError("source references are required for decision evidence in Prompt 38")
        if not self.validation_report_required:
            raise ValueError("validation reports are required for decision evidence in Prompt 38")
        if not self.human_review_required:
            raise ValueError("human review is required for decision evidence in Prompt 38")
        return self


class DecisionEvidenceProvenanceMap(BaseModel):
    map_id: str
    requirements: list[DecisionEvidenceProvenanceRequirement]
    complete: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("map_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence provenance map text fields")

    @field_validator("requirements")
    @classmethod
    def requirements_must_be_present(
        cls,
        value: list[DecisionEvidenceProvenanceRequirement],
    ) -> list[DecisionEvidenceProvenanceRequirement]:
        if not value:
            raise ValueError("decision evidence provenance requirements cannot be empty")
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
    def complete_map_cannot_have_blockers(self) -> DecisionEvidenceProvenanceMap:
        if self.complete and self.blockers:
            raise ValueError("complete decision evidence provenance map cannot have blockers")
        return self


def default_decision_evidence_provenance_requirements(
    items: list[DecisionEvidenceItemContract] | None = None,
) -> list[DecisionEvidenceProvenanceRequirement]:
    resolved_items = items or default_decision_evidence_item_contracts()
    requirements: list[DecisionEvidenceProvenanceRequirement] = []
    for item in resolved_items:
        source_types = ["source_reference", "validation_report"]
        if item.kind.value in {"DATA_QUALITY", "REGIME_FEATURE_CONTEXT"}:
            source_types.append("dataset_manifest")
        requirements.append(
            DecisionEvidenceProvenanceRequirement(
                provenance_id=f"decision-evidence-provenance-{item.item_id}",
                item_id=item.item_id,
                required_source_types=source_types,
                dataset_manifest_required="dataset_manifest" in source_types,
            )
        )
    return requirements


def build_decision_evidence_provenance_map(
    requirements: list[DecisionEvidenceProvenanceRequirement] | None = None,
    satisfied_provenance_ids: set[str] | None = None,
    warnings: list[str] | None = None,
) -> DecisionEvidenceProvenanceMap:
    resolved_requirements = requirements or default_decision_evidence_provenance_requirements()
    satisfied = satisfied_provenance_ids or set()
    blockers = [
        f"missing required decision evidence provenance: {requirement.provenance_id}"
        for requirement in resolved_requirements
        if requirement.provenance_id not in satisfied
    ]
    return DecisionEvidenceProvenanceMap(
        map_id="decision-evidence-provenance-map-v1",
        requirements=resolved_requirements,
        complete=not blockers,
        blockers=blockers,
        warnings=warnings or [],
    )


def evaluate_decision_evidence_provenance_map(
    provenance_map: DecisionEvidenceProvenanceMap,
) -> DecisionEvidenceProvenanceMap:
    if provenance_map.complete:
        return provenance_map
    blockers = provenance_map.blockers or ["required decision evidence provenance remains incomplete"]
    return provenance_map.model_copy(update={"blockers": sanitize_decision_evidence_notes(blockers), "complete": False})

