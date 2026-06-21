from __future__ import annotations

from datetime import datetime, timedelta, timezone

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import FixtureKind, Timeframe
from stark_terminal_data_platform.fixtures.manifests import FixtureManifest, create_fixture_manifest
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments


class FixtureCatalog:
    def __init__(self, manifests: list[FixtureManifest] | None = None) -> None:
        self._manifests: dict[str, FixtureManifest] = {}
        for manifest in manifests or []:
            self.register_manifest(manifest)

    def register_manifest(self, manifest: FixtureManifest, *, replace: bool = False) -> None:
        if manifest.fixture_id in self._manifests and not replace:
            raise ValueError(f"fixture already registered: {manifest.fixture_id}")
        self._manifests[manifest.fixture_id] = manifest

    def list_manifests(self) -> list[FixtureManifest]:
        return [self._manifests[key] for key in sorted(self._manifests)]

    def get_manifest(self, fixture_id: str) -> FixtureManifest | None:
        return self._manifests.get(fixture_id)

    def clear(self) -> None:
        self._manifests.clear()


def _manifest_for_instrument(settings: Settings, symbol: str, instrument_key: str, seed: int) -> FixtureManifest:
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    timeframe = Timeframe(settings.synthetic_fixture_default_timeframe)
    if timeframe == Timeframe.DAILY:
        step = timedelta(days=1)
    elif timeframe == Timeframe.FIFTEEN_MINUTE:
        step = timedelta(minutes=15)
    elif timeframe == Timeframe.FIVE_MINUTE:
        step = timedelta(minutes=5)
    else:
        step = timedelta(days=1)
    end = start + (step * max(settings.synthetic_fixture_default_bar_count - 1, 1))
    return create_fixture_manifest(
        fixture_id=f"synthetic_ohlcv_{symbol.lower()}",
        name=f"Synthetic OHLCV {symbol}",
        kind=FixtureKind.SYNTHETIC_OHLCV,
        label=settings.synthetic_fixture_label,
        schema_version=settings.synthetic_fixture_schema_version,
        instrument_key=instrument_key,
        row_count=settings.synthetic_fixture_default_bar_count,
        timeframe=timeframe,
        start_timestamp=start,
        end_timestamp=end,
        seed=seed,
        source_data_reference=settings.synthetic_fixture_label,
        notes=[
            "synthetic local-only test/dev metadata",
            "not real market data",
            "not trading data",
        ],
    )


def create_default_synthetic_fixture_catalog(settings: Settings | None = None) -> FixtureCatalog:
    resolved = settings or get_settings()
    wanted_symbols = {"RELIANCE", "HDFCBANK", "TCS", "NIFTY", "BANKNIFTY"}
    manifests: list[FixtureManifest] = []
    for offset, instrument in enumerate(create_sample_instruments()):
        symbol = instrument.instrument_id.symbol
        if symbol not in wanted_symbols:
            continue
        manifests.append(
            _manifest_for_instrument(
                resolved,
                symbol,
                str(instrument.instrument_id),
                resolved.synthetic_fixture_default_seed + offset,
            )
        )
    return FixtureCatalog(manifests)
