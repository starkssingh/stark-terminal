from datetime import datetime, timedelta, timezone

from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import (
    DataProviderType,
    MarketDataRequestKind,
    Timeframe,
)
from stark_terminal_core.domain.identifiers import DataProviderId, InstrumentId
from stark_terminal_core.domain.market_data_contracts import (
    MarketDataRequest,
    MarketDataResponse,
    create_market_data_request,
)
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments


def instrument_id() -> InstrumentId:
    return InstrumentId(symbol="RELIANCE", exchange="NSE", segment="NSE_EQUITY")


def test_valid_instrument_master_request() -> None:
    request = create_market_data_request(MarketDataRequestKind.INSTRUMENT_MASTER)

    assert request.request_id
    assert request.kind == MarketDataRequestKind.INSTRUMENT_MASTER
    assert request.created_at.tzinfo is not None


def test_valid_historical_bars_request() -> None:
    start = datetime.now(timezone.utc)
    end = start + timedelta(days=1)

    request = create_market_data_request(
        MarketDataRequestKind.HISTORICAL_BARS,
        instrument_id=instrument_id(),
        timeframe=Timeframe.DAILY,
        start=start,
        end=end,
    )

    assert request.instrument_id == instrument_id()


def test_historical_bars_request_requires_shape_and_time_order() -> None:
    start = datetime.now(timezone.utc)
    with pytest.raises(ValidationError):
        MarketDataRequest(kind=MarketDataRequestKind.HISTORICAL_BARS)
    with pytest.raises(ValidationError):
        create_market_data_request(
            MarketDataRequestKind.HISTORICAL_BARS,
            instrument_id=instrument_id(),
            timeframe=Timeframe.DAILY,
            start=start,
            end=start,
        )


def test_provider_identity_must_not_contain_secret_text() -> None:
    provider = DataProviderId(
        name="database_url_provider",
        provider_type=DataProviderType.LOCAL_SAMPLE,
    )
    with pytest.raises(ValidationError):
        create_market_data_request(MarketDataRequestKind.HEALTH_CHECK, provider=provider)


def test_response_requires_content_and_sanitizes_errors() -> None:
    with pytest.raises(ValidationError):
        MarketDataResponse(request_id="r1", kind=MarketDataRequestKind.HEALTH_CHECK)

    response = MarketDataResponse(
        request_id="r1",
        kind=MarketDataRequestKind.INSTRUMENT_MASTER,
        instruments=create_sample_instruments(),
        errors=["database_url=postgresql://secret"],
    )

    assert response.errors == ["SanitizedMarketDataError"]
    assert len(response.instruments) == 6
