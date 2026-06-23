from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.regime.contracts import RegimeAnalyticsPlan


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


class RegimeSafetyPolicy(BaseModel):
    policy_id: str
    name: str
    allow_classification: bool = False
    allow_real_data: bool = False
    allow_trade_signals: bool = False
    allow_recommendations: bool = False
    allow_decision_objects: bool = False
    allow_execution: bool = False
    require_evidence: bool = True
    require_human_review: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime safety policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)

    @model_validator(mode="after")
    def policy_must_fail_closed(self) -> RegimeSafetyPolicy:
        if self.allow_classification:
            raise ValueError("regime classification is forbidden in Prompt 33")
        if self.allow_real_data:
            raise ValueError("regime real data usage is forbidden in Prompt 33")
        if self.allow_trade_signals:
            raise ValueError("regime trade signals are forbidden in Prompt 33")
        if self.allow_recommendations:
            raise ValueError("regime recommendations are forbidden in Prompt 33")
        if self.allow_decision_objects:
            raise ValueError("regime DecisionObject generation is forbidden in Prompt 33")
        if self.allow_execution:
            raise ValueError("regime execution is forbidden in Prompt 33")
        if not self.require_evidence:
            raise ValueError("regime evidence is required in Prompt 33")
        if not self.require_human_review:
            raise ValueError("regime human review is required in Prompt 33")
        return self


class RegimeSafetyResult(BaseModel):
    decision: str
    reasons: list[str]
    policy_id: str
    evaluated_at: datetime = Field(default_factory=_utc_now)
    schema_version: str = "v1"

    @field_validator("decision", "policy_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime safety result text fields")

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_analytics_notes(value)
        if not sanitized:
            raise ValueError("regime safety result reasons cannot be empty")
        return sanitized

    @field_validator("evaluated_at")
    @classmethod
    def evaluated_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)


def default_regime_safety_policy(settings: Any | None = None) -> RegimeSafetyPolicy:
    notes = ["Prompt 33 permits planning metadata only."]
    if settings is not None:
        notes.append(f"dependency_stage={settings.regime_analytics_dependency_stage}")
    return RegimeSafetyPolicy(
        policy_id="regime-safety-policy-v1",
        name="Regime Analytics Planning Safety Policy",
        notes=notes,
    )


def evaluate_regime_plan_safety(
    plan: RegimeAnalyticsPlan,
    policy: RegimeSafetyPolicy,
) -> RegimeSafetyResult:
    reasons: list[str] = []
    if policy.allow_classification or plan.classification_allowed:
        reasons.append("classification is not allowed")
    if policy.allow_real_data or plan.real_data_allowed:
        reasons.append("real market data is not allowed")
    if not policy.require_evidence or not plan.required_evidence_kinds:
        reasons.append("evidence requirements are missing")
    if not policy.require_human_review or not plan.requires_human_review:
        reasons.append("human review is required")
    for label in plan.planned_labels:
        if label.classification_allowed or label.trade_signal or label.recommendation or label.decision_object_generated:
            reasons.append(f"unsafe regime label placeholder: {label.label_id}")
    if reasons:
        return RegimeSafetyResult(decision="blocked", reasons=reasons, policy_id=policy.policy_id)
    return RegimeSafetyResult(
        decision="planning_allowed",
        reasons=[
            "planning-only regime contract is safe for documentation and template use",
            "classification, real data, signals, recommendations, DecisionObject generation, and execution remain blocked",
        ],
        policy_id=policy.policy_id,
    )


def reject_regime_classification_output(reason: str = "classification output is forbidden") -> RegimeSafetyResult:
    return RegimeSafetyResult(
        decision="blocked",
        reasons=[reason],
        policy_id="regime-safety-policy-v1",
    )


def reject_regime_signal_or_decision(reason: str = "regime signal or decision output is forbidden") -> RegimeSafetyResult:
    return RegimeSafetyResult(
        decision="blocked",
        reasons=[reason],
        policy_id="regime-safety-policy-v1",
    )
