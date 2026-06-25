from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


def test_retail_trader_experience_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.retail_trader_experience_enabled is True
    assert settings.retail_trader_experience_schema_version == "v1"
    assert settings.retail_trader_experience_allow_active_ui is False
    assert settings.retail_trader_experience_allow_frontend_components is False
    assert settings.retail_trader_experience_allow_desktop_components is False
    assert settings.retail_trader_experience_allow_recommendations is False
    assert settings.retail_trader_experience_allow_action_generation is False
    assert settings.retail_trader_experience_allow_confidence_scoring is False
    assert settings.retail_trader_experience_allow_decision_object_generation is False
    assert settings.retail_trader_experience_allow_readiness_to_trade is False
    assert settings.retail_trader_experience_allow_broker_controls is False
    assert settings.retail_trader_experience_allow_execution is False
    assert settings.retail_trader_experience_allow_approval is False
    assert settings.retail_trader_experience_allow_override is False
    assert settings.retail_trader_experience_return_unavailable_by_default is True
    assert settings.retail_trader_experience_stage == "planning_and_guardrails"


def test_retail_trader_experience_safe_snapshot_exposes_safe_fields() -> None:
    snapshot = Settings().safe_settings_snapshot()
    expected = {
        "retail_trader_experience_enabled": True,
        "retail_trader_experience_schema_version": "v1",
        "retail_trader_experience_allow_active_ui": False,
        "retail_trader_experience_allow_frontend_components": False,
        "retail_trader_experience_allow_desktop_components": False,
        "retail_trader_experience_allow_recommendations": False,
        "retail_trader_experience_allow_action_generation": False,
        "retail_trader_experience_allow_confidence_scoring": False,
        "retail_trader_experience_allow_decision_object_generation": False,
        "retail_trader_experience_allow_readiness_to_trade": False,
        "retail_trader_experience_allow_broker_controls": False,
        "retail_trader_experience_allow_execution": False,
        "retail_trader_experience_allow_approval": False,
        "retail_trader_experience_allow_override": False,
        "retail_trader_experience_return_unavailable_by_default": True,
        "retail_trader_experience_stage": "planning_and_guardrails",
    }
    for key, value in expected.items():
        assert snapshot[key] == value
    assert "password" not in snapshot
    assert "secret" not in snapshot


@pytest.mark.parametrize(
    "field_name",
    [
        "retail_trader_experience_allow_active_ui",
        "retail_trader_experience_allow_frontend_components",
        "retail_trader_experience_allow_desktop_components",
        "retail_trader_experience_allow_recommendations",
        "retail_trader_experience_allow_action_generation",
        "retail_trader_experience_allow_confidence_scoring",
        "retail_trader_experience_allow_decision_object_generation",
        "retail_trader_experience_allow_readiness_to_trade",
        "retail_trader_experience_allow_broker_controls",
        "retail_trader_experience_allow_execution",
        "retail_trader_experience_allow_approval",
        "retail_trader_experience_allow_override",
    ],
)
def test_retail_trader_experience_settings_reject_unsafe_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field_name: True})


def test_retail_trader_experience_settings_reject_empty_schema_bad_stage_and_available_false() -> None:
    with pytest.raises(ValidationError):
        Settings(retail_trader_experience_schema_version="")
    with pytest.raises(ValidationError):
        Settings(retail_trader_experience_stage="active_ui")
    with pytest.raises(ValidationError):
        Settings(retail_trader_experience_return_unavailable_by_default=False)
