from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_display.contracts import _non_empty_text, _utc_datetime, _utc_now


class DecisionDisplayEvidenceReference(BaseModel):
    reference_id: str
    evidence_bundle_id: str | None = None
    required: bool = True
    complete: bool = False
    validation_passed: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision display evidence reference text fields")

    @field_validator("evidence_bundle_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def evidence_reference_must_remain_placeholder(self) -> DecisionDisplayEvidenceReference:
        if not self.required:
            raise ValueError("decision display evidence references are required in Prompt 43")
        if self.complete:
            raise ValueError("display evidence reference completeness is forbidden in Prompt 43")
        if self.validation_passed:
            raise ValueError("display evidence validation cannot pass in Prompt 43")
        if self.display_ready:
            raise ValueError("display readiness is forbidden in Prompt 43")
        return self


class DecisionDisplaySafetyReference(BaseModel):
    reference_id: str
    safety_report_id: str | None = None
    required: bool = True
    passed: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    execution_allowed: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision display safety reference text fields")

    @field_validator("safety_report_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def safety_reference_must_fail_closed(self) -> DecisionDisplaySafetyReference:
        if not self.required:
            raise ValueError("decision display safety references are required in Prompt 43")
        if self.passed:
            raise ValueError("display safety reference cannot pass in Prompt 43")
        if self.approval_granted:
            raise ValueError("approval cannot be granted in Prompt 43")
        if self.override_granted:
            raise ValueError("override cannot be granted in Prompt 43")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 43")
        if self.display_ready:
            raise ValueError("display readiness is forbidden in Prompt 43")
        return self


def default_decision_display_evidence_reference() -> DecisionDisplayEvidenceReference:
    return DecisionDisplayEvidenceReference(reference_id="decision-display-evidence-reference-v1")


def default_decision_display_safety_reference() -> DecisionDisplaySafetyReference:
    return DecisionDisplaySafetyReference(reference_id="decision-display-safety-reference-v1")

