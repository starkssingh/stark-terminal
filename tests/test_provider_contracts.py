from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import (
    DataProviderType,
    MarketDataRequestKind,
    ProviderCapability,
    ProviderStatus,
)
from stark_terminal_core.domain.identifiers import DataProviderId
from stark_terminal_core.domain.market_data_contracts import create_market_data_request
from stark_terminal_data_platform.providers.base import (
    LocalSampleMarketDataProvider,
    MarketDataProvider,
)
from stark_terminal_data_platform.providers.contracts import ProviderCapabilityReport


def test_provider_capability_report_validation() -> None:
    provider = DataProviderId(name="local_sample", provider_type=DataProviderType.LOCAL_SAMPLE)

    report = ProviderCapabilityReport(
        provider=provider,
        status=ProviderStatus.DISABLED,
        capabilities=[],
        network_calls_allowed=False,
    )
    assert report.status == ProviderStatus.DISABLED

    with pytest.raises(ValidationError):
        ProviderCapabilityReport(
            provider=provider,
            status=ProviderStatus.ENABLED,
            capabilities=[],
            network_calls_allowed=False,
        )


def test_base_provider_returns_safe_unavailable_response() -> None:
    provider = MarketDataProvider()
    request = create_market_data_request(MarketDataRequestKind.HEALTH_CHECK)

    response = provider.get_latest_bar(request)

    assert response.errors
    assert response.provider == provider.provider_id


def test_local_sample_provider_capabilities_and_instrument_master_response() -> None:
    provider = LocalSampleMarketDataProvider()
    request = create_market_data_request(MarketDataRequestKind.INSTRUMENT_MASTER)

    report = provider.capabilities()
    response = provider.get_instrument_master(request)

    assert ProviderCapability.INSTRUMENT_MASTER in report.capabilities
    assert ProviderCapability.HEALTH_CHECK in report.capabilities
    assert report.network_calls_allowed is False
    assert len(response.instruments) == 6
    assert not response.errors
    assert "execution" not in provider.provider_id.name.lower()
