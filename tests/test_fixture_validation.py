from datetime import datetime, timezone

from stark_terminal_core.domain.enums import Exchange, FixtureKind, MarketSegment, Timeframe
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_data_platform.fixtures.manifests import FixtureManifest, create_fixture_manifest
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import (
    SyntheticOHLCVConfig,
    generate_synthetic_market_data_batch,
    generate_synthetic_ohlcv_bars,
)
from stark_terminal_data_platform.fixtures.validation import (
    validate_fixture_bars,
    validate_fixture_batch,
    validate_fixture_manifest,
    validate_generated_fixture,
)
from stark_terminal_data_platform.quality.enums import ValidationStatus


def _config(source_data_reference: str = "synthetic-local-test-only") -> SyntheticOHLCVConfig:
    return SyntheticOHLCVConfig(
        instrument_id=InstrumentId(symbol="RELIANCE", exchange=Exchange.NSE, segment=MarketSegment.NSE_EQUITY),
        timeframe=Timeframe.DAILY,
        start_timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc),
        bar_count=3,
        start_price=100.0,
        source_data_reference=source_data_reference,
    )


def test_valid_generated_bars_pass_validation() -> None:
    report = validate_fixture_bars(generate_synthetic_ohlcv_bars(_config()))

    assert report.status == ValidationStatus.PASS


def test_valid_generated_batch_passes_validation() -> None:
    report = validate_fixture_batch(generate_synthetic_market_data_batch(_config()))

    assert report.status == ValidationStatus.PASS


def test_valid_manifest_passes_validation() -> None:
    manifest = create_fixture_manifest("fixture", "Synthetic", FixtureKind.SYNTHETIC_OHLCV)

    report = validate_fixture_manifest(manifest)

    assert report.status == ValidationStatus.PASS


def test_bad_manifest_fails_validation() -> None:
    manifest = FixtureManifest.model_construct(
        fixture_id="bad_fixture",
        name="Bad Fixture",
        kind=FixtureKind.SYNTHETIC_OHLCV,
        label="live",
        schema_version="v1",
        source_data_reference="live-provider-feed",
        row_count=-1,
        notes=[],
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )

    report = validate_fixture_manifest(manifest)

    assert report.status == ValidationStatus.FAIL
    assert report.error_count >= 1


def test_validate_generated_fixture_passes() -> None:
    report = validate_generated_fixture(_config())

    assert report.status == ValidationStatus.PASS
