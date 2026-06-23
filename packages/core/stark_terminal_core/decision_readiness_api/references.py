from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_readiness_api.requests import _non_empty_text, _utc_datetime, _utc_now


class DecisionReadinessEvidenceReference(BaseModel):
    reference_id: str
    evidence_bundle_id: str | None = None
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
        return _non_empty_text(value, "decision readiness evidence reference text fields")

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
    def evidence_reference_must_remain_placeholder(self) -> DecisionReadinessEvidenceReference:
        if not self.required:
            raise ValueError("decision readiness evidence references are required in Prompt 42")
        if self.complete:
            raise ValueError("evidence reference completeness is forbidden in Prompt 42")
        if self.validation_passed:
            raise ValueError("evidence reference validation cannot pass in Prompt 42")
        if self.human_review_attached:
            raise ValueError("human-review attachment cannot be treated as attached in Prompt 42")
        if self.active_decision_object_ready:
            raise ValueError("active DecisionObject readiness is forbidden in Prompt 42")
        return self


class DecisionReadinessSafetyReference(BaseModel):
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
        return _non_empty_text(value, "decision readiness safety reference text fields")

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
    def safety_reference_must_fail_closed(self) -> DecisionReadinessSafetyReference:
        if not self.required:
            raise ValueError("decision readiness safety references are required in Prompt 42")
        if self.passed:
            raise ValueError("decision safety reference cannot pass in Prompt 42")
        if self.approval_granted:
            raise ValueError("approval cannot be granted in Prompt 42")
        if self.override_granted:
            raise ValueError("override cannot be granted in Prompt 42")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 42")
        return self


class DecisionReadinessHumanReviewReference(BaseModel):
    reference_id: str
    gate_set_id: str | None = None
    required: bool = True
    complete: bool = False
    approval_granted: bool = False
    bypass_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision readiness human-review reference text fields")

    @field_validator("gate_set_id")
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
    def human_review_reference_must_not_grant_approval(self) -> DecisionReadinessHumanReviewReference:
        if not self.required:
            raise ValueError("human-review references are required in Prompt 42")
        if self.approval_granted:
            raise ValueError("approval cannot be granted in Prompt 42")
        if self.bypass_allowed:
            raise ValueError("human-review bypass is forbidden in Prompt 42")
        return self


class DecisionReadinessBlockedOutputReference(BaseModel):
    reference_id: str
    policy_id: str | None = None
    required: bool = True
    policy_active: bool = True
    bypass_allowed: bool = False
    recommendations_blocked: bool = True
    action_generation_blocked: bool = True
    confidence_scoring_blocked: bool = True
    decision_object_generation_blocked: bool = True
    execution_blocked: bool = True
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision readiness blocked-output reference text fields")

    @field_validator("policy_id")
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
    def blocked_output_reference_must_fail_closed(self) -> DecisionReadinessBlockedOutputReference:
        if not self.required:
            raise ValueError("blocked-output references are required in Prompt 42")
        if not self.policy_active:
            raise ValueError("blocked-output policy must remain active in Prompt 42")
        if self.bypass_allowed:
            raise ValueError("blocked-output bypass is forbidden in Prompt 42")
        blocked_flags = [
            self.recommendations_blocked,
            self.action_generation_blocked,
            self.confidence_scoring_blocked,
            self.decision_object_generation_blocked,
            self.execution_blocked,
        ]
        if not all(blocked_flags):
            raise ValueError("all dangerous outputs must remain blocked in Prompt 42")
        return self


def default_decision_readiness_evidence_reference() -> DecisionReadinessEvidenceReference:
    return DecisionReadinessEvidenceReference(reference_id="decision-readiness-evidence-reference-v1")


def default_decision_readiness_safety_reference() -> DecisionReadinessSafetyReference:
    return DecisionReadinessSafetyReference(reference_id="decision-readiness-safety-reference-v1")


def default_decision_readiness_human_review_reference() -> DecisionReadinessHumanReviewReference:
    return DecisionReadinessHumanReviewReference(reference_id="decision-readiness-human-review-reference-v1")


def default_decision_readiness_blocked_output_reference() -> DecisionReadinessBlockedOutputReference:
    return DecisionReadinessBlockedOutputReference(reference_id="decision-readiness-blocked-output-reference-v1")
