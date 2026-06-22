from datetime import datetime, timedelta, timezone

from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import MarketDataRequestKind, Timeframe
from stark_terminal_core.domain.market_data_contracts import MarketDataRequest, create_market_data_request
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.providers.local_sample import (
    LOCAL_SAMPLE_SOURCE_REFERENCE,
    LocalSampleProviderAdapter,
)
from stark_terminal_data_platform.quality.builtins import MarketDataResponseValidator
from stark_terminal_data_platform.quality.enums import ValidationStatus


def _request(timeframe: Timeframe = Timeframe.DAILY):
    instrument = create_sample_instruments()[0]
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return create_market_data_request(
        MarketDataRequestKind.HISTORICAL_BARS,
        instrument_id=instrument.instrument_id,
        timeframe=timeframe,
        start=start,
        end=start + timedelta(days=5),
    )


def test_historical_response_passes_data_quality_validation() -> None:
    provider = LocalSampleProviderAdapter(settings=Settings())
    response = provider.get_historical_bars(_request())

    report = MarketDataResponseValidator(settings=Settings()).validate(response)

    assert report.status == ValidationStatus.PASS
    assert response.source_data_reference == LOCAL_SAMPLE_SOURCE_REFERENCE


def test_invalid_request_shape_returns_sanitized_error_without_crashing() -> None:
    provider = LocalSampleProviderAdapter(settings=Settings())
    unsafe_request = MarketDataRequest.model_construct(
        request_id="unsafe_local_sample_request",
        kind=MarketDataRequestKind.HISTORICAL_BARS,
        instrument_id=None,
        timeframe=None,
        start=None,
        end=None,
        provider=None,
        schema_version="v1",
        created_at=datetime.now(timezone.utc),
    )

    response = provider.get_historical_bars(unsafe_request)

    assert response.errors
    assert "missing required fields" in response.errors[0].lower()
    assert "password" not in str(response.model_dump()).lower()
    assert "secret" not in str(response.model_dump()).lower()


def test_unsupported_timeframe_returns_safe_error() -> None:
    provider = LocalSampleProviderAdapter(settings=Settings())
    request = _request(Timeframe.WEEKLY)

    response = provider.get_historical_bars(request)

    assert response.errors
    assert "supports only" in response.errors[0]


def test_settings_reject_invalid_local_sample_provider_values() -> None:
    with pytest.raises(ValidationError):
        Settings(local_sample_provider_schema_version="")
    with pytest.raises(ValidationError):
        Settings(local_sample_provider_default_bar_count=0)
    with pytest.raises(ValidationError):
        Settings(local_sample_provider_default_start_price=0)
