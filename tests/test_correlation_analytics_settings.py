from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings, get_settings


def test_correlation_beta_settings_defaults_are_safe() -> None:
    settings = get_settings()

    assert settings.prompt_number == "54"
    assert settings.correlation_analytics_enabled is True
    assert settings.beta_analytics_enabled is True
    assert settings.correlation_analytics_schema_version == "v1"
    assert settings.correlation_analytics_allow_real_data is False
    assert settings.correlation_analytics_allow_trade_signals is False
    assert settings.correlation_analytics_allow_recommendations is False
    assert settings.correlation_analytics_allow_decision_objects is False
    assert settings.correlation_analytics_min_observations >= 2
    assert settings.beta_analytics_min_observations >= 2
    assert settings.beta_analytics_allow_signal_labels is False


@pytest.mark.parametrize(
    "field",
    [
        "correlation_analytics_allow_real_data",
        "correlation_analytics_allow_trade_signals",
        "correlation_analytics_allow_recommendations",
        "correlation_analytics_allow_decision_objects",
        "beta_analytics_allow_signal_labels",
    ],
)
def test_correlation_beta_settings_reject_unsafe_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: True})


@pytest.mark.parametrize("field", ["correlation_analytics_min_observations", "beta_analytics_min_observations"])
def test_correlation_beta_min_observations_must_be_at_least_two(field: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: 1})


def test_safe_settings_snapshot_exposes_relationship_analytics_settings() -> None:
    snapshot = get_settings().safe_settings_snapshot()

    assert snapshot["correlation_analytics_enabled"] is True
    assert snapshot["correlation_analytics_schema_version"] == "v1"
    assert snapshot["correlation_analytics_allow_real_data"] is False
    assert snapshot["correlation_analytics_allow_trade_signals"] is False
    assert snapshot["correlation_analytics_allow_recommendations"] is False
    assert snapshot["correlation_analytics_allow_decision_objects"] is False
    assert snapshot["correlation_analytics_min_observations"] == 2
    assert snapshot["beta_analytics_enabled"] is True
    assert snapshot["beta_analytics_min_observations"] == 2
    assert snapshot["beta_analytics_allow_signal_labels"] is False
