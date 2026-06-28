from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


def test_decision_safety_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "107"
    assert settings.decision_safety_enabled is True
    assert settings.decision_safety_schema_version == "v1"
    assert settings.decision_safety_allow_recommendations is False
    assert settings.decision_safety_allow_action_generation is False
    assert settings.decision_safety_allow_confidence_scoring is False
    assert settings.decision_safety_allow_decision_object_generation is False
    assert settings.decision_safety_allow_execution is False
    assert settings.decision_safety_allow_human_approval is False
    assert settings.decision_safety_allow_overrides is False
    assert settings.decision_safety_require_human_review is True
    assert settings.decision_safety_require_blocked_output_policy is True
    assert settings.decision_safety_stage == "guardrails_only"


@pytest.mark.parametrize(
    "override",
    [
        {"decision_safety_schema_version": " "},
        {"decision_safety_allow_recommendations": True},
        {"decision_safety_allow_action_generation": True},
        {"decision_safety_allow_confidence_scoring": True},
        {"decision_safety_allow_decision_object_generation": True},
        {"decision_safety_allow_execution": True},
        {"decision_safety_allow_human_approval": True},
        {"decision_safety_allow_overrides": True},
        {"decision_safety_require_human_review": False},
        {"decision_safety_require_blocked_output_policy": False},
        {"decision_safety_stage": "unsafe"},
    ],
)
def test_decision_safety_unsafe_settings_fail_closed(override: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        Settings(**override)


def test_safe_settings_snapshot_exposes_decision_safety_settings() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["decision_safety_enabled"] is True
    assert snapshot["decision_safety_schema_version"] == "v1"
    assert snapshot["decision_safety_allow_recommendations"] is False
    assert snapshot["decision_safety_allow_action_generation"] is False
    assert snapshot["decision_safety_allow_confidence_scoring"] is False
    assert snapshot["decision_safety_allow_decision_object_generation"] is False
    assert snapshot["decision_safety_allow_execution"] is False
    assert snapshot["decision_safety_allow_human_approval"] is False
    assert snapshot["decision_safety_allow_overrides"] is False
    assert snapshot["decision_safety_require_human_review"] is True
    assert snapshot["decision_safety_require_blocked_output_policy"] is True
    assert snapshot["decision_safety_stage"] == "guardrails_only"
