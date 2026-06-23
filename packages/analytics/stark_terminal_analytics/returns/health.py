from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings


class ReturnsAnalyticsHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    real_data_allowed: bool
    trade_signals_allowed: bool
    recommendations_allowed: bool
    decision_objects_allowed: bool
    execution_allowed: bool = False
    rolling_enabled: bool
    rolling_max_window: int
    status: str
    error: str | None = None


def check_returns_analytics_health(settings: Settings | None = None) -> ReturnsAnalyticsHealthStatus:
    resolved_settings = settings or get_settings()
    try:
        safe_flags = not any(
            [
                resolved_settings.returns_analytics_allow_real_data,
                resolved_settings.returns_analytics_allow_trade_signals,
                resolved_settings.returns_analytics_allow_recommendations,
                resolved_settings.returns_analytics_allow_decision_objects,
                resolved_settings.rolling_analytics_allow_signal_labels,
                resolved_settings.execution_apis_enabled,
            ]
        )
        status = "healthy" if resolved_settings.returns_analytics_enabled and safe_flags else "blocked"
        return ReturnsAnalyticsHealthStatus(
            enabled=resolved_settings.returns_analytics_enabled,
            schema_version=resolved_settings.returns_analytics_schema_version,
            real_data_allowed=resolved_settings.returns_analytics_allow_real_data,
            trade_signals_allowed=resolved_settings.returns_analytics_allow_trade_signals,
            recommendations_allowed=resolved_settings.returns_analytics_allow_recommendations,
            decision_objects_allowed=resolved_settings.returns_analytics_allow_decision_objects,
            execution_allowed=False,
            rolling_enabled=resolved_settings.rolling_analytics_enabled,
            rolling_max_window=resolved_settings.rolling_analytics_max_window,
            status=status,
            error=None if status == "healthy" else "returns/rolling analytics safety flags are not fail-closed",
        )
    except Exception as exc:  # pragma: no cover - defensive health surface
        return ReturnsAnalyticsHealthStatus(
            enabled=resolved_settings.returns_analytics_enabled,
            schema_version=resolved_settings.returns_analytics_schema_version,
            real_data_allowed=False,
            trade_signals_allowed=False,
            recommendations_allowed=False,
            decision_objects_allowed=False,
            execution_allowed=False,
            rolling_enabled=resolved_settings.rolling_analytics_enabled,
            rolling_max_window=resolved_settings.rolling_analytics_max_window,
            status="error",
            error=str(exc).splitlines()[0][:160],
        )
