from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_instrument_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "13"
    assert settings.instrument_master_mode == "local"
    assert settings.instrument_master_source == "synthetic"
    assert settings.allow_external_market_data_calls is False
    assert settings.allow_provider_network_calls is False
    assert settings.market_data_contract_schema_version == "v1"
    assert settings.default_market_data_provider == "local_sample"
    assert settings.default_exchange == "NSE"
    assert settings.default_market_segment == "NSE_EQUITY"


def test_instrument_settings_safe_snapshot_includes_contract_fields() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["instrument_master_mode"] == "local"
    assert snapshot["instrument_master_source"] == "synthetic"
    assert snapshot["allow_external_market_data_calls"] is False
    assert snapshot["allow_provider_network_calls"] is False
    assert snapshot["market_data_contract_schema_version"] == "v1"
    assert snapshot["default_market_data_provider"] == "local_sample"
    assert snapshot["default_exchange"] == "NSE"
    assert snapshot["default_market_segment"] == "NSE_EQUITY"
    assert not any("credential" in key or "broker_token" in key for key in snapshot)


@pytest.mark.parametrize(
    "field,value",
    [
        ("instrument_master_mode", "network"),
        ("instrument_master_source", ""),
        ("market_data_contract_schema_version", ""),
        ("default_market_data_provider", ""),
        ("default_exchange", ""),
        ("default_market_segment", ""),
    ],
)
def test_instrument_setting_validation(field: str, value: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})


@pytest.mark.parametrize(
    "field",
    ["allow_external_market_data_calls", "allow_provider_network_calls"],
)
def test_external_market_data_call_flags_fail_closed(field: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: True})
