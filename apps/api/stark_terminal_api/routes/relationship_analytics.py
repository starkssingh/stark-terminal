from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_analytics.correlation.health import check_relationship_analytics_health

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


@router.get("/relationship-analytics/health")
def relationship_analytics_health() -> dict[str, Any]:
    status = check_relationship_analytics_health(get_settings())
    return {
        "service": "stark-terminal-relationship-analytics",
        **status.model_dump(),
    }


@router.get("/relationship-analytics/contracts")
def relationship_analytics_contracts() -> dict[str, Any]:
    settings = get_settings()
    return {
        "service": "stark-terminal-relationship-analytics",
        "schema_version": settings.correlation_analytics_schema_version,
        "computation_scope": "descriptive-correlation-and-beta-v0",
        "real_data_allowed_now": False,
        "trade_signals_allowed_now": False,
        "recommendations_allowed_now": False,
        "decision_objects_allowed_now": False,
        "execution_allowed_now": False,
        "supported_correlation_methods": ["PEARSON"],
        "supported_beta_methods": ["SAMPLE_COVARIANCE"],
        "forbidden_analytics": FORBIDDEN_ANALYTICS,
        "note": "Prompt 31 exposes relationship analytics metadata only; no user-supplied analytics computation endpoint exists.",
    }

