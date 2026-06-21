from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import FeatureQualityStatus
from stark_terminal_data_platform.features.definitions import _normalize_non_empty


SECRET_TEXT_PARTS = ("password", "secret", "token", "api_key", "broker", "credential")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _sanitize_text(value: str) -> str:
    normalized = _normalize_non_empty(value, "quality message")
    lowered = normalized.lower()
    if any(part in lowered for part in SECRET_TEXT_PARTS):
        return "[redacted]"
    return normalized


class FeatureQualityReport(BaseModel):
    report_id: str
    feature_set_name: str
    feature_set_version: str = "v1"
    status: FeatureQualityStatus
    row_count: int | None = None
    missing_value_count: int | None = None
    stale_value_count: int | None = None
    invalid_value_count: int | None = None
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=_utc_now)
    source_data_reference: str | None = None

    @field_validator("report_id", "feature_set_name", "feature_set_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _normalize_non_empty(value, "feature quality field")

    @field_validator("row_count", "missing_value_count", "stale_value_count", "invalid_value_count")
    @classmethod
    def counts_must_be_non_negative(cls, value: int | None) -> int | None:
        if value is not None and value < 0:
            raise ValueError("feature quality counts must be non-negative")
        return value

    @field_validator("warnings", "errors")
    @classmethod
    def messages_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return [_sanitize_text(item) for item in value]

    @field_validator("generated_at")
    @classmethod
    def generated_at_must_be_utc_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def pass_reports_must_not_have_errors(self) -> FeatureQualityReport:
        if self.status == FeatureQualityStatus.PASS and self.errors:
            raise ValueError("PASS feature quality reports cannot contain errors")
        return self


def create_quality_report(
    report_id: str,
    feature_set_name: str,
    status: FeatureQualityStatus,
    feature_set_version: str = "v1",
    row_count: int | None = None,
    missing_value_count: int | None = None,
    stale_value_count: int | None = None,
    invalid_value_count: int | None = None,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
    source_data_reference: str | None = None,
) -> FeatureQualityReport:
    return FeatureQualityReport(
        report_id=report_id,
        feature_set_name=feature_set_name,
        feature_set_version=feature_set_version,
        status=status,
        row_count=row_count,
        missing_value_count=missing_value_count,
        stale_value_count=stale_value_count,
        invalid_value_count=invalid_value_count,
        warnings=warnings or [],
        errors=errors or [],
        source_data_reference=source_data_reference,
    )


def summarize_quality(report: FeatureQualityReport) -> dict[str, int | str | None]:
    return {
        "status": report.status.value,
        "row_count": report.row_count,
        "missing_value_count": report.missing_value_count,
        "stale_value_count": report.stale_value_count,
        "invalid_value_count": report.invalid_value_count,
        "warning_count": len(report.warnings),
        "error_count": len(report.errors),
    }

