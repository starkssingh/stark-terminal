from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
import math

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.correlation.contracts import RelationshipMetricSafetyLabel
from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.numerical.contracts import NumericalSourceReference, NumericalVectorContract


class BetaMethod(StrEnum):
    SAMPLE_COVARIANCE = "SAMPLE_COVARIANCE"
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


class BetaCalculationRequest(BaseModel):
    request_id: str
    asset_returns: NumericalVectorContract
    benchmark_returns: NumericalVectorContract
    method: BetaMethod = BetaMethod.SAMPLE_COVARIANCE
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
        return _non_empty_text(value, "beta request text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def request_must_remain_safe(self) -> BetaCalculationRequest:
        if self.method == BetaMethod.UNKNOWN:
            raise ValueError("beta method cannot be UNKNOWN")
        if not self.asset_returns.descriptive_only or not self.benchmark_returns.descriptive_only:
            raise ValueError("beta requests require descriptive-only vectors")
        if self.asset_returns.source is None or self.benchmark_returns.source is None:
            raise ValueError("beta requests require source references")
        if len(self.asset_returns.values) != len(self.benchmark_returns.values):
            raise ValueError("beta vectors must have equal length")
        if not self.require_source_reference:
            raise ValueError("beta requests must require source references")
        if self.allow_real_data:
            raise ValueError("beta requests cannot allow real data in Prompt 31")
        if self.allow_trade_signal:
            raise ValueError("beta requests cannot allow trade signals")
        if self.allow_recommendation:
            raise ValueError("beta requests cannot allow recommendations")
        if self.allow_decision_object:
            raise ValueError("beta requests cannot allow DecisionObject generation")
        return self


class BetaResult(BaseModel):
    result_id: str
    request_id: str
    method: BetaMethod
    beta: float | None
    covariance: float | None = None
    benchmark_variance: float | None = None
    asset_source: NumericalSourceReference
    benchmark_source: NumericalSourceReference
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
        return _non_empty_text(value, "beta result text fields")

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
    def result_must_remain_descriptive(self) -> BetaResult:
        if self.method == BetaMethod.UNKNOWN and self.status == "ok":
            raise ValueError("successful beta results require a known method")
        if self.beta is None and self.status == "ok":
            raise ValueError("successful beta results require a beta value")
        for value, field_name in [
            (self.beta, "beta"),
            (self.covariance, "covariance"),
            (self.benchmark_variance, "benchmark_variance"),
        ]:
            if value is not None and not math.isfinite(value):
                raise ValueError(f"{field_name} must be finite")
        if self.trade_signal:
            raise ValueError("beta results cannot be trade signals")
        if self.recommendation:
            raise ValueError("beta results cannot be recommendations")
        if self.decision_object_generated:
            raise ValueError("beta results cannot generate DecisionObjects")
        if not self.descriptive_only:
            raise ValueError("beta results must remain descriptive-only")
        if self.safety_label == RelationshipMetricSafetyLabel.UNKNOWN:
            raise ValueError("beta safety label cannot be UNKNOWN")
        return self


def create_beta_request(
    request_id: str,
    asset_returns: NumericalVectorContract,
    benchmark_returns: NumericalVectorContract,
    method: BetaMethod = BetaMethod.SAMPLE_COVARIANCE,
    min_observations: int = 2,
) -> BetaCalculationRequest:
    return BetaCalculationRequest(
        request_id=request_id,
        asset_returns=asset_returns,
        benchmark_returns=benchmark_returns,
        method=method,
        min_observations=min_observations,
    )


def create_beta_result(
    result_id: str,
    request_id: str,
    method: BetaMethod,
    beta: float | None,
    covariance: float | None,
    benchmark_variance: float | None,
    asset_source: NumericalSourceReference,
    benchmark_source: NumericalSourceReference,
    observation_count: int,
    status: str = "ok",
    error: str | None = None,
) -> BetaResult:
    return BetaResult(
        result_id=result_id,
        request_id=request_id,
        method=method,
        beta=beta,
        covariance=covariance,
        benchmark_variance=benchmark_variance,
        asset_source=asset_source,
        benchmark_source=benchmark_source,
        observation_count=observation_count,
        status=status,
        error=error,
    )

