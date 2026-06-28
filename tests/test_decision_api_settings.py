from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


def test_decision_api_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "107"
    assert settings.decision_api_enabled is True
    assert settings.decision_api_schema_version == "v1"
    assert settings.decision_api_allow_recommendations is False
    assert settings.decision_api_allow_action_generation is False
    assert settings.decision_api_allow_confidence_scoring is False
    assert settings.decision_api_allow_decision_object_generation is False
    assert settings.decision_api_allow_execution is False
    assert settings.decision_api_allow_approval is False
    assert settings.decision_api_allow_override is False
    assert settings.decision_api_return_unavailable_by_default is True
    assert settings.decision_api_stage == "contract_skeleton"


@pytest.mark.parametrize(
    "override",
    [
        {"decision_api_schema_version": " "},
        {"decision_api_allow_recommendations": True},
        {"decision_api_allow_action_generation": True},
        {"decision_api_allow_confidence_scoring": True},
        {"decision_api_allow_decision_object_generation": True},
        {"decision_api_allow_execution": True},
        {"decision_api_allow_approval": True},
        {"decision_api_allow_override": True},
        {"decision_api_return_unavailable_by_default": False},
        {"decision_api_stage": "unsafe"},
    ],
)
def test_decision_api_unsafe_settings_fail_closed(override: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        Settings(**override)


def test_safe_settings_snapshot_exposes_decision_api_settings() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["decision_api_enabled"] is True
    assert snapshot["decision_api_schema_version"] == "v1"
    assert snapshot["decision_api_allow_recommendations"] is False
    assert snapshot["decision_api_allow_action_generation"] is False
    assert snapshot["decision_api_allow_confidence_scoring"] is False
    assert snapshot["decision_api_allow_decision_object_generation"] is False
    assert snapshot["decision_api_allow_execution"] is False
    assert snapshot["decision_api_allow_approval"] is False
    assert snapshot["decision_api_allow_override"] is False
    assert snapshot["decision_api_return_unavailable_by_default"] is True
    assert snapshot["decision_api_stage"] == "contract_skeleton"
