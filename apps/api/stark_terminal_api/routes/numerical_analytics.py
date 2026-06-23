from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_analytics.numerical.dependencies import default_numerical_dependency_gate
from stark_terminal_analytics.numerical.health import check_numerical_analytics_health

router = APIRouter()


FORBIDDEN_ANALYTICS = [
    "returns",
    "rolling_windows",
    "volatility",
    "drawdown",
    "correlation_beta",
    "indicators",
    "factor_models",
    "feature_computation",
    "backtests",
    "regimes",
    "trading_signals",
    "recommendations",
    "decision_objects",
    "execution_apis",
]


@router.get("/numerical-analytics/health")
def numerical_analytics_health() -> dict[str, Any]:
    status = check_numerical_analytics_health(get_settings())
    return {
        "service": "stark-terminal-numerical-analytics",
        **status.model_dump(),
    }


@router.get("/numerical-analytics/contracts")
def numerical_analytics_contracts() -> dict[str, Any]:
    settings = get_settings()
    return {
        "service": "stark-terminal-numerical-analytics",
        "schema_version": settings.numerical_analytics_schema_version,
        "computation_scope": "contracts-and-safe-descriptive-stdlib-only",
        "real_data_allowed_now": False,
        "trade_signals_allowed_now": False,
        "recommendations_allowed_now": False,
        "decision_objects_allowed_now": False,
        "execution_allowed_now": False,
        "allowed_summary_metrics": ["count", "min", "max", "mean"],
        "forbidden_analytics": FORBIDDEN_ANALYTICS,
        "note": "Prompt 27 exposes numerical contracts only; no user-supplied analytics computation endpoint exists.",
    }


@router.get("/numerical-analytics/dependency-gate")
def numerical_analytics_dependency_gate() -> dict[str, Any]:
    gate = default_numerical_dependency_gate()
    return {
        "service": "stark-terminal-numerical-analytics",
        "dependency_stage": gate.stage,
        "allowed_now": gate.allowed_now,
        "blocked_now": gate.blocked_now,
        "heavy_dependencies_blocked": gate.heavy_dependencies_blocked,
        "schema_version": gate.schema_version,
        "no_new_heavy_dependencies": True,
    }
