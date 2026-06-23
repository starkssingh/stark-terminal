from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
import math

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.numerical.contracts import NumericalSourceReference


class TimestampOrderStatus(StrEnum):
    STRICTLY_INCREASING = "STRICTLY_INCREASING"
    NON_DECREASING = "NON_DECREASING"
    NON_MONOTONIC = "NON_MONOTONIC"
    UNKNOWN = "UNKNOWN"


class TimeSeriesDiagnosticKind(StrEnum):
    MONOTONICITY = "MONOTONICITY"
    DUPLICATES = "DUPLICATES"
    GAPS = "GAPS"
    IRREGULAR_INTERVALS = "IRREGULAR_INTERVALS"
    SPACING_SUMMARY = "SPACING_SUMMARY"
    UNKNOWN = "UNKNOWN"


class TimeSeriesDiagnosticSafetyLabel(StrEnum):
    DESCRIPTIVE_ONLY = "DESCRIPTIVE_ONLY"
    DATA_QUALITY_ONLY = "DATA_QUALITY_ONLY"
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


def _normalize_timestamp(value: datetime) -> datetime:
    if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
        return value
    return value.astimezone(timezone.utc)


def _timezone_aware(value: datetime) -> bool:
    return value.tzinfo is not None and value.tzinfo.utcoffset(value) is not None


class TimestampSeriesContract(BaseModel):
    series_id: str
    name: str
    timestamps: list[datetime]
    source: NumericalSourceReference
    require_timezone_aware: bool = True
    descriptive_only: bool = True
    safety_label: TimeSeriesDiagnosticSafetyLabel = TimeSeriesDiagnosticSafetyLabel.DATA_QUALITY_ONLY
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("series_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "timestamp series text fields")

    @field_validator("timestamps")
    @classmethod
    def timestamps_must_be_present(cls, value: list[datetime]) -> list[datetime]:
        if not value:
            raise ValueError("timestamps cannot be empty")
        return [_normalize_timestamp(timestamp) for timestamp in value]

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if not _timezone_aware(value):
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def series_must_remain_safe(self) -> TimestampSeriesContract:
        if self.source.real_market_data:
            raise ValueError("time-series diagnostics cannot accept real market data in Prompt 32")
        if self.require_timezone_aware and any(not _timezone_aware(timestamp) for timestamp in self.timestamps):
            raise ValueError("time-series diagnostics require timezone-aware timestamps")
        if not self.descriptive_only:
            raise ValueError("time-series diagnostics must remain descriptive-only")
        if self.safety_label == TimeSeriesDiagnosticSafetyLabel.UNKNOWN:
            raise ValueError("time-series diagnostic safety label cannot be UNKNOWN")
        return self


class TimeSeriesDiagnosticsRequest(BaseModel):
    request_id: str
    timestamp_series: TimestampSeriesContract
    diagnostics: list[TimeSeriesDiagnosticKind]
    expected_interval_seconds: int | None = None
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
        return _non_empty_text(value, "time-series diagnostics request text fields")

    @field_validator("diagnostics")
    @classmethod
    def diagnostics_must_be_known(cls, value: list[TimeSeriesDiagnosticKind]) -> list[TimeSeriesDiagnosticKind]:
        if not value:
            raise ValueError("diagnostics cannot be empty")
        if TimeSeriesDiagnosticKind.UNKNOWN in value:
            raise ValueError("UNKNOWN diagnostic is not allowed")
        return value

    @field_validator("expected_interval_seconds")
    @classmethod
    def expected_interval_must_be_positive(cls, value: int | None) -> int | None:
        if value is not None and value <= 0:
            raise ValueError("expected_interval_seconds must be positive")
        return value

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if not _timezone_aware(value):
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def request_must_remain_safe(self) -> TimeSeriesDiagnosticsRequest:
        if not self.require_source_reference:
            raise ValueError("time-series diagnostics requests must require source references")
        if self.allow_real_data:
            raise ValueError("time-series diagnostics requests cannot allow real data")
        if self.allow_trade_signal:
            raise ValueError("time-series diagnostics requests cannot allow trade signals")
        if self.allow_recommendation:
            raise ValueError("time-series diagnostics requests cannot allow recommendations")
        if self.allow_decision_object:
            raise ValueError("time-series diagnostics requests cannot allow DecisionObject generation")
        return self


class TimestampGap(BaseModel):
    start_timestamp: datetime
    end_timestamp: datetime
    observed_interval_seconds: int | float
    expected_interval_seconds: int
    missing_count_estimate: int = Field(ge=0)

    @field_validator("start_timestamp", "end_timestamp")
    @classmethod
    def timestamps_must_be_normalized(cls, value: datetime) -> datetime:
        return _normalize_timestamp(value)

    @model_validator(mode="after")
    def gap_must_be_consistent(self) -> TimestampGap:
        if self.end_timestamp <= self.start_timestamp:
            raise ValueError("gap end_timestamp must be after start_timestamp")
        if not math.isfinite(float(self.observed_interval_seconds)) or self.observed_interval_seconds <= 0:
            raise ValueError("observed interval must be positive and finite")
        if self.expected_interval_seconds <= 0:
            raise ValueError("expected interval must be positive")
        return self


class TimeSeriesDiagnosticsResult(BaseModel):
    result_id: str
    request_id: str
    source: NumericalSourceReference
    observation_count: int = Field(ge=0)
    order_status: TimestampOrderStatus | None = None
    duplicate_count: int | None = None
    duplicate_timestamps: list[datetime] = []
    gap_count: int | None = None
    gaps: list[TimestampGap] = []
    interval_count: int | None = None
    min_interval_seconds: float | None = None
    max_interval_seconds: float | None = None
    mean_interval_seconds: float | None = None
    descriptive_only: bool = True
    trade_signal: bool = False
    recommendation: bool = False
    decision_object_generated: bool = False
    safety_label: TimeSeriesDiagnosticSafetyLabel = TimeSeriesDiagnosticSafetyLabel.DATA_QUALITY_ONLY
    status: str
    error: str | None = None
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "request_id", "status", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "time-series diagnostics result text fields")

    @field_validator("duplicate_timestamps")
    @classmethod
    def duplicate_timestamps_must_be_normalized(cls, value: list[datetime]) -> list[datetime]:
        return [_normalize_timestamp(timestamp) for timestamp in value]

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
        if not _timezone_aware(value):
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def result_must_remain_descriptive(self) -> TimeSeriesDiagnosticsResult:
        non_negative_fields = {
            "duplicate_count": self.duplicate_count,
            "gap_count": self.gap_count,
            "interval_count": self.interval_count,
        }
        for field_name, value in non_negative_fields.items():
            if value is not None and value < 0:
                raise ValueError(f"{field_name} cannot be negative")
        interval_values = [
            self.min_interval_seconds,
            self.max_interval_seconds,
            self.mean_interval_seconds,
        ]
        if any(value is not None and (not math.isfinite(value) or value < 0) for value in interval_values):
            raise ValueError("interval summary values must be finite and non-negative")
        if self.trade_signal:
            raise ValueError("time-series diagnostics results cannot be trade signals")
        if self.recommendation:
            raise ValueError("time-series diagnostics results cannot be recommendations")
        if self.decision_object_generated:
            raise ValueError("time-series diagnostics results cannot generate DecisionObjects")
        if not self.descriptive_only:
            raise ValueError("time-series diagnostics results must remain descriptive-only")
        if self.safety_label == TimeSeriesDiagnosticSafetyLabel.UNKNOWN:
            raise ValueError("time-series diagnostics safety label cannot be UNKNOWN")
        return self


def create_timestamp_series(
    series_id: str,
    name: str,
    timestamps: list[datetime],
    source: NumericalSourceReference,
    require_timezone_aware: bool = True,
) -> TimestampSeriesContract:
    return TimestampSeriesContract(
        series_id=series_id,
        name=name,
        timestamps=timestamps,
        source=source,
        require_timezone_aware=require_timezone_aware,
    )


def create_time_series_diagnostics_request(
    request_id: str,
    timestamp_series: TimestampSeriesContract,
    diagnostics: list[TimeSeriesDiagnosticKind],
    expected_interval_seconds: int | None = None,
) -> TimeSeriesDiagnosticsRequest:
    return TimeSeriesDiagnosticsRequest(
        request_id=request_id,
        timestamp_series=timestamp_series,
        diagnostics=diagnostics,
        expected_interval_seconds=expected_interval_seconds,
    )


def create_time_series_diagnostics_result(
    result_id: str,
    request_id: str,
    source: NumericalSourceReference,
    observation_count: int,
    status: str = "ok",
    error: str | None = None,
    order_status: TimestampOrderStatus | None = None,
    duplicate_count: int | None = None,
    duplicate_timestamps: list[datetime] | None = None,
    gap_count: int | None = None,
    gaps: list[TimestampGap] | None = None,
    interval_count: int | None = None,
    min_interval_seconds: float | None = None,
    max_interval_seconds: float | None = None,
    mean_interval_seconds: float | None = None,
) -> TimeSeriesDiagnosticsResult:
    return TimeSeriesDiagnosticsResult(
        result_id=result_id,
        request_id=request_id,
        source=source,
        observation_count=observation_count,
        order_status=order_status,
        duplicate_count=duplicate_count,
        duplicate_timestamps=duplicate_timestamps or [],
        gap_count=gap_count,
        gaps=gaps or [],
        interval_count=interval_count,
        min_interval_seconds=min_interval_seconds,
        max_interval_seconds=max_interval_seconds,
        mean_interval_seconds=mean_interval_seconds,
        status=status,
        error=error,
    )

