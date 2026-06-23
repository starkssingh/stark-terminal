from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_safety.approval import default_decision_approval_placeholders
from stark_terminal_core.decision_safety.blocked_outputs import default_decision_blocked_output_policy
from stark_terminal_core.decision_safety.guardrails import (
    build_decision_safety_guardrail_set,
    evaluate_decision_safety_guardrail_set,
)
from stark_terminal_core.decision_safety.human_review import (
    build_decision_human_review_gate_set,
    evaluate_decision_human_review_gate_set,
)
from stark_terminal_core.decision_safety.overrides import default_decision_override_prohibitions
from stark_terminal_core.decision_safety.readiness import (
    DecisionSafetyReadinessReport,
    build_decision_safety_readiness_report,
    decision_safety_ready_for_api_skeleton,
    decision_safety_ready_for_decision_object_generation,
    decision_safety_ready_for_execution,
    decision_safety_ready_for_recommendations,
)


def test_decision_safety_readiness_report_blocks_dangerous_readiness() -> None:
    report = DecisionSafetyReadinessReport(
        report_id="report-1",
        guardrails_complete=True,
        human_review_gates_complete=True,
        approval_placeholders_complete=True,
        override_prohibitions_complete=True,
        blocked_output_policy_complete=True,
    )

    assert decision_safety_ready_for_recommendations(report) is False
    assert decision_safety_ready_for_decision_object_generation(report) is False
    assert decision_safety_ready_for_execution(report) is False
    assert decision_safety_ready_for_api_skeleton(report) is True

    for field in [
        "ready_for_recommendations",
        "ready_for_action_generation",
        "ready_for_confidence_scoring",
        "ready_for_decision_object_generation",
        "ready_for_execution",
    ]:
        with pytest.raises(ValidationError):
            DecisionSafetyReadinessReport(
                report_id="report-1",
                guardrails_complete=True,
                human_review_gates_complete=True,
                approval_placeholders_complete=True,
                override_prohibitions_complete=True,
                blocked_output_policy_complete=True,
                **{field: True},
            )


def test_blockers_prevent_api_skeleton_readiness() -> None:
    with pytest.raises(ValidationError):
        DecisionSafetyReadinessReport(
            report_id="report-1",
            guardrails_complete=True,
            human_review_gates_complete=True,
            approval_placeholders_complete=True,
            override_prohibitions_complete=True,
            blocked_output_policy_complete=True,
            ready_for_decision_desk_api_skeleton=True,
            blockers=["blocked"],
        )


def test_build_decision_safety_readiness_report_is_conservative() -> None:
    guardrail_set = evaluate_decision_safety_guardrail_set(build_decision_safety_guardrail_set())
    gate_set = evaluate_decision_human_review_gate_set(build_decision_human_review_gate_set())
    report = build_decision_safety_readiness_report(
        guardrail_set,
        gate_set,
        default_decision_approval_placeholders(),
        default_decision_override_prohibitions(),
        default_decision_blocked_output_policy(),
    )

    assert report.guardrails_complete is True
    assert report.human_review_gates_complete is True
    assert report.approval_placeholders_complete is True
    assert report.override_prohibitions_complete is True
    assert report.blocked_output_policy_complete is True
    assert report.ready_for_decision_desk_api_skeleton is True
    assert report.ready_for_recommendations is False
    assert report.ready_for_action_generation is False
    assert report.ready_for_confidence_scoring is False
    assert report.ready_for_decision_object_generation is False
    assert report.ready_for_execution is False
