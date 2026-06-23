from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
import math

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.numerical.contracts import NumericalSourceReference, NumericalVectorContract
from stark_terminal_analytics.returns.contracts import ReturnSeriesSafetyLabel


class RollingMetric(StrEnum):
    MEAN = "MEAN"
    MIN = "MIN"
    MAX = "MAX"
    COUNT = "COUNT"
    UNKNOWN = "UNKNOWN"


class RollingWindowAlignment(StrEnum):
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    CENTER = "CENTER"
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


def _status_allows_empty_values(status: str) -> bool:
    return status.strip().lower() in {"failed", "failure", "error", "blocked"}


class RollingWindowRequest(BaseModel):
    request_id: str
    vector: NumericalVectorContract
    window: int = Field(gt=0)
    metric: RollingMetric
    alignment: RollingWindowAlignment = RollingWindowAlignment.RIGHT
    require_finite_values: bool = True
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
        return _non_empty_text(value, "rolling request text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def request_must_remain_safe(self) -> RollingWindowRequest:
        if self.metric == RollingMetric.UNKNOWN:
            raise ValueError("rolling metric cannot be UNKNOWN")
        if self.alignment != RollingWindowAlignment.RIGHT:
            raise ValueError("Prompt 28 supports RIGHT rolling alignment only")
        if self.vector.source is None:
            raise ValueError("rolling requests require a vector source reference")
        if not self.vector.descriptive_only:
            raise ValueError("rolling requests require descriptive-only vectors")
        if not self.require_source_reference:
            raise ValueError("rolling requests must require source references")
        if self.allow_real_data:
            raise ValueError("rolling requests cannot allow real data in Prompt 28")
        if self.allow_trade_signal:
            raise ValueError("rolling requests cannot allow trade signals")
        if self.allow_recommendation:
            raise ValueError("rolling requests cannot allow recommendations")
        if self.allow_decision_object:
            raise ValueError("rolling requests cannot allow DecisionObject generation")
        return self


class RollingWindowResult(BaseModel):
    result_id: str
    request_id: str
    metric: RollingMetric
    window: int = Field(gt=0)
    values: list[float | int | None]
    source: NumericalSourceReference
    input_count: int = Field(ge=0)
    output_count: int = Field(ge=0)
    descriptive_only: bool = True
    trade_signal: bool = False
    recommendation: bool = False
    decision_object_generated: bool = False
    safety_label: ReturnSeriesSafetyLabel = ReturnSeriesSafetyLabel.DESCRIPTIVE_ONLY
    status: str
    error: str | None = None
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "request_id", "status", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "rolling result text fields")

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
    def result_must_remain_descriptive(self) -> RollingWindowResult:
        if self.metric == RollingMetric.UNKNOWN and not _status_allows_empty_values(self.status):
            raise ValueError("successful rolling results require a known metric")
        if self.output_count != len(self.values):
            raise ValueError("rolling result output_count must equal len(values)")
        if not self.values and not _status_allows_empty_values(self.status):
            raise ValueError("successful rolling results require values")
        finite_values = [value for value in self.values if value is not None]
        if any(not math.isfinite(float(value)) for value in finite_values):
            raise ValueError("rolling result values must be finite when present")
        if self.trade_signal:
            raise ValueError("rolling results cannot be trade signals")
        if self.recommendation:
            raise ValueError("rolling results cannot be recommendations")
        if self.decision_object_generated:
            raise ValueError("rolling results cannot generate DecisionObjects")
        if not self.descriptive_only:
            raise ValueError("rolling results must remain descriptive-only")
        if self.safety_label == ReturnSeriesSafetyLabel.UNKNOWN:
            raise ValueError("rolling result safety label cannot be UNKNOWN")
        return self


def create_rolling_request(
    request_id: str,
    vector: NumericalVectorContract,
    window: int,
    metric: RollingMetric,
) -> RollingWindowRequest:
    return RollingWindowRequest(
        request_id=request_id,
        vector=vector,
        window=window,
        metric=metric,
    )


def create_rolling_result(
    result_id: str,
    request_id: str,
    metric: RollingMetric,
    window: int,
    values: list[float | int | None] | None,
    source: NumericalSourceReference,
    input_count: int,
    status: str = "ok",
    error: str | None = None,
) -> RollingWindowResult:
    resolved_values = list(values or [])
    return RollingWindowResult(
        result_id=result_id,
        request_id=request_id,
        metric=metric,
        window=window,
        values=resolved_values,
        source=source,
        input_count=input_count,
        output_count=len(resolved_values),
        status=status,
        error=error,
    )
