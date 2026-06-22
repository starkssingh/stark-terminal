from datetime import datetime, timedelta, timezone

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import (
    DataProviderType,
    MarketDataRequestKind,
    ProviderCapability,
    Timeframe,
)
from stark_terminal_core.domain.market_data_contracts import create_market_data_request
from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.providers.local_sample import (
    LOCAL_SAMPLE_SOURCE_REFERENCE,
    LocalSampleProviderAdapter,
)


def _historical_request():
    instrument = create_sample_instruments()[0]
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return create_market_data_request(
        MarketDataRequestKind.HISTORICAL_BARS,
        instrument_id=instrument.instrument_id,
        timeframe=Timeframe.DAILY,
        start=start,
        end=start + timedelta(days=10),
    )


def test_local_sample_provider_identity_capabilities_and_health() -> None:
    provider = LocalSampleProviderAdapter(settings=Settings())

    report = provider.capabilities()
    health = provider.health_check()

    assert provider.provider_id.name == "local_sample"
    assert provider.provider_id.provider_type == DataProviderType.LOCAL_SAMPLE
    assert provider.provider_id.version == "v0"
    assert ProviderCapability.INSTRUMENT_MASTER in report.capabilities
    assert ProviderCapability.HISTORICAL_BARS in report.capabilities
    assert ProviderCapability.HEALTH_CHECK in report.capabilities
    assert ProviderCapability.LATEST_BAR not in report.capabilities
    assert report.network_calls_allowed is False
    assert health.synthetic_only is True
    assert health.real_data_allowed is False
    assert health.network_allowed is False
    assert health.credentials_required is False
    assert health.status == "HEALTHY"


def test_instrument_master_response_is_synthetic_local_only() -> None:
    provider = LocalSampleProviderAdapter(settings=Settings())
    request = create_market_data_request(MarketDataRequestKind.INSTRUMENT_MASTER)

    response = provider.get_instrument_master(request)

    assert response.provider == provider.provider_id
    assert response.source_data_reference == LOCAL_SAMPLE_SOURCE_REFERENCE
    assert len(response.instruments) >= 5
    assert not response.errors
    assert "Synthetic" in response.instruments[0].display_name


def test_historical_bars_are_deterministic_and_synthetic() -> None:
    provider = LocalSampleProviderAdapter(settings=Settings())
    request = _historical_request()

    first = provider.get_historical_bars(request)
    second = provider.get_historical_bars(request)

    assert first.errors == []
    assert second.errors == []
    assert to_jsonable(first.bars) == to_jsonable(second.bars)
    assert len(first.bars) == 11
    for bar in first.bars:
        assert bar.provider == provider.provider_id
        assert bar.source_data_reference == LOCAL_SAMPLE_SOURCE_REFERENCE
        assert bar.timestamp.tzinfo is not None
        assert bar.high >= max(bar.open, bar.close, bar.low)
        assert bar.low <= min(bar.open, bar.close, bar.high)
        assert bar.volume is not None and bar.volume >= 0


def test_unsupported_capability_methods_return_safe_errors() -> None:
    provider = LocalSampleProviderAdapter(settings=Settings())
    latest = create_market_data_request(MarketDataRequestKind.LATEST_BAR)
    options = create_market_data_request(MarketDataRequestKind.OPTIONS_CHAIN)
    futures = create_market_data_request(MarketDataRequestKind.FUTURES_CHAIN)

    latest_response = provider.get_latest_bar(latest)
    options_response = provider.get_options_chain(options)
    futures_response = provider.get_futures_chain(futures)

    assert latest_response.errors
    assert options_response.errors
    assert futures_response.errors
    assert "live" not in str(options_response.model_dump()).lower()
    assert "execution" not in str(latest_response.model_dump()).lower()
