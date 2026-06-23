from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.decision_safety.approval import default_decision_approval_placeholders
from stark_terminal_core.decision_safety.blocked_outputs import default_decision_blocked_output_policy
from stark_terminal_core.decision_safety.guardrails import (
    build_decision_safety_guardrail_set,
    default_blocked_output_kinds,
    default_decision_safety_guardrails,
    evaluate_decision_safety_guardrail_set,
)
from stark_terminal_core.decision_safety.health import check_decision_safety_health
from stark_terminal_core.decision_safety.human_review import (
    build_decision_human_review_gate_set,
    default_decision_human_review_gates,
    evaluate_decision_human_review_gate_set,
)
from stark_terminal_core.decision_safety.overrides import default_decision_override_prohibitions
from stark_terminal_core.decision_safety.readiness import build_decision_safety_readiness_report

router = APIRouter()


@router.get("/decision-safety/health")
def decision_safety_health() -> dict[str, Any]:
    status = check_decision_safety_health(get_settings())
    return {
        "service": "stark-terminal-decision-safety",
        **status.model_dump(),
    }


@router.get("/decision-safety/contracts")
def decision_safety_contracts() -> dict[str, Any]:
    settings = get_settings()
    guardrails = default_decision_safety_guardrails()
    blocked_outputs = default_blocked_output_kinds()
    return {
        "service": "stark-terminal-decision-safety",
        "schema_version": settings.decision_safety_schema_version,
        "computation_scope": "guardrails-only",
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "execution_allowed_now": False,
        "human_approval_allowed_now": False,
        "overrides_allowed_now": False,
        "blocked_outputs": [blocked_output.value for blocked_output in blocked_outputs],
        "guardrail_count": len(guardrails),
        "forbidden_outputs": [
            "recommendation_generation",
            "action_generation",
            "confidence_scoring",
            "DecisionObject_generation",
            "human_approval",
            "override_bypass",
            "execution_apis",
            "broker_orders",
            "market_state_decisions",
        ],
    }


@router.get("/decision-safety/readiness-template")
def decision_safety_readiness_template() -> dict[str, Any]:
    guardrail_set = evaluate_decision_safety_guardrail_set(build_decision_safety_guardrail_set())
    human_review_gate_set = evaluate_decision_human_review_gate_set(build_decision_human_review_gate_set())
    approval_placeholders = default_decision_approval_placeholders()
    override_prohibitions = default_decision_override_prohibitions()
    blocked_output_policy = default_decision_blocked_output_policy()
    readiness = build_decision_safety_readiness_report(
        guardrail_set,
        human_review_gate_set,
        approval_placeholders,
        override_prohibitions,
        blocked_output_policy,
    )
    return {
        "service": "stark-terminal-decision-safety",
        "guardrails_only": True,
        "recommendations_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "execution_allowed_now": False,
        "approval_granted": False,
        "overrides_allowed_now": False,
        "guardrail_set": guardrail_set.model_dump(mode="json"),
        "human_review_gate_set": human_review_gate_set.model_dump(mode="json"),
        "readiness_report": readiness.model_dump(mode="json"),
        "must_not_generate_action_states": True,
        "must_not_generate_confidence_scores": True,
        "must_not_generate_decision_objects": True,
        "must_not_generate_recommendations": True,
    }


@router.get("/decision-safety/human-review-template")
def decision_safety_human_review_template() -> dict[str, Any]:
    gates = default_decision_human_review_gates()
    gate_set = evaluate_decision_human_review_gate_set(
        build_decision_human_review_gate_set(gates=gates),
    )
    return {
        "service": "stark-terminal-decision-safety",
        "guardrails_only": True,
        "gates": [gate.model_dump(mode="json") for gate in gates],
        "gate_set": gate_set.model_dump(mode="json"),
        "approval_granted": False,
        "no_decision_object_generation": True,
        "no_execution": True,
    }
