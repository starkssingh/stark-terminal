import pytest

from stark_terminal_core.domain.enums import DataProviderType
from stark_terminal_core.domain.identifiers import DataProviderId
from stark_terminal_data_platform.providers.base import LocalSampleMarketDataProvider
from stark_terminal_data_platform.providers.registry import ProviderRegistry, ProviderRegistryError


def test_provider_registry_register_get_list_unregister_clear() -> None:
    registry = ProviderRegistry()
    provider = LocalSampleMarketDataProvider()

    registry.register(provider)

    assert registry.get("local_sample") is provider
    assert registry.list_providers() == [provider]
    assert len(registry.capabilities()) == 1

    registry.unregister("local_sample")
    assert registry.get("local_sample") is None

    registry.register(provider)
    registry.clear()
    assert registry.list_providers() == []


def test_provider_registry_duplicate_requires_replace() -> None:
    registry = ProviderRegistry()
    first = LocalSampleMarketDataProvider()
    second = LocalSampleMarketDataProvider()

    registry.register(first)
    with pytest.raises(ProviderRegistryError):
        registry.register(second)

    registry.register(second, replace=True)
    assert registry.get("local_sample") is second


def test_provider_registry_rejects_execution_provider_name() -> None:
    class ExecutionProvider(LocalSampleMarketDataProvider):
        provider_id = DataProviderId(
            name="execution_provider",
            provider_type=DataProviderType.LOCAL_SAMPLE,
        )

    with pytest.raises(ProviderRegistryError):
        ProviderRegistry().register(ExecutionProvider())
