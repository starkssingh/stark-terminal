from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_safety.human_review import (
    DecisionHumanReviewGate,
    DecisionHumanReviewGateSet,
    build_decision_human_review_gate_set,
    default_decision_human_review_gates,
    evaluate_decision_human_review_gate_set,
)


def test_valid_decision_human_review_gate_is_not_approval() -> None:
    gate = DecisionHumanReviewGate(
        gate_id="gate-1",
        title="Review Gate",
        description="Requires review but does not approve.",
    )

    assert gate.approval_granted is False
    assert gate.blocks_recommendations is True
    assert gate.blocks_action_generation is True
    assert gate.blocks_confidence_scoring is True
    assert gate.blocks_decision_object_generation is True
    assert gate.blocks_execution is True


def test_human_review_gate_rejects_approval_and_unblocked_outputs() -> None:
    with pytest.raises(ValidationError):
        DecisionHumanReviewGate(
            gate_id="gate-1",
            title="Review Gate",
            description="Unsafe gate.",
            approval_granted=True,
        )

    for field in [
        "blocks_recommendations",
        "blocks_action_generation",
        "blocks_confidence_scoring",
        "blocks_decision_object_generation",
        "blocks_execution",
    ]:
        with pytest.raises(ValidationError):
            DecisionHumanReviewGate(
                gate_id="gate-1",
                title="Review Gate",
                description="Unsafe gate.",
                **{field: False},
            )


def test_human_review_gate_set_cannot_grant_approval_or_outputs() -> None:
    gates = default_decision_human_review_gates()

    for field in [
        "approval_granted",
        "recommendations_allowed",
        "decision_object_generation_allowed",
        "execution_allowed",
    ]:
        with pytest.raises(ValidationError):
            DecisionHumanReviewGateSet(
                gate_set_id="gate-set-1",
                gates=gates,
                **{field: True},
            )

    with pytest.raises(ValidationError):
        DecisionHumanReviewGateSet(
            gate_set_id="gate-set-1",
            gates=gates,
            complete=True,
            blockers=["blocked"],
        )


def test_default_human_review_gates_evaluate_complete_without_approval() -> None:
    gate_set = evaluate_decision_human_review_gate_set(build_decision_human_review_gate_set())

    assert gate_set.complete is True
    assert gate_set.approval_granted is False
    assert gate_set.recommendations_allowed is False
    assert gate_set.decision_object_generation_allowed is False
    assert gate_set.execution_allowed is False
    assert not gate_set.blockers
