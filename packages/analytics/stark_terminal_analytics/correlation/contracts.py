from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
import math

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.numerical.contracts import NumericalSourceReference, NumericalVectorContract


class CorrelationMethod(StrEnum):
    PEARSON = "PEARSON"
    UNKNOWN = "UNKNOWN"


class RelationshipMetricSafetyLabel(StrEnum):
    DESCRIPTIVE_ONLY = "DESCRIPTIVE_ONLY"
    RESEARCH_ONLY = "RESEARCH_ONLY"
    NOT_A_SIGNAL = "NOT_A_SIGNAL"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _non_empty_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class CorrelationCalculationRequest(BaseModel):
    request_id: str
    x_vector: NumericalVectorContract
    y_vector: NumericalVectorContract
    method: CorrelationMethod = CorrelationMethod.PEARSON
    min_observations: int = Field(default=2, ge=2)
    require_source_reference: bool = True
    allow_real_data: bool = False
    allow_trade_signal: bool = False
    allow_recommendation: bool = False
    allow_decision_object: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("request_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "correlation request text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def request_must_remain_safe(self) -> CorrelationCalculationRequest:
        if self.method == CorrelationMethod.UNKNOWN:
            raise ValueError("correlation method cannot be UNKNOWN")
        if not self.x_vector.descriptive_only or not self.y_vector.descriptive_only:
            raise ValueError("correlation requests require descriptive-only vectors")
        if self.x_vector.source is None or self.y_vector.source is None:
            raise ValueError("correlation requests require source references")
        if len(self.x_vector.values) != len(self.y_vector.values):
            raise ValueError("correlation vectors must have equal length")
        if not self.require_source_reference:
            raise ValueError("correlation requests must require source references")
        if self.allow_real_data:
            raise ValueError("correlation requests cannot allow real data in Prompt 31")
        if self.allow_trade_signal:
            raise ValueError("correlation requests cannot allow trade signals")
        if self.allow_recommendation:
            raise ValueError("correlation requests cannot allow recommendations")
        if self.allow_decision_object:
            raise ValueError("correlation requests cannot allow DecisionObject generation")
        return self


class CorrelationResult(BaseModel):
    result_id: str
    request_id: str
    method: CorrelationMethod
    correlation: float | None
    covariance: float | None = None
    x_source: NumericalSourceReference
    y_source: NumericalSourceReference
    observation_count: int = Field(ge=0)
    descriptive_only: bool = True
    trade_signal: bool = False
    recommendation: bool = False
    decision_object_generated: bool = False
    safety_label: RelationshipMetricSafetyLabel = RelationshipMetricSafetyLabel.DESCRIPTIVE_ONLY
    status: str
    error: str | None = None
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "request_id", "status", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "correlation result text fields")

    @field_validator("error")
    @classmethod
    def error_must_be_sanitized(cls, value: str | None) -> str | None:
        if value is None:
            return None
        sanitized = sanitize_analytics_notes([value])
        return sanitized[0] if sanitized else None

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def result_must_remain_descriptive(self) -> CorrelationResult:
        if self.method == CorrelationMethod.UNKNOWN and self.status == "ok":
            raise ValueError("successful correlation results require a known method")
        if self.correlation is None and self.status == "ok":
            raise ValueError("successful correlation results require a correlation value")
        if self.correlation is not None:
            if not math.isfinite(self.correlation):
                raise ValueError("correlation values must be finite")
            if self.correlation < -1.000000000001 or self.correlation > 1.000000000001:
                raise ValueError("correlation must be between -1 and 1")
        if self.covariance is not None and not math.isfinite(self.covariance):
            raise ValueError("covariance must be finite")
        if self.trade_signal:
            raise ValueError("correlation results cannot be trade signals")
        if self.recommendation:
            raise ValueError("correlation results cannot be recommendations")
        if self.decision_object_generated:
            raise ValueError("correlation results cannot generate DecisionObjects")
        if not self.descriptive_only:
            raise ValueError("correlation results must remain descriptive-only")
        if self.safety_label == RelationshipMetricSafetyLabel.UNKNOWN:
            raise ValueError("correlation safety label cannot be UNKNOWN")
        return self


def create_correlation_request(
    request_id: str,
    x_vector: NumericalVectorContract,
    y_vector: NumericalVectorContract,
    method: CorrelationMethod = CorrelationMethod.PEARSON,
    min_observations: int = 2,
) -> CorrelationCalculationRequest:
    return CorrelationCalculationRequest(
        request_id=request_id,
        x_vector=x_vector,
        y_vector=y_vector,
        method=method,
        min_observations=min_observations,
    )


def create_correlation_result(
    result_id: str,
    request_id: str,
    method: CorrelationMethod,
    correlation: float | None,
    covariance: float | None,
    x_source: NumericalSourceReference,
    y_source: NumericalSourceReference,
    observation_count: int,
    status: str = "ok",
    error: str | None = None,
) -> CorrelationResult:
    return CorrelationResult(
        result_id=result_id,
        request_id=request_id,
        method=method,
        correlation=correlation,
        covariance=covariance,
        x_source=x_source,
        y_source=y_source,
        observation_count=observation_count,
        status=status,
        error=error,
    )

