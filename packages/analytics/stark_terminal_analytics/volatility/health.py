from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings


class RiskAnalyticsHealthStatus(BaseModel):
    volatility_enabled: bool
    drawdown_enabled: bool
    schema_version: str
    real_data_allowed: bool
    trade_signals_allowed: bool
    recommendations_allowed: bool
    decision_objects_allowed: bool
    execution_allowed: bool = False
    default_stddev_method: str
    annualization_allowed: bool
    drawdown_positive_values_required: bool
    status: str
    error: str | None = None


def check_risk_analytics_health(settings: Settings | None = None) -> RiskAnalyticsHealthStatus:
    resolved_settings = settings or get_settings()
    try:
        safe_flags = not any(
            [
                resolved_settings.volatility_analytics_allow_real_data,
                resolved_settings.volatility_analytics_allow_trade_signals,
                resolved_settings.volatility_analytics_allow_recommendations,
                resolved_settings.volatility_analytics_allow_decision_objects,
                resolved_settings.drawdown_analytics_allow_signal_labels,
                resolved_settings.execution_apis_enabled,
            ]
        )
        positive_drawdown = resolved_settings.drawdown_analytics_require_positive_values
        method_valid = resolved_settings.volatility_analytics_default_stddev_method in {"sample", "population"}
        status = (
            "healthy"
            if resolved_settings.volatility_analytics_enabled
            and resolved_settings.drawdown_analytics_enabled
            and safe_flags
            and positive_drawdown
            and method_valid
            else "blocked"
        )
        return RiskAnalyticsHealthStatus(
            volatility_enabled=resolved_settings.volatility_analytics_enabled,
            drawdown_enabled=resolved_settings.drawdown_analytics_enabled,
            schema_version=resolved_settings.volatility_analytics_schema_version,
            real_data_allowed=resolved_settings.volatility_analytics_allow_real_data,
            trade_signals_allowed=resolved_settings.volatility_analytics_allow_trade_signals,
            recommendations_allowed=resolved_settings.volatility_analytics_allow_recommendations,
            decision_objects_allowed=resolved_settings.volatility_analytics_allow_decision_objects,
            execution_allowed=False,
            default_stddev_method=resolved_settings.volatility_analytics_default_stddev_method,
            annualization_allowed=resolved_settings.volatility_analytics_allow_annualization,
            drawdown_positive_values_required=positive_drawdown,
            status=status,
            error=None if status == "healthy" else "risk analytics safety flags are not fail-closed",
        )
    except Exception as exc:  # pragma: no cover - defensive health surface
        return RiskAnalyticsHealthStatus(
            volatility_enabled=resolved_settings.volatility_analytics_enabled,
            drawdown_enabled=resolved_settings.drawdown_analytics_enabled,
            schema_version=resolved_settings.volatility_analytics_schema_version,
            real_data_allowed=False,
            trade_signals_allowed=False,
            recommendations_allowed=False,
            decision_objects_allowed=False,
            execution_allowed=False,
            default_stddev_method="sample",
            annualization_allowed=False,
            drawdown_positive_values_required=True,
            status="error",
            error=str(exc).splitlines()[0][:160],
        )
