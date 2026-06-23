from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_analytics.foundation.contracts import (
    AnalyticsOutputContract,
    sanitize_analytics_notes,
)


class AnalyticsSafetyPolicy(BaseModel):
    policy_id: str
    name: str
    allow_real_data: bool = False
    allow_trade_signals: bool = False
    allow_recommendations: bool = False
    allow_execution: bool = False
    require_validated_inputs: bool = True
    require_source_reference: bool = True
    require_descriptive_label: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("analytics safety policy text fields cannot be empty")
        return normalized

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)

    @model_validator(mode="after")
    def unsafe_flags_must_remain_disabled(self) -> AnalyticsSafetyPolicy:
        if self.allow_trade_signals:
            raise ValueError("analytics safety policy cannot allow trade signals in Prompt 26")
        if self.allow_recommendations:
            raise ValueError("analytics safety policy cannot allow recommendations in Prompt 26")
        if self.allow_execution:
            raise ValueError("analytics safety policy cannot allow execution")
        if self.allow_real_data:
            raise ValueError("analytics safety policy cannot allow real data in Prompt 26")
        if not self.require_validated_inputs:
            raise ValueError("analytics safety policy must require validated inputs")
        if not self.require_source_reference:
            raise ValueError("analytics safety policy must require source references")
        return self


class AnalyticsSafetyResult(BaseModel):
    decision: str
    reasons: list[str]
    policy_id: str
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    schema_version: str = "v1"

    @field_validator("decision", "policy_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("analytics safety result text fields cannot be empty")
        return normalized

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_analytics_notes(value)
        if not sanitized:
            raise ValueError("analytics safety result requires reasons")
        return sanitized

    @field_validator("evaluated_at")
    @classmethod
    def evaluated_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


def default_analytics_safety_policy(settings: Settings | None = None) -> AnalyticsSafetyPolicy:
    resolved_settings = settings or get_settings()
    return AnalyticsSafetyPolicy(
        policy_id="analytics_safety_policy_v1",
        name="Prompt 26 analytics descriptive-only safety policy",
        allow_real_data=resolved_settings.analytics_allow_real_data,
        allow_trade_signals=resolved_settings.analytics_allow_trade_signals,
        allow_recommendations=resolved_settings.analytics_allow_recommendations,
        allow_execution=False,
        require_validated_inputs=resolved_settings.analytics_require_validated_inputs,
        require_source_reference=resolved_settings.analytics_require_source_reference,
        schema_version=resolved_settings.analytics_schema_version,
        notes=[
            "Analytics foundation is planning-only in Prompt 26.",
            "No analytics-as-trade-call, no recommendations, and no execution APIs.",
        ],
    )


def reject_signal_or_recommendation_contract(output: AnalyticsOutputContract) -> list[str]:
    reasons: list[str] = []
    if getattr(output, "trade_signal", False):
        reasons.append("analytics output is marked as a trade signal")
    if getattr(output, "recommendation", False):
        reasons.append("analytics output is marked as a recommendation")
    if getattr(output, "execution_ready", False):
        reasons.append("analytics output is marked execution-ready")
    if not getattr(output, "descriptive_only", True):
        reasons.append("analytics output is not descriptive-only")
    return reasons


def evaluate_analytics_output_contract(
    output: AnalyticsOutputContract,
    policy: AnalyticsSafetyPolicy,
) -> AnalyticsSafetyResult:
    reasons = reject_signal_or_recommendation_contract(output)
    if policy.allow_real_data:
        reasons.append("policy allows real data, which is blocked in Prompt 26")
    if policy.allow_trade_signals:
        reasons.append("policy allows trade signals, which is blocked in Prompt 26")
    if policy.allow_recommendations:
        reasons.append("policy allows recommendations, which is blocked in Prompt 26")
    if policy.allow_execution:
        reasons.append("policy allows execution, which is forbidden")
    if policy.require_descriptive_label and not getattr(output, "descriptive_only", False):
        reasons.append("descriptive-only label is required")

    if reasons:
        return AnalyticsSafetyResult(decision="BLOCK", reasons=reasons, policy_id=policy.policy_id)

    return AnalyticsSafetyResult(
        decision="ALLOW",
        reasons=["analytics output contract is descriptive/research-only"],
        policy_id=policy.policy_id,
    )
