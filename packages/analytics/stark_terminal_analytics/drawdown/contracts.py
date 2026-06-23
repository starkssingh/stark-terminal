from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
import math

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.numerical.contracts import NumericalSourceReference, NumericalVectorContract
from stark_terminal_analytics.volatility.contracts import RiskMetricSafetyLabel


class DrawdownMetric(StrEnum):
    DRAWDOWN_SERIES = "DRAWDOWN_SERIES"
    MAX_DRAWDOWN = "MAX_DRAWDOWN"
    DRAWDOWN_DURATION = "DRAWDOWN_DURATION"
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


class DrawdownCalculationRequest(BaseModel):
    request_id: str
    value_vector: NumericalVectorContract
    require_positive_values: bool = True
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
        return _non_empty_text(value, "drawdown request text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def request_must_remain_safe(self) -> DrawdownCalculationRequest:
        if not self.value_vector.descriptive_only:
            raise ValueError("drawdown requests require descriptive-only value vectors")
        if self.value_vector.source is None:
            raise ValueError("drawdown requests require a value vector source reference")
        if not self.require_source_reference:
            raise ValueError("drawdown requests must require source references")
        if self.allow_real_data:
            raise ValueError("drawdown requests cannot allow real data in Prompt 29")
        if self.allow_trade_signal:
            raise ValueError("drawdown requests cannot allow trade signals")
        if self.allow_recommendation:
            raise ValueError("drawdown requests cannot allow recommendations")
        if self.allow_decision_object:
            raise ValueError("drawdown requests cannot allow DecisionObject generation")
        return self


class DrawdownResult(BaseModel):
    result_id: str
    request_id: str
    drawdown_values: list[float]
    max_drawdown: float | None
    max_drawdown_index: int | None = None
    longest_drawdown_duration: int | None = None
    source: NumericalSourceReference
    input_count: int = Field(ge=0)
    output_count: int = Field(ge=0)
    descriptive_only: bool = True
    trade_signal: bool = False
    recommendation: bool = False
    decision_object_generated: bool = False
    safety_label: RiskMetricSafetyLabel = RiskMetricSafetyLabel.DESCRIPTIVE_ONLY
    status: str
    error: str | None = None
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "request_id", "status", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "drawdown result text fields")

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
    def result_must_remain_descriptive(self) -> DrawdownResult:
        if self.output_count != len(self.drawdown_values):
            raise ValueError("drawdown result output_count must equal len(drawdown_values)")
        if not self.drawdown_values and not _status_allows_empty_values(self.status):
            raise ValueError("successful drawdown results require drawdown values")
        if any(not math.isfinite(value) for value in self.drawdown_values):
            raise ValueError("drawdown result values must be finite")
        if self.status == "ok" and any(value > 0 for value in self.drawdown_values):
            raise ValueError("drawdown values must be zero or negative")
        if self.status == "ok" and (self.max_drawdown is None or self.max_drawdown > 0):
            raise ValueError("successful drawdown results require max_drawdown <= 0")
        if self.max_drawdown is not None and not math.isfinite(self.max_drawdown):
            raise ValueError("max_drawdown must be finite")
        if self.max_drawdown_index is not None and self.max_drawdown_index < 0:
            raise ValueError("max_drawdown_index cannot be negative")
        if self.longest_drawdown_duration is not None and self.longest_drawdown_duration < 0:
            raise ValueError("longest_drawdown_duration cannot be negative")
        if self.trade_signal:
            raise ValueError("drawdown results cannot be trade signals")
        if self.recommendation:
            raise ValueError("drawdown results cannot be recommendations")
        if self.decision_object_generated:
            raise ValueError("drawdown results cannot generate DecisionObjects")
        if not self.descriptive_only:
            raise ValueError("drawdown results must remain descriptive-only")
        if self.safety_label == RiskMetricSafetyLabel.UNKNOWN:
            raise ValueError("drawdown safety label cannot be UNKNOWN")
        return self


def create_drawdown_request(
    request_id: str,
    value_vector: NumericalVectorContract,
) -> DrawdownCalculationRequest:
    return DrawdownCalculationRequest(request_id=request_id, value_vector=value_vector)


def create_drawdown_result(
    result_id: str,
    request_id: str,
    drawdown_values: list[float] | None,
    max_drawdown: float | None,
    source: NumericalSourceReference,
    input_count: int,
    max_drawdown_index: int | None = None,
    longest_drawdown_duration: int | None = None,
    status: str = "ok",
    error: str | None = None,
) -> DrawdownResult:
    resolved_values = list(drawdown_values or [])
    return DrawdownResult(
        result_id=result_id,
        request_id=request_id,
        drawdown_values=resolved_values,
        max_drawdown=max_drawdown,
        max_drawdown_index=max_drawdown_index,
        longest_drawdown_duration=longest_drawdown_duration,
        source=source,
        input_count=input_count,
        output_count=len(resolved_values),
        status=status,
        error=error,
    )
