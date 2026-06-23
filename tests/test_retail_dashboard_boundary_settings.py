from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


def test_retail_dashboard_boundary_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.retail_dashboard_boundary_enabled is True
    assert settings.retail_dashboard_boundary_schema_version == "v1"
    assert settings.retail_dashboard_boundary_allow_active_ui is False
    assert settings.retail_dashboard_boundary_allow_frontend_components is False
    assert settings.retail_dashboard_boundary_allow_desktop_components is False
    assert settings.retail_dashboard_boundary_allow_recommendations is False
    assert settings.retail_dashboard_boundary_allow_action_generation is False
    assert settings.retail_dashboard_boundary_allow_confidence_scoring is False
    assert settings.retail_dashboard_boundary_allow_decision_object_generation is False
    assert settings.retail_dashboard_boundary_allow_readiness_to_trade is False
    assert settings.retail_dashboard_boundary_allow_broker_controls is False
    assert settings.retail_dashboard_boundary_allow_execution is False
    assert settings.retail_dashboard_boundary_allow_approval is False
    assert settings.retail_dashboard_boundary_allow_override is False
    assert settings.retail_dashboard_boundary_stage == "boundary_hardening"


def test_retail_dashboard_boundary_safe_snapshot_exposes_safe_fields() -> None:
    snapshot = Settings().safe_settings_snapshot()
    expected = {
        "retail_dashboard_boundary_enabled": True,
        "retail_dashboard_boundary_schema_version": "v1",
        "retail_dashboard_boundary_allow_active_ui": False,
        "retail_dashboard_boundary_allow_frontend_components": False,
        "retail_dashboard_boundary_allow_desktop_components": False,
        "retail_dashboard_boundary_allow_recommendations": False,
        "retail_dashboard_boundary_allow_action_generation": False,
        "retail_dashboard_boundary_allow_confidence_scoring": False,
        "retail_dashboard_boundary_allow_decision_object_generation": False,
        "retail_dashboard_boundary_allow_readiness_to_trade": False,
        "retail_dashboard_boundary_allow_broker_controls": False,
        "retail_dashboard_boundary_allow_execution": False,
        "retail_dashboard_boundary_allow_approval": False,
        "retail_dashboard_boundary_allow_override": False,
        "retail_dashboard_boundary_stage": "boundary_hardening",
    }

    for key, value in expected.items():
        assert snapshot[key] == value
    assert "password" not in snapshot
    assert "secret" not in snapshot


@pytest.mark.parametrize(
    "field_name",
    [
        "retail_dashboard_boundary_allow_active_ui",
        "retail_dashboard_boundary_allow_frontend_components",
        "retail_dashboard_boundary_allow_desktop_components",
        "retail_dashboard_boundary_allow_recommendations",
        "retail_dashboard_boundary_allow_action_generation",
        "retail_dashboard_boundary_allow_confidence_scoring",
        "retail_dashboard_boundary_allow_decision_object_generation",
        "retail_dashboard_boundary_allow_readiness_to_trade",
        "retail_dashboard_boundary_allow_broker_controls",
        "retail_dashboard_boundary_allow_execution",
        "retail_dashboard_boundary_allow_approval",
        "retail_dashboard_boundary_allow_override",
    ],
)
def test_retail_dashboard_boundary_settings_reject_unsafe_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field_name: True})


def test_retail_dashboard_boundary_settings_reject_empty_schema_and_bad_stage() -> None:
    with pytest.raises(ValidationError):
        Settings(retail_dashboard_boundary_schema_version="")
    with pytest.raises(ValidationError):
        Settings(retail_dashboard_boundary_stage="active_ui")
