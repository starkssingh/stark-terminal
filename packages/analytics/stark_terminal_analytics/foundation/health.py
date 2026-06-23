from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_analytics.foundation.contracts import default_analytics_module_plans
from stark_terminal_analytics.foundation.roadmap import default_analytics_roadmap


class AnalyticsFoundationHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    dependency_stage: str
    real_data_allowed: bool
    trade_signals_allowed: bool
    recommendations_allowed: bool
    execution_allowed: bool = False
    module_plan_count: int
    roadmap_item_count: int
    status: str
    error: str | None = None


def check_analytics_foundation_health(settings: Settings | None = None) -> AnalyticsFoundationHealthStatus:
    resolved_settings = settings or get_settings()
    try:
        plans = default_analytics_module_plans()
        roadmap = default_analytics_roadmap()
        safe_flags = not any(
            [
                resolved_settings.analytics_allow_real_data,
                resolved_settings.analytics_allow_trade_signals,
                resolved_settings.analytics_allow_recommendations,
                resolved_settings.execution_apis_enabled,
            ]
        )
        status = "healthy" if resolved_settings.analytics_foundation_enabled and safe_flags and plans else "blocked"
        return AnalyticsFoundationHealthStatus(
            enabled=resolved_settings.analytics_foundation_enabled,
            schema_version=resolved_settings.analytics_schema_version,
            dependency_stage=resolved_settings.analytics_dependency_stage,
            real_data_allowed=resolved_settings.analytics_allow_real_data,
            trade_signals_allowed=resolved_settings.analytics_allow_trade_signals,
            recommendations_allowed=resolved_settings.analytics_allow_recommendations,
            execution_allowed=False,
            module_plan_count=len(plans),
            roadmap_item_count=len(roadmap),
            status=status,
            error=None if status == "healthy" else "analytics foundation safety flags are not fail-closed",
        )
    except Exception as exc:  # pragma: no cover - defensive health surface
        return AnalyticsFoundationHealthStatus(
            enabled=resolved_settings.analytics_foundation_enabled,
            schema_version=resolved_settings.analytics_schema_version,
            dependency_stage=resolved_settings.analytics_dependency_stage,
            real_data_allowed=False,
            trade_signals_allowed=False,
            recommendations_allowed=False,
            execution_allowed=False,
            module_plan_count=0,
            roadmap_item_count=0,
            status="error",
            error=str(exc).splitlines()[0][:160],
        )
