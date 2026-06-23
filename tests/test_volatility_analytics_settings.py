from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings, get_settings


def test_volatility_drawdown_settings_defaults_are_safe() -> None:
    settings = get_settings()

    assert settings.prompt_number == "54"
    assert settings.volatility_analytics_enabled is True
    assert settings.drawdown_analytics_enabled is True
    assert settings.volatility_analytics_allow_real_data is False
    assert settings.volatility_analytics_allow_trade_signals is False
    assert settings.volatility_analytics_allow_recommendations is False
    assert settings.volatility_analytics_allow_decision_objects is False
    assert settings.volatility_analytics_default_stddev_method in {"sample", "population"}
    assert settings.volatility_analytics_allow_annualization is True
    assert settings.drawdown_analytics_require_positive_values is True
    assert settings.drawdown_analytics_allow_signal_labels is False


@pytest.mark.parametrize(
    "field",
    [
        "volatility_analytics_allow_real_data",
        "volatility_analytics_allow_trade_signals",
        "volatility_analytics_allow_recommendations",
        "volatility_analytics_allow_decision_objects",
        "drawdown_analytics_allow_signal_labels",
    ],
)
def test_volatility_drawdown_settings_reject_unsafe_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: True})


def test_drawdown_settings_require_positive_values() -> None:
    with pytest.raises(ValidationError):
        Settings(drawdown_analytics_require_positive_values=False)


def test_volatility_stddev_method_validation() -> None:
    assert Settings(volatility_analytics_default_stddev_method="population").volatility_analytics_default_stddev_method == "population"

    with pytest.raises(ValidationError):
        Settings(volatility_analytics_default_stddev_method="median")


def test_safe_settings_snapshot_exposes_risk_analytics_settings() -> None:
    snapshot = get_settings().safe_settings_snapshot()

    assert snapshot["volatility_analytics_enabled"] is True
    assert snapshot["volatility_analytics_schema_version"] == "v1"
    assert snapshot["volatility_analytics_allow_real_data"] is False
    assert snapshot["volatility_analytics_allow_trade_signals"] is False
    assert snapshot["volatility_analytics_allow_recommendations"] is False
    assert snapshot["volatility_analytics_allow_decision_objects"] is False
    assert snapshot["volatility_analytics_default_stddev_method"] == "sample"
    assert snapshot["volatility_analytics_allow_annualization"] is True
    assert snapshot["drawdown_analytics_enabled"] is True
    assert snapshot["drawdown_analytics_require_positive_values"] is True
    assert snapshot["drawdown_analytics_allow_signal_labels"] is False
