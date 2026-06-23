from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.regime_features.contracts import (
    RegimeFeatureCandidate,
    RegimeFeatureGroupPlan,
)


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


class RegimeFeatureSafetyPolicy(BaseModel):
    policy_id: str
    name: str
    allow_real_data: bool = False
    allow_feature_computation: bool = False
    allow_feature_registry_writes: bool = False
    allow_classification: bool = False
    allow_trade_signals: bool = False
    allow_recommendations: bool = False
    allow_decision_objects: bool = False
    allow_execution: bool = False
    require_provenance: bool = True
    require_evidence_mapping: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime feature safety policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)

    @model_validator(mode="after")
    def policy_must_fail_closed(self) -> RegimeFeatureSafetyPolicy:
        if self.allow_real_data:
            raise ValueError("real data is forbidden for regime feature preparation in Prompt 34")
        if self.allow_feature_computation:
            raise ValueError("feature computation is forbidden in Prompt 34")
        if self.allow_feature_registry_writes:
            raise ValueError("feature registry writes are forbidden in Prompt 34")
        if self.allow_classification:
            raise ValueError("regime classification is forbidden in Prompt 34")
        if self.allow_trade_signals:
            raise ValueError("trade signals are forbidden in Prompt 34")
        if self.allow_recommendations:
            raise ValueError("recommendations are forbidden in Prompt 34")
        if self.allow_decision_objects:
            raise ValueError("DecisionObject generation is forbidden in Prompt 34")
        if self.allow_execution:
            raise ValueError("execution is forbidden in Prompt 34")
        if not self.require_provenance:
            raise ValueError("regime feature provenance is required in Prompt 34")
        if not self.require_evidence_mapping:
            raise ValueError("regime feature evidence mapping is required in Prompt 34")
        return self


class RegimeFeatureSafetyResult(BaseModel):
    decision: str
    reasons: list[str]
    policy_id: str
    evaluated_at: datetime = Field(default_factory=_utc_now)
    schema_version: str = "v1"

    @field_validator("decision", "policy_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime feature safety result text fields")

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_analytics_notes(value)
        if not sanitized:
            raise ValueError("regime feature safety result reasons cannot be empty")
        return sanitized

    @field_validator("evaluated_at")
    @classmethod
    def evaluated_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)


def default_regime_feature_safety_policy(settings: Any | None = None) -> RegimeFeatureSafetyPolicy:
    notes = ["Prompt 34 permits contracts and preparation metadata only."]
    if settings is not None:
        notes.append(f"dependency_stage={settings.regime_feature_preparation_dependency_stage}")
    return RegimeFeatureSafetyPolicy(
        policy_id="regime-feature-safety-policy-v1",
        name="Regime Feature Preparation Safety Policy",
        notes=notes,
    )


def evaluate_regime_feature_candidate_safety(
    candidate: RegimeFeatureCandidate,
    policy: RegimeFeatureSafetyPolicy,
) -> RegimeFeatureSafetyResult:
    reasons: list[str] = []
    if candidate.computation_allowed or policy.allow_feature_computation:
        reasons.append("feature computation is not allowed")
    if candidate.registry_write_allowed or policy.allow_feature_registry_writes:
        reasons.append("feature registry writes are not allowed")
    if candidate.classification_allowed or policy.allow_classification:
        reasons.append("regime classification is not allowed")
    if candidate.trade_signal or policy.allow_trade_signals:
        reasons.append("trade signals are not allowed")
    if candidate.recommendation or policy.allow_recommendations:
        reasons.append("recommendations are not allowed")
    if candidate.decision_object_generated or policy.allow_decision_objects:
        reasons.append("DecisionObject generation is not allowed")
    if policy.allow_real_data:
        reasons.append("real data is not allowed")
    if policy.allow_execution:
        reasons.append("execution is not allowed")
    if reasons:
        return RegimeFeatureSafetyResult(decision="blocked", reasons=reasons, policy_id=policy.policy_id)
    return RegimeFeatureSafetyResult(
        decision="preparation_allowed",
        reasons=["candidate is metadata-only and safe for contracts-only preparation"],
        policy_id=policy.policy_id,
    )


def evaluate_regime_feature_plan_safety(
    candidates: list[RegimeFeatureCandidate],
    groups: list[RegimeFeatureGroupPlan],
    policy: RegimeFeatureSafetyPolicy,
) -> RegimeFeatureSafetyResult:
    reasons: list[str] = []
    if not candidates:
        reasons.append("regime feature candidates are missing")
    if not groups:
        reasons.append("regime feature groups are missing")
    if not policy.require_provenance:
        reasons.append("provenance is required")
    if not policy.require_evidence_mapping:
        reasons.append("evidence mapping is required")
    for candidate in candidates:
        candidate_result = evaluate_regime_feature_candidate_safety(candidate, policy)
        if candidate_result.decision == "blocked":
            reasons.extend(f"{candidate.feature_id}: {reason}" for reason in candidate_result.reasons)
    for group in groups:
        if group.computation_allowed:
            reasons.append(f"{group.group_id}: feature computation is not allowed")
        if group.classification_allowed:
            reasons.append(f"{group.group_id}: regime classification is not allowed")
    if reasons:
        return RegimeFeatureSafetyResult(decision="blocked", reasons=reasons, policy_id=policy.policy_id)
    return RegimeFeatureSafetyResult(
        decision="preparation_allowed",
        reasons=[
            "regime feature preparation plan is contracts-only",
            "feature computation, registry writes, classification, signals, recommendations, DecisionObject generation, and execution remain blocked",
        ],
        policy_id=policy.policy_id,
    )


def reject_feature_computation_output(reason: str = "feature computation output is forbidden") -> RegimeFeatureSafetyResult:
    return RegimeFeatureSafetyResult(
        decision="blocked",
        reasons=[reason],
        policy_id="regime-feature-safety-policy-v1",
    )


def reject_feature_signal_or_decision(reason: str = "feature signal or decision output is forbidden") -> RegimeFeatureSafetyResult:
    return RegimeFeatureSafetyResult(
        decision="blocked",
        reasons=[reason],
        policy_id="regime-feature-safety-policy-v1",
    )
