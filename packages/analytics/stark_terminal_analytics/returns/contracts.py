from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
import math

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.numerical.contracts import NumericalSourceReference, NumericalVectorContract


class ReturnMethod(StrEnum):
    SIMPLE = "SIMPLE"
    LOG = "LOG"
    UNKNOWN = "UNKNOWN"


class ReturnSeriesSafetyLabel(StrEnum):
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


def _status_allows_empty_values(status: str) -> bool:
    return status.strip().lower() in {"failed", "failure", "error", "blocked"}


class ReturnCalculationRequest(BaseModel):
    request_id: str
    price_vector: NumericalVectorContract
    method: ReturnMethod = ReturnMethod.SIMPLE
    require_positive_prices: bool = True
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
        return _non_empty_text(value, "return calculation request text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def request_must_remain_safe(self) -> ReturnCalculationRequest:
        if self.method == ReturnMethod.UNKNOWN:
            raise ValueError("return method cannot be UNKNOWN")
        if not self.price_vector.descriptive_only:
            raise ValueError("return requests require descriptive-only price vectors")
        if self.price_vector.source is None:
            raise ValueError("return requests require a price vector source reference")
        if not self.require_source_reference:
            raise ValueError("return requests must require source references")
        if self.allow_real_data:
            raise ValueError("return requests cannot allow real data in Prompt 28")
        if self.allow_trade_signal:
            raise ValueError("return requests cannot allow trade signals")
        if self.allow_recommendation:
            raise ValueError("return requests cannot allow recommendations")
        if self.allow_decision_object:
            raise ValueError("return requests cannot allow DecisionObject generation")
        return self


class ReturnSeriesResult(BaseModel):
    result_id: str
    request_id: str
    method: ReturnMethod
    values: list[float]
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
        return _non_empty_text(value, "return series result text fields")

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
    def result_must_remain_descriptive(self) -> ReturnSeriesResult:
        if self.method == ReturnMethod.UNKNOWN and not _status_allows_empty_values(self.status):
            raise ValueError("successful return results require a known method")
        if self.output_count != len(self.values):
            raise ValueError("return result output_count must equal len(values)")
        if not self.values and not _status_allows_empty_values(self.status):
            raise ValueError("successful return results require values")
        if any(not math.isfinite(value) for value in self.values):
            raise ValueError("return result values must be finite")
        if self.trade_signal:
            raise ValueError("return results cannot be trade signals")
        if self.recommendation:
            raise ValueError("return results cannot be recommendations")
        if self.decision_object_generated:
            raise ValueError("return results cannot generate DecisionObjects")
        if not self.descriptive_only:
            raise ValueError("return results must remain descriptive-only")
        if self.safety_label == ReturnSeriesSafetyLabel.UNKNOWN:
            raise ValueError("return result safety label cannot be UNKNOWN")
        return self


def create_return_request(
    request_id: str,
    price_vector: NumericalVectorContract,
    method: ReturnMethod = ReturnMethod.SIMPLE,
) -> ReturnCalculationRequest:
    return ReturnCalculationRequest(
        request_id=request_id,
        price_vector=price_vector,
        method=method,
    )


def create_return_result(
    result_id: str,
    request_id: str,
    method: ReturnMethod,
    values: list[float] | None,
    source: NumericalSourceReference,
    input_count: int,
    status: str = "ok",
    error: str | None = None,
) -> ReturnSeriesResult:
    resolved_values = list(values or [])
    return ReturnSeriesResult(
        result_id=result_id,
        request_id=request_id,
        method=method,
        values=resolved_values,
        source=source,
        input_count=input_count,
        output_count=len(resolved_values),
        status=status,
        error=error,
    )
