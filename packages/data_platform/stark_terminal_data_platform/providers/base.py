from __future__ import annotations

from stark_terminal_core.domain.enums import (
    DataProviderType,
    DataQualityStatus,
    MarketDataRequestKind,
    ProviderCapability,
    ProviderStatus,
)
from stark_terminal_core.domain.identifiers import DataProviderId
from stark_terminal_core.domain.market_data_contracts import (
    MarketDataRequest,
    MarketDataResponse,
)
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.instruments.master import LocalInstrumentMaster
from stark_terminal_data_platform.providers.contracts import ProviderCapabilityReport


class MarketDataProvider:
    provider_id: DataProviderId = DataProviderId(
        name="base_unavailable",
        provider_type=DataProviderType.UNKNOWN,
        version="v1",
    )

    def __init__(self, network_calls_allowed: bool = False) -> None:
        self.network_calls_allowed = network_calls_allowed

    def capabilities(self) -> ProviderCapabilityReport:
        return ProviderCapabilityReport(
            provider=self.provider_id,
            status=ProviderStatus.UNAVAILABLE,
            capabilities=[],
            network_calls_allowed=self.network_calls_allowed,
            notes=["Base provider contract only; no external calls are implemented."],
        )

    def health_check(self) -> ProviderCapabilityReport:
        return self.capabilities()

    def _unavailable_response(self, request: MarketDataRequest, reason: str) -> MarketDataResponse:
        return MarketDataResponse(
            request_id=request.request_id,
            kind=request.kind,
            provider=self.provider_id,
            quality_status=DataQualityStatus.UNKNOWN,
            errors=[reason],
        )

    def get_instrument_master(self, request: MarketDataRequest) -> MarketDataResponse:
        return self._unavailable_response(request, "Provider instrument master is unavailable")

    def get_historical_bars(self, request: MarketDataRequest) -> MarketDataResponse:
        return self._unavailable_response(request, "Provider historical bars are unavailable")

    def get_latest_bar(self, request: MarketDataRequest) -> MarketDataResponse:
        return self._unavailable_response(request, "Provider latest bar is unavailable")

    def get_options_chain(self, request: MarketDataRequest) -> MarketDataResponse:
        return self._unavailable_response(request, "Provider options chain is unavailable")

    def get_futures_chain(self, request: MarketDataRequest) -> MarketDataResponse:
        return self._unavailable_response(request, "Provider futures chain is unavailable")


class LocalSampleMarketDataProvider(MarketDataProvider):
    provider_id = DataProviderId(
        name="local_sample",
        provider_type=DataProviderType.LOCAL_SAMPLE,
        version="synthetic-v1",
    )

    def __init__(
        self,
        instrument_master: LocalInstrumentMaster | None = None,
        network_calls_allowed: bool = False,
    ) -> None:
        super().__init__(network_calls_allowed=network_calls_allowed)
        self.instrument_master = instrument_master or LocalInstrumentMaster(
            create_sample_instruments(),
            source="synthetic",
            schema_version="v1",
        )

    def capabilities(self) -> ProviderCapabilityReport:
        return ProviderCapabilityReport(
            provider=self.provider_id,
            status=ProviderStatus.ENABLED,
            capabilities=[
                ProviderCapability.INSTRUMENT_MASTER,
                ProviderCapability.HEALTH_CHECK,
            ],
            network_calls_allowed=self.network_calls_allowed,
            notes=["Synthetic/local sample provider. No external calls."],
        )

    def health_check(self) -> ProviderCapabilityReport:
        return self.capabilities()

    def get_instrument_master(self, request: MarketDataRequest) -> MarketDataResponse:
        if request.kind not in {
            MarketDataRequestKind.INSTRUMENT_MASTER,
            MarketDataRequestKind.HEALTH_CHECK,
        }:
            return self._unavailable_response(
                request,
                "Local sample provider only supports instrument master and health checks",
            )
        return MarketDataResponse(
            request_id=request.request_id,
            kind=request.kind,
            provider=self.provider_id,
            instruments=self.instrument_master.list_instruments(),
            quality_status=DataQualityStatus.NORMALIZED,
            source_data_reference="synthetic://local_sample/instruments",
        )
