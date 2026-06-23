from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_api.requests import _non_empty_text, _utc_datetime, _utc_now


class DecisionEvidenceBundleReferencePlaceholder(BaseModel):
    reference_id: str
    bundle_id: str | None = None
    required: bool = True
    complete: bool = False
    validation_passed: bool = False
    human_review_attached: bool = False
    active_decision_object_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence bundle reference text fields")

    @field_validator("bundle_id")
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
    def evidence_reference_must_remain_placeholder(self) -> DecisionEvidenceBundleReferencePlaceholder:
        if not self.required:
            raise ValueError("evidence bundle references are required in Prompt 40")
        if self.complete:
            raise ValueError("evidence bundle reference completeness is forbidden in Prompt 40")
        if self.validation_passed:
            raise ValueError("evidence bundle reference validation cannot pass in Prompt 40")
        if self.human_review_attached:
            raise ValueError("human review attachment cannot be treated as attached in Prompt 40")
        if self.active_decision_object_ready:
            raise ValueError("active DecisionObject readiness is forbidden in Prompt 40")
        return self


class DecisionSafetyReferencePlaceholder(BaseModel):
    reference_id: str
    safety_report_id: str | None = None
    required: bool = True
    passed: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    execution_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision safety reference text fields")

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
    def safety_reference_must_fail_closed(self) -> DecisionSafetyReferencePlaceholder:
        if not self.required:
            raise ValueError("decision safety references are required in Prompt 40")
        if self.passed:
            raise ValueError("decision safety reference cannot pass in Prompt 40")
        if self.approval_granted:
            raise ValueError("approval cannot be granted in Prompt 40")
        if self.override_granted:
            raise ValueError("override cannot be granted in Prompt 40")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 40")
        return self


def default_evidence_bundle_reference_placeholder() -> DecisionEvidenceBundleReferencePlaceholder:
    return DecisionEvidenceBundleReferencePlaceholder(
        reference_id="decision-evidence-bundle-reference-placeholder-v1",
    )


def default_decision_safety_reference_placeholder() -> DecisionSafetyReferencePlaceholder:
    return DecisionSafetyReferencePlaceholder(
        reference_id="decision-safety-reference-placeholder-v1",
    )

