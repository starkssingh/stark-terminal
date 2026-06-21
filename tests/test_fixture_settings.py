from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_fixture_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.synthetic_fixtures_enabled is True
    assert settings.synthetic_fixture_schema_version == "v1"
    assert settings.synthetic_fixture_default_seed == 42
    assert settings.synthetic_fixture_default_bar_count == 30
    assert settings.synthetic_fixture_default_start_price == 100.0
    assert settings.synthetic_fixture_default_timeframe == "DAILY"
    assert settings.synthetic_fixture_allow_disk_writes is False
    assert settings.synthetic_fixture_output_root == "data/synthetic_fixtures"
    assert settings.synthetic_fixture_label == "synthetic-local-test-only"


@pytest.mark.parametrize(
    "field,value",
    [
        ("synthetic_fixture_schema_version", ""),
        ("synthetic_fixture_default_timeframe", ""),
        ("synthetic_fixture_output_root", ""),
        ("synthetic_fixture_label", ""),
        ("synthetic_fixture_default_bar_count", 0),
        ("synthetic_fixture_default_start_price", 0),
    ],
)
def test_fixture_settings_validation(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})


def test_fixture_settings_safe_snapshot_exposes_only_safe_fields() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["synthetic_fixtures_enabled"] is True
    assert snapshot["synthetic_fixture_schema_version"] == "v1"
    assert snapshot["synthetic_fixture_default_seed"] == 42
    assert snapshot["synthetic_fixture_default_bar_count"] == 30
    assert snapshot["synthetic_fixture_default_start_price"] == 100.0
    assert snapshot["synthetic_fixture_default_timeframe"] == "DAILY"
    assert snapshot["synthetic_fixture_allow_disk_writes"] is False
    assert snapshot["synthetic_fixture_output_root"] == "data/synthetic_fixtures"
    assert snapshot["synthetic_fixture_label"] == "synthetic-local-test-only"
    assert "provider_api_key" not in snapshot
    assert "broker_secret" not in snapshot
