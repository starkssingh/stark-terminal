from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


def test_decision_boundary_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.decision_boundary_enabled is True
    assert settings.decision_boundary_schema_version == "v1"
    assert settings.decision_boundary_allow_recommendations is False
    assert settings.decision_boundary_allow_action_generation is False
    assert settings.decision_boundary_allow_confidence_scoring is False
    assert settings.decision_boundary_allow_decision_object_generation is False
    assert settings.decision_boundary_allow_execution is False
    assert settings.decision_boundary_allow_approval is False
    assert settings.decision_boundary_allow_override is False
    assert settings.decision_boundary_allow_active_ui is False
    assert settings.decision_boundary_allow_active_workflow is False
    assert settings.decision_boundary_allow_readiness_to_trade is False
    assert settings.decision_boundary_stage == "boundary_hardening"


def test_decision_boundary_safe_snapshot_exposes_safe_fields() -> None:
    snapshot = Settings().safe_settings_snapshot()

    expected = {
        "decision_boundary_enabled": True,
        "decision_boundary_schema_version": "v1",
        "decision_boundary_allow_recommendations": False,
        "decision_boundary_allow_action_generation": False,
        "decision_boundary_allow_confidence_scoring": False,
        "decision_boundary_allow_decision_object_generation": False,
        "decision_boundary_allow_execution": False,
        "decision_boundary_allow_approval": False,
        "decision_boundary_allow_override": False,
        "decision_boundary_allow_active_ui": False,
        "decision_boundary_allow_active_workflow": False,
        "decision_boundary_allow_readiness_to_trade": False,
        "decision_boundary_stage": "boundary_hardening",
    }
    for key, value in expected.items():
        assert snapshot[key] == value

    assert "password" not in snapshot
    assert "secret" not in snapshot


@pytest.mark.parametrize(
    "field_name",
    [
        "decision_boundary_allow_recommendations",
        "decision_boundary_allow_action_generation",
        "decision_boundary_allow_confidence_scoring",
        "decision_boundary_allow_decision_object_generation",
        "decision_boundary_allow_execution",
        "decision_boundary_allow_approval",
        "decision_boundary_allow_override",
        "decision_boundary_allow_active_ui",
        "decision_boundary_allow_active_workflow",
        "decision_boundary_allow_readiness_to_trade",
    ],
)
def test_decision_boundary_settings_reject_unsafe_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field_name: True})


def test_decision_boundary_settings_reject_empty_schema_version_and_unknown_stage() -> None:
    with pytest.raises(ValidationError):
        Settings(decision_boundary_schema_version="")
    with pytest.raises(ValidationError):
        Settings(decision_boundary_stage="active_workflow")
