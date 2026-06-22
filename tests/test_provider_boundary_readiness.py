from pathlib import Path

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_data_platform.providers.guardrails import default_provider_guardrail_policy
from stark_terminal_data_platform.providers.local_file import (
    LocalFileProviderAdapter,
    validate_local_file_path,
)
from stark_terminal_data_platform.providers.local_sample import LocalSampleProviderAdapter
from stark_terminal_data_platform.providers.selection import check_provider_readiness_health


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_local_sample_provider_remains_synthetic_local_only() -> None:
    provider = LocalSampleProviderAdapter()
    health = provider.health_check()
    capabilities = provider.capabilities()

    assert health.synthetic_only is True
    assert health.real_data_allowed is False
    assert health.network_allowed is False
    assert health.credentials_required is False
    assert ProviderCapability.HISTORICAL_BARS in capabilities.capabilities
    assert ProviderCapability.LATEST_BAR not in capabilities.capabilities


def test_local_file_provider_remains_local_file_only() -> None:
    provider = LocalFileProviderAdapter()
    health = provider.health_check()
    capabilities = provider.capabilities()

    assert health.synthetic_or_local_only is True
    assert health.real_data_claims_allowed is False
    assert health.network_allowed is False
    assert health.credentials_required is False
    assert ProviderCapability.HISTORICAL_BARS in capabilities.capabilities
    assert ProviderCapability.LATEST_BAR not in capabilities.capabilities


def test_local_file_api_exposes_no_arbitrary_file_read_route() -> None:
    api_inventory = _read("docs/API_SURFACE_INVENTORY.md")
    route = _read("apps/api/stark_terminal_api/routes/local_file_provider.py")

    assert "/local-file-provider/contracts" in api_inventory
    assert "no arbitrary file read API" in api_inventory
    assert "path:" not in route
    assert "@router.post" not in route


def test_provider_readiness_remains_governance_only() -> None:
    status = check_provider_readiness_health()

    assert status.real_implementation_allowed is False
    assert status.network_checks_allowed is False
    assert status.scraping_checks_allowed is False
    assert status.credentials_allowed is False
    assert status.status == "HEALTHY"


def test_guardrails_and_settings_block_production_provider_behavior() -> None:
    settings = Settings()
    policy = default_provider_guardrail_policy(settings)

    assert policy.execution_allowed is False
    assert policy.network_calls_allowed is False
    assert policy.scraping_allowed is False
    assert policy.credentials_allowed is False
    assert policy.real_ingestion_allowed is False
    assert settings.provider_candidate_real_implementation_allowed is False
    assert settings.provider_candidate_credentials_allowed is False


def test_local_file_path_validation_rejects_network_path() -> None:
    try:
        validate_local_file_path("https://example.invalid/file.csv", settings=Settings())
    except ValueError as exc:
        assert "network paths are forbidden" in str(exc)
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("network path unexpectedly passed validation")
