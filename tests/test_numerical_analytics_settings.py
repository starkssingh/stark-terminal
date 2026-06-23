from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_numerical_analytics_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "54"
    assert settings.numerical_analytics_enabled is True
    assert settings.numerical_analytics_schema_version == "v1"
    assert settings.numerical_analytics_allow_real_data is False
    assert settings.numerical_analytics_allow_trade_signals is False
    assert settings.numerical_analytics_allow_recommendations is False
    assert settings.numerical_analytics_allow_decision_objects is False
    assert settings.numerical_analytics_require_source_reference is True
    assert settings.numerical_analytics_require_finite_values is True
    assert settings.numerical_analytics_max_vector_length > 0
    assert settings.numerical_analytics_dependency_stage == "contracts_and_safe_stdlib"


def test_numerical_analytics_settings_safe_snapshot() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["numerical_analytics_enabled"] is True
    assert snapshot["numerical_analytics_schema_version"] == "v1"
    assert snapshot["numerical_analytics_allow_real_data"] is False
    assert snapshot["numerical_analytics_allow_trade_signals"] is False
    assert snapshot["numerical_analytics_allow_recommendations"] is False
    assert snapshot["numerical_analytics_allow_decision_objects"] is False
    assert snapshot["numerical_analytics_require_source_reference"] is True
    assert snapshot["numerical_analytics_require_finite_values"] is True
    assert snapshot["numerical_analytics_max_vector_length"] == 100000
    assert snapshot["numerical_analytics_dependency_stage"] == "contracts_and_safe_stdlib"
    assert "numerical_analytics_api_key" not in snapshot
    assert "broker_secret" not in snapshot


@pytest.mark.parametrize(
    "overrides",
    [
        {"numerical_analytics_schema_version": ""},
        {"numerical_analytics_allow_real_data": True},
        {"numerical_analytics_allow_trade_signals": True},
        {"numerical_analytics_allow_recommendations": True},
        {"numerical_analytics_allow_decision_objects": True},
        {"numerical_analytics_require_source_reference": False},
        {"numerical_analytics_require_finite_values": False},
        {"numerical_analytics_max_vector_length": 0},
        {"numerical_analytics_dependency_stage": "unsupported"},
    ],
)
def test_numerical_analytics_settings_fail_closed(overrides: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        Settings(**overrides)
