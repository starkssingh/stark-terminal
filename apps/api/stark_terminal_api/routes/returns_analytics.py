from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_analytics.returns.health import check_returns_analytics_health

router = APIRouter()


FORBIDDEN_ANALYTICS = [
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


@router.get("/returns-analytics/health")
def returns_analytics_health() -> dict[str, Any]:
    status = check_returns_analytics_health(get_settings())
    return {
        "service": "stark-terminal-returns-analytics",
        **status.model_dump(),
    }


@router.get("/returns-analytics/contracts")
def returns_analytics_contracts() -> dict[str, Any]:
    settings = get_settings()
    return {
        "service": "stark-terminal-returns-analytics",
        "schema_version": settings.returns_analytics_schema_version,
        "computation_scope": "descriptive-returns-and-rolling-windows-v0",
        "real_data_allowed_now": False,
        "trade_signals_allowed_now": False,
        "recommendations_allowed_now": False,
        "decision_objects_allowed_now": False,
        "execution_allowed_now": False,
        "supported_return_methods": ["SIMPLE", "LOG"],
        "supported_rolling_metrics": ["MEAN", "MIN", "MAX", "COUNT"],
        "forbidden_analytics": FORBIDDEN_ANALYTICS,
        "note": "Prompt 28 exposes returns/rolling metadata only; no user-supplied analytics computation endpoint exists.",
    }
