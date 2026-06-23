from __future__ import annotations

from stark_terminal_core.config.settings import Settings


def test_decision_human_review_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.decision_human_review_enabled is True
    assert settings.decision_human_review_schema_version == "v1"
    assert settings.decision_human_review_allow_active_workflow is False
    assert settings.decision_human_review_allow_task_assignment is False
    assert settings.decision_human_review_allow_reviewer_auth is False
    assert settings.decision_human_review_allow_notifications is False
    assert settings.decision_human_review_allow_approval is False
    assert settings.decision_human_review_allow_override is False
    assert settings.decision_human_review_allow_recommendations is False
    assert settings.decision_human_review_allow_action_generation is False
    assert settings.decision_human_review_allow_confidence_scoring is False
    assert settings.decision_human_review_allow_decision_object_generation is False
    assert settings.decision_human_review_allow_execution is False
    assert settings.decision_human_review_allow_readiness_to_trade is False
    assert settings.decision_human_review_return_unavailable_by_default is True
    assert settings.decision_human_review_stage == "workflow_skeleton"


def test_decision_human_review_safe_snapshot_exposes_only_safe_fields() -> None:
    snapshot = Settings().safe_settings_snapshot()

    expected = {
        "decision_human_review_enabled": True,
        "decision_human_review_schema_version": "v1",
        "decision_human_review_allow_active_workflow": False,
        "decision_human_review_allow_task_assignment": False,
        "decision_human_review_allow_reviewer_auth": False,
        "decision_human_review_allow_notifications": False,
        "decision_human_review_allow_approval": False,
        "decision_human_review_allow_override": False,
        "decision_human_review_allow_recommendations": False,
        "decision_human_review_allow_action_generation": False,
        "decision_human_review_allow_confidence_scoring": False,
        "decision_human_review_allow_decision_object_generation": False,
        "decision_human_review_allow_execution": False,
        "decision_human_review_allow_readiness_to_trade": False,
        "decision_human_review_return_unavailable_by_default": True,
        "decision_human_review_stage": "workflow_skeleton",
    }
    for key, value in expected.items():
        assert snapshot[key] == value

    assert "password" not in snapshot
    assert "secret" not in snapshot
