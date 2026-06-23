from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings


class RelationshipAnalyticsHealthStatus(BaseModel):
    correlation_enabled: bool
    beta_enabled: bool
    schema_version: str
    real_data_allowed: bool
    trade_signals_allowed: bool
    recommendations_allowed: bool
    decision_objects_allowed: bool
    execution_allowed: bool = False
    correlation_min_observations: int
    beta_min_observations: int
    status: str
    error: str | None = None


def check_relationship_analytics_health(settings: Settings | None = None) -> RelationshipAnalyticsHealthStatus:
    resolved_settings = settings or get_settings()
    try:
        safe_flags = not any(
            [
                resolved_settings.correlation_analytics_allow_real_data,
                resolved_settings.correlation_analytics_allow_trade_signals,
                resolved_settings.correlation_analytics_allow_recommendations,
                resolved_settings.correlation_analytics_allow_decision_objects,
                resolved_settings.beta_analytics_allow_signal_labels,
                resolved_settings.execution_apis_enabled,
            ]
        )
        min_observations_valid = (
            resolved_settings.correlation_analytics_min_observations >= 2
            and resolved_settings.beta_analytics_min_observations >= 2
        )
        status = (
            "healthy"
            if resolved_settings.correlation_analytics_enabled
            and resolved_settings.beta_analytics_enabled
            and safe_flags
            and min_observations_valid
            else "blocked"
        )
        return RelationshipAnalyticsHealthStatus(
            correlation_enabled=resolved_settings.correlation_analytics_enabled,
            beta_enabled=resolved_settings.beta_analytics_enabled,
            schema_version=resolved_settings.correlation_analytics_schema_version,
            real_data_allowed=resolved_settings.correlation_analytics_allow_real_data,
            trade_signals_allowed=resolved_settings.correlation_analytics_allow_trade_signals,
            recommendations_allowed=resolved_settings.correlation_analytics_allow_recommendations,
            decision_objects_allowed=resolved_settings.correlation_analytics_allow_decision_objects,
            execution_allowed=False,
            correlation_min_observations=resolved_settings.correlation_analytics_min_observations,
            beta_min_observations=resolved_settings.beta_analytics_min_observations,
            status=status,
            error=None if status == "healthy" else "relationship analytics safety flags are not fail-closed",
        )
    except Exception as exc:  # pragma: no cover - defensive health surface
        return RelationshipAnalyticsHealthStatus(
            correlation_enabled=resolved_settings.correlation_analytics_enabled,
            beta_enabled=resolved_settings.beta_analytics_enabled,
            schema_version=resolved_settings.correlation_analytics_schema_version,
            real_data_allowed=False,
            trade_signals_allowed=False,
            recommendations_allowed=False,
            decision_objects_allowed=False,
            execution_allowed=False,
            correlation_min_observations=2,
            beta_min_observations=2,
            status="error",
            error=str(exc).splitlines()[0][:160],
        )

