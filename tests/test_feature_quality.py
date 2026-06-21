from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import FeatureQualityStatus
from stark_terminal_data_platform.features.quality import (
    FeatureQualityReport,
    create_quality_report,
    summarize_quality,
)


def test_valid_quality_report_creation() -> None:
    report = create_quality_report(
        report_id="quality-1",
        feature_set_name="instrument_daily_features",
        status=FeatureQualityStatus.WARN,
        row_count=10,
        missing_value_count=1,
        warnings=["missing values"],
    )

    summary = summarize_quality(report)
    assert summary["status"] == "WARN"
    assert summary["warning_count"] == 1
    assert report.generated_at.tzinfo is not None


@pytest.mark.parametrize("field", ["row_count", "missing_value_count", "stale_value_count", "invalid_value_count"])
def test_quality_report_rejects_negative_counts(field: str) -> None:
    with pytest.raises(ValidationError):
        FeatureQualityReport(
            report_id="quality-1",
            feature_set_name="instrument_daily_features",
            status=FeatureQualityStatus.WARN,
            **{field: -1},
        )


def test_pass_quality_report_rejects_errors() -> None:
    with pytest.raises(ValidationError):
        FeatureQualityReport(
            report_id="quality-1",
            feature_set_name="instrument_daily_features",
            status=FeatureQualityStatus.PASS,
            errors=["bad row"],
        )


def test_quality_messages_are_sanitized() -> None:
    report = FeatureQualityReport(
        report_id="quality-1",
        feature_set_name="instrument_daily_features",
        status=FeatureQualityStatus.WARN,
        warnings=["token leaked"],
    )
    assert report.warnings == ["[redacted]"]

