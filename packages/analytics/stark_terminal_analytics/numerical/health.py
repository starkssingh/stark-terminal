from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings


class NumericalAnalyticsHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    dependency_stage: str
    real_data_allowed: bool
    trade_signals_allowed: bool
    recommendations_allowed: bool
    decision_objects_allowed: bool
    execution_allowed: bool = False
    max_vector_length: int
    status: str
    error: str | None = None


def check_numerical_analytics_health(settings: Settings | None = None) -> NumericalAnalyticsHealthStatus:
    resolved_settings = settings or get_settings()
    try:
        safe_flags = not any(
            [
                resolved_settings.numerical_analytics_allow_real_data,
                resolved_settings.numerical_analytics_allow_trade_signals,
                resolved_settings.numerical_analytics_allow_recommendations,
                resolved_settings.numerical_analytics_allow_decision_objects,
                resolved_settings.execution_apis_enabled,
            ]
        )
        status = "healthy" if resolved_settings.numerical_analytics_enabled and safe_flags else "blocked"
        return NumericalAnalyticsHealthStatus(
            enabled=resolved_settings.numerical_analytics_enabled,
            schema_version=resolved_settings.numerical_analytics_schema_version,
            dependency_stage=resolved_settings.numerical_analytics_dependency_stage,
            real_data_allowed=resolved_settings.numerical_analytics_allow_real_data,
            trade_signals_allowed=resolved_settings.numerical_analytics_allow_trade_signals,
            recommendations_allowed=resolved_settings.numerical_analytics_allow_recommendations,
            decision_objects_allowed=resolved_settings.numerical_analytics_allow_decision_objects,
            execution_allowed=False,
            max_vector_length=resolved_settings.numerical_analytics_max_vector_length,
            status=status,
            error=None if status == "healthy" else "numerical analytics safety flags are not fail-closed",
        )
    except Exception as exc:  # pragma: no cover - defensive health surface
        return NumericalAnalyticsHealthStatus(
            enabled=resolved_settings.numerical_analytics_enabled,
            schema_version=resolved_settings.numerical_analytics_schema_version,
            dependency_stage=resolved_settings.numerical_analytics_dependency_stage,
            real_data_allowed=False,
            trade_signals_allowed=False,
            recommendations_allowed=False,
            decision_objects_allowed=False,
            execution_allowed=False,
            max_vector_length=resolved_settings.numerical_analytics_max_vector_length,
            status="error",
            error=str(exc).splitlines()[0][:160],
        )
