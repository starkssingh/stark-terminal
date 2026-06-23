import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


def test_regime_feature_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "54"
    assert settings.regime_feature_preparation_enabled is True
    assert settings.regime_feature_preparation_schema_version == "v1"
    assert settings.regime_feature_preparation_allow_real_data is False
    assert settings.regime_feature_preparation_allow_feature_computation is False
    assert settings.regime_feature_preparation_allow_feature_registry_writes is False
    assert settings.regime_feature_preparation_allow_classification is False
    assert settings.regime_feature_preparation_allow_trade_signals is False
    assert settings.regime_feature_preparation_allow_recommendations is False
    assert settings.regime_feature_preparation_allow_decision_objects is False
    assert settings.regime_feature_preparation_require_provenance is True
    assert settings.regime_feature_preparation_require_evidence_mapping is True
    assert settings.regime_feature_preparation_dependency_stage == "contracts_only"


def test_safe_settings_snapshot_exposes_regime_feature_settings() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["regime_feature_preparation_enabled"] is True
    assert snapshot["regime_feature_preparation_schema_version"] == "v1"
    assert snapshot["regime_feature_preparation_allow_real_data"] is False
    assert snapshot["regime_feature_preparation_allow_feature_computation"] is False
    assert snapshot["regime_feature_preparation_allow_feature_registry_writes"] is False
    assert snapshot["regime_feature_preparation_allow_classification"] is False
    assert snapshot["regime_feature_preparation_allow_trade_signals"] is False
    assert snapshot["regime_feature_preparation_allow_recommendations"] is False
    assert snapshot["regime_feature_preparation_allow_decision_objects"] is False
    assert snapshot["regime_feature_preparation_require_provenance"] is True
    assert snapshot["regime_feature_preparation_require_evidence_mapping"] is True
    assert snapshot["regime_feature_preparation_dependency_stage"] == "contracts_only"


@pytest.mark.parametrize(
    "override",
    [
        {"regime_feature_preparation_schema_version": " "},
        {"regime_feature_preparation_allow_real_data": True},
        {"regime_feature_preparation_allow_feature_computation": True},
        {"regime_feature_preparation_allow_feature_registry_writes": True},
        {"regime_feature_preparation_allow_classification": True},
        {"regime_feature_preparation_allow_trade_signals": True},
        {"regime_feature_preparation_allow_recommendations": True},
        {"regime_feature_preparation_allow_decision_objects": True},
        {"regime_feature_preparation_require_provenance": False},
        {"regime_feature_preparation_require_evidence_mapping": False},
        {"regime_feature_preparation_dependency_stage": "unsafe"},
    ],
)
def test_regime_feature_unsafe_settings_fail_closed(override: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        Settings(**override)
