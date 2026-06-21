from __future__ import annotations

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.market_data import MarketDataBar, MarketDataBatch
from stark_terminal_data_platform.fixtures.manifests import (
    FixtureManifest,
    text_implies_real_market_data,
    text_mentions_synthetic_local_test,
)
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_market_data_batch
from stark_terminal_data_platform.quality.builtins import MarketDataBarValidator
from stark_terminal_data_platform.quality.enums import ValidationScope, ValidationSeverity
from stark_terminal_data_platform.quality.issues import ValidationIssue
from stark_terminal_data_platform.quality.reports import ValidationReport, build_validation_report
from stark_terminal_data_platform.quality.results import fail_result, pass_result


def _settings(settings: Settings | None) -> Settings:
    return settings or get_settings()


def validate_fixture_bars(bars: list[MarketDataBar], settings: Settings | None = None) -> ValidationReport:
    resolved = _settings(settings)
    if not bars:
        result = fail_result(
            ValidationScope.MARKET_DATA_BAR,
            "fixture_bars",
            ValidationIssue(
                code="FIXTURE_BARS_EMPTY",
                severity=ValidationSeverity.ERROR,
                message="fixture bars cannot be empty",
                scope=ValidationScope.MARKET_DATA_BAR,
            ),
        )
        return build_validation_report(ValidationScope.MARKET_DATA_BAR, "fixture_bars", [result], resolved)

    validator = MarketDataBarValidator(settings=resolved)
    results = []
    for bar in bars:
        results.extend(validator.validate(bar).results)
    return build_validation_report(
        ValidationScope.MARKET_DATA_BAR,
        "fixture_bars",
        results,
        resolved,
        source_data_reference=bars[0].source_data_reference,
        notes=["synthetic local-only test/dev fixture validation"],
    )


def validate_fixture_batch(batch: MarketDataBatch, settings: Settings | None = None) -> ValidationReport:
    return validate_fixture_bars(batch.bars, settings=settings)


def validate_fixture_manifest(manifest: FixtureManifest, settings: Settings | None = None) -> ValidationReport:
    resolved = _settings(settings)
    results = []
    if not text_mentions_synthetic_local_test(manifest.label):
        results.append(
            fail_result(
                ValidationScope.UNKNOWN,
                manifest.fixture_id,
                ValidationIssue(
                    code="FIXTURE_LABEL_NOT_SYNTHETIC",
                    severity=ValidationSeverity.ERROR,
                    message="fixture label must include synthetic, local, and test semantics",
                    field="label",
                    scope=ValidationScope.UNKNOWN,
                ),
            )
        )
    if manifest.source_data_reference:
        if text_implies_real_market_data(manifest.source_data_reference) or not text_mentions_synthetic_local_test(manifest.source_data_reference):
            results.append(
                fail_result(
                    ValidationScope.UNKNOWN,
                    manifest.fixture_id,
                    ValidationIssue(
                        code="FIXTURE_SOURCE_REFERENCE_INVALID",
                        severity=ValidationSeverity.ERROR,
                        message="fixture source reference must be synthetic local test data only",
                        field="source_data_reference",
                        scope=ValidationScope.UNKNOWN,
                    ),
                )
            )
    if manifest.row_count is not None and manifest.row_count < 0:
        results.append(
            fail_result(
                ValidationScope.UNKNOWN,
                manifest.fixture_id,
                ValidationIssue(
                    code="FIXTURE_ROW_COUNT_NEGATIVE",
                    severity=ValidationSeverity.ERROR,
                    message="fixture row_count cannot be negative",
                    field="row_count",
                    scope=ValidationScope.UNKNOWN,
                ),
            )
        )
    if manifest.start_timestamp and manifest.end_timestamp and manifest.start_timestamp >= manifest.end_timestamp:
        results.append(
            fail_result(
                ValidationScope.UNKNOWN,
                manifest.fixture_id,
                ValidationIssue(
                    code="FIXTURE_TIME_RANGE_INVALID",
                    severity=ValidationSeverity.ERROR,
                    message="fixture start_timestamp must be before end_timestamp",
                    field="start_timestamp",
                    scope=ValidationScope.UNKNOWN,
                ),
            )
        )
    if not results:
        results.append(
            pass_result(
                ValidationScope.UNKNOWN,
                manifest.fixture_id,
                metadata={"kind": manifest.kind.value, "label": manifest.label},
            )
        )
    return build_validation_report(
        ValidationScope.UNKNOWN,
        manifest.fixture_id,
        results,
        resolved,
        source_data_reference=manifest.source_data_reference,
        notes=["synthetic fixture manifest validation"],
    )


def validate_generated_fixture(config: SyntheticOHLCVConfig, settings: Settings | None = None) -> ValidationReport:
    resolved = _settings(settings)
    try:
        batch = generate_synthetic_market_data_batch(config)
    except Exception as exc:
        result = fail_result(
            ValidationScope.MARKET_DATA_BAR,
            str(config.instrument_id),
            ValidationIssue(
                code="FIXTURE_GENERATION_FAILED",
                severity=ValidationSeverity.ERROR,
                message=str(exc) or "synthetic fixture generation failed",
                scope=ValidationScope.MARKET_DATA_BAR,
            ),
        )
        return build_validation_report(ValidationScope.MARKET_DATA_BAR, str(config.instrument_id), [result], resolved)
    return validate_fixture_batch(batch, settings=resolved)
