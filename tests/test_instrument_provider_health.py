from stark_terminal_core.config.settings import Settings
from stark_terminal_data_platform.instruments.health import check_instrument_master_health
from stark_terminal_data_platform.providers.health import check_provider_contract_health


def test_instrument_health_uses_local_synthetic_fixtures() -> None:
    status = check_instrument_master_health(Settings())

    assert status.configured is True
    assert status.mode == "local"
    assert status.source == "synthetic"
    assert status.instrument_count == 6
    assert status.external_calls_allowed is False
    assert status.provider_network_calls_allowed is False
    assert status.status == "HEALTHY"
    assert "secret" not in status.model_dump_json()


def test_provider_health_uses_local_sample_provider() -> None:
    status = check_provider_contract_health(Settings())

    assert status.provider_count == 1
    assert status.default_provider == "local_sample"
    assert status.external_calls_allowed is False
    assert status.network_calls_allowed is False
    assert status.providers == ["local_sample"]
    assert status.status == "HEALTHY"
    assert "secret" not in status.model_dump_json()
