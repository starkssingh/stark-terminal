from __future__ import annotations

from stark_terminal_data_platform.providers.base import MarketDataProvider
from stark_terminal_data_platform.providers.contracts import ProviderCapabilityReport


FORBIDDEN_PROVIDER_TERMS = (
    "execution",
    "order",
    "order_placement",
    "broker_credential",
    "broker_secret",
    "live_trading",
    "real_money",
)


class ProviderRegistryError(ValueError):
    """Raised when provider registry operations are invalid."""


def _provider_name(provider: MarketDataProvider) -> str:
    return provider.provider_id.name.strip().lower()


def _provider_is_forbidden(provider: MarketDataProvider) -> bool:
    name = _provider_name(provider)
    return any(term in name for term in FORBIDDEN_PROVIDER_TERMS)


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, MarketDataProvider] = {}

    def register(self, provider: MarketDataProvider, replace: bool = False) -> None:
        name = _provider_name(provider)
        if not name:
            raise ProviderRegistryError("provider name cannot be empty")
        if _provider_is_forbidden(provider):
            raise ProviderRegistryError("execution/order/broker credential providers are forbidden")
        if name in self._providers and not replace:
            raise ProviderRegistryError(f"provider already registered: {name}")
        self._providers[name] = provider

    def unregister(self, provider_name: str) -> None:
        self._providers.pop(provider_name.strip().lower(), None)

    def get(self, provider_name: str) -> MarketDataProvider | None:
        return self._providers.get(provider_name.strip().lower())

    def list_providers(self) -> list[MarketDataProvider]:
        return list(self._providers.values())

    def capabilities(self) -> list[ProviderCapabilityReport]:
        return [provider.capabilities() for provider in self.list_providers()]

    def clear(self) -> None:
        self._providers.clear()
