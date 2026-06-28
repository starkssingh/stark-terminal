from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_returns_analytics_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "107"
    assert settings.returns_analytics_enabled is True
    assert settings.returns_analytics_schema_version == "v1"
    assert settings.returns_analytics_allow_real_data is False
    assert settings.returns_analytics_allow_trade_signals is False
    assert settings.returns_analytics_allow_recommendations is False
    assert settings.returns_analytics_allow_decision_objects is False
    assert settings.returns_analytics_require_positive_prices is True
    assert settings.returns_analytics_require_source_reference is True
    assert settings.rolling_analytics_enabled is True
    assert settings.rolling_analytics_max_window > 0
    assert settings.rolling_analytics_allow_signal_labels is False


def test_returns_analytics_settings_safe_snapshot() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["returns_analytics_enabled"] is True
    assert snapshot["returns_analytics_schema_version"] == "v1"
    assert snapshot["returns_analytics_allow_real_data"] is False
    assert snapshot["returns_analytics_allow_trade_signals"] is False
    assert snapshot["returns_analytics_allow_recommendations"] is False
    assert snapshot["returns_analytics_allow_decision_objects"] is False
    assert snapshot["returns_analytics_require_positive_prices"] is True
    assert snapshot["returns_analytics_require_source_reference"] is True
    assert snapshot["rolling_analytics_enabled"] is True
    assert snapshot["rolling_analytics_max_window"] == 252
    assert snapshot["rolling_analytics_allow_signal_labels"] is False
    assert "returns_analytics_api_key" not in snapshot
    assert "broker_secret" not in snapshot


@pytest.mark.parametrize(
    "overrides",
    [
        {"returns_analytics_schema_version": ""},
        {"returns_analytics_allow_real_data": True},
        {"returns_analytics_allow_trade_signals": True},
        {"returns_analytics_allow_recommendations": True},
        {"returns_analytics_allow_decision_objects": True},
        {"returns_analytics_require_positive_prices": False},
        {"returns_analytics_require_source_reference": False},
        {"rolling_analytics_max_window": 0},
        {"rolling_analytics_allow_signal_labels": True},
    ],
)
def test_returns_analytics_settings_fail_closed(overrides: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        Settings(**overrides)
