from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
import math

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.numerical.contracts import NumericalSourceReference, NumericalVectorContract


class VolatilityMethod(StrEnum):
    SAMPLE_STDDEV = "SAMPLE_STDDEV"
    POPULATION_STDDEV = "POPULATION_STDDEV"
    UNKNOWN = "UNKNOWN"


class RiskMetricSafetyLabel(StrEnum):
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


def _status_allows_empty_value(status: str) -> bool:
    return status.strip().lower() in {"failed", "failure", "error", "blocked"}


class VolatilityCalculationRequest(BaseModel):
    request_id: str
    return_vector: NumericalVectorContract
    method: VolatilityMethod = VolatilityMethod.SAMPLE_STDDEV
    annualize: bool = False
    periods_per_year: int | None = None
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
        return _non_empty_text(value, "volatility request text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def request_must_remain_safe(self) -> VolatilityCalculationRequest:
        if self.method == VolatilityMethod.UNKNOWN:
            raise ValueError("volatility method cannot be UNKNOWN")
        if not self.return_vector.descriptive_only:
            raise ValueError("volatility requests require descriptive-only return vectors")
        if self.return_vector.source is None:
            raise ValueError("volatility requests require a return vector source reference")
        if self.annualize and (self.periods_per_year is None or self.periods_per_year <= 0):
            raise ValueError("annualized volatility requires positive periods_per_year")
        if not self.require_source_reference:
            raise ValueError("volatility requests must require source references")
        if self.allow_real_data:
            raise ValueError("volatility requests cannot allow real data in Prompt 29")
        if self.allow_trade_signal:
            raise ValueError("volatility requests cannot allow trade signals")
        if self.allow_recommendation:
            raise ValueError("volatility requests cannot allow recommendations")
        if self.allow_decision_object:
            raise ValueError("volatility requests cannot allow DecisionObject generation")
        return self


class VolatilityResult(BaseModel):
    result_id: str
    request_id: str
    method: VolatilityMethod
    volatility: float | None
    annualized_volatility: float | None = None
    annualize: bool = False
    periods_per_year: int | None = None
    source: NumericalSourceReference
    input_count: int = Field(ge=0)
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
        return _non_empty_text(value, "volatility result text fields")

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
    def result_must_remain_descriptive(self) -> VolatilityResult:
        if self.method == VolatilityMethod.UNKNOWN and not _status_allows_empty_value(self.status):
            raise ValueError("successful volatility results require a known method")
        if self.volatility is None and not _status_allows_empty_value(self.status):
            raise ValueError("successful volatility results require volatility")
        if self.volatility is not None and not math.isfinite(self.volatility):
            raise ValueError("volatility result values must be finite")
        if self.annualized_volatility is not None and not math.isfinite(self.annualized_volatility):
            raise ValueError("annualized volatility must be finite")
        if not self.annualize and self.annualized_volatility is not None:
            raise ValueError("annualized_volatility must be None when annualize is false")
        if self.annualize and self.status == "ok" and self.annualized_volatility is None:
            raise ValueError("annualized volatility is required for successful annualized results")
        if self.annualize and (self.periods_per_year is None or self.periods_per_year <= 0):
            raise ValueError("annualized results require positive periods_per_year")
        if self.trade_signal:
            raise ValueError("volatility results cannot be trade signals")
        if self.recommendation:
            raise ValueError("volatility results cannot be recommendations")
        if self.decision_object_generated:
            raise ValueError("volatility results cannot generate DecisionObjects")
        if not self.descriptive_only:
            raise ValueError("volatility results must remain descriptive-only")
        if self.safety_label == RiskMetricSafetyLabel.UNKNOWN:
            raise ValueError("volatility safety label cannot be UNKNOWN")
        return self


def create_volatility_request(
    request_id: str,
    return_vector: NumericalVectorContract,
    method: VolatilityMethod = VolatilityMethod.SAMPLE_STDDEV,
    annualize: bool = False,
    periods_per_year: int | None = None,
) -> VolatilityCalculationRequest:
    return VolatilityCalculationRequest(
        request_id=request_id,
        return_vector=return_vector,
        method=method,
        annualize=annualize,
        periods_per_year=periods_per_year,
    )


def create_volatility_result(
    result_id: str,
    request_id: str,
    method: VolatilityMethod,
    volatility: float | None,
    source: NumericalSourceReference,
    input_count: int,
    annualize: bool = False,
    periods_per_year: int | None = None,
    annualized_volatility: float | None = None,
    status: str = "ok",
    error: str | None = None,
) -> VolatilityResult:
    return VolatilityResult(
        result_id=result_id,
        request_id=request_id,
        method=method,
        volatility=volatility,
        annualized_volatility=annualized_volatility,
        annualize=annualize,
        periods_per_year=periods_per_year,
        source=source,
        input_count=input_count,
        status=status,
        error=error,
    )
