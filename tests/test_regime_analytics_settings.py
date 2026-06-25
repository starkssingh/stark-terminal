import pytest

from stark_terminal_core.config.settings import Settings


def test_regime_analytics_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "67"
    assert settings.regime_analytics_enabled is True
    assert settings.regime_analytics_schema_version == "v1"
    assert settings.regime_analytics_allow_real_data is False
    assert settings.regime_analytics_allow_classification is False
    assert settings.regime_analytics_allow_trade_signals is False
    assert settings.regime_analytics_allow_recommendations is False
    assert settings.regime_analytics_allow_decision_objects is False
    assert settings.regime_analytics_require_evidence is True
    assert settings.regime_analytics_require_human_review is True
    assert settings.regime_analytics_dependency_stage == "planning_only"
    assert settings.regime_analytics_allow_signal_labels is False


def test_safe_settings_snapshot_exposes_regime_analytics_settings() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["regime_analytics_enabled"] is True
    assert snapshot["regime_analytics_schema_version"] == "v1"
    assert snapshot["regime_analytics_allow_real_data"] is False
    assert snapshot["regime_analytics_allow_classification"] is False
    assert snapshot["regime_analytics_allow_trade_signals"] is False
    assert snapshot["regime_analytics_allow_recommendations"] is False
    assert snapshot["regime_analytics_allow_decision_objects"] is False
    assert snapshot["regime_analytics_require_evidence"] is True
    assert snapshot["regime_analytics_require_human_review"] is True
    assert snapshot["regime_analytics_dependency_stage"] == "planning_only"
    assert snapshot["regime_analytics_allow_signal_labels"] is False


@pytest.mark.parametrize(
    "override",
    [
        {"regime_analytics_schema_version": " "},
        {"regime_analytics_allow_real_data": True},
        {"regime_analytics_allow_classification": True},
        {"regime_analytics_allow_trade_signals": True},
        {"regime_analytics_allow_recommendations": True},
        {"regime_analytics_allow_decision_objects": True},
        {"regime_analytics_require_evidence": False},
        {"regime_analytics_require_human_review": False},
        {"regime_analytics_dependency_stage": "unsafe"},
        {"regime_analytics_allow_signal_labels": True},
    ],
)
def test_regime_analytics_unsafe_settings_fail_closed(override: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        Settings(**override)
