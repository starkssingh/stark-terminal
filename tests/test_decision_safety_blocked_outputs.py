from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_safety.blocked_outputs import (
    DecisionBlockedOutputEvaluation,
    DecisionBlockedOutputPolicy,
    default_decision_blocked_output_policy,
    evaluate_decision_blocked_output_policy,
)
from stark_terminal_core.decision_safety.guardrails import DecisionBlockedOutputKind, default_blocked_output_kinds


def test_default_blocked_output_policy_blocks_required_outputs() -> None:
    policy = default_decision_blocked_output_policy()
    blocked = set(policy.blocked_outputs)

    assert DecisionBlockedOutputKind.RECOMMENDATION in blocked
    assert DecisionBlockedOutputKind.ACTION_GENERATION in blocked
    assert DecisionBlockedOutputKind.CONFIDENCE_SCORE in blocked
    assert DecisionBlockedOutputKind.DECISION_OBJECT in blocked
    assert DecisionBlockedOutputKind.EXECUTION in blocked
    assert DecisionBlockedOutputKind.BROKER_ORDER in blocked
    assert DecisionBlockedOutputKind.MARKET_STATE_DECISION in blocked
    assert policy.blocks_all_recommendation_like_outputs is True
    assert policy.blocks_all_execution_like_outputs is True


def test_blocked_output_policy_rejects_missing_unknown_or_unblocked_categories() -> None:
    with pytest.raises(ValidationError):
        DecisionBlockedOutputPolicy(
            policy_id="policy-1",
            name="Policy",
            blocked_outputs=[DecisionBlockedOutputKind.UNKNOWN],
        )

    with pytest.raises(ValidationError):
        DecisionBlockedOutputPolicy(
            policy_id="policy-1",
            name="Policy",
            blocked_outputs=[DecisionBlockedOutputKind.RECOMMENDATION],
        )

    for field in ["blocks_all_recommendation_like_outputs", "blocks_all_execution_like_outputs"]:
        with pytest.raises(ValidationError):
            DecisionBlockedOutputPolicy(
                policy_id="policy-1",
                name="Policy",
                blocked_outputs=default_blocked_output_kinds(),
                **{field: False},
            )


def test_blocked_output_evaluation_always_blocked_in_prompt_39() -> None:
    evaluation = evaluate_decision_blocked_output_policy()

    assert evaluation.blocked is True
    assert evaluation.forbidden_outputs
    assert evaluation.reasons

    with pytest.raises(ValidationError):
        DecisionBlockedOutputEvaluation(
            evaluation_id="evaluation-1",
            policy_id="policy-1",
            blocked=False,
            forbidden_outputs=default_blocked_output_kinds(),
            reasons=["unsafe"],
        )
