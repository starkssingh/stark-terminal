from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.domain.enums import MarketDataRequestKind
from stark_terminal_core.domain.market_data_contracts import create_market_data_request
from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.providers.local_sample import (
    LOCAL_SAMPLE_SOURCE_REFERENCE,
    UNSUPPORTED_LOCAL_SAMPLE_CAPABILITIES,
    LocalSampleProviderAdapter,
    sample_historical_bars_request,
)

router = APIRouter()


def _provider() -> LocalSampleProviderAdapter:
    return LocalSampleProviderAdapter(settings=get_settings())


@router.get("/local-sample-provider/health")
def local_sample_provider_health() -> dict[str, Any]:
    status = _provider().health_check()
    return {
        "service": "stark-terminal-local-sample-provider",
        **status.model_dump(),
    }


@router.get("/local-sample-provider/contracts")
def local_sample_provider_contracts() -> dict[str, Any]:
    settings = get_settings()
    provider = _provider()
    capabilities = provider.capabilities()
    return {
        "service": "stark-terminal-local-sample-provider",
        "provider_name": provider.provider_id.name,
        "synthetic_only": True,
        "real_market_data": False,
        "network_calls": False,
        "credentials_required": False,
        "supported_capabilities": [capability.value for capability in capabilities.capabilities],
        "unsupported_capabilities": [capability.value for capability in UNSUPPORTED_LOCAL_SAMPLE_CAPABILITIES],
        "schema_version": settings.local_sample_provider_schema_version,
        "source_data_reference": LOCAL_SAMPLE_SOURCE_REFERENCE,
    }


@router.get("/local-sample-provider/instruments")
def local_sample_provider_instruments() -> dict[str, Any]:
    provider = _provider()
    request = create_market_data_request(
        MarketDataRequestKind.INSTRUMENT_MASTER,
        provider=provider.provider_id,
        schema_version=get_settings().local_sample_provider_schema_version,
    )
    response = provider.get_instrument_master(request)
    return {
        "service": "stark-terminal-local-sample-provider",
        "synthetic": True,
        "real_market_data": False,
        "source_data_reference": LOCAL_SAMPLE_SOURCE_REFERENCE,
        "count": len(response.instruments),
        "instruments": to_jsonable(response.instruments),
        "errors": response.errors,
    }


@router.get("/local-sample-provider/sample-bars")
def local_sample_provider_sample_bars() -> dict[str, Any]:
    provider = _provider()
    request = sample_historical_bars_request(settings=get_settings())
    response = provider.get_historical_bars(request)
    return {
        "service": "stark-terminal-local-sample-provider",
        "synthetic": True,
        "real_market_data": False,
        "source_data_reference": LOCAL_SAMPLE_SOURCE_REFERENCE,
        "count": min(len(response.bars), 5),
        "bars": to_jsonable(response.bars[:5]),
        "errors": response.errors,
        "note": "Synthetic local sample test/dev only; not live market data and not a trading signal.",
    }
