from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.regime.contracts import RegimeEvidenceKind


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _non_empty_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


class RegimeEvidenceRequirement(BaseModel):
    requirement_id: str
    evidence_kind: RegimeEvidenceKind
    description: str
    required: bool = True
    source_reference_required: bool = True
    validation_required: bool = True
    minimum_observations: int | None = None
    allowed_data_scope: str = "synthetic-local-until-approved"
    schema_version: str = "v1"

    @field_validator("requirement_id", "description", "allowed_data_scope", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime evidence requirement text fields")

    @field_validator("minimum_observations")
    @classmethod
    def minimum_observations_must_be_positive(cls, value: int | None) -> int | None:
        if value is not None and value <= 0:
            raise ValueError("minimum_observations must be positive when provided")
        return value

    @model_validator(mode="after")
    def evidence_kind_must_be_known(self) -> RegimeEvidenceRequirement:
        if self.evidence_kind == RegimeEvidenceKind.UNKNOWN:
            raise ValueError("UNKNOWN evidence kind is not allowed")
        return self


class RegimeEvidenceChecklist(BaseModel):
    checklist_id: str
    requirements: list[RegimeEvidenceRequirement]
    complete: bool = False
    classification_allowed: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("checklist_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime evidence checklist text fields")

    @field_validator("requirements")
    @classmethod
    def requirements_must_be_present(
        cls,
        value: list[RegimeEvidenceRequirement],
    ) -> list[RegimeEvidenceRequirement]:
        if not value:
            raise ValueError("regime evidence checklist requirements cannot be empty")
        return value

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def checklist_must_remain_planning_only(self) -> RegimeEvidenceChecklist:
        if self.classification_allowed:
            raise ValueError("regime evidence checklist cannot allow classification in Prompt 33")
        if self.complete and self.blockers:
            raise ValueError("complete regime evidence checklist cannot have blockers")
        return self


def default_regime_evidence_requirements() -> list[RegimeEvidenceRequirement]:
    return [
        RegimeEvidenceRequirement(
            requirement_id="returns-evidence",
            evidence_kind=RegimeEvidenceKind.RETURNS,
            description="Validated descriptive returns evidence with source references.",
            minimum_observations=2,
        ),
        RegimeEvidenceRequirement(
            requirement_id="volatility-evidence",
            evidence_kind=RegimeEvidenceKind.VOLATILITY,
            description="Validated descriptive volatility evidence with explicit convention.",
            minimum_observations=2,
        ),
        RegimeEvidenceRequirement(
            requirement_id="drawdown-evidence",
            evidence_kind=RegimeEvidenceKind.DRAWDOWN,
            description="Validated descriptive drawdown evidence with positive value inputs.",
            minimum_observations=1,
        ),
        RegimeEvidenceRequirement(
            requirement_id="correlation-evidence",
            evidence_kind=RegimeEvidenceKind.CORRELATION,
            description="Validated descriptive correlation evidence from equal-length paired vectors.",
            minimum_observations=2,
        ),
        RegimeEvidenceRequirement(
            requirement_id="beta-evidence",
            evidence_kind=RegimeEvidenceKind.BETA,
            description="Validated descriptive beta evidence from equal-length paired return vectors.",
            minimum_observations=2,
        ),
        RegimeEvidenceRequirement(
            requirement_id="time-series-diagnostics-evidence",
            evidence_kind=RegimeEvidenceKind.TIME_SERIES_DIAGNOSTICS,
            description="Timestamp quality evidence covering ordering, duplicates, gaps, and spacing.",
            minimum_observations=1,
        ),
        RegimeEvidenceRequirement(
            requirement_id="volume-evidence",
            evidence_kind=RegimeEvidenceKind.VOLUME,
            description="Future validated volume context; not computed in Prompt 33.",
        ),
        RegimeEvidenceRequirement(
            requirement_id="liquidity-evidence",
            evidence_kind=RegimeEvidenceKind.LIQUIDITY,
            description="Future validated liquidity context; not computed in Prompt 33.",
        ),
        RegimeEvidenceRequirement(
            requirement_id="options-context-evidence",
            evidence_kind=RegimeEvidenceKind.OPTIONS_CONTEXT,
            description="Future options context requirement; not computed in Prompt 33.",
        ),
        RegimeEvidenceRequirement(
            requirement_id="macro-context-evidence",
            evidence_kind=RegimeEvidenceKind.MACRO_CONTEXT,
            description="Future macro context requirement; not computed in Prompt 33.",
        ),
    ]


def build_regime_evidence_checklist(
    requirements: list[RegimeEvidenceRequirement] | None = None,
    completed_requirement_ids: set[str] | None = None,
    warnings: list[str] | None = None,
) -> RegimeEvidenceChecklist:
    resolved_requirements = requirements or default_regime_evidence_requirements()
    completed = completed_requirement_ids or set()
    blockers = [
        f"missing required evidence: {requirement.requirement_id}"
        for requirement in resolved_requirements
        if requirement.required and requirement.requirement_id not in completed
    ]
    return RegimeEvidenceChecklist(
        checklist_id="regime-evidence-checklist-v1",
        requirements=resolved_requirements,
        complete=not blockers,
        blockers=blockers,
        warnings=warnings or [],
    )


def evaluate_evidence_readiness(checklist: RegimeEvidenceChecklist) -> RegimeEvidenceChecklist:
    if checklist.complete:
        return checklist
    blockers = checklist.blockers or ["required regime evidence remains incomplete"]
    return checklist.model_copy(update={"blockers": sanitize_analytics_notes(blockers), "complete": False})
