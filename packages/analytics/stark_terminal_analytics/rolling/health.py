from __future__ import annotations

from stark_terminal_analytics.returns.health import ReturnsAnalyticsHealthStatus, check_returns_analytics_health


def check_rolling_analytics_health() -> ReturnsAnalyticsHealthStatus:
    return check_returns_analytics_health()
