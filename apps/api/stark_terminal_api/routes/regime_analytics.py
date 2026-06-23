from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_analytics.regime.contracts import default_regime_analytics_plan
from stark_terminal_analytics.regime.dependencies import default_regime_dependency_plan
from stark_terminal_analytics.regime.evidence import (
    build_regime_evidence_checklist,
    evaluate_evidence_readiness,
)
from stark_terminal_analytics.regime.health import check_regime_analytics_health
from stark_terminal_analytics.regime.readiness import build_regime_readiness_report
from stark_terminal_analytics.regime.safety import (
    default_regime_safety_policy,
    evaluate_regime_plan_safety,
)

router = APIRouter()


@router.get("/regime-analytics/health")
def regime_analytics_health() -> dict[str, Any]:
    status = check_regime_analytics_health(get_settings())
    return {
        "service": "stark-terminal-regime-analytics",
        **status.model_dump(),
    }


@router.get("/regime-analytics/contracts")
def regime_analytics_contracts() -> dict[str, Any]:
    settings = get_settings()
    plan = default_regime_analytics_plan()
    return {
        "service": "stark-terminal-regime-analytics",
        "schema_version": settings.regime_analytics_schema_version,
        "computation_scope": "planning-and-guardrails-only",
        "classification_allowed_now": False,
        "real_data_allowed_now": False,
        "trade_signals_allowed_now": False,
        "recommendations_allowed_now": False,
        "decision_objects_allowed_now": False,
        "execution_allowed_now": False,
        "planned_labels": [label.label.value for label in plan.planned_labels],
        "required_evidence_kinds": [kind.value for kind in plan.required_evidence_kinds],
        "forbidden_outputs": plan.forbidden_outputs,
        "note": "Prompt 33 exposes regime planning metadata only; no market-state assignment endpoint exists.",
    }


@router.get("/regime-analytics/readiness-template")
def regime_analytics_readiness_template() -> dict[str, Any]:
    settings = get_settings()
    plan = default_regime_analytics_plan()
    checklist = evaluate_evidence_readiness(build_regime_evidence_checklist())
    policy = default_regime_safety_policy(settings)
    safety_result = evaluate_regime_plan_safety(plan, policy)
    readiness = build_regime_readiness_report(plan, checklist, safety_result)
    return {
        "service": "stark-terminal-regime-analytics",
        "planning_only": True,
        "classification_allowed_now": False,
        "checklist": checklist.model_dump(mode="json"),
        "readiness_report": readiness.model_dump(mode="json"),
        "must_not_classify_market_state": True,
        "must_not_generate_signals_or_decisions": True,
    }


@router.get("/regime-analytics/dependency-gate")
def regime_analytics_dependency_gate() -> dict[str, Any]:
    gate = default_regime_dependency_plan()
    return {
        "service": "stark-terminal-regime-analytics",
        "current_stage": gate.current_stage,
        "allowed_now": gate.allowed_now,
        "blocked_now": gate.blocked_now,
        "heavy_dependencies_blocked": gate.heavy_dependencies_blocked,
        "no_classification": True,
    }
