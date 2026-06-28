from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_analytics_foundation_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "107"
    assert settings.analytics_foundation_enabled is True
    assert settings.analytics_schema_version == "v1"
    assert settings.analytics_allow_real_data is False
    assert settings.analytics_allow_trade_signals is False
    assert settings.analytics_allow_recommendations is False
    assert settings.analytics_require_validated_inputs is True
    assert settings.analytics_require_source_reference is True
    assert settings.analytics_dependency_stage == "contracts_only"


def test_analytics_foundation_settings_safe_snapshot() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["analytics_foundation_enabled"] is True
    assert snapshot["analytics_schema_version"] == "v1"
    assert snapshot["analytics_allow_real_data"] is False
    assert snapshot["analytics_allow_trade_signals"] is False
    assert snapshot["analytics_allow_recommendations"] is False
    assert snapshot["analytics_require_validated_inputs"] is True
    assert snapshot["analytics_require_source_reference"] is True
    assert snapshot["analytics_dependency_stage"] == "contracts_only"
    assert "analytics_api_key" not in snapshot
    assert "broker_secret" not in snapshot


@pytest.mark.parametrize(
    "overrides",
    [
        {"analytics_schema_version": ""},
        {"analytics_allow_real_data": True},
        {"analytics_allow_trade_signals": True},
        {"analytics_allow_recommendations": True},
        {"analytics_require_validated_inputs": False},
        {"analytics_require_source_reference": False},
        {"analytics_dependency_stage": "unsupported"},
    ],
)
def test_analytics_foundation_settings_fail_closed(overrides: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        Settings(**overrides)
