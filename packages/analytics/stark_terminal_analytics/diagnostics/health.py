from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings


class TimeSeriesDiagnosticsHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    real_data_allowed: bool
    trade_signals_allowed: bool
    recommendations_allowed: bool
    decision_objects_allowed: bool
    execution_allowed: bool = False
    require_timezone_aware: bool
    default_expected_interval_seconds: int
    max_observations: int
    status: str
    error: str | None = None


def check_time_series_diagnostics_health(
    settings: Settings | None = None,
) -> TimeSeriesDiagnosticsHealthStatus:
    resolved = settings or get_settings()
    unsafe_flags = (
        resolved.time_series_diagnostics_allow_real_data
        or resolved.time_series_diagnostics_allow_trade_signals
        or resolved.time_series_diagnostics_allow_recommendations
        or resolved.time_series_diagnostics_allow_decision_objects
        or resolved.time_series_diagnostics_allow_signal_labels
        or resolved.execution_apis_enabled
    )
    has_required_configuration = (
        bool(resolved.time_series_diagnostics_schema_version.strip())
        and resolved.time_series_diagnostics_default_expected_interval_seconds > 0
        and resolved.time_series_diagnostics_max_observations > 0
    )
    status = "healthy" if resolved.time_series_diagnostics_enabled and not unsafe_flags and has_required_configuration else "blocked"
    error = None if status == "healthy" else "time-series diagnostics foundation safety flags are not fail-closed"
    return TimeSeriesDiagnosticsHealthStatus(
        enabled=resolved.time_series_diagnostics_enabled,
        schema_version=resolved.time_series_diagnostics_schema_version,
        real_data_allowed=resolved.time_series_diagnostics_allow_real_data,
        trade_signals_allowed=resolved.time_series_diagnostics_allow_trade_signals,
        recommendations_allowed=resolved.time_series_diagnostics_allow_recommendations,
        decision_objects_allowed=resolved.time_series_diagnostics_allow_decision_objects,
        execution_allowed=False,
        require_timezone_aware=resolved.time_series_diagnostics_require_timezone_aware,
        default_expected_interval_seconds=resolved.time_series_diagnostics_default_expected_interval_seconds,
        max_observations=resolved.time_series_diagnostics_max_observations,
        status=status,
        error=error,
    )

