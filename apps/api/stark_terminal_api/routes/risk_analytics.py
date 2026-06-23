from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_analytics.volatility.health import check_risk_analytics_health

router = APIRouter()


FORBIDDEN_ANALYTICS = [
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


@router.get("/risk-analytics/health")
def risk_analytics_health() -> dict[str, Any]:
    status = check_risk_analytics_health(get_settings())
    return {
        "service": "stark-terminal-risk-analytics",
        **status.model_dump(),
    }


@router.get("/risk-analytics/contracts")
def risk_analytics_contracts() -> dict[str, Any]:
    settings = get_settings()
    return {
        "service": "stark-terminal-risk-analytics",
        "schema_version": settings.volatility_analytics_schema_version,
        "computation_scope": "descriptive-volatility-and-drawdown-v0",
        "real_data_allowed_now": False,
        "trade_signals_allowed_now": False,
        "recommendations_allowed_now": False,
        "decision_objects_allowed_now": False,
        "execution_allowed_now": False,
        "supported_volatility_methods": ["SAMPLE_STDDEV", "POPULATION_STDDEV"],
        "supported_drawdown_metrics": ["DRAWDOWN_SERIES", "MAX_DRAWDOWN", "DRAWDOWN_DURATION"],
        "forbidden_analytics": FORBIDDEN_ANALYTICS,
        "note": "Prompt 29 exposes risk analytics metadata only; no user-supplied analytics computation endpoint exists.",
    }
