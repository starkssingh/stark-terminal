from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


def test_retail_trader_experience_boundary_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "107"
    assert settings.retail_trader_experience_boundary_enabled is True
    assert settings.retail_trader_experience_boundary_schema_version == "v1"
    assert settings.retail_trader_experience_boundary_allow_active_ui is False
    assert settings.retail_trader_experience_boundary_allow_frontend_components is False
    assert settings.retail_trader_experience_boundary_allow_desktop_components is False
    assert settings.retail_trader_experience_boundary_allow_recommendations is False
    assert settings.retail_trader_experience_boundary_allow_action_generation is False
    assert settings.retail_trader_experience_boundary_allow_confidence_scoring is False
    assert settings.retail_trader_experience_boundary_allow_decision_object_generation is False
    assert settings.retail_trader_experience_boundary_allow_readiness_to_trade is False
    assert settings.retail_trader_experience_boundary_allow_suitability_profiling is False
    assert settings.retail_trader_experience_boundary_allow_broker_controls is False
    assert settings.retail_trader_experience_boundary_allow_execution is False
    assert settings.retail_trader_experience_boundary_allow_approval is False
    assert settings.retail_trader_experience_boundary_allow_override is False
    assert settings.retail_trader_experience_boundary_stage == "boundary_hardening"


def test_retail_trader_experience_boundary_settings_snapshot_is_safe() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["retail_trader_experience_boundary_enabled"] is True
    assert snapshot["retail_trader_experience_boundary_schema_version"] == "v1"
    assert snapshot["retail_trader_experience_boundary_stage"] == "boundary_hardening"
    for key, value in snapshot.items():
        if key.startswith("retail_trader_experience_boundary_allow_"):
            assert value is False


@pytest.mark.parametrize(
    "field_name",
    [
        "retail_trader_experience_boundary_allow_active_ui",
        "retail_trader_experience_boundary_allow_frontend_components",
        "retail_trader_experience_boundary_allow_desktop_components",
        "retail_trader_experience_boundary_allow_recommendations",
        "retail_trader_experience_boundary_allow_action_generation",
        "retail_trader_experience_boundary_allow_confidence_scoring",
        "retail_trader_experience_boundary_allow_decision_object_generation",
        "retail_trader_experience_boundary_allow_readiness_to_trade",
        "retail_trader_experience_boundary_allow_suitability_profiling",
        "retail_trader_experience_boundary_allow_broker_controls",
        "retail_trader_experience_boundary_allow_execution",
        "retail_trader_experience_boundary_allow_approval",
        "retail_trader_experience_boundary_allow_override",
    ],
)
def test_retail_trader_experience_boundary_rejects_dangerous_allow_flags(
    field_name: str,
) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field_name: True})


def test_retail_trader_experience_boundary_stage_validation() -> None:
    assert Settings(retail_trader_experience_boundary_stage="audit_only").retail_trader_experience_boundary_stage == (
        "audit_only"
    )
    with pytest.raises(ValidationError):
        Settings(retail_trader_experience_boundary_stage="active_ui")
