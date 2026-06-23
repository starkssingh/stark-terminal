from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_analytics.diagnostics.health import check_time_series_diagnostics_health

router = APIRouter()


FORBIDDEN_ANALYTICS = [
    "stationarity_tests",
    "adf",
    "kpss",
    "hurst",
    "autocorrelation",
    "regime_detection",
    "indicators",
    "feature_computation",
    "factor_models",
    "backtests",
    "trading_signals",
    "recommendations",
    "decision_objects",
    "execution_apis",
]


@router.get("/time-series-diagnostics/health")
def time_series_diagnostics_health() -> dict[str, Any]:
    status = check_time_series_diagnostics_health(get_settings())
    return {
        "service": "stark-terminal-time-series-diagnostics",
        **status.model_dump(),
    }


@router.get("/time-series-diagnostics/contracts")
def time_series_diagnostics_contracts() -> dict[str, Any]:
    settings = get_settings()
    return {
        "service": "stark-terminal-time-series-diagnostics",
        "schema_version": settings.time_series_diagnostics_schema_version,
        "computation_scope": "descriptive-time-series-data-quality-diagnostics-v0",
        "real_data_allowed_now": False,
        "trade_signals_allowed_now": False,
        "recommendations_allowed_now": False,
        "decision_objects_allowed_now": False,
        "execution_allowed_now": False,
        "supported_diagnostics": [
            "MONOTONICITY",
            "DUPLICATES",
            "GAPS",
            "IRREGULAR_INTERVALS",
            "SPACING_SUMMARY",
        ],
        "deferred_diagnostics": [
            "ADF",
            "KPSS",
            "HURST",
            "AUTOCORRELATION",
            "REGIME_DETECTION",
        ],
        "forbidden_analytics": FORBIDDEN_ANALYTICS,
        "note": "Prompt 32 exposes time-series diagnostics metadata only; no user-supplied diagnostics endpoint exists.",
    }

