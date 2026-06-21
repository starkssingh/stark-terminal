from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.providers.base import LocalSampleMarketDataProvider
from stark_terminal_data_platform.providers.registry import ProviderRegistry


class ProviderContractHealthStatus(BaseModel):
    provider_count: int
    default_provider: str
    external_calls_allowed: bool
    network_calls_allowed: bool
    providers: list[str]
    status: str
    error: str | None = None


def _default_registry() -> ProviderRegistry:
    registry = ProviderRegistry()
    registry.register(LocalSampleMarketDataProvider())
    return registry


def check_provider_contract_health(
    settings: Settings | None = None,
    registry: ProviderRegistry | None = None,
) -> ProviderContractHealthStatus:
    resolved_settings = settings or get_settings()
    resolved_registry = registry or _default_registry()
    providers = [provider.provider_id.name for provider in resolved_registry.list_providers()]
    status = "HEALTHY" if providers else "UNAVAILABLE"

    return ProviderContractHealthStatus(
        provider_count=len(providers),
        default_provider=resolved_settings.default_market_data_provider,
        external_calls_allowed=resolved_settings.allow_external_market_data_calls,
        network_calls_allowed=resolved_settings.allow_provider_network_calls,
        providers=providers,
        status=status,
        error=None,
    )
