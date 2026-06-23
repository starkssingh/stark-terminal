from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_safety.guardrails import (
    DecisionBlockedOutputKind,
    DecisionSafetyGuardrail,
    DecisionSafetyGuardrailSet,
    build_decision_safety_guardrail_set,
    default_blocked_output_kinds,
    default_decision_safety_guardrails,
    evaluate_decision_safety_guardrail_set,
)


def test_valid_decision_safety_guardrail_blocks_dangerous_outputs() -> None:
    guardrail = DecisionSafetyGuardrail(
        guardrail_id="guardrail-1",
        name="Guardrail",
        description="Blocks dangerous outputs.",
        blocked_outputs=default_blocked_output_kinds(),
    )

    assert guardrail.blocks_recommendations is True
    assert guardrail.blocks_action_generation is True
    assert guardrail.blocks_confidence_scoring is True
    assert guardrail.blocks_decision_object_generation is True
    assert guardrail.blocks_execution is True


def test_decision_safety_guardrail_rejects_unknown_or_unblocked_outputs() -> None:
    with pytest.raises(ValidationError):
        DecisionSafetyGuardrail(
            guardrail_id="guardrail-1",
            name="Guardrail",
            description="Bad blocked output.",
            blocked_outputs=[DecisionBlockedOutputKind.UNKNOWN],
        )

    for field in [
        "blocks_recommendations",
        "blocks_action_generation",
        "blocks_confidence_scoring",
        "blocks_decision_object_generation",
        "blocks_execution",
    ]:
        with pytest.raises(ValidationError):
            DecisionSafetyGuardrail(
                guardrail_id="guardrail-1",
                name="Guardrail",
                description="Unsafe guardrail.",
                blocked_outputs=default_blocked_output_kinds(),
                **{field: False},
            )


def test_default_decision_safety_guardrails_exist_and_evaluate_complete() -> None:
    guardrails = default_decision_safety_guardrails()

    assert guardrails
    assert all(guardrail.blocked_outputs for guardrail in guardrails)

    evaluated = evaluate_decision_safety_guardrail_set(build_decision_safety_guardrail_set(guardrails=guardrails))
    assert evaluated.complete is True
    assert not evaluated.blockers
    assert evaluated.recommendations_allowed is False


def test_guardrail_set_rejects_dangerous_allowed_flags_and_blockers_when_complete() -> None:
    guardrails = default_decision_safety_guardrails()

    for field in [
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "execution_allowed",
    ]:
        with pytest.raises(ValidationError):
            DecisionSafetyGuardrailSet(
                guardrail_set_id="guardrail-set-1",
                guardrails=guardrails,
                **{field: True},
            )

    with pytest.raises(ValidationError):
        DecisionSafetyGuardrailSet(
            guardrail_set_id="guardrail-set-1",
            guardrails=guardrails,
            complete=True,
            blockers=["blocked"],
        )
