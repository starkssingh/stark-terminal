from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import Timeframe
from stark_terminal_data_platform.fixtures.catalog import create_default_synthetic_fixture_catalog
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_ohlcv_bars
from stark_terminal_data_platform.fixtures.validation import validate_fixture_bars
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.quality.enums import ValidationStatus


class FixtureHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    default_seed: int
    default_bar_count: int
    default_timeframe: str
    disk_writes_allowed: bool
    catalog_count: int
    sample_generation_ok: bool
    validation_ok: bool
    status: str
    error: str | None = None


def check_fixture_health(settings: Settings | None = None) -> FixtureHealthStatus:
    resolved = settings or get_settings()
    catalog_count = 0
    sample_generation_ok = False
    validation_ok = False
    status = "disabled" if not resolved.synthetic_fixtures_enabled else "healthy"
    error: str | None = None

    try:
        catalog = create_default_synthetic_fixture_catalog(settings=resolved)
        catalog_count = len(catalog.list_manifests())
        instrument = create_sample_instruments()[0]
        config = SyntheticOHLCVConfig(
            instrument_id=instrument.instrument_id,
            timeframe=Timeframe(resolved.synthetic_fixture_default_timeframe),
            start_timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc),
            bar_count=min(resolved.synthetic_fixture_default_bar_count, 3),
            start_price=resolved.synthetic_fixture_default_start_price,
            seed=resolved.synthetic_fixture_default_seed,
            source_data_reference=resolved.synthetic_fixture_label,
        )
        bars = generate_synthetic_ohlcv_bars(config)
        sample_generation_ok = bool(bars)
        report = validate_fixture_bars(bars, settings=resolved)
        validation_ok = report.status == ValidationStatus.PASS
        if resolved.synthetic_fixtures_enabled and (not sample_generation_ok or not validation_ok):
            status = "unhealthy"
    except Exception as exc:
        status = "unhealthy"
        error = str(exc) or "fixture health check failed"

    return FixtureHealthStatus(
        enabled=resolved.synthetic_fixtures_enabled,
        schema_version=resolved.synthetic_fixture_schema_version,
        default_seed=resolved.synthetic_fixture_default_seed,
        default_bar_count=resolved.synthetic_fixture_default_bar_count,
        default_timeframe=resolved.synthetic_fixture_default_timeframe,
        disk_writes_allowed=resolved.synthetic_fixture_allow_disk_writes,
        catalog_count=catalog_count,
        sample_generation_ok=sample_generation_ok,
        validation_ok=validation_ok,
        status=status,
        error=error,
    )
