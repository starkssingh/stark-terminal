from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_analytics.regime_features.contracts import (
    default_regime_feature_candidates,
    default_regime_feature_group_plans,
)
from stark_terminal_analytics.regime_features.dependencies import default_regime_feature_dependency_plan
from stark_terminal_analytics.regime_features.evidence_mapping import (
    build_regime_feature_evidence_map,
    evaluate_regime_feature_evidence_map,
)
from stark_terminal_analytics.regime_features.health import check_regime_feature_preparation_health
from stark_terminal_analytics.regime_features.provenance import (
    build_regime_feature_provenance_map,
    evaluate_regime_feature_provenance_map,
)
from stark_terminal_analytics.regime_features.readiness import build_regime_feature_readiness_report
from stark_terminal_analytics.regime_features.safety import (
    default_regime_feature_safety_policy,
    evaluate_regime_feature_plan_safety,
)

router = APIRouter()


@router.get("/regime-features/health")
def regime_features_health() -> dict[str, Any]:
    status = check_regime_feature_preparation_health(get_settings())
    return {
        "service": "stark-terminal-regime-features",
        **status.model_dump(),
    }


@router.get("/regime-features/contracts")
def regime_features_contracts() -> dict[str, Any]:
    settings = get_settings()
    candidates = default_regime_feature_candidates()
    groups = default_regime_feature_group_plans()
    return {
        "service": "stark-terminal-regime-features",
        "schema_version": settings.regime_feature_preparation_schema_version,
        "computation_scope": "contracts-and-preparation-only",
        "feature_computation_allowed_now": False,
        "feature_registry_writes_allowed_now": False,
        "classification_allowed_now": False,
        "real_data_allowed_now": False,
        "trade_signals_allowed_now": False,
        "recommendations_allowed_now": False,
        "decision_objects_allowed_now": False,
        "execution_allowed_now": False,
        "feature_groups": [group.group.value for group in groups],
        "candidate_feature_names": [candidate.name for candidate in candidates],
        "forbidden_outputs": [
            "feature_computation",
            "feature_registry_writes",
            "regime_classification",
            "trading_signals",
            "recommendations",
            "DecisionObject_generation",
            "execution_apis",
        ],
    }


@router.get("/regime-features/readiness-template")
def regime_features_readiness_template() -> dict[str, Any]:
    settings = get_settings()
    candidates = default_regime_feature_candidates()
    groups = default_regime_feature_group_plans()
    provenance_map = evaluate_regime_feature_provenance_map(build_regime_feature_provenance_map())
    evidence_map = evaluate_regime_feature_evidence_map(build_regime_feature_evidence_map())
    policy = default_regime_feature_safety_policy(settings)
    safety_result = evaluate_regime_feature_plan_safety(candidates, groups, policy)
    readiness = build_regime_feature_readiness_report(
        candidates,
        groups,
        provenance_map,
        evidence_map,
        safety_result,
    )
    return {
        "service": "stark-terminal-regime-features",
        "preparation_only": True,
        "feature_computation_allowed_now": False,
        "classification_allowed_now": False,
        "provenance_map": provenance_map.model_dump(mode="json"),
        "evidence_map": evidence_map.model_dump(mode="json"),
        "readiness_report": readiness.model_dump(mode="json"),
        "must_not_compute_features": True,
        "must_not_classify_market_state": True,
        "must_not_generate_signals_or_decisions": True,
    }


@router.get("/regime-features/dependency-gate")
def regime_features_dependency_gate() -> dict[str, Any]:
    gate = default_regime_feature_dependency_plan()
    return {
        "service": "stark-terminal-regime-features",
        "current_stage": gate.current_stage,
        "allowed_now": gate.allowed_now,
        "blocked_now": gate.blocked_now,
        "heavy_dependencies_blocked": gate.heavy_dependencies_blocked,
        "feature_computation_allowed": gate.feature_computation_allowed,
    }
