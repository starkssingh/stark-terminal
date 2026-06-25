from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


def test_retail_trader_experience_display_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "67"
    assert settings.retail_trader_experience_display_enabled is True
    assert settings.retail_trader_experience_display_schema_version == "v1"
    assert settings.retail_trader_experience_display_allow_active_ui is False
    assert settings.retail_trader_experience_display_allow_frontend_components is False
    assert settings.retail_trader_experience_display_allow_desktop_components is False
    assert settings.retail_trader_experience_display_allow_recommendations is False
    assert settings.retail_trader_experience_display_allow_action_generation is False
    assert settings.retail_trader_experience_display_allow_confidence_scoring is False
    assert settings.retail_trader_experience_display_allow_decision_object_generation is False
    assert settings.retail_trader_experience_display_allow_readiness_to_trade is False
    assert settings.retail_trader_experience_display_allow_broker_controls is False
    assert settings.retail_trader_experience_display_allow_execution is False
    assert settings.retail_trader_experience_display_allow_approval is False
    assert settings.retail_trader_experience_display_allow_override is False
    assert settings.retail_trader_experience_display_allow_suitability_profiling is False
    assert settings.retail_trader_experience_display_return_unavailable_by_default is True
    assert settings.retail_trader_experience_display_stage == "display_contract_skeleton"


def test_retail_trader_experience_display_safe_snapshot_exposes_display_settings() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["retail_trader_experience_display_enabled"] is True
    assert snapshot["retail_trader_experience_display_schema_version"] == "v1"
    assert snapshot["retail_trader_experience_display_allow_active_ui"] is False
    assert snapshot["retail_trader_experience_display_allow_frontend_components"] is False
    assert snapshot["retail_trader_experience_display_allow_desktop_components"] is False
    assert snapshot["retail_trader_experience_display_allow_recommendations"] is False
    assert snapshot["retail_trader_experience_display_allow_action_generation"] is False
    assert snapshot["retail_trader_experience_display_allow_confidence_scoring"] is False
    assert snapshot["retail_trader_experience_display_allow_decision_object_generation"] is False
    assert snapshot["retail_trader_experience_display_allow_readiness_to_trade"] is False
    assert snapshot["retail_trader_experience_display_allow_broker_controls"] is False
    assert snapshot["retail_trader_experience_display_allow_execution"] is False
    assert snapshot["retail_trader_experience_display_allow_approval"] is False
    assert snapshot["retail_trader_experience_display_allow_override"] is False
    assert snapshot["retail_trader_experience_display_allow_suitability_profiling"] is False
    assert snapshot["retail_trader_experience_display_return_unavailable_by_default"] is True
    assert snapshot["retail_trader_experience_display_stage"] == "display_contract_skeleton"


@pytest.mark.parametrize(
    "field",
    [
        "retail_trader_experience_display_allow_active_ui",
        "retail_trader_experience_display_allow_frontend_components",
        "retail_trader_experience_display_allow_desktop_components",
        "retail_trader_experience_display_allow_recommendations",
        "retail_trader_experience_display_allow_action_generation",
        "retail_trader_experience_display_allow_confidence_scoring",
        "retail_trader_experience_display_allow_decision_object_generation",
        "retail_trader_experience_display_allow_readiness_to_trade",
        "retail_trader_experience_display_allow_broker_controls",
        "retail_trader_experience_display_allow_execution",
        "retail_trader_experience_display_allow_approval",
        "retail_trader_experience_display_allow_override",
        "retail_trader_experience_display_allow_suitability_profiling",
    ],
)
def test_retail_trader_experience_display_dangerous_settings_are_rejected(field: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: True})


def test_retail_trader_experience_display_unavailable_by_default_is_enforced() -> None:
    with pytest.raises(ValidationError):
        Settings(retail_trader_experience_display_return_unavailable_by_default=False)


def test_retail_trader_experience_display_stage_is_validated() -> None:
    assert Settings(retail_trader_experience_display_stage="unavailable_only").retail_trader_experience_display_stage == (
        "unavailable_only"
    )

    with pytest.raises(ValidationError):
        Settings(retail_trader_experience_display_stage="active")
