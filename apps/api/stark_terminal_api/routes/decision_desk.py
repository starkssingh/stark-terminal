from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.decision_desk.action_placeholders import default_retail_action_placeholder_contracts
from stark_terminal_core.decision_desk.display import default_retail_display_boundary_contract
from stark_terminal_core.decision_desk.evidence import (
    build_retail_decision_evidence_checklist,
    evaluate_retail_decision_evidence_checklist,
)
from stark_terminal_core.decision_desk.health import check_retail_decision_desk_health
from stark_terminal_core.decision_desk.human_review import (
    build_retail_human_review_checklist,
    evaluate_retail_human_review_checklist,
)
from stark_terminal_core.decision_desk.planning import default_retail_decision_desk_plan
from stark_terminal_core.decision_desk.readiness import build_retail_decision_desk_readiness_report
from stark_terminal_core.decision_desk.safety import (
    default_retail_decision_desk_safety_policy,
    evaluate_action_placeholder_safety,
    evaluate_retail_decision_desk_plan_safety,
)

router = APIRouter()


@router.get("/decision-desk/health")
def decision_desk_health() -> dict[str, Any]:
    status = check_retail_decision_desk_health(get_settings())
    return {
        "service": "stark-terminal-decision-desk",
        **status.model_dump(),
    }


@router.get("/decision-desk/contracts")
def decision_desk_contracts() -> dict[str, Any]:
    settings = get_settings()
    plan = default_retail_decision_desk_plan()
    return {
        "service": "stark-terminal-decision-desk",
        "schema_version": settings.retail_decision_desk_schema_version,
        "computation_scope": "planning-and-guardrails-only",
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_objects_allowed_now": False,
        "execution_allowed_now": False,
        "planned_action_placeholders": plan.planned_action_placeholders,
        "required_evidence_kinds": plan.required_evidence_kinds,
        "forbidden_outputs": plan.forbidden_outputs,
    }


@router.get("/decision-desk/readiness-template")
def decision_desk_readiness_template() -> dict[str, Any]:
    settings = get_settings()
    plan = default_retail_decision_desk_plan()
    evidence_checklist = evaluate_retail_decision_evidence_checklist(
        build_retail_decision_evidence_checklist(),
    )
    human_review_checklist = evaluate_retail_human_review_checklist(
        build_retail_human_review_checklist(),
    )
    policy = default_retail_decision_desk_safety_policy(settings)
    plan_safety = evaluate_retail_decision_desk_plan_safety(plan, policy)
    placeholder_safety = evaluate_action_placeholder_safety(
        default_retail_action_placeholder_contracts(),
        policy,
    )
    safety_result = plan_safety if plan_safety.decision == "blocked" else placeholder_safety
    readiness = build_retail_decision_desk_readiness_report(
        plan,
        evidence_checklist,
        human_review_checklist,
        safety_result,
    )
    return {
        "service": "stark-terminal-decision-desk",
        "planning_only": True,
        "recommendations_allowed_now": False,
        "decision_objects_allowed_now": False,
        "execution_allowed_now": False,
        "evidence_checklist": evidence_checklist.model_dump(mode="json"),
        "human_review_checklist": human_review_checklist.model_dump(mode="json"),
        "readiness_report": readiness.model_dump(mode="json"),
        "must_not_generate_action_states": True,
        "must_not_generate_confidence_scores": True,
        "must_not_generate_decision_objects": True,
        "must_not_generate_recommendations": True,
    }


@router.get("/decision-desk/display-boundary")
def decision_desk_display_boundary() -> dict[str, Any]:
    boundary = default_retail_display_boundary_contract()
    return {
        "service": "stark-terminal-decision-desk",
        "planning_only": True,
        "allowed_sections": boundary.allowed_sections,
        "forbidden_sections": boundary.forbidden_sections,
        "no_recommendations": True,
        "no_confidence": True,
        "no_execution": True,
        "display_boundary": boundary.model_dump(mode="json"),
    }
