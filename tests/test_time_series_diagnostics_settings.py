import pytest

from stark_terminal_core.config.settings import Settings


def test_time_series_diagnostics_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.time_series_diagnostics_enabled is True
    assert settings.time_series_diagnostics_schema_version == "v1"
    assert settings.time_series_diagnostics_allow_real_data is False
    assert settings.time_series_diagnostics_allow_trade_signals is False
    assert settings.time_series_diagnostics_allow_recommendations is False
    assert settings.time_series_diagnostics_allow_decision_objects is False
    assert settings.time_series_diagnostics_require_source_reference is True
    assert settings.time_series_diagnostics_require_timezone_aware is True
    assert settings.time_series_diagnostics_default_expected_interval_seconds > 0
    assert settings.time_series_diagnostics_max_observations > 0
    assert settings.time_series_diagnostics_allow_signal_labels is False


def test_safe_settings_snapshot_exposes_time_series_diagnostics_settings() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["time_series_diagnostics_enabled"] is True
    assert snapshot["time_series_diagnostics_schema_version"] == "v1"
    assert snapshot["time_series_diagnostics_allow_real_data"] is False
    assert snapshot["time_series_diagnostics_allow_trade_signals"] is False
    assert snapshot["time_series_diagnostics_allow_recommendations"] is False
    assert snapshot["time_series_diagnostics_allow_decision_objects"] is False
    assert snapshot["time_series_diagnostics_require_source_reference"] is True
    assert snapshot["time_series_diagnostics_require_timezone_aware"] is True
    assert snapshot["time_series_diagnostics_default_expected_interval_seconds"] == 60
    assert snapshot["time_series_diagnostics_max_observations"] == 100000
    assert snapshot["time_series_diagnostics_allow_signal_labels"] is False


@pytest.mark.parametrize(
    "override",
    [
        {"time_series_diagnostics_schema_version": " "},
        {"time_series_diagnostics_allow_real_data": True},
        {"time_series_diagnostics_allow_trade_signals": True},
        {"time_series_diagnostics_allow_recommendations": True},
        {"time_series_diagnostics_allow_decision_objects": True},
        {"time_series_diagnostics_require_source_reference": False},
        {"time_series_diagnostics_require_timezone_aware": False},
        {"time_series_diagnostics_default_expected_interval_seconds": 0},
        {"time_series_diagnostics_max_observations": 0},
        {"time_series_diagnostics_allow_signal_labels": True},
    ],
)
def test_time_series_diagnostics_unsafe_settings_fail_closed(override: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        Settings(**override)

